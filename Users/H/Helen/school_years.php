<?php
$html = scraperWiki::scrape("http://cms.walsall.gov.uk/index/environment/planning/planning_registers/weekly_list_of_received_planning_applications.htm");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );
        scraperwiki::save(array('country'), $record);

}




?>
<?php
$html = scraperWiki::scrape("http://cms.walsall.gov.uk/index/environment/planning/planning_registers/weekly_list_of_received_planning_applications.htm");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );
        scraperwiki::save(array('country'), $record);

}




?>
