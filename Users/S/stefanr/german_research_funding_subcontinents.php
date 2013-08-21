<?php

require 'scraperwiki/simple_html_dom.php';

$domain = "http://gepris.dfg.de";
$view = $domain . "/gepris/OCTOPUS/";
$params = "extendButton=Erweiterte+Suche+ausklappen&task=doSearchSimple&context=projekt";

$html = load_html($view, $params);

$dom = new simple_html_dom();
$dom->load($html);

$dropDownList = ($dom->find("#continentId", 0));

$max = 200;

foreach ($dropDownList->children() as $option) {
    if ($option->tag != 'option') continue;
    if ($option->value == '#') continue;
    if ($max-- < 1) break;

    $subContinent = array();
    $subContinent['continent'] = (int) ($option->value);
    $params = 'task=doSearchExtended&context=projekt&nurProjekteMitAB=false&refreshButton=refresh&fachlicheZuordnung=%23&procedure=%23&teilprojekte=false&teilprojekte=true&bewilligungsStatus=&beginOfFunding=&oldContinentId=%23&oldSubContinentId=%23%23&subContinentId=%23%23&oldCountryId=%23%23%23&countryKey=%23%23%23&continentId=' . ($option->value);

    $html = load_html($view, $params);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $subContinentList = ($dom->find("#subContinentId", 0));

    foreach ($subContinentList->children() as $option) {

        if ($option->tag != 'option') continue;
        if (((int) ($option->value)) == $subContinent['continent']) continue;

        $subContinent['id'] = (int) ($option->value);
        $subContinent['name'] = $option->plaintext;

        scraperwiki::save(array('id'), $subContinent);
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