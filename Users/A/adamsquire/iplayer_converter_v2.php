<?php
require 'scraperwiki/simple_html_dom.php';
function format_date($str)
{
    list($day,$month,$y) = explode('/',$str);
    $year = substr($y,0,4);
    $time = substr($y,5,5);
    return $year.'-'.$month.'-'.$day.' '.$time;
}
scraperwiki::sqliteexecute("delete from swdata");
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/1/aod/default.aspx');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/56/aod/default.aspx');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/4/aod/default.aspx');

foreach($data as $d)
{
    $html = scraperWiki::scrape($d['url']);   
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("tr") as $data){
        $tds = $data->find("td");
        if(!$tds)
          continue;
        $broadcast_date = format_date($tds[1]->plaintext);
        $results[] = array('program'=>$tds[0]->plaintext,
                             'pid'=>substr($tds[3]->plaintext,0,strpos($tds[3]->plaintext,'&')),
                             'broadcast_date'=>$broadcast_date,
                             'broadcast_timestamp'=> strtotime($broadcast_date)
                              );
    }
   scraperwiki::save(array('pid'),$results);
}
?>