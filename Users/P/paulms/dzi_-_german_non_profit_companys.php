<?php

require_once 'scraperwiki/simple_html_dom.php';           

//create a list of the A-Z Index URLS
$indexUrl = "http://www.dzi.de/spenderberatung/das-spenden-siegel/liste-aller-spenden-siegel-organisationen-a-z/index/%s/";

//Loop through A-Z and parse all NGOS
$ngos = array();
foreach(range('A', 'Z') as $letter) {
    $url = sprintf($indexUrl,  $letter);
    $ngos = array_merge($ngos, scrapeIndex($url));
}

/*
    scrape an index page and return an array of all ngos (name, url) found on the page
*/
function scrapeIndex($url){
    $html_content = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html_content);

    $ngos = array();
    foreach ($dom->find('h2') as $h2){
        $name = str_replace("&#8211;", "-", html_entity_decode($h2->plaintext));
        $url = $h2->find('a',0);
        $url = $url->href;
        
        $ngos[] = array("name" => $name, "url" => $url);
        scraperwiki::save_sqlite(array("name"),array("name"=> $name, "url"=>$url), "ngos");
    }
    print_r($ngos);
    return $ngos;
}





?>
<?php

require_once 'scraperwiki/simple_html_dom.php';           

//create a list of the A-Z Index URLS
$indexUrl = "http://www.dzi.de/spenderberatung/das-spenden-siegel/liste-aller-spenden-siegel-organisationen-a-z/index/%s/";

//Loop through A-Z and parse all NGOS
$ngos = array();
foreach(range('A', 'Z') as $letter) {
    $url = sprintf($indexUrl,  $letter);
    $ngos = array_merge($ngos, scrapeIndex($url));
}

/*
    scrape an index page and return an array of all ngos (name, url) found on the page
*/
function scrapeIndex($url){
    $html_content = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html_content);

    $ngos = array();
    foreach ($dom->find('h2') as $h2){
        $name = str_replace("&#8211;", "-", html_entity_decode($h2->plaintext));
        $url = $h2->find('a',0);
        $url = $url->href;
        
        $ngos[] = array("name" => $name, "url" => $url);
        scraperwiki::save_sqlite(array("name"),array("name"=> $name, "url"=>$url), "ngos");
    }
    print_r($ngos);
    return $ngos;
}





?>
