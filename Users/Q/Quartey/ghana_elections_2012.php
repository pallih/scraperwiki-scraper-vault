<?php

print "Hello, coding in the cloud!";
$html = scraperWiki::scrape("http://www.ec.gov.gh/page.php?page=469&section=49&typ=1");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'name' => $tds[0]->plaintext, 
            'region' => intval($tds[4]->plaintext),
            'consltituency' => intval($tds[4]->plaintext),
            'party' => intval($tds[4]->plaintext),
            'image' => intval($tds[4]->image)
        );
        print json_encode($record) . "\n";
    }
}
scraperwiki::save(array('region'), $record);


?>
<?php

print "Hello, coding in the cloud!";
$html = scraperWiki::scrape("http://www.ec.gov.gh/page.php?page=469&section=49&typ=1");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'name' => $tds[0]->plaintext, 
            'region' => intval($tds[4]->plaintext),
            'consltituency' => intval($tds[4]->plaintext),
            'party' => intval($tds[4]->plaintext),
            'image' => intval($tds[4]->image)
        );
        print json_encode($record) . "\n";
    }
}
scraperwiki::save(array('region'), $record);


?>
