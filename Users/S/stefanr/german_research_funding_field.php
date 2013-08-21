<?php

require 'scraperwiki/simple_html_dom.php';

$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$params = "context=projekt&module=gepris&task=showKatalog";

$html = load_html($view, $params);

$dom = new simple_html_dom();
$dom->load($html);

$dropDownList = ($dom->find("#fachgebiet", 0));

foreach ($dropDownList->children() as $option) {
    if ($option->tag != 'option') continue;
    if ($option->value == '#') continue;

    echo 'Wechsel zu Fachgebiet ' . $option->plaintext . "\n";
    $subjectGroup = ($option->value);
    $params = 'beginOfFunding=&bewilligungsStatus=&bundesland=DEU%23&context=projekt&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=%23&procedure=%23&task=doKatalog&teilprojekte=true&fachgebiet=' . $subjectGroup;

    $html = load_html($view, $params);
    $dom->load($html);
    
    $councilList = ($dom->find("#fachkollegium", 0));

    foreach ($councilList->children() as $option) {

        if ($option->tag != 'option') continue;
        if ($option->value == '#') continue;

        $field = array();
        $field['council'] = (int) ($option->value);

        echo 'Wechsel zu Fachkollegium ' . $option->plaintext . "\n";
        $params = 'task=doKatalog&context=projekt&nurProjekteMitAB=false&bundesland=DEU%23&procedure=%23&bewilligungsStatus=&beginOfFunding=&teilprojekte=false&teilprojekte=true&oldGgsHunderter=0&ggsHunderter=0&oldfachgebiet=' . $subjectGroup . '&fachgebiet=' . $subjectGroup . '&fachkollegium=' . ($option->value);
    
        $html = load_html($view, $params);
        $dom->load($html);
       
        $fieldList = ($dom->find("#fach", 0));
    
        foreach ($fieldList->children() as $option) {
    
            if ($option->tag != 'option') continue;
            if ($option->value == '#') continue;

            $field['id'] = (int) ($option->value);
            $field['name'] = $option->plaintext;

            scraperwiki::save(array('id'), $field);
        }
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

$dropDownList = ($dom->find("#fachgebiet", 0));

foreach ($dropDownList->children() as $option) {
    if ($option->tag != 'option') continue;
    if ($option->value == '#') continue;

    echo 'Wechsel zu Fachgebiet ' . $option->plaintext . "\n";
    $subjectGroup = ($option->value);
    $params = 'beginOfFunding=&bewilligungsStatus=&bundesland=DEU%23&context=projekt&ggsHunderter=0&module=gepris&nurProjekteMitAB=false&oldGgsHunderter=0&oldfachgebiet=%23&procedure=%23&task=doKatalog&teilprojekte=true&fachgebiet=' . $subjectGroup;

    $html = load_html($view, $params);
    $dom->load($html);
    
    $councilList = ($dom->find("#fachkollegium", 0));

    foreach ($councilList->children() as $option) {

        if ($option->tag != 'option') continue;
        if ($option->value == '#') continue;

        $field = array();
        $field['council'] = (int) ($option->value);

        echo 'Wechsel zu Fachkollegium ' . $option->plaintext . "\n";
        $params = 'task=doKatalog&context=projekt&nurProjekteMitAB=false&bundesland=DEU%23&procedure=%23&bewilligungsStatus=&beginOfFunding=&teilprojekte=false&teilprojekte=true&oldGgsHunderter=0&ggsHunderter=0&oldfachgebiet=' . $subjectGroup . '&fachgebiet=' . $subjectGroup . '&fachkollegium=' . ($option->value);
    
        $html = load_html($view, $params);
        $dom->load($html);
       
        $fieldList = ($dom->find("#fach", 0));
    
        foreach ($fieldList->children() as $option) {
    
            if ($option->tag != 'option') continue;
            if ($option->value == '#') continue;

            $field['id'] = (int) ($option->value);
            $field['name'] = $option->plaintext;

            scraperwiki::save(array('id'), $field);
        }
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