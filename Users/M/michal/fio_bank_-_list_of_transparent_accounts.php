<?php

require 'scraperwiki/simple_html_dom.php'; 

//first page
$url = "http://www.fio.cz/bankovni-sluzby/bankovni-ucty/transparentni-ucet/vypis-transparentnich-uctu";
$html = iconv("cp1250", "UTF-8//TRANSLIT",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

//find number of pages
$divs = $dom->find('div[class=paginator]');
$as = $divs[0]->find('a');
$number = end($as)->innertext;

$data = array();
for ($i = 0; $i < $number; $i++) {
  $offset = 30*$i;
  $url = "http://www.fio.cz/bankovni-sluzby/bankovni-ucty/transparentni-ucet/vypis-transparentnich-uctu?offset=".$offset;
  $html = iconv("cp1250", "UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //table
  $tables = $dom->find('table');
  $trs = $tables[0]->find('tr');
  array_shift($trs);
  foreach($trs as $tr) {
    $tds = $tr->find('td');
    $row = array(
      'name' => $tds[0]->plaintext,
      'account' => $tds[1]->plaintext,
    );
    $as = $tds[0]->find('a');
    if (count($as) > 0)
      $row['link'] = $as[0]->href;
    $data[] = $row;
  }
}
scraperwiki::save_sqlite(array('account'),$data);
?>
