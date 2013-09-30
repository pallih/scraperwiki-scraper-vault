<?php
$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$doc = new DOMDocument();
$docSingleView = new DOMDocument();


$max_single_view_pages = 22 + 129 + 865;
$max_list_view_pages = 700;

foreach(range('X','Z') as $c) {
    if ($max_single_view_pages < 1) break;
    if ($max_list_view_pages < 1) break;

    echo "Namen mit \"" . $c . "\"..." . "\n";
    $params = "module=gepris&task=browsePersonIndex&character=" . $c . "&index=0";

    $html = load_html($view, $params);
    @$doc->loadHTML($html);
    $xpath = new DOMXpath($doc);
    $headline = $xpath->query('//div[contains(@class,"letterFilter")]/p');
    if (!is_null($headline)) {
        $headline = $headline->item(0);
        echo strip_off_multiple_spaces(strip_tags($headline->nodeValue)) . "\n";
    }
    do {
        $buttons = $xpath->query('//div[contains(@class,"listennaviright")]/a');
        $button = $buttons->item(0);
        $more_pages = (strpos($button->getAttribute('class'), 'active') !== FALSE);
    
        $rows = $xpath->query('//div[contains(@class,"content_inside")]//tr/td/a');
        
        echo "processing " . ($rows->length) . " persons...\n";
        foreach ($rows as $a) {
            if ($max_single_view_pages-- < 1) break;
            $single_view = ltrim(html_entity_decode($a->getAttribute('href')), "?");
            if (!preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $single_view, $m)) continue;
    
            $person = array();
            $person['id'] = $m[1];
            echo "loading single view of " . strip_off_multiple_spaces(strip_tags($a->nodeValue)) . "\n";
            
            $html = load_html($view, $single_view);
            @$docSingleView->loadHTML($html);
            $xpathSingleView = new DOMXpath($docSingleView);
            
            $h3 = $xpathSingleView->query('//div[contains(@class,"detailed")]/h3');
            $h3 = $h3->item(0);
            $person['name'] = strip_off_multiple_spaces($h3->nodeValue);
            $data = $xpathSingleView->query('//div[contains(@class,"detailed")]/div[contains(@class,"details")]/p/span');

            for ($i = 0; $i < (($data->length) - 1); $i+=2) {
                $key = $data->item($i);
                $key = strip_off_multiple_spaces(strip_tags($key->nodeValue));
                $value = $data->item($i + 1);
                if ($key == 'E-Mail')
                    $person[$key] = (strip_off_multiple_spaces(preg_replace('/^(.*?)<img.*src=".*?at_symbol\.png".*?\salt="@".*\/{0,1}>(.*?)$/i','$1@$2', (innerHTML($value)))));
                elseif ($key == 'Internet')
                    $person[$key] = html_entity_decode(strip_off_multiple_spaces(($value->firstChild->getAttribute('href'))));
                else
                    $person[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
            }

            //echo json_encode($institution) . "\n";

            scraperwiki::save(array('id'), $person);
        }
        
        if ($max_single_view_pages < 1) break;
        if ($max_list_view_pages-- < 1) break;

        if ($more_pages) {
            echo "loading next page..." . "\n";
            $params = ltrim(html_entity_decode($button->getAttribute('href')), "?");
            $html = load_html($view, $params);
            @$doc->loadHTML($html);
            $xpath = new DOMXpath($doc);
        }
    } while ($more_pages);
}

function innerHTML($element) {
    $innerHTML = "";
    $children = $element->childNodes;
    foreach ($children as $child)
    {
        $tmp_dom = new DOMDocument();
        $tmp_dom->appendChild($tmp_dom->importNode($child, true));
        $innerHTML.=trim($tmp_dom->saveHTML());
    }
    return $innerHTML;
}

function br2nl($str) {
    return preg_replace('/\s*<br\s*\/?\s*>\s*/i',"\r\n", $str);
}
function strip_off_multiple_spaces($str) {
    return trim(preg_replace('/\s[\s]+/', ' ', str_replace('&nbsp;', ' ', $str)));
}

