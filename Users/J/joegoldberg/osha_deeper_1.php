<?php

require 'scraperwiki/simple_html_dom.php';
$establishment = "kiewit";
for ($i=1;$i<100;$i++){
    $html=scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.search?establishment=".($establishment)."&state=all&officetype=all&office=all&startmonth=09&startday=13&startyear=2007&endmonth=09&endday=13&endyear=2012&p_case=closed&p_start=&p_finish=".(($i-1)*20)."&p_sort=12&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("div tr") as $data){
       $tds = $data->find("td");
       $record = array('activity number' => $tds[2]->plaintext,);
       ///$html=scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.inspection_detail?id=".($record[i-1]).);

   // $dom = new simple_html_dom();
    //$dom->load($html);
}
}



<?php

require 'scraperwiki/simple_html_dom.php';
$establishment = "kiewit";
for ($i=1;$i<100;$i++){
    $html=scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.search?establishment=".($establishment)."&state=all&officetype=all&office=all&startmonth=09&startday=13&startyear=2007&endmonth=09&endday=13&endyear=2012&p_case=closed&p_start=&p_finish=".(($i-1)*20)."&p_sort=12&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("div tr") as $data){
       $tds = $data->find("td");
       $record = array('activity number' => $tds[2]->plaintext,);
       ///$html=scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.inspection_detail?id=".($record[i-1]).);

   // $dom = new simple_html_dom();
    //$dom->load($html);
}
}



