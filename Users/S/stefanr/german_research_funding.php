<?php
$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$doc = new DOMDocument();
$docSingleView = new DOMDocument();

/*
$projects = array(
5377227,
5380173,
);
*/

// /*
$max_single_view_pages = 13636;
$max_list_view_pages = 1400;

$params = "beginOfFunding=&bewilligungsStatus=&bundesland=DEU%23&context=projekt&fachgebiet=%23&findButton=historyCall&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=&procedure=%23&task=doKatalog&teilprojekte=true&index=73010";

$html = load_html($view, $params);
@$doc->loadHTML($html);
$xpath = new DOMXpath($doc);
$headline = $xpath->query("//div[@id='listennavi']/span");
if (!is_null($headline)) {
   $headline = $headline->item(0);
   echo strip_off_multiple_spaces(strip_tags($headline->nodeValue)) . "\n";
}
do {
    $buttons = $xpath->query('//div[@id="listennavi"]/div[contains(@class,"listennaviright")]/a');
    $button = $buttons->item(0);
    $more_pages = (strpos($button->getAttribute('class'), 'active') !== FALSE);
    
    $rows = $xpath->query('//div[@id="liste"]//h2/a');
    
    echo "processing " . ($rows->length) . " projects...\n";
    foreach ($rows as $a) {
        if ($max_single_view_pages-- < 1) break;
        $single_view = ltrim(html_entity_decode($a->getAttribute('href')), "?");
// */

/*
    foreach ($projects as $p) {
        $single_view = "module=gepris&task=showDetail&context=projekt&id=" . $p;
*/

        if (!preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $single_view, $m)) continue;

        $project = array();
        $project['id'] = $m[1];
// /*
        echo "loading single view of " . strip_off_multiple_spaces(strip_tags($a->nodeValue)) . "\n";
// */
            
        $html = load_html($view, $single_view);
        @$docSingleView->loadHTML($html);
        $xpathSingleView = new DOMXpath($docSingleView);
            
        $h3 = $xpathSingleView->query('//div[contains(@class,"detailed")]/div[contains(@class,"details")]/h3');
        $h3 = $h3->item(0);
        $project['name'] = strip_off_multiple_spaces($h3->nodeValue);

        $description = $xpathSingleView->query('//div[contains(@class,"detailed")]//div[@id="projekttext"]');
        $description = $description->item(0);
        $project['description'] = strip_off_multiple_spaces($description->nodeValue);

        $data = $xpathSingleView->query('//div[contains(@class,"detailed")]//div/div/span');

        for ($i = 0; $i < (($data->length) - 1); $i+=2) {
            $key = $data->item($i);
            $key = strip_off_multiple_spaces(strip_tags($key->nodeValue));
            $key = trim($key);
            $value = $data->item($i + 1);
            if ($key == 'Webseite') {
                $anchor = $xpathSingleView->query($value->getNodePath() . '/a');
                $anchor = $anchor->item(0);
                $project[$key] = html_entity_decode(strip_off_multiple_spaces(($anchor->getAttribute('href'))));
            }
            elseif ($key == 'Teilprojekt zu' || $key == 'beteiligter Wissenschaftler:' || $key == 'Teilprojektleiter:' || $key == 'Sprecher:' || $key == 'Antragstellende Institution:' || $key == 'Mitantragstellende Institution:' || $key == 'Beteiligte Institution:' || $key == 'ausländische Institution:' || $key == 'Kooperationspartner:' || $key == 'ausländischer Sprecher:' || $key == 'Stellvertreter:' || $key == 'Antragsteller:' || $key == 'Beteiligte Person:' || $key == 'Mitantragsteller:' || $key == 'Leiter:' || $key == 'Beteiligte Hochschule:' || $key == 'Partnerorganisation:') {
                $anchors = $xpathSingleView->query($value->getNodePath() . '/a');
                $idString = "";
                foreach ($anchors as $anchor) {
                    preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $anchor->getAttribute('href'), $m);
                    $idString .= $m[1] . ",";
                }
                $project[$key] = $idString;
            }
            elseif ($key == 'Ehemaliger Antragsteller:') {
                $anchors = $xpathSingleView->query($value->getNodePath() . '/a');
                if ($anchors->length == 1) {
                    $value = html_entity_decode(innerHTML($value));
                    echo $value;
                    $idString = "";
                    preg_match('/^.*?href=\"(?:(?:\?id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?\".*?>.*?<\/a>(?:, (?:von \d+\/\d\d\d\d )?bis (\d+\/\d\d\d\d))?.*?$/', $value, $m);
                    $idString .= $m[1] . (isset($m[2]) ? " (" . $m[2] . ")" : '');
                    $project[$key] = $idString;
                }
                else
                    $project[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
            }
            elseif ($key == 'verfahrenstechnischer DFG-Ansprechpartner:') ;
            elseif ($key == 'fachlicher DFG-Ansprechpartner:') ;
            else
                $project[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
        }

        //echo json_encode($institution) . "\n";

        scraperwiki::save(array('id'), $project);
    }

// /*
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
// */

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

/*
$projects = array(
5377227,
5380173,
);
*/

// /*
$max_single_view_pages = 13636;
$max_list_view_pages = 1400;

$params = "beginOfFunding=&bewilligungsStatus=&bundesland=DEU%23&context=projekt&fachgebiet=%23&findButton=historyCall&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=&procedure=%23&task=doKatalog&teilprojekte=true&index=73010";

$html = load_html($view, $params);
@$doc->loadHTML($html);
$xpath = new DOMXpath($doc);
$headline = $xpath->query("//div[@id='listennavi']/span");
if (!is_null($headline)) {
   $headline = $headline->item(0);
   echo strip_off_multiple_spaces(strip_tags($headline->nodeValue)) . "\n";
}
do {
    $buttons = $xpath->query('//div[@id="listennavi"]/div[contains(@class,"listennaviright")]/a');
    $button = $buttons->item(0);
    $more_pages = (strpos($button->getAttribute('class'), 'active') !== FALSE);
    
    $rows = $xpath->query('//div[@id="liste"]//h2/a');
    
    echo "processing " . ($rows->length) . " projects...\n";
    foreach ($rows as $a) {
        if ($max_single_view_pages-- < 1) break;
        $single_view = ltrim(html_entity_decode($a->getAttribute('href')), "?");
// */

/*
    foreach ($projects as $p) {
        $single_view = "module=gepris&task=showDetail&context=projekt&id=" . $p;
*/

        if (!preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $single_view, $m)) continue;

        $project = array();
        $project['id'] = $m[1];
// /*
        echo "loading single view of " . strip_off_multiple_spaces(strip_tags($a->nodeValue)) . "\n";
// */
            
        $html = load_html($view, $single_view);
        @$docSingleView->loadHTML($html);
        $xpathSingleView = new DOMXpath($docSingleView);
            
        $h3 = $xpathSingleView->query('//div[contains(@class,"detailed")]/div[contains(@class,"details")]/h3');
        $h3 = $h3->item(0);
        $project['name'] = strip_off_multiple_spaces($h3->nodeValue);

        $description = $xpathSingleView->query('//div[contains(@class,"detailed")]//div[@id="projekttext"]');
        $description = $description->item(0);
        $project['description'] = strip_off_multiple_spaces($description->nodeValue);

        $data = $xpathSingleView->query('//div[contains(@class,"detailed")]//div/div/span');

        for ($i = 0; $i < (($data->length) - 1); $i+=2) {
            $key = $data->item($i);
            $key = strip_off_multiple_spaces(strip_tags($key->nodeValue));
            $key = trim($key);
            $value = $data->item($i + 1);
            if ($key == 'Webseite') {
                $anchor = $xpathSingleView->query($value->getNodePath() . '/a');
                $anchor = $anchor->item(0);
                $project[$key] = html_entity_decode(strip_off_multiple_spaces(($anchor->getAttribute('href'))));
            }
            elseif ($key == 'Teilprojekt zu' || $key == 'beteiligter Wissenschaftler:' || $key == 'Teilprojektleiter:' || $key == 'Sprecher:' || $key == 'Antragstellende Institution:' || $key == 'Mitantragstellende Institution:' || $key == 'Beteiligte Institution:' || $key == 'ausländische Institution:' || $key == 'Kooperationspartner:' || $key == 'ausländischer Sprecher:' || $key == 'Stellvertreter:' || $key == 'Antragsteller:' || $key == 'Beteiligte Person:' || $key == 'Mitantragsteller:' || $key == 'Leiter:' || $key == 'Beteiligte Hochschule:' || $key == 'Partnerorganisation:') {
                $anchors = $xpathSingleView->query($value->getNodePath() . '/a');
                $idString = "";
                foreach ($anchors as $anchor) {
                    preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $anchor->getAttribute('href'), $m);
                    $idString .= $m[1] . ",";
                }
                $project[$key] = $idString;
            }
            elseif ($key == 'Ehemaliger Antragsteller:') {
                $anchors = $xpathSingleView->query($value->getNodePath() . '/a');
                if ($anchors->length == 1) {
                    $value = html_entity_decode(innerHTML($value));
                    echo $value;
                    $idString = "";
                    preg_match('/^.*?href=\"(?:(?:\?id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?\".*?>.*?<\/a>(?:, (?:von \d+\/\d\d\d\d )?bis (\d+\/\d\d\d\d))?.*?$/', $value, $m);
                    $idString .= $m[1] . (isset($m[2]) ? " (" . $m[2] . ")" : '');
                    $project[$key] = $idString;
                }
                else
                    $project[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
            }
            elseif ($key == 'verfahrenstechnischer DFG-Ansprechpartner:') ;
            elseif ($key == 'fachlicher DFG-Ansprechpartner:') ;
            else
                $project[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
        }

        //echo json_encode($institution) . "\n";

        scraperwiki::save(array('id'), $project);
    }

// /*
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
// */

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

/*
$projects = array(
5377227,
5380173,
);
*/

// /*
$max_single_view_pages = 13636;
$max_list_view_pages = 1400;

$params = "beginOfFunding=&bewilligungsStatus=&bundesland=DEU%23&context=projekt&fachgebiet=%23&findButton=historyCall&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=&procedure=%23&task=doKatalog&teilprojekte=true&index=73010";

$html = load_html($view, $params);
@$doc->loadHTML($html);
$xpath = new DOMXpath($doc);
$headline = $xpath->query("//div[@id='listennavi']/span");
if (!is_null($headline)) {
   $headline = $headline->item(0);
   echo strip_off_multiple_spaces(strip_tags($headline->nodeValue)) . "\n";
}
do {
    $buttons = $xpath->query('//div[@id="listennavi"]/div[contains(@class,"listennaviright")]/a');
    $button = $buttons->item(0);
    $more_pages = (strpos($button->getAttribute('class'), 'active') !== FALSE);
    
    $rows = $xpath->query('//div[@id="liste"]//h2/a');
    
    echo "processing " . ($rows->length) . " projects...\n";
    foreach ($rows as $a) {
        if ($max_single_view_pages-- < 1) break;
        $single_view = ltrim(html_entity_decode($a->getAttribute('href')), "?");
// */

/*
    foreach ($projects as $p) {
        $single_view = "module=gepris&task=showDetail&context=projekt&id=" . $p;
*/

        if (!preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $single_view, $m)) continue;

        $project = array();
        $project['id'] = $m[1];
// /*
        echo "loading single view of " . strip_off_multiple_spaces(strip_tags($a->nodeValue)) . "\n";
// */
            
        $html = load_html($view, $single_view);
        @$docSingleView->loadHTML($html);
        $xpathSingleView = new DOMXpath($docSingleView);
            
        $h3 = $xpathSingleView->query('//div[contains(@class,"detailed")]/div[contains(@class,"details")]/h3');
        $h3 = $h3->item(0);
        $project['name'] = strip_off_multiple_spaces($h3->nodeValue);

        $description = $xpathSingleView->query('//div[contains(@class,"detailed")]//div[@id="projekttext"]');
        $description = $description->item(0);
        $project['description'] = strip_off_multiple_spaces($description->nodeValue);

        $data = $xpathSingleView->query('//div[contains(@class,"detailed")]//div/div/span');

        for ($i = 0; $i < (($data->length) - 1); $i+=2) {
            $key = $data->item($i);
            $key = strip_off_multiple_spaces(strip_tags($key->nodeValue));
            $key = trim($key);
            $value = $data->item($i + 1);
            if ($key == 'Webseite') {
                $anchor = $xpathSingleView->query($value->getNodePath() . '/a');
                $anchor = $anchor->item(0);
                $project[$key] = html_entity_decode(strip_off_multiple_spaces(($anchor->getAttribute('href'))));
            }
            elseif ($key == 'Teilprojekt zu' || $key == 'beteiligter Wissenschaftler:' || $key == 'Teilprojektleiter:' || $key == 'Sprecher:' || $key == 'Antragstellende Institution:' || $key == 'Mitantragstellende Institution:' || $key == 'Beteiligte Institution:' || $key == 'ausländische Institution:' || $key == 'Kooperationspartner:' || $key == 'ausländischer Sprecher:' || $key == 'Stellvertreter:' || $key == 'Antragsteller:' || $key == 'Beteiligte Person:' || $key == 'Mitantragsteller:' || $key == 'Leiter:' || $key == 'Beteiligte Hochschule:' || $key == 'Partnerorganisation:') {
                $anchors = $xpathSingleView->query($value->getNodePath() . '/a');
                $idString = "";
                foreach ($anchors as $anchor) {
                    preg_match('/^(?:(?:id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?$/', $anchor->getAttribute('href'), $m);
                    $idString .= $m[1] . ",";
                }
                $project[$key] = $idString;
            }
            elseif ($key == 'Ehemaliger Antragsteller:') {
                $anchors = $xpathSingleView->query($value->getNodePath() . '/a');
                if ($anchors->length == 1) {
                    $value = html_entity_decode(innerHTML($value));
                    echo $value;
                    $idString = "";
                    preg_match('/^.*?href=\"(?:(?:\?id=)|(?:.*?&id=))(.+?)(?:&.+=.*)?\".*?>.*?<\/a>(?:, (?:von \d+\/\d\d\d\d )?bis (\d+\/\d\d\d\d))?.*?$/', $value, $m);
                    $idString .= $m[1] . (isset($m[2]) ? " (" . $m[2] . ")" : '');
                    $project[$key] = $idString;
                }
                else
                    $project[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
            }
            elseif ($key == 'verfahrenstechnischer DFG-Ansprechpartner:') ;
            elseif ($key == 'fachlicher DFG-Ansprechpartner:') ;
            else
                $project[$key] = br2nl(strip_off_multiple_spaces(html_entity_decode(innerHTML($value), ENT_QUOTES, "UTF-8")));
        }

        //echo json_encode($institution) . "\n";

        scraperwiki::save(array('id'), $project);
    }

// /*
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
// */

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