function dom_children($element, $selector) {
    $found_children = array();

    if (preg_match('/^([^#\.]+){1}/', $selector, $m)) $child_tagname = $m[1];
    if (preg_match('/#([^\.]*){0,1}/', $selector, $m)) $child_id = $m[1];
    if (preg_match_all('/\.([^#\.]*){0,1}/', $selector, $m)) $child_classes = $m[1];

    $total_selector = "";
    if (isset($child_tagname)) $total_selector .= $child_tagname;
    if (isset($child_id)) $total_selector .= "#" . $child_id;
    if (isset($child_classes))
        foreach ($child_classes as $child_class)
            $total_selector .= "." . $child_class;
    echo "selector is: \"$total_selector\"\n";

    echo "element is: " . $element . "\n";
    echo "children: " . count($element->children()) . "\n";
    if (count($element->children()) > 0)
        foreach ($element->children() as $child) {
            if (isset($child_tagname) && ($child->tag != $child_tagname)) continue;
            if (isset($child_id) && ($child->getAttribute('id') != $child_id)) continue;
            if (isset($child_classes)) {
                $css_classes = explode(" ", $child->getAttribute('class'));
                foreach ($child_classes as $child_class)
                    if (!in_array($child_class, $css_classes)) continue;
            }
            $found_children[] = $child;
        }
    
    return $found_children;
}
function load_html($url, $parameters) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'task=copyRequestParametersToSession&' . $parameters);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    preg_match_all('|Set-Cookie: (.*?);|U', $result, $m);
    $cookies = implode(';', $m[1]);
    //echo $cookies . "\n";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    curl_setopt($ch, CURLOPT_COOKIE, $cookies);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $parameters);
    $html = curl_exec($ch);
    curl_close($ch);

    return $html;
}
?><?php
$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$doc = new DOMDocument();
$docSingleView = new DOMDocument();


$max_single_view_pages = 22 + 129 + 865;
$max_list_view_pages = 700;

foreach(range('X','Z') as $c) {
    if ($max_single_view_pages < 1) break;
    if ($max_list_view_pages < 1) break;

    echo "Namen mit \"" . $c . "\"..." . "\n";
    $params = "module=gepris&task=browsePersonIndex&character=" . $c . "&index=0";

    $html = load_html($view, $params);
    @$doc->loadHTML($html);
    $xpath = new DOMXpath($doc);
    $headline = $xpath->query('//div[contains(@class,"letterFilter")]/p');
    if (!is_null($headline)) {
        $headline = $headline->item(0);
        echo strip_off_multiple_spaces(strip_tags($headline->nodeValue)) . "\n";
    }
    do {
        $buttons = $xpath->query('//div[contains(@class,"listennaviright")]/a');
        $button = $buttons->item(0);
        $more_pages = (strpos($button->getAttribute('class'), 'active') !== FALSE);
    
        $rows = $xpath->query('//div[contains(@class,"content_inside")]//tr/td/a');
        
        echo "processing " . ($rows->length) . " persons...\n";
        foreach ($rows as $a) {
            if ($max_single_view_pages-- < 1) break;
            $single_view = ltrim(html_entity_decode($a->getAttribute('href')), "?");
            if (!preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $single_view, $m)) continue;
    
            $person = array();
            $person['id'] = $m[1];
            echo "loading single view of " . strip_off_multiple_spaces(strip_tags($a->nodeValue)) . "\n";
            
            $html = load_html($view, $single_view);
            @$docSingleView->loadHTML($html);
            $xpathSingleView = new DOMXpath($docSingleView);
            
            $h3 = $xpathSingleView->query('//div[contains(@class,"detailed")]/h3');
            $h3 = $h3->item(0);
            $person['name'] = strip_off_multiple_spaces($h3->nodeValue);
            $data = $xpathSingleView->query('//div[contains(@class,"detailed")]/div[contains(@class,"details")]/p/span');

            for ($i = 0; $i < (($data->length) - 1); $i+=2) {
                $key = $data->item($i);
                $key = strip_off_multiple_spaces(strip_tags($key->nodeValue));
                $value = $data->item($i + 1);
                if ($key == 'E-Mail')
                    $person[$key] = (strip_off_multiple_spaces(preg_replace('/^(.*?)<img.*src=".*?at_symbol\.png".*?\salt="@".*\/{0,1}>(.*?)$/i','$1@$2', (innerHTML($value)))));
                elseif ($key == 'Internet')
                    $person[$key] = html_entity_decode(strip_off_multiple_spaces(($value->firstChild->getAttribute('href'))));
                else
                    $person[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
            }

            //echo json_encode($institution) . "\n";

            scraperwiki::save(array('id'), $person);
        }
        
        if ($max_single_view_pages < 1) break;
        if ($max_list_view_pages-- < 1) break;

        if ($more_pages) {
            echo "loading next page..." . "\n";
            $params = ltrim(html_entity_decode($button->getAttribute('href')), "?");
            $html = load_html($view, $params);
            @$doc->loadHTML($html);
            $xpath = new DOMXpath($doc);
        }
    } while ($more_pages);
}

