<?php
require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();

for ($i=1; $i <= 8; $i++){

    $page_URL = "http://www.apsc.ru/apsc-members/page_".$i;
    $html = scraperWiki::scrape($page_URL); 
                  

    $dom->load($html);
    foreach($dom->find("td.sobi2Details") as $data){
    
        $title = $data->find("p.sobi2ItemTitle");
        $city = $data->find("span.sobi2Listing_field_city");
        $services = $data->find("ul.sobi2Listing_field_1");
        $phone = $data->find("span.sobi2Listing_field_phone"); 
        $site = $data->find("span.sobi2Listing_field_website"); 
    
        $record = array(
            'title' => $title[0]->plaintext, 
            'city' => $city[0]->plaintext,
            'services' => $services[0]->innertext,
            'phone' => $phone[0]->plaintext,
            'site' => $site[0]->plaintext
        );
     
    
        //print_r($record);
        scraperwiki::save(array('title'), $record);
    
    }
}

?>
<?php
require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();

for ($i=1; $i <= 8; $i++){

    $page_URL = "http://www.apsc.ru/apsc-members/page_".$i;
    $html = scraperWiki::scrape($page_URL); 
                  

    $dom->load($html);
    foreach($dom->find("td.sobi2Details") as $data){
    
        $title = $data->find("p.sobi2ItemTitle");
        $city = $data->find("span.sobi2Listing_field_city");
        $services = $data->find("ul.sobi2Listing_field_1");
        $phone = $data->find("span.sobi2Listing_field_phone"); 
        $site = $data->find("span.sobi2Listing_field_website"); 
    
        $record = array(
            'title' => $title[0]->plaintext, 
            'city' => $city[0]->plaintext,
            'services' => $services[0]->innertext,
            'phone' => $phone[0]->plaintext,
            'site' => $site[0]->plaintext
        );
     
    
        //print_r($record);
        scraperwiki::save(array('title'), $record);
    
    }
}

?>
