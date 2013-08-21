<?php
$html = scraperWiki::scrape("http://jackfmoxfordshire.co.uk/partners");
require 'scraperwiki/simple_html_dom.php';
$directory = new simple_html_dom();
$directory->load($html);

foreach($directory->find(".views-accordion-item") as $company){

    $record = array(
        'company' => $company->find(".title", 0)->plaintext,
        'notes' => $company->find(".intro", 0)->plaintext,
        'address' => $company->find(".address", 0)->plaintext,
        'phone' => $company->find(".phone", 0)->plaintext,
        'website' => $company->find(".website a", 0)->href
    );

    scraperwiki::save(array('company'), $record);
    //print json_encode($record) . "\n";

}
?>
