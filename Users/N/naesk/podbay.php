<?php

$html = scraperWiki::scrape("http://podupti.me/");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("//table/tbody/tr/td[1]") as $data){
    $pod = $data->find("a[href]");
    $record = array(
        'pod' => $pod[0]->plaintext, 
        'country' => geoip_country_code_by_name($pod[0]->plaintext),
    );
        //print_r($record);
        scraperwiki::save(array('pod','country'), $record);

}

?>
<?php

$html = scraperWiki::scrape("http://podupti.me/");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("//table/tbody/tr/td[1]") as $data){
    $pod = $data->find("a[href]");
    $record = array(
        'pod' => $pod[0]->plaintext, 
        'country' => geoip_country_code_by_name($pod[0]->plaintext),
    );
        //print_r($record);
        scraperwiki::save(array('pod','country'), $record);

}

?>
