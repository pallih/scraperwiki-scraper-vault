<?php
//source 1: http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html
//source 2: http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=500&periodId=18280&resolutionNumber=&printNumber=&s=1&meeting=&start=500
// important: periodId, start
// others shall be there (even empty)
// size - max 500
// we need to get the divisions' overview first, because there is no info about the division at the detailed page (not even date, etc.)

require 'scraperwiki/simple_html_dom.php'; 

//get ids of periods
$url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html";
$html = scraperwiki::scrape($url);
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //periods
$selects = $dom->find("select");
$pers = $selects[0]->find("option");
foreach((array) $pers as $per) {
  if ($per->value != '') {
    $periods[$per->value]['id'] = $per->value;
    $periods[$per->value]['period'] = $per->plaintext;
  }
}
//save periods
foreach ((array) $periods as $period) {
  scraperwiki::save_sqlite(array('id'), $period, 'period');
}

//get number
$url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?periodId=&resolutionNumber=&printNumber=&s=1&meeting=&start=0&size=5";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);
//find number
$divs = $dom->find("div[class=pg-count]");
preg_match('/([0-9]{1,})/' ,$divs[0]->innertext,$matches);
$number = $matches[0];

//get the pages
for ($i=0; $i < $number; $i=$i+200) {
  $url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?periodId=&resolutionNumber=&printNumber=&s=1&meeting=&size=200&start=".$i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //get table
  $tables = $dom->find("table");
  //save it
  $out = array (
    'i' => round($i/200),
    'html' => $tables[0]->outertext,
  );
  scraperwiki::save_sqlite(array('i'),$out);
}





?>
