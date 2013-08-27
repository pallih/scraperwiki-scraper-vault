<?php

//list of Chilean MPs (diputados)

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.camara.cl/camara/diputados.aspx';
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$date = date("Y-m-d H:i:s");

$div = $dom->find("div[class=content-head]",1);
$term_full = $div->find("h2",0);
$term = trim(substr($term_full->plaintext, strlen("Organización y Autoridades Parlamentarias periodo legislativo")));

/*
//directors = mesa directiva
$table = $dom->find("table[class=tabla]",0);
$trs = $table->find("tr");
array_shift($trs);
foreach ($trs as $tr) {
  $tds = $tr->find("td");
  preg_match("/prmid=([0-9]{1,})/",$tds[1]->find("a",0)->href,$matches);
  $mps[] = array(
    'id' => $matches[1],
    'name' => $tds[1]->find("a",0)->plaintext,
    'updated_on' => $date,
  );
}*/
//all mps
$ul = $dom->find("ul[class=diputados]",0);
$lis = $ul->find("li[class=alturaDiputado]");
foreach ($lis as $li) {
  preg_match("/diputado_detalle.aspx\?prmid=([0-9]{1,})/",$li->find("a",1)->href,$matches);
  $name_ar = explode("  ",trim($li->find("a",1)->plaintext));
  $name = trim(end($name_ar));
  $ul2 = $li->find("ul[class=links]",0);
  $as = $ul2->find("a");
  $region_ar = explode("  ",trim($as[0]->innertext));
  $region_rome = trim(end($region_ar));
  $distrito_ar = explode("°",trim($as[1]->innertext));
  $distrito = end($distrito_ar);
  $partido_ar = explode("  ",trim($as[2]->innertext));
  $partido_short_name = trim(end($partido_ar));
  $mps[] = array(
    'id' => $matches[1],
    'name' => $name,
    'updated_on' => $date,
    'current_term' => $term,
    'region_rome' => $region_rome,
    'distrito' => $distrito,
    'party_short_name' => $partido_short_name,
  );
}
//print_r($mps);
scraperwiki::save_sqlite(array('id','current_term'),$mps);

?>
<?php

//list of Chilean MPs (diputados)

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.camara.cl/camara/diputados.aspx';
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$date = date("Y-m-d H:i:s");

$div = $dom->find("div[class=content-head]",1);
$term_full = $div->find("h2",0);
$term = trim(substr($term_full->plaintext, strlen("Organización y Autoridades Parlamentarias periodo legislativo")));

/*
//directors = mesa directiva
$table = $dom->find("table[class=tabla]",0);
$trs = $table->find("tr");
array_shift($trs);
foreach ($trs as $tr) {
  $tds = $tr->find("td");
  preg_match("/prmid=([0-9]{1,})/",$tds[1]->find("a",0)->href,$matches);
  $mps[] = array(
    'id' => $matches[1],
    'name' => $tds[1]->find("a",0)->plaintext,
    'updated_on' => $date,
  );
}*/
//all mps
$ul = $dom->find("ul[class=diputados]",0);
$lis = $ul->find("li[class=alturaDiputado]");
foreach ($lis as $li) {
  preg_match("/diputado_detalle.aspx\?prmid=([0-9]{1,})/",$li->find("a",1)->href,$matches);
  $name_ar = explode("  ",trim($li->find("a",1)->plaintext));
  $name = trim(end($name_ar));
  $ul2 = $li->find("ul[class=links]",0);
  $as = $ul2->find("a");
  $region_ar = explode("  ",trim($as[0]->innertext));
  $region_rome = trim(end($region_ar));
  $distrito_ar = explode("°",trim($as[1]->innertext));
  $distrito = end($distrito_ar);
  $partido_ar = explode("  ",trim($as[2]->innertext));
  $partido_short_name = trim(end($partido_ar));
  $mps[] = array(
    'id' => $matches[1],
    'name' => $name,
    'updated_on' => $date,
    'current_term' => $term,
    'region_rome' => $region_rome,
    'distrito' => $distrito,
    'party_short_name' => $partido_short_name,
  );
}
//print_r($mps);
scraperwiki::save_sqlite(array('id','current_term'),$mps);

?>
<?php

//list of Chilean MPs (diputados)

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.camara.cl/camara/diputados.aspx';
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$date = date("Y-m-d H:i:s");

$div = $dom->find("div[class=content-head]",1);
$term_full = $div->find("h2",0);
$term = trim(substr($term_full->plaintext, strlen("Organización y Autoridades Parlamentarias periodo legislativo")));

/*
//directors = mesa directiva
$table = $dom->find("table[class=tabla]",0);
$trs = $table->find("tr");
array_shift($trs);
foreach ($trs as $tr) {
  $tds = $tr->find("td");
  preg_match("/prmid=([0-9]{1,})/",$tds[1]->find("a",0)->href,$matches);
  $mps[] = array(
    'id' => $matches[1],
    'name' => $tds[1]->find("a",0)->plaintext,
    'updated_on' => $date,
  );
}*/
//all mps
$ul = $dom->find("ul[class=diputados]",0);
$lis = $ul->find("li[class=alturaDiputado]");
foreach ($lis as $li) {
  preg_match("/diputado_detalle.aspx\?prmid=([0-9]{1,})/",$li->find("a",1)->href,$matches);
  $name_ar = explode("  ",trim($li->find("a",1)->plaintext));
  $name = trim(end($name_ar));
  $ul2 = $li->find("ul[class=links]",0);
  $as = $ul2->find("a");
  $region_ar = explode("  ",trim($as[0]->innertext));
  $region_rome = trim(end($region_ar));
  $distrito_ar = explode("°",trim($as[1]->innertext));
  $distrito = end($distrito_ar);
  $partido_ar = explode("  ",trim($as[2]->innertext));
  $partido_short_name = trim(end($partido_ar));
  $mps[] = array(
    'id' => $matches[1],
    'name' => $name,
    'updated_on' => $date,
    'current_term' => $term,
    'region_rome' => $region_rome,
    'distrito' => $distrito,
    'party_short_name' => $partido_short_name,
  );
}
//print_r($mps);
scraperwiki::save_sqlite(array('id','current_term'),$mps);

?>
