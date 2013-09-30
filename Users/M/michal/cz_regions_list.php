<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696

require 'scraperwiki/simple_html_dom.php';

//scrape
$url = "http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$ul = $dom->find('ul[class=odkazy-modre]',0);
$lis = $ul->find('li');

foreach ($lis as $li) {
  $as = $li->find('a');
  preg_match('/kod=([0-9a-zA-Z]{1,})/',$as[0]->href,$matches);
  $k_code = $matches[1];
  $k_name = $as[0]->plaintext;
  $data_k = array(
    'name' => $k_name,
    'code' => $k_code,
  );
  array_shift($as);
  $data_o = array();
  if (count($as) > 0) { //not Praha
    foreach ($as as $a) {
      preg_match('/kod=([0-9a-zA-Z]{1,})/',$a->href,$matches);
      $data_o[] = array(
        'name' => $a->plaintext,
        'code' => $matches[1],
        'sup_name' => $k_name,
        'sup_code' => $k_code
      );
    }
  } else { //Praha
    //correct the errors

    $praha = array(
        array('code'=>'CZ0101','name'=>'Praha 1',),
        array('code'=>'CZ0102','name'=>'Praha 2',),
        array('code'=>'CZ0103','name'=>'Praha 3',),
        array('code'=>'CZ0104','name'=>'Praha 4',),
        array('code'=>'CZ0105','name'=>'Praha 5',),
        array('code'=>'CZ0106','name'=>'Praha 6',),
        array('code'=>'CZ0107','name'=>'Praha 7',),
        array('code'=>'CZ0108','name'=>'Praha 8',),
        array('code'=>'CZ0109','name'=>'Praha 9',),
        array('code'=>'CZ010A','name'=>'Praha 10',),
        array('code'=>'CZ010B','name'=>'Praha 11',),
        array('code'=>'CZ010C','name'=>'Praha 12',),
        array('code'=>'CZ010D','name'=>'Praha 13',),
        array('code'=>'CZ010E','name'=>'Praha 14',),
        array('code'=>'CZ010F','name'=>'Praha 15'),
    );
    foreach ($praha as $p) {
      $p['sup_name'] = $k_name;
      $p['sup_code'] = $k_code;
      $data_o[] = $p;
    }
    $data_o[] = array(
        'name' => 'Praha',
        'code' => 'CZ0100',       
        'sup_name' => $k_name,
        'sup_code' => $k_code
    );
  }
  scraperwiki::save_sqlite(array('code'),$data_k,'kraj');
  scraperwiki::save_sqlite(array('code'),$data_o,'okres');
  
}
?>
<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696

require 'scraperwiki/simple_html_dom.php';

//scrape
$url = "http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$ul = $dom->find('ul[class=odkazy-modre]',0);
$lis = $ul->find('li');

foreach ($lis as $li) {
  $as = $li->find('a');
  preg_match('/kod=([0-9a-zA-Z]{1,})/',$as[0]->href,$matches);
  $k_code = $matches[1];
  $k_name = $as[0]->plaintext;
  $data_k = array(
    'name' => $k_name,
    'code' => $k_code,
  );
  array_shift($as);
  $data_o = array();
  if (count($as) > 0) { //not Praha
    foreach ($as as $a) {
      preg_match('/kod=([0-9a-zA-Z]{1,})/',$a->href,$matches);
      $data_o[] = array(
        'name' => $a->plaintext,
        'code' => $matches[1],
        'sup_name' => $k_name,
        'sup_code' => $k_code
      );
    }
  } else { //Praha
    //correct the errors

    $praha = array(
        array('code'=>'CZ0101','name'=>'Praha 1',),
        array('code'=>'CZ0102','name'=>'Praha 2',),
        array('code'=>'CZ0103','name'=>'Praha 3',),
        array('code'=>'CZ0104','name'=>'Praha 4',),
        array('code'=>'CZ0105','name'=>'Praha 5',),
        array('code'=>'CZ0106','name'=>'Praha 6',),
        array('code'=>'CZ0107','name'=>'Praha 7',),
        array('code'=>'CZ0108','name'=>'Praha 8',),
        array('code'=>'CZ0109','name'=>'Praha 9',),
        array('code'=>'CZ010A','name'=>'Praha 10',),
        array('code'=>'CZ010B','name'=>'Praha 11',),
        array('code'=>'CZ010C','name'=>'Praha 12',),
        array('code'=>'CZ010D','name'=>'Praha 13',),
        array('code'=>'CZ010E','name'=>'Praha 14',),
        array('code'=>'CZ010F','name'=>'Praha 15'),
    );
    foreach ($praha as $p) {
      $p['sup_name'] = $k_name;
      $p['sup_code'] = $k_code;
      $data_o[] = $p;
    }
    $data_o[] = array(
        'name' => 'Praha',
        'code' => 'CZ0100',       
        'sup_name' => $k_name,
        'sup_code' => $k_code
    );
  }
  scraperwiki::save_sqlite(array('code'),$data_k,'kraj');
  scraperwiki::save_sqlite(array('code'),$data_o,'okres');
  
}
?>
<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696

