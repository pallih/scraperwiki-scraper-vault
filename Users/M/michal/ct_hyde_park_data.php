<?php

//data from Czech TV Hyde Parks
//http://www.ceskatelevize.cz/specialy/hydepark/4.1.2010/

require 'scraperwiki/simple_html_dom.php';

//scraperwiki::save_var('last_date','2010-01-03');

$last_date = scraperwiki::get_var('last_date','2010-01-03');

$date = new DateTime($last_date);
$now = new DateTime("now");
$date2 = new DateTime("tomorrow");

while ($date < $now) {
  //echo $date->format('j.n.Y');

  //html
  $url = 'http://www.ceskatelevize.cz/specialy/hydepark/' .$date->format('j.n.Y') . '/';
  $html = scraperwiki::scrape($url);

  //check if hyde park exists at that day
  if (!strpos($html,$date->format('j.n.Y'))) continue;

  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $h2 = $dom->find('h2',0);
  $name = $h2->innertext;

  $h3 = $dom->find('h3',0);
  $description = $h3->innertext;

  $div = $dom->find('div[id=descriptionBox]',0);
  $long_description = $div->plaintext;

  $spans = $dom->find('span[class=globalRatingBarInfo]');
    //negative
    $span = $spans[0]->find('span[class=average]',0);
    $negative = trim(trim($span->plaintext),'%');
    //positive
    $span = $spans[1]->find('span[class=average]',0);
    $positive = trim(trim($span->plaintext),'%');
    //count
    $span = $spans[1]->find('span[class=countUser]',0);
    $ar = explode(':',$span->plaintext);
    $count = trim($ar[1]);
  
  $span = $dom->find('span[class=globalRatingTypeBar]',0);
  $id_ar = explode('-',$span->id);
  $globalRating_id = $id_ar[1];

  $iframe = $dom->find('iframe',1);
  $charts_link = str_replace('&amp;','&',$iframe->src);

  

  $data = array(
    'date' => $date->format('Y-m-d'),
    'name' => $name,
    'description' => $description,
    'long_description' => $long_description,
    'positive' => $positive,
    'negative' => $negative,
    'count' => $count,
    'globalRating_id' => $globalRating_id,
    'charts_link'=> $charts_link
  );

    scraperwiki::save_sqlite(array('date'),$data,'info');
    //print_r($data);

  /*charts*/
  $data_chart = array();
  //html
  $url = 'http://www.ceskatelevize.cz' . $charts_link;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  $script = $dom->find('script',2);
  $ar1 = explode(']]',$script->innertext);
  //chart 1
  $ar2 = explode('[[[',str_replace("\t",'',str_replace("\n",'',str_replace(' ','',$ar1[0]))));
  $ar3 = explode('],[',trim(trim($ar2[1]),']'));
  foreach ($ar3 as $row) {
    $ar4 = explode(',',$row);
    $data_chart[] = array(
      'date' => $date->format('Y-m-d'),
      'chart' => '1',
      'minute' => $ar4[0],
      'value' => $ar4[1],
    );
  }
  //chart 2
  $ar2 = explode('[[[',str_replace("\t",'',str_replace("\n",'',str_replace(' ','',$ar1[1]))));
  $ar3 = explode('],[',trim(trim($ar2[1]),']'));
  foreach ($ar3 as $row) {
    $ar4 = explode(',',$row);
    $data_chart[] = array(
      'date' => $date->format('Y-m-d'),
      'chart' => '2',
      'minute' => $ar4[0],
      'value' => $ar4[1],
    );
  }

    scraperwiki::save_sqlite(array('date','chart','minute'),$data_chart,'chart');
    //print_r($data_chart);

  scraperwiki::save_var('last_date',$date->format('Y-m-d'));
  $date->add(new DateInterval('P1D'));
}



?>
