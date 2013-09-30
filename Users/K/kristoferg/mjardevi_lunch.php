<?php
require 'scraperwiki/simple_html_dom.php';           

$html = scraperWiki::scrape("http://www.mjardevi.se/en/service/restaurants/lunch-menues?tmpl=component&print=1&page=");

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.lunchMeny") as $div){
    $p = $div->find("p");

        $record = array(
        'restaurant' => 'Chili & Lime',
        'menu' => $p[1]->plaintext
        );
$record['menu'] = preg_replace('/\s\s+/', ' ', $record['menu']);
print_r($record['menu']);

        scraperwiki::save(array('restaurant'), $record);  

        $record = array(
        'restaurant' => 'Collegium',
        'menu' => $p[3]->plaintext
        );
        scraperwiki::save(array('restaurant'), $record);  

        $record = array(
        'restaurant' => 'Com.Inn',
        'menu' => $p[5]->plaintext
        );
        scraperwiki::save(array('restaurant'), $record);  

        $record = array(
        'restaurant' => 'Husman',
        'menu' => $p[9]->plaintext
        );
        scraperwiki::save(array('restaurant'), $record);  
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';           

$html = scraperWiki::scrape("http://www.mjardevi.se/en/service/restaurants/lunch-menues?tmpl=component&print=1&page=");

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.lunchMeny") as $div){
    $p = $div->find("p");

        $record = array(
        'restaurant' => 'Chili & Lime',
        'menu' => $p[1]->plaintext
        );
$record['menu'] = preg_replace('/\s\s+/', ' ', $record['menu']);
print_r($record['menu']);

        scraperwiki::save(array('restaurant'), $record);  

        $record = array(
        'restaurant' => 'Collegium',
        'menu' => $p[3]->plaintext
        );
        scraperwiki::save(array('restaurant'), $record);  

        $record = array(
        'restaurant' => 'Com.Inn',
        'menu' => $p[5]->plaintext
        );
        scraperwiki::save(array('restaurant'), $record);  

        $record = array(
        'restaurant' => 'Husman',
        'menu' => $p[9]->plaintext
        );
        scraperwiki::save(array('restaurant'), $record);  
}

?>