require 'scraperwiki/simple_html_dom.php';

//scrape
$url = "http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$ul = $dom->find('ul[class=odkazy-modre]',0);
$lis = $ul->find('li');

foreach ($lis as $li) {
  $as = $li->find('a');
  preg_match('/kod=([0-9a-zA-Z]{1,})/',$as[0]->href,$matches);
  $k_code = $matches[1];
  $k_name = $as[0]->plaintext;
  $data_k = array(
    'name' => $k_name,
    'code' => $k_code,
  );
  array_shift($as);
  $data_o = array();
  if (count($as) > 0) { //not Praha
    foreach ($as as $a) {
      preg_match('/kod=([0-9a-zA-Z]{1,})/',$a->href,$matches);
      $data_o[] = array(
        'name' => $a->plaintext,
        'code' => $matches[1],
        'sup_name' => $k_name,
        'sup_code' => $k_code
      );
    }
  } else { //Praha
    //correct the errors

    $praha = array(
        array('code'=>'CZ0101','name'=>'Praha 1',),
        array('code'=>'CZ0102','name'=>'Praha 2',),
        array('code'=>'CZ0103','name'=>'Praha 3',),
        array('code'=>'CZ0104','name'=>'Praha 4',),
        array('code'=>'CZ0105','name'=>'Praha 5',),
        array('code'=>'CZ0106','name'=>'Praha 6',),
        array('code'=>'CZ0107','name'=>'Praha 7',),
        array('code'=>'CZ0108','name'=>'Praha 8',),
        array('code'=>'CZ0109','name'=>'Praha 9',),
        array('code'=>'CZ010A','name'=>'Praha 10',),
        array('code'=>'CZ010B','name'=>'Praha 11',),
        array('code'=>'CZ010C','name'=>'Praha 12',),
        array('code'=>'CZ010D','name'=>'Praha 13',),
        array('code'=>'CZ010E','name'=>'Praha 14',),
        array('code'=>'CZ010F','name'=>'Praha 15'),
    );
    foreach ($praha as $p) {
      $p['sup_name'] = $k_name;
      $p['sup_code'] = $k_code;
      $data_o[] = $p;
    }
    $data_o[] = array(
        'name' => 'Praha',
        'code' => 'CZ0100',       
        'sup_name' => $k_name,
        'sup_code' => $k_code
    );
  }
  scraperwiki::save_sqlite(array('code'),$data_k,'kraj');
  scraperwiki::save_sqlite(array('code'),$data_o,'okres');
  
}
?>
<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696

require 'scraperwiki/simple_html_dom.php';

//scrape
$url = "http://portal.gov.cz/wps/portal/_s.155/696/_s.155/696";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$ul = $dom->find('ul[class=odkazy-modre]',0);
$lis = $ul->find('li');

foreach ($lis as $li) {
  $as = $li->find('a');
  preg_match('/kod=([0-9a-zA-Z]{1,})/',$as[0]->href,$matches);
  $k_code = $matches[1];
  $k_name = $as[0]->plaintext;
  $data_k = array(
    'name' => $k_name,
    'code' => $k_code,
  );
  array_shift($as);
  $data_o = array();
  if (count($as) > 0) { //not Praha
    foreach ($as as $a) {
      preg_match('/kod=([0-9a-zA-Z]{1,})/',$a->href,$matches);
      $data_o[] = array(
        'name' => $a->plaintext,
        'code' => $matches[1],
        'sup_name' => $k_name,
        'sup_code' => $k_code
      );
    }
  } else { //Praha
    //correct the errors

    $praha = array(
        array('code'=>'CZ0101','name'=>'Praha 1',),
        array('code'=>'CZ0102','name'=>'Praha 2',),
        array('code'=>'CZ0103','name'=>'Praha 3',),
        array('code'=>'CZ0104','name'=>'Praha 4',),
        array('code'=>'CZ0105','name'=>'Praha 5',),
        array('code'=>'CZ0106','name'=>'Praha 6',),
        array('code'=>'CZ0107','name'=>'Praha 7',),
        array('code'=>'CZ0108','name'=>'Praha 8',),
        array('code'=>'CZ0109','name'=>'Praha 9',),
        array('code'=>'CZ010A','name'=>'Praha 10',),
        array('code'=>'CZ010B','name'=>'Praha 11',),
        array('code'=>'CZ010C','name'=>'Praha 12',),
        array('code'=>'CZ010D','name'=>'Praha 13',),
        array('code'=>'CZ010E','name'=>'Praha 14',),
        array('code'=>'CZ010F','name'=>'Praha 15'),
    );
    foreach ($praha as $p) {
      $p['sup_name'] = $k_name;
      $p['sup_code'] = $k_code;
      $data_o[] = $p;
    }
    $data_o[] = array(
        'name' => 'Praha',
        'code' => 'CZ0100',       
        'sup_name' => $k_name,
        'sup_code' => $k_code
    );
  }
  scraperwiki::save_sqlite(array('code'),$data_k,'kraj');
  scraperwiki::save_sqlite(array('code'),$data_o,'okres');
  
}
?>
