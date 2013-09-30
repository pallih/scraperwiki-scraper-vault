<?php

$html = scraperWiki::scrape("http://www.saatiopalvelu.fi/fi/apurahan-hakijalle/hae-apurahojen-myontajia/?field=all&allowanceSearch=&pastPeriods=t&currentPeriods=t&upcomingPeriods=t&search=Hae");

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span.foundationName") as $data){
//[@align='left'] tr
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );
    print $record . "\n";
//    scraperwiki::save(array('country'), $record);
}


?>
<?php

$html = scraperWiki::scrape("http://www.saatiopalvelu.fi/fi/apurahan-hakijalle/hae-apurahojen-myontajia/?field=all&allowanceSearch=&pastPeriods=t&currentPeriods=t&upcomingPeriods=t&search=Hae");

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span.foundationName") as $data){
//[@align='left'] tr
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );
    print $record . "\n";
//    scraperwiki::save(array('country'), $record);
}


?>
