<?php

//source: http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=313 (lov_stranka = 0 ... )

require 'scraperwiki/simple_html_dom.php'; 

//scrape first to get number of pages
$url = "http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=0";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

//find number of pages
$tables = $dom->find('table');
$tables2 = $tables[1]->find('table');
$tds = $tables2[0]->find('td');
$parts = explode('/',str_replace('&nbsp;','',$tds[0]->plaintext));
$number = trim($parts[1]);

$data = array();
for ($i = 0; $i < $number; $i++) {
  $url = "http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //get the table and rows
  $tables = $dom->find('table');
  $tables2 = $tables[1]->find('table');
  $trs = $tables2[1]->find('tr');
  //shift off the first row (header)
  array_shift($trs);
  //foreach row
  foreach ($trs as $tr) {
    $tds = $tr->find('td');
    //prepare the data
    $d = array();
    $d['code'] = $tds[0]->plaintext;
    $tmp = explode('(',$tds[1]->plaintext);
    //correction for e.g. 'Březina (dříve okres Blansko) (okr. Brno-venkov)'
    if (count($tmp) > 2) {
      $d['name'] = implode('(', array($tmp[0],trim($tmp[1])));
      $d['region'] = str_replace('okr. ','',rtrim($tmp[2],')'));
    } else {
      $d['name'] = trim($tmp[0]);
      $d['region'] = str_replace('okr. ','',rtrim($tmp[1],')'));
    }
    $data[] = $d;
  }
}
scraperwiki::save_sqlite(array('code'),$data);
?>
<?php

//source: http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=313 (lov_stranka = 0 ... )

require 'scraperwiki/simple_html_dom.php'; 

//scrape first to get number of pages
$url = "http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=0";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

//find number of pages
$tables = $dom->find('table');
$tables2 = $tables[1]->find('table');
$tds = $tables2[0]->find('td');
$parts = explode('/',str_replace('&nbsp;','',$tds[0]->plaintext));
$number = trim($parts[1]);

$data = array();
for ($i = 0; $i < $number; $i++) {
  $url = "http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //get the table and rows
  $tables = $dom->find('table');
  $tables2 = $tables[1]->find('table');
  $trs = $tables2[1]->find('tr');
  //shift off the first row (header)
  array_shift($trs);
  //foreach row
  foreach ($trs as $tr) {
    $tds = $tr->find('td');
    //prepare the data
    $d = array();
    $d['code'] = $tds[0]->plaintext;
    $tmp = explode('(',$tds[1]->plaintext);
    //correction for e.g. 'Březina (dříve okres Blansko) (okr. Brno-venkov)'
    if (count($tmp) > 2) {
      $d['name'] = implode('(', array($tmp[0],trim($tmp[1])));
      $d['region'] = str_replace('okr. ','',rtrim($tmp[2],')'));
    } else {
      $d['name'] = trim($tmp[0]);
      $d['region'] = str_replace('okr. ','',rtrim($tmp[1],')'));
    }
    $data[] = $d;
  }
}
scraperwiki::save_sqlite(array('code'),$data);
?>
<?php

//source: http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=313 (lov_stranka = 0 ... )

require 'scraperwiki/simple_html_dom.php'; 

//scrape first to get number of pages
$url = "http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=0";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

//find number of pages
$tables = $dom->find('table');
$tables2 = $tables[1]->find('table');
$tds = $tables2[0]->find('td');
$parts = explode('/',str_replace('&nbsp;','',$tds[0]->plaintext));
$number = trim($parts[1]);

$data = array();
for ($i = 0; $i < $number; $i++) {
  $url = "http://vdb.czso.cz/vdbvo/lovcisel.jsp?param_typ=pro&app=vdb&param_id=3980560&lov_stranka=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //get the table and rows
  $tables = $dom->find('table');
  $tables2 = $tables[1]->find('table');
  $trs = $tables2[1]->find('tr');
  //shift off the first row (header)
  array_shift($trs);
  //foreach row
  foreach ($trs as $tr) {
    $tds = $tr->find('td');
    //prepare the data
    $d = array();
    $d['code'] = $tds[0]->plaintext;
    $tmp = explode('(',$tds[1]->plaintext);
    //correction for e.g. 'Březina (dříve okres Blansko) (okr. Brno-venkov)'
    if (count($tmp) > 2) {
      $d['name'] = implode('(', array($tmp[0],trim($tmp[1])));
      $d['region'] = str_replace('okr. ','',rtrim($tmp[2],')'));
    } else {
      $d['name'] = trim($tmp[0]);
      $d['region'] = str_replace('okr. ','',rtrim($tmp[1],')'));
    }
    $data[] = $d;
  }
}
scraperwiki::save_sqlite(array('code'),$data);
?>
