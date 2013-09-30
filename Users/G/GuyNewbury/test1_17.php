<?php

$html = scraperWiki::scrape("http://www.easyinfo.co.za/catsearch.php?link_code=12&heading=Bed&province=2|021");            
require 'scraperwiki/simple_html_dom.php';            
$dom = new simple_html_dom();
$dom->load($html);

$foundCompanies = array();
$i = 1;
while ($i <= 10) {
    echo $i++;
    
    //$result_heading = $data->find('results_heading', $i)->plaintext;
    $company_name = $dom->find('div[id=results_heading]', $i)->plaintext;
    echo $company_name;
//    $company_name = trim($company_name);
//    $company_name = substr($company_name, 5);
//    $company_name = trim($company_name);
    
    //$foundCompanies['name'] = $company_name;


    //print_r(scraperwiki::show_tables());
 

    //$record = array('company' => $company_name);     
    //print_r($record);
    //scraperwiki::save_sqlite('company' => $company_name);
    //scraperwiki::save_sqlite(array("company"),array("company" => $company_name, "bbb"=>"Hi there"));
    //scraperwiki::save(array('country'), $record);



            $foundCompanies = array_push (
                'name' => html_entity_decode($company_name),
            );


}

            scraperwiki::save(array('name'), $prem);

?><?php

$html = scraperWiki::scrape("http://www.easyinfo.co.za/catsearch.php?link_code=12&heading=Bed&province=2|021");            
require 'scraperwiki/simple_html_dom.php';            
$dom = new simple_html_dom();
$dom->load($html);

$foundCompanies = array();
$i = 1;
while ($i <= 10) {
    echo $i++;
    
    //$result_heading = $data->find('results_heading', $i)->plaintext;
    $company_name = $dom->find('div[id=results_heading]', $i)->plaintext;
    echo $company_name;
//    $company_name = trim($company_name);
//    $company_name = substr($company_name, 5);
//    $company_name = trim($company_name);
    
    //$foundCompanies['name'] = $company_name;


    //print_r(scraperwiki::show_tables());
 

    //$record = array('company' => $company_name);     
    //print_r($record);
    //scraperwiki::save_sqlite('company' => $company_name);
    //scraperwiki::save_sqlite(array("company"),array("company" => $company_name, "bbb"=>"Hi there"));
    //scraperwiki::save(array('country'), $record);



            $foundCompanies = array_push (
                'name' => html_entity_decode($company_name),
            );


}

            scraperwiki::save(array('name'), $prem);

?>