function innerHTML($element) {
    $innerHTML = "";
    $children = $element->childNodes;
    foreach ($children as $child)
    {
        $tmp_dom = new DOMDocument();
        $tmp_dom->appendChild($tmp_dom->importNode($child, true));
        $innerHTML.=trim($tmp_dom->saveHTML());
    }
    return $innerHTML;
}

function br2nl($str) {
    return preg_replace('/\s*<br\s*\/?\s*>\s*/i',"\r\n", $str);
}
function strip_off_multiple_spaces($str) {
    return trim(preg_replace('/\s[\s]+/', ' ', str_replace('&nbsp;', ' ', $str)));
}

function dom_children($element, $selector) {
    $found_children = array();

    if (preg_match('/^([^#\.]+){1}/', $selector, $m)) $child_tagname = $m[1];
    if (preg_match('/#([^\.]*){0,1}/', $selector, $m)) $child_id = $m[1];
    if (preg_match_all('/\.([^#\.]*){0,1}/', $selector, $m)) $child_classes = $m[1];

    $total_selector = "";
    if (isset($child_tagname)) $total_selector .= $child_tagname;
    if (isset($child_id)) $total_selector .= "#" . $child_id;
    if (isset($child_classes))
        foreach ($child_classes as $child_class)
            $total_selector .= "." . $child_class;
    echo "selector is: \"$total_selector\"\n";

    echo "element is: " . $element . "\n";
    echo "children: " . count($element->children()) . "\n";
    if (count($element->children()) > 0)
        foreach ($element->children() as $child) {
            if (isset($child_tagname) && ($child->tag != $child_tagname)) continue;
            if (isset($child_id) && ($child->getAttribute('id') != $child_id)) continue;
            if (isset($child_classes)) {
                $css_classes = explode(" ", $child->getAttribute('class'));
                foreach ($child_classes as $child_class)
                    if (!in_array($child_class, $css_classes)) continue;
            }
            $found_children[] = $child;
        }
    
    return $found_children;
}
function load_html($url, $parameters) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'task=copyRequestParametersToSession&' . $parameters);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    preg_match_all('|Set-Cookie: (.*?);|U', $result, $m);
    $cookies = implode(';', $m[1]);
    //echo $cookies . "\n";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    curl_setopt($ch, CURLOPT_COOKIE, $cookies);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $parameters);
    $html = curl_exec($ch);
    curl_close($ch);

    return $html;
}
?><?php
$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$doc = new DOMDocument();
$docSingleView = new DOMDocument();


$max_single_view_pages = 22 + 129 + 865;
$max_list_view_pages = 700;

foreach(range('X','Z') as $c) {
    if ($max_single_view_pages < 1) break;
    if ($max_list_view_pages < 1) break;

    echo "Namen mit \"" . $c . "\"..." . "\n";
    $params = "module=gepris&task=browsePersonIndex&character=" . $c . "&index=0";

    $html = load_html($view, $params);
    @$doc->loadHTML($html);
    $xpath = new DOMXpath($doc);
    $headline = $xpath->query('//div[contains(@class,"letterFilter")]/p');
    if (!is_null($headline)) {
        $headline = $headline->item(0);
        echo strip_off_multiple_spaces(strip_tags($headline->nodeValue)) . "\n";
    }
    do {
        $buttons = $xpath->query('//div[contains(@class,"listennaviright")]/a');
        $button = $buttons->item(0);
        $more_pages = (strpos($button->getAttribute('class'), 'active') !== FALSE);
    
        $rows = $xpath->query('//div[contains(@class,"content_inside")]//tr/td/a');
        
        echo "processing " . ($rows->length) . " persons...\n";
        foreach ($rows as $a) {
            if ($max_single_view_pages-- < 1) break;
            $single_view = ltrim(html_entity_decode($a->getAttribute('href')), "?");
            if (!preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $single_view, $m)) continue;
    
            $person = array();
            $person['id'] = $m[1];
            echo "loading single view of " . strip_off_multiple_spaces(strip_tags($a->nodeValue)) . "\n";
            
            $html = load_html($view, $single_view);
            @$docSingleView->loadHTML($html);
            $xpathSingleView = new DOMXpath($docSingleView);
            
            $h3 = $xpathSingleView->query('//div[contains(@class,"detailed")]/h3');
            $h3 = $h3->item(0);
            $person['name'] = strip_off_multiple_spaces($h3->nodeValue);
            $data = $xpathSingleView->query('//div[contains(@class,"detailed")]/div[contains(@class,"details")]/p/span');

            for ($i = 0; $i < (($data->length) - 1); $i+=2) {
                $key = $data->item($i);
                $key = strip_off_multiple_spaces(strip_tags($key->nodeValue));
                $value = $data->item($i + 1);
                if ($key == 'E-Mail')
                    $person[$key] = (strip_off_multiple_spaces(preg_replace('/^(.*?)<img.*src=".*?at_symbol\.png".*?\salt="@".*\/{0,1}>(.*?)$/i','$1@$2', (innerHTML($value)))));
                elseif ($key == 'Internet')
                    $person[$key] = html_entity_decode(strip_off_multiple_spaces(($value->firstChild->getAttribute('href'))));
                else
                    $person[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
            }

            //echo json_encode($institution) . "\n";

            scraperwiki::save(array('id'), $person);
        }
        
        if ($max_single_view_pages < 1) break;
        if ($max_list_view_pages-- < 1) break;

        if ($more_pages) {
            echo "loading next page..." . "\n";
            $params = ltrim(html_entity_decode($button->getAttribute('href')), "?");
            $html = load_html($view, $params);
            @$doc->loadHTML($html);
            $xpath = new DOMXpath($doc);
        }
    } while ($more_pages);
}

