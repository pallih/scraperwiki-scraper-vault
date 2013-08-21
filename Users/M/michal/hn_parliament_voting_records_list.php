<?php
//scrapes list of pdf files containing the voting records.
//http://www.congresonacional.hn/index.php?option=com_jcalpro&Itemid=149&extmode=flat&date=2012-12-01
//it starts from 02/2012, 2011 in different format

//working on !!!!

require 'scraperwiki/simple_html_dom.php';

//temp
//scraperwiki::save_var('last_month','201101');
//die();

$last_month = scraperwiki::get_var('last_month');
$lyear = substr($last_month,0,4);
$lmonth = substr($last_month,4);
if ($last_month < date('Ym')) {
    for($y=2012;$y<=date('Y');$y++) {
        for($m=2;$m<=date('m');$m++) {
            if ((date('m')>$lmonth) or (date('Y')>$lyear)) {
                scrape_month($y,$m);
            }
        }
    }

}

function scrape_month($year,$month) {
  $month2 = n2($month);
  $url = "http://www.congresonacional.hn/index.php?option=com_jcalpro&Itemid=149&extmode=flat&date={$year}-{$month2}-01";
  $html = scraperwiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);

  $table0= $dom->find('table[class=maintable]',0);
echo $year.$month;
echo $table0->outertext;
  $tables = $table0->find('table[width=100%]');
  foreach ($tables as $table) {
    $a = $table->find('a',0);
    echo $a->outertext;die();
  }
}

function n2($n) {
  if ($n<10) return '0'.$n;
  else return $n;
}

?>
