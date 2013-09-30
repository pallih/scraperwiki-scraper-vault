<?php

require 'scraperwiki/simple_html_dom.php';

for ($i=1;$i<100;$i++){
    $html=scraperWiki::scrape("http://www.osha.gov/pls/imis/industry.search?sic=&sicgroup=&naicsgroup=&naics=23&state=All&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2010&opt=&optt=&scope=&fedagncode=&owner=&emph=&emphtp=&p_start=".(($i-1)*20)."&p_finish=".($i*20)."&p_sort=&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div tr") as $data){
        $tds = $data->find("td");
        if(count($tds)==12){
        $record = array(
           'activity number' => $tds[2]->plaintext,
           'opened' => $tds[3]->plaintext,
           'report id' => $tds[4]->plaintext,
           'state' => $tds[5]->plaintext,
           'type' => $tds[6]->plaintext,
           'scope' => $tds[7]->plaintext,
           'SIC' => $tds[8]->plaintext,
           'NAICS' => $tds[9]->plaintext,
           'violation' => $tds[10]->plaintext,
           'establishment name' => $tds[11]->plaintext

      );
       //print json_encode($record) . "\n";
       scraperwiki::save(array('activity number'), $record);
  }
}
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

for ($i=1;$i<100;$i++){
    $html=scraperWiki::scrape("http://www.osha.gov/pls/imis/industry.search?sic=&sicgroup=&naicsgroup=&naics=23&state=All&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2010&opt=&optt=&scope=&fedagncode=&owner=&emph=&emphtp=&p_start=".(($i-1)*20)."&p_finish=".($i*20)."&p_sort=&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div tr") as $data){
        $tds = $data->find("td");
        if(count($tds)==12){
        $record = array(
           'activity number' => $tds[2]->plaintext,
           'opened' => $tds[3]->plaintext,
           'report id' => $tds[4]->plaintext,
           'state' => $tds[5]->plaintext,
           'type' => $tds[6]->plaintext,
           'scope' => $tds[7]->plaintext,
           'SIC' => $tds[8]->plaintext,
           'NAICS' => $tds[9]->plaintext,
           'violation' => $tds[10]->plaintext,
           'establishment name' => $tds[11]->plaintext

      );
       //print json_encode($record) . "\n";
       scraperwiki::save(array('activity number'), $record);
  }
}
}

?>