function innerHTML($element) {
    $innerHTML = "";
    $children = $element->childNodes;
    foreach ($children as $child)
    {
        $tmp_dom = new DOMDocument();
        $tmp_dom->appendChild($tmp_dom->importNode($child, true));
        $innerHTML.=trim($tmp_dom->saveHTML());
    }
    return $innerHTML;
}

function br2nl($str) {
    return preg_replace('/\s*<br\s*\/?\s*>\s*/i',"\r\n", $str);
}
function strip_off_multiple_spaces($str) {
    return trim(preg_replace('/\s[\s]+/', ' ', str_replace('&nbsp;', ' ', $str)));
}

function dom_children($element, $selector) {
    $found_children = array();

    if (preg_match('/^([^#\.]+){1}/', $selector, $m)) $child_tagname = $m[1];
    if (preg_match('/#([^\.]*){0,1}/', $selector, $m)) $child_id = $m[1];
    if (preg_match_all('/\.([^#\.]*){0,1}/', $selector, $m)) $child_classes = $m[1];

    $total_selector = "";
    if (isset($child_tagname)) $total_selector .= $child_tagname;
    if (isset($child_id)) $total_selector .= "#" . $child_id;
    if (isset($child_classes))
        foreach ($child_classes as $child_class)
            $total_selector .= "." . $child_class;
    echo "selector is: \"$total_selector\"\n";

    echo "element is: " . $element . "\n";
    echo "children: " . count($element->children()) . "\n";
    if (count($element->children()) > 0)
        foreach ($element->children() as $child) {
            if (isset($child_tagname) && ($child->tag != $child_tagname)) continue;
            if (isset($child_id) && ($child->getAttribute('id') != $child_id)) continue;
            if (isset($child_classes)) {
                $css_classes = explode(" ", $child->getAttribute('class'));
                foreach ($child_classes as $child_class)
                    if (!in_array($child_class, $css_classes)) continue;
            }
            $found_children[] = $child;
        }
    
    return $found_children;
}
function load_html($url, $parameters) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'task=copyRequestParametersToSession&' . $parameters);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    preg_match_all('|Set-Cookie: (.*?);|U', $result, $m);
    $cookies = implode(';', $m[1]);
    //echo $cookies . "\n";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    curl_setopt($ch, CURLOPT_COOKIE, $cookies);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $parameters);
    $html = curl_exec($ch);
    curl_close($ch);

    return $html;
}
?><?php
$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$doc = new DOMDocument();
$docSingleView = new DOMDocument();


$max_single_view_pages = 22 + 129 + 865;
$max_list_view_pages = 700;

