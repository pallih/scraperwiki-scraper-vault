<?php

require 'scraperwiki/simple_html_dom.php';
print "Hello world! Running...";
for($u=15;$u<18;$u++){
$html = scraperWiki::scrape("http://www.osha.gov/pls/imis/AccidentSearch.search?p_logger=1&sic=".$u."&Office=All&officetype=All&endmonth=01&endday=01&endyear=2002&startmonth=12&startday=31&startyear=2013&p_sort=event_date&p_desc=DESC");
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


//$html=scraperWiki::scrape("http://www.osha.gov/pls/imis/accidentsearch.search?sic=".$u."&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2002&keyword_list=&p_start=0&p_finish=20&p_desc=DESC&p_direction=Next&p_show=20");

//$dom = new simple_html_dom();
//$dom->load($html);
//foreach($dom->find("div tr") as $data){
//    $tds = $data->find("td");
//    if(count($tds)==8){
//        $record = array(
//            'summary link' => $tds[2]->plaintext,
//            'event date' => $tds[3]->plaintext,
//           'report id' => $tds[4]->plaintext,
//           'fatality' => $tds[5]->plaintext,
//           'SIC' => $tds[6]->plaintext,
//          'event description' => $tds[7]->plaintext
//      );
//       print json_encode($record) . "\n";
//       scraperwiki::save(array('summary link'), $record);
//  }}

for ($i=1;$i<500;$i++){
    $html=scraperWiki::scrape("http://www.osha.gov/pls/imis/accidentsearch.search?sic=".$u."&officetype=All&office=All&startmonth=12&startday=31&startyear=2013&endmonth=01&endday=01&endyear=2002&p_start=".(($i-1)*20)."&p_finish=".($i*20)."&p_direction=Next&p_show=20&p_sort=event_date&p_desc=DESC");
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
}

?>
