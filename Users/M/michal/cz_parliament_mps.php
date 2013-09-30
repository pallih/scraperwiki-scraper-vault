<?php

//get all MPs from given term (6) (all, including not active ones)

require 'scraperwiki/simple_html_dom.php'; 

$term = 6;

$url = 'http://www.psp.cz/sqw/snem.sqw?P1=0&P2=0&o=' . $term;
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$trs = $dom->find('table[class=wide]',0)->find('tr');
array_shift($trs);

foreach ($trs as $tr) {
  $item = array();
  $tds = $tr->find('td');
  $th = $tr->find('th',0); 
  if (!strpos($tr->innertext,'colspan=10')) {
      $item['name'] = trim(str_replace('&nbsp;',' ',$th->find('a',0)->plaintext));
      $item['region'] = trim($tds[0]->plaintext);
      $item['club'] = trim(str_replace(', ',',',(str_replace('&nbsp;',' ',$tds[1]->plaintext))));
      $a = explode('id=',$th->find('a',0)->href);
      $a = explode('&',$a[1]);
      $item['id'] = $a[0];
    //print_r($item);
      scraperwiki::save_sqlite(array('id'),$item);
  }
//die();
}


?>
<?php

//get all MPs from given term (6) (all, including not active ones)

require 'scraperwiki/simple_html_dom.php'; 

$term = 6;

$url = 'http://www.psp.cz/sqw/snem.sqw?P1=0&P2=0&o=' . $term;
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$trs = $dom->find('table[class=wide]',0)->find('tr');
array_shift($trs);

foreach ($trs as $tr) {
  $item = array();
  $tds = $tr->find('td');
  $th = $tr->find('th',0); 
  if (!strpos($tr->innertext,'colspan=10')) {
      $item['name'] = trim(str_replace('&nbsp;',' ',$th->find('a',0)->plaintext));
      $item['region'] = trim($tds[0]->plaintext);
      $item['club'] = trim(str_replace(', ',',',(str_replace('&nbsp;',' ',$tds[1]->plaintext))));
      $a = explode('id=',$th->find('a',0)->href);
      $a = explode('&',$a[1]);
      $item['id'] = $a[0];
    //print_r($item);
      scraperwiki::save_sqlite(array('id'),$item);
  }
//die();
}


?>
<?php

//get all MPs from given term (6) (all, including not active ones)

require 'scraperwiki/simple_html_dom.php'; 

$term = 6;

$url = 'http://www.psp.cz/sqw/snem.sqw?P1=0&P2=0&o=' . $term;
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$trs = $dom->find('table[class=wide]',0)->find('tr');
array_shift($trs);

foreach ($trs as $tr) {
  $item = array();
  $tds = $tr->find('td');
  $th = $tr->find('th',0); 
  if (!strpos($tr->innertext,'colspan=10')) {
      $item['name'] = trim(str_replace('&nbsp;',' ',$th->find('a',0)->plaintext));
      $item['region'] = trim($tds[0]->plaintext);
      $item['club'] = trim(str_replace(', ',',',(str_replace('&nbsp;',' ',$tds[1]->plaintext))));
      $a = explode('id=',$th->find('a',0)->href);
      $a = explode('&',$a[1]);
      $item['id'] = $a[0];
    //print_r($item);
      scraperwiki::save_sqlite(array('id'),$item);
  }
//die();
}


?>
<?php

//get all MPs from given term (6) (all, including not active ones)

require 'scraperwiki/simple_html_dom.php'; 

$term = 6;

$url = 'http://www.psp.cz/sqw/snem.sqw?P1=0&P2=0&o=' . $term;
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$trs = $dom->find('table[class=wide]',0)->find('tr');
array_shift($trs);

foreach ($trs as $tr) {
  $item = array();
  $tds = $tr->find('td');
  $th = $tr->find('th',0); 
  if (!strpos($tr->innertext,'colspan=10')) {
      $item['name'] = trim(str_replace('&nbsp;',' ',$th->find('a',0)->plaintext));
      $item['region'] = trim($tds[0]->plaintext);
      $item['club'] = trim(str_replace(', ',',',(str_replace('&nbsp;',' ',$tds[1]->plaintext))));
      $a = explode('id=',$th->find('a',0)->href);
      $a = explode('&',$a[1]);
      $item['id'] = $a[0];
    //print_r($item);
      scraperwiki::save_sqlite(array('id'),$item);
  }
//die();
}


?>