foreach(range('X','Z') as $c) {
    if ($max_single_view_pages < 1) break;
    if ($max_list_view_pages < 1) break;

    echo "Namen mit \"" . $c . "\"..." . "\n";
    $params = "module=gepris&task=browsePersonIndex&character=" . $c . "&index=0";

    $html = load_html($view, $params);
    @$doc->loadHTML($html);
    $xpath = new DOMXpath($doc);
    $headline = $xpath->query('//div[contains(@class,"letterFilter")]/p');
    if (!is_null($headline)) {
        $headline = $headline->item(0);
        echo strip_off_multiple_spaces(strip_tags($headline->nodeValue)) . "\n";
    }
    do {
        $buttons = $xpath->query('//div[contains(@class,"listennaviright")]/a');
        $button = $buttons->item(0);
        $more_pages = (strpos($button->getAttribute('class'), 'active') !== FALSE);
    
        $rows = $xpath->query('//div[contains(@class,"content_inside")]//tr/td/a');
        
        echo "processing " . ($rows->length) . " persons...\n";
        foreach ($rows as $a) {
            if ($max_single_view_pages-- < 1) break;
            $single_view = ltrim(html_entity_decode($a->getAttribute('href')), "?");
            if (!preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $single_view, $m)) continue;
    
            $person = array();
            $person['id'] = $m[1];
            echo "loading single view of " . strip_off_multiple_spaces(strip_tags($a->nodeValue)) . "\n";
            
            $html = load_html($view, $single_view);
            @$docSingleView->loadHTML($html);
            $xpathSingleView = new DOMXpath($docSingleView);
            
            $h3 = $xpathSingleView->query('//div[contains(@class,"detailed")]/h3');
            $h3 = $h3->item(0);
            $person['name'] = strip_off_multiple_spaces($h3->nodeValue);
            $data = $xpathSingleView->query('//div[contains(@class,"detailed")]/div[contains(@class,"details")]/p/span');

            for ($i = 0; $i < (($data->length) - 1); $i+=2) {
                $key = $data->item($i);
                $key = strip_off_multiple_spaces(strip_tags($key->nodeValue));
                $value = $data->item($i + 1);
                if ($key == 'E-Mail')
                    $person[$key] = (strip_off_multiple_spaces(preg_replace('/^(.*?)<img.*src=".*?at_symbol\.png".*?\salt="@".*\/{0,1}>(.*?)$/i','$1@$2', (innerHTML($value)))));
                elseif ($key == 'Internet')
                    $person[$key] = html_entity_decode(strip_off_multiple_spaces(($value->firstChild->getAttribute('href'))));
                else
                    $person[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
            }

            //echo json_encode($institution) . "\n";

            scraperwiki::save(array('id'), $person);
        }
        
        if ($max_single_view_pages < 1) break;
        if ($max_list_view_pages-- < 1) break;

        if ($more_pages) {
            echo "loading next page..." . "\n";
            $params = ltrim(html_entity_decode($button->getAttribute('href')), "?");
            $html = load_html($view, $params);
            @$doc->loadHTML($html);
            $xpath = new DOMXpath($doc);
        }
    } while ($more_pages);
}

function innerHTML($element) {
    $innerHTML = "";
    $children = $element->childNodes;
    foreach ($children as $child)
    {
        $tmp_dom = new DOMDocument();
        $tmp_dom->appendChild($tmp_dom->importNode($child, true));
        $innerHTML.=trim($tmp_dom->saveHTML());
    }
    return $innerHTML;
}

function br2nl($str) {
    return preg_replace('/\s*<br\s*\/?\s*>\s*/i',"\r\n", $str);
}
function strip_off_multiple_spaces($str) {
    return trim(preg_replace('/\s[\s]+/', ' ', str_replace('&nbsp;', ' ', $str)));
}

function dom_children($element, $selector) {
    $found_children = array();

    if (preg_match('/^([^#\.]+){1}/', $selector, $m)) $child_tagname = $m[1];
    if (preg_match('/#([^\.]*){0,1}/', $selector, $m)) $child_id = $m[1];
    if (preg_match_all('/\.([^#\.]*){0,1}/', $selector, $m)) $child_classes = $m[1];

    $total_selector = "";
    if (isset($child_tagname)) $total_selector .= $child_tagname;
    if (isset($child_id)) $total_selector .= "#" . $child_id;
    if (isset($child_classes))
        foreach ($child_classes as $child_class)
            $total_selector .= "." . $child_class;
    echo "selector is: \"$total_selector\"\n";

    echo "element is: " . $element . "\n";
    echo "children: " . count($element->children()) . "\n";
    if (count($element->children()) > 0)
        foreach ($element->children() as $child) {
            if (isset($child_tagname) && ($child->tag != $child_tagname)) continue;
            if (isset($child_id) && ($child->getAttribute('id') != $child_id)) continue;
            if (isset($child_classes)) {
                $css_classes = explode(" ", $child->getAttribute('class'));
                foreach ($child_classes as $child_class)
                    if (!in_array($child_class, $css_classes)) continue;
            }
            $found_children[] = $child;
        }
    
    return $found_children;
}
function load_html($url, $parameters) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'task=copyRequestParametersToSession&' . $parameters);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    preg_match_all('|Set-Cookie: (.*?);|U', $result, $m);
    $cookies = implode(';', $m[1]);
    //echo $cookies . "\n";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    curl_setopt($ch, CURLOPT_COOKIE, $cookies);
    curl_setopt($ch, CURLOPT_POST, count(explode('&', $parameters)));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $parameters);
    $html = curl_exec($ch);
    curl_close($ch);

    return $html;
}
?>