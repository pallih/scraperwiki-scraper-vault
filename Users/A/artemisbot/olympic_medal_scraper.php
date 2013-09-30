<?php

include('scraperwiki/simple_html_dom.php');

$html = file_get_html('http://m.london2012.com/medals/medal-winners/');
 

$athletes = array();

foreach($html->find('table.overall-medalist tr') as $element) 
{
    $name = $element->find('div.athlete a',0)->plaintext;
  
    $country = $element->find('span.countryName',0)->plaintext;
    
    $fullCountryName = $element->find('div.country img',0)->alt;
    
    $sport = $element->find('span.disciplineName',0)->plaintext;
    
    $golds = $element->find('td.g',0)->plaintext;
    
    $silvers = $element->find('td.s',0)->plaintext;
    
    $bronzes = $element->find('td.b',0)->plaintext;

    $medals = $golds + $silvers + $bronzes;

    
    $athletes = array(
        "name" => $name,
        "country_code" => $country,
        "country_name" => $fullCountryName,
        "sport" => $sport,
        "golds" => $golds,
        "silvers" => $silvers,
        "bronze" => $bronzes,
        "overall_medals" => $medals
   );
}
scraperwiki::save(array("name"),$athletes);
 <?php

include('scraperwiki/simple_html_dom.php');

$html = file_get_html('http://m.london2012.com/medals/medal-winners/');
 

$athletes = array();

foreach($html->find('table.overall-medalist tr') as $element) 
{
    $name = $element->find('div.athlete a',0)->plaintext;
  
    $country = $element->find('span.countryName',0)->plaintext;
    
    $fullCountryName = $element->find('div.country img',0)->alt;
    
    $sport = $element->find('span.disciplineName',0)->plaintext;
    
    $golds = $element->find('td.g',0)->plaintext;
    
    $silvers = $element->find('td.s',0)->plaintext;
    
    $bronzes = $element->find('td.b',0)->plaintext;

    $medals = $golds + $silvers + $bronzes;

    
    $athletes = array(
        "name" => $name,
        "country_code" => $country,
        "country_name" => $fullCountryName,
        "sport" => $sport,
        "golds" => $golds,
        "silvers" => $silvers,
        "bronze" => $bronzes,
        "overall_medals" => $medals
   );
}
scraperwiki::save(array("name"),$athletes);
 