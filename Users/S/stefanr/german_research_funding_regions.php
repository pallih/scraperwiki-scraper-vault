<?php

require 'scraperwiki/simple_html_dom.php';

$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$params = "context=projekt&module=gepris&task=showKatalog";

$html = load_html($view, $params);

$dom = new simple_html_dom();
$dom->load($html);

$dropDownList = ($dom->find("#bundesland", 0));

$max = 200;

foreach ($dropDownList->children() as $option) {
    if ($option->tag != 'option') continue;
    if ($option->value == 'DEU#') continue;
    if ($max-- < 1) break;

    preg_match('/^DEU(\d+)$/', $option->value, $m);

    $region = array();
    $region['state'] = (int) ($m[1]);
    echo 'Wechsel zu Bundesland ' . $option->plaintext . "\n";
    $params = 'beginOfFunding=&bewilligungsStatus=&context=projekt&fachgebiet=%23&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=%23&procedure=%23&task=doKatalog&teilprojekte=true&bundesland=' . ($option->value);

    $html = load_html($view, $params);
    $dom->load($html);
    
    $regionList = ($dom->find("#locationKey", 0));

    foreach ($regionList->children() as $option) {

        if ($option->tag != 'option') continue;
        if ($option->value == 'DEU' . $region['state'] . '#') continue;

        preg_match('/^DEU' . $region['state'] . '(.*?)$/', $option->value, $m);

        $region['id'] = ($m[1]);
        $region['name'] = $option->plaintext;

        scraperwiki::save(array('id'), $region);
    }
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
    echo $cookies . "\n";
    
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

require 'scraperwiki/simple_html_dom.php';

$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$params = "context=projekt&module=gepris&task=showKatalog";

$html = load_html($view, $params);

$dom = new simple_html_dom();
$dom->load($html);

$dropDownList = ($dom->find("#bundesland", 0));

$max = 200;

foreach ($dropDownList->children() as $option) {
    if ($option->tag != 'option') continue;
    if ($option->value == 'DEU#') continue;
    if ($max-- < 1) break;

    preg_match('/^DEU(\d+)$/', $option->value, $m);

    $region = array();
    $region['state'] = (int) ($m[1]);
    echo 'Wechsel zu Bundesland ' . $option->plaintext . "\n";
    $params = 'beginOfFunding=&bewilligungsStatus=&context=projekt&fachgebiet=%23&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=%23&procedure=%23&task=doKatalog&teilprojekte=true&bundesland=' . ($option->value);

    $html = load_html($view, $params);
    $dom->load($html);
    
    $regionList = ($dom->find("#locationKey", 0));

    foreach ($regionList->children() as $option) {

        if ($option->tag != 'option') continue;
        if ($option->value == 'DEU' . $region['state'] . '#') continue;

        preg_match('/^DEU' . $region['state'] . '(.*?)$/', $option->value, $m);

        $region['id'] = ($m[1]);
        $region['name'] = $option->plaintext;

        scraperwiki::save(array('id'), $region);
    }
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
    echo $cookies . "\n";
    
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

require 'scraperwiki/simple_html_dom.php';

$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$params = "context=projekt&module=gepris&task=showKatalog";

$html = load_html($view, $params);

$dom = new simple_html_dom();
$dom->load($html);

$dropDownList = ($dom->find("#bundesland", 0));

$max = 200;

foreach ($dropDownList->children() as $option) {
    if ($option->tag != 'option') continue;
    if ($option->value == 'DEU#') continue;
    if ($max-- < 1) break;

    preg_match('/^DEU(\d+)$/', $option->value, $m);

    $region = array();
    $region['state'] = (int) ($m[1]);
    echo 'Wechsel zu Bundesland ' . $option->plaintext . "\n";
    $params = 'beginOfFunding=&bewilligungsStatus=&context=projekt&fachgebiet=%23&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=%23&procedure=%23&task=doKatalog&teilprojekte=true&bundesland=' . ($option->value);

    $html = load_html($view, $params);
    $dom->load($html);
    
    $regionList = ($dom->find("#locationKey", 0));

    foreach ($regionList->children() as $option) {

        if ($option->tag != 'option') continue;
        if ($option->value == 'DEU' . $region['state'] . '#') continue;

        preg_match('/^DEU' . $region['state'] . '(.*?)$/', $option->value, $m);

        $region['id'] = ($m[1]);
        $region['name'] = $option->plaintext;

        scraperwiki::save(array('id'), $region);
    }
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
    echo $cookies . "\n";
    
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

require 'scraperwiki/simple_html_dom.php';

$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$params = "context=projekt&module=gepris&task=showKatalog";

$html = load_html($view, $params);

$dom = new simple_html_dom();
$dom->load($html);

$dropDownList = ($dom->find("#bundesland", 0));

$max = 200;

foreach ($dropDownList->children() as $option) {
    if ($option->tag != 'option') continue;
    if ($option->value == 'DEU#') continue;
    if ($max-- < 1) break;

    preg_match('/^DEU(\d+)$/', $option->value, $m);

    $region = array();
    $region['state'] = (int) ($m[1]);
    echo 'Wechsel zu Bundesland ' . $option->plaintext . "\n";
    $params = 'beginOfFunding=&bewilligungsStatus=&context=projekt&fachgebiet=%23&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=%23&procedure=%23&task=doKatalog&teilprojekte=true&bundesland=' . ($option->value);

    $html = load_html($view, $params);
    $dom->load($html);
    
    $regionList = ($dom->find("#locationKey", 0));

    foreach ($regionList->children() as $option) {

        if ($option->tag != 'option') continue;
        if ($option->value == 'DEU' . $region['state'] . '#') continue;

        preg_match('/^DEU' . $region['state'] . '(.*?)$/', $option->value, $m);

        $region['id'] = ($m[1]);
        $region['name'] = $option->plaintext;

        scraperwiki::save(array('id'), $region);
    }
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
    echo $cookies . "\n";
    
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