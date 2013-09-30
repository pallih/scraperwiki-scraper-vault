<?php

$html = scraperWiki::scrape("http://www.helloaddress.com/onlineproperty/af/search/search/SearchProperty.do?PROPERTY_DISTRICT=Ernakulam&searchProperty=true");        require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("td[@class='srtdStyle1']") as $data){
    $title= $data->find("strong");
     
        $record = array(
            'title' => $title[0]->plaintext
        );
        print json_encode($record) . "\n";
scraperwiki::save(array('title'), $record);  
     
}   
         

?>
<?php

$html = scraperWiki::scrape("http://www.helloaddress.com/onlineproperty/af/search/search/SearchProperty.do?PROPERTY_DISTRICT=Ernakulam&searchProperty=true");        require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("td[@class='srtdStyle1']") as $data){
    $title= $data->find("strong");
     
        $record = array(
            'title' => $title[0]->plaintext
        );
        print json_encode($record) . "\n";
scraperwiki::save(array('title'), $record);  
     
}   
         

?>
