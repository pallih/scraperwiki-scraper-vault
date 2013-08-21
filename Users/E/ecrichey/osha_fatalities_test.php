<?php

require 'scraperwiki/simple_html_dom.php';
print "Hello world! Running...";

$html = scraperWiki::scrape("http://www.osha.gov/pls/imis/AccidentSearch.search?p_logger=1&Fatal=fatal&sic=15&Office=All&officetype=All&endmonth=01&endday=01&endyear=2002&startmonth=12&startday=31&startyear=2012");
//print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==8){
        $record = array(
            'summary link' => $tds[2]->plaintext,
            'event date' => $tds[3]->plaintext,
           'report id' => $tds[4]->plaintext,
           'fatality' => $tds[5]->plaintext,
           'SIC' => $tds[6]->plaintext,
          'event description' => $tds[7]->plaintext
      );
       print json_encode($record) . "\n";
       scraperwiki::save(array('summary link'), $record);
  }}


$html=scraperWiki::scrape("http://www.osha.gov/pls/imis/accidentsearch.search?sic=15&sicgroup=&acc_description=&acc_abstract=&acc_keyword=&inspnr=&fatal=fatal&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2002&keyword_list=&p_start=40&p_finish=60&p_sort=&p_desc=DESC&p_direction=Prev&p_show=20");

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==8){
        $record = array(
            'summary link' => $tds[2]->plaintext,
            'event date' => $tds[3]->plaintext,
           'report id' => $tds[4]->plaintext,
           'fatality' => $tds[5]->plaintext,
           'SIC' => $tds[6]->plaintext,
          'event description' => $tds[7]->plaintext
      );
       print json_encode($record) . "\n";
       scraperwiki::save(array('summary link'), $record);
  }}

for ($i=2;$i<50;$i++){
    $html=scraperWiki::scrape("http://www.osha.gov/pls/imis/accidentsearch.search?sic=15&sicgroup=&acc_description=&acc_abstract=&acc_keyword=&inspnr=&fatal=fatal&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2002&keyword_list=&p_start=".(($i-1)*20)."&p_finish=".($i*20)."&p_sort=&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div tr") as $data){
        $tds = $data->find("td");
        if(count($tds)==8){
            $record = array(
                'summary link' => $tds[2]->plaintext,
                'event date' => $tds[3]->plaintext,
               'report id' => $tds[4]->plaintext,
               'fatality' => $tds[5]->plaintext,
               'SIC' => $tds[6]->plaintext,
              'event description' => $tds[7]->plaintext
          );
           print json_encode($record) . "\n";
           scraperwiki::save(array('summary link'), $record);
}}
}

?>
