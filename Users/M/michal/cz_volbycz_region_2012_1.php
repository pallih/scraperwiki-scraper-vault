<?php

//get all counties (okresy)
//http://www.volby.cz/pls/kz2012/kz3?xjazyk=CZ&xdatum=20121012

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.volby.cz/pls/kz2012/kz3?xjazyk=CZ&xdatum=20121012';
$html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
$dom = new simple_html_dom();
$dom->load($html);

$h3s = $dom->find('h3');

//foreach region (kraj)
foreach ($h3s as $key=>$h3) { 
  $table = $dom->find('table',$key);
  $trs = $table->find('tr');
  array_shift($trs);
  array_shift($trs);

  $supregion = $h3->plaintext;
  
  //foreach county (okres)
  foreach ($trs as $tr) {
    $tds = $tr->find('td');
      $data = array(
        'supregion' => $supregion,
        'region' => $tds[1]->plaintext,
        'region_code' => $tds[0]->plaintext,
        'link' => html_entity_decode($tds[3]->find('a',0)->href),
      );
    scraperwiki::save_sqlite(array('region_code'),$data,'county');
    
    //get all towns
    scraperwiki::save_sqlite(array('town_code'),town($data['link'],$data['region_code'],$data['region']),'town');
  }

}

function town($link,$region_code,$region) {
  $out = array();

  $url = 'http://www.volby.cz/pls/kz2012/' . $link;
  $html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
  $dom = new simple_html_dom();
  $dom->load($html);

  $tables = $dom->find('table');
  foreach ($tables as $table) {
    $trs = $table->find('tr');
    array_shift($trs);
    array_shift($trs);

    //foreach town (obec)
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      
      if ($tds[0]->plaintext != '-') {
          $data = array(
            'town' => $tds[1]->plaintext,
            'town_code' => $tds[0]->plaintext,
            'link' => html_entity_decode($tds[0]->find('a',0)->href),
            'region_code' => $region_code,
            'region' => $region,
          );
          $out[] = $data;
      }
    }
  }
  return $out;
}

?>
<?php

//get all counties (okresy)
//http://www.volby.cz/pls/kz2012/kz3?xjazyk=CZ&xdatum=20121012

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.volby.cz/pls/kz2012/kz3?xjazyk=CZ&xdatum=20121012';
$html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
$dom = new simple_html_dom();
$dom->load($html);

$h3s = $dom->find('h3');

//foreach region (kraj)
foreach ($h3s as $key=>$h3) { 
  $table = $dom->find('table',$key);
  $trs = $table->find('tr');
  array_shift($trs);
  array_shift($trs);

  $supregion = $h3->plaintext;
  
  //foreach county (okres)
  foreach ($trs as $tr) {
    $tds = $tr->find('td');
      $data = array(
        'supregion' => $supregion,
        'region' => $tds[1]->plaintext,
        'region_code' => $tds[0]->plaintext,
        'link' => html_entity_decode($tds[3]->find('a',0)->href),
      );
    scraperwiki::save_sqlite(array('region_code'),$data,'county');
    
    //get all towns
    scraperwiki::save_sqlite(array('town_code'),town($data['link'],$data['region_code'],$data['region']),'town');
  }

}

function town($link,$region_code,$region) {
  $out = array();

  $url = 'http://www.volby.cz/pls/kz2012/' . $link;
  $html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
  $dom = new simple_html_dom();
  $dom->load($html);

  $tables = $dom->find('table');
  foreach ($tables as $table) {
    $trs = $table->find('tr');
    array_shift($trs);
    array_shift($trs);

    //foreach town (obec)
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      
      if ($tds[0]->plaintext != '-') {
          $data = array(
            'town' => $tds[1]->plaintext,
            'town_code' => $tds[0]->plaintext,
            'link' => html_entity_decode($tds[0]->find('a',0)->href),
            'region_code' => $region_code,
            'region' => $region,
          );
          $out[] = $data;
      }
    }
  }
  return $out;
}

?>
<?php

//get all counties (okresy)
//http://www.volby.cz/pls/kz2012/kz3?xjazyk=CZ&xdatum=20121012

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.volby.cz/pls/kz2012/kz3?xjazyk=CZ&xdatum=20121012';
$html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
$dom = new simple_html_dom();
$dom->load($html);

$h3s = $dom->find('h3');

//foreach region (kraj)
foreach ($h3s as $key=>$h3) { 
  $table = $dom->find('table',$key);
  $trs = $table->find('tr');
  array_shift($trs);
  array_shift($trs);

  $supregion = $h3->plaintext;
  
  //foreach county (okres)
  foreach ($trs as $tr) {
    $tds = $tr->find('td');
      $data = array(
        'supregion' => $supregion,
        'region' => $tds[1]->plaintext,
        'region_code' => $tds[0]->plaintext,
        'link' => html_entity_decode($tds[3]->find('a',0)->href),
      );
    scraperwiki::save_sqlite(array('region_code'),$data,'county');
    
    //get all towns
    scraperwiki::save_sqlite(array('town_code'),town($data['link'],$data['region_code'],$data['region']),'town');
  }

}

function town($link,$region_code,$region) {
  $out = array();

  $url = 'http://www.volby.cz/pls/kz2012/' . $link;
  $html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
  $dom = new simple_html_dom();
  $dom->load($html);

  $tables = $dom->find('table');
  foreach ($tables as $table) {
    $trs = $table->find('tr');
    array_shift($trs);
    array_shift($trs);

    //foreach town (obec)
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      
      if ($tds[0]->plaintext != '-') {
          $data = array(
            'town' => $tds[1]->plaintext,
            'town_code' => $tds[0]->plaintext,
            'link' => html_entity_decode($tds[0]->find('a',0)->href),
            'region_code' => $region_code,
            'region' => $region,
          );
          $out[] = $data;
      }
    }
  }
  return $out;
}

?>
