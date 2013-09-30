<?php

require 'scraperwiki/simple_html_dom.php';
$result = array();

$dom = new simple_html_dom();

$uri = "http://support.google.com/webmasters/bin/answer.py?hl=en&answer=1645432";
$content = scraperwiki::scrape($uri); 
$dom->load($content);

$headings = $dom->find('#article-content-div h4');
$tables = $dom->find('#article-content-div table');
foreach ($headings as $heading) {
    $types = explode('&gt;', $heading);
    $type = trim(str_replace('</h4>', '', array_pop($types)));

    $properties = array();

    $table = array_shift($tables);
    foreach ($table->find('tr') as $tr) {
        $tds = $tr->find('td');
        if ($td = array_shift($tds)) {
            $properties[] = $td->text();
        }
    }
    if ($type == 'SoftwareApplication') {
        $softapp_properties = $properties;
    }
    else {
        $properties = array_merge($softapp_properties, $properties);
    }
    $record = array(
        'label' => $type,
        'url' => 'http://schema.org/' . $type,
        'properties' => serialize($properties),
    );
    scraperwiki::save(array('url'), $record);
}

/*$uri = "http://support.google.com/webmasters/bin/answer.py?hl=en&answer=1645527";
$content = scraperwiki::scrape($uri); 
$dom->load($content);

foreach ($dom->find('#article-content-div li') as $li) {
    $split = explode(' ', $li->text());
    $type = $split[0];
    /*$attributes = array(
        'label' => $type,
        'url' => 'http://schema.org/' . $type,
        'properties' => $softapp_properties,
    );
    $result['types'][$type] = $attributes;
}*/

?>
<?php

require 'scraperwiki/simple_html_dom.php';
$result = array();

$dom = new simple_html_dom();

$uri = "http://support.google.com/webmasters/bin/answer.py?hl=en&answer=1645432";
$content = scraperwiki::scrape($uri); 
$dom->load($content);

$headings = $dom->find('#article-content-div h4');
$tables = $dom->find('#article-content-div table');
foreach ($headings as $heading) {
    $types = explode('&gt;', $heading);
    $type = trim(str_replace('</h4>', '', array_pop($types)));

    $properties = array();

    $table = array_shift($tables);
    foreach ($table->find('tr') as $tr) {
        $tds = $tr->find('td');
        if ($td = array_shift($tds)) {
            $properties[] = $td->text();
        }
    }
    if ($type == 'SoftwareApplication') {
        $softapp_properties = $properties;
    }
    else {
        $properties = array_merge($softapp_properties, $properties);
    }
    $record = array(
        'label' => $type,
        'url' => 'http://schema.org/' . $type,
        'properties' => serialize($properties),
    );
    scraperwiki::save(array('url'), $record);
}

/*$uri = "http://support.google.com/webmasters/bin/answer.py?hl=en&answer=1645527";
$content = scraperwiki::scrape($uri); 
$dom->load($content);

foreach ($dom->find('#article-content-div li') as $li) {
    $split = explode(' ', $li->text());
    $type = $split[0];
    /*$attributes = array(
        'label' => $type,
        'url' => 'http://schema.org/' . $type,
        'properties' => $softapp_properties,
    );
    $result['types'][$type] = $attributes;
}*/

?>
