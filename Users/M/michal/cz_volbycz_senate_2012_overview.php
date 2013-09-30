<?php

//all senate candidates 2012

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/senat/se1111?xjazyk=CZ&xdatum=20121012&xv=1&xt=2';
$html = iconv("ISO-8859-2","UTF-8//IGNORE",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",0);

$trs = $table->find("tr");
array_shift($trs);
array_shift($trs);

foreach ($trs as $tr) {
  $td = $tr->find("td");
  $data = array(
    'obvod' => $td[0]->plaintext,
    'cislo' => $td[1]->plaintext,
    'name' => str_replace('&nbsp;',' ',$td[2]->plaintext),
    'age' => $td[3]->plaintext,
    'volebni_strana' => $td[4]->plaintext,
    'navrhujici_strana' => $td[5]->plaintext,
    'politicka_prislusnost' => $td[6]->plaintext,
    'povolani' => $td[7]->plaintext,
    'bydliste' => $td[8]->plaintext,
    '1_kolo_hlasy' => $td[9]->plaintext,
    '1_kolo_procenta' => $td[10]->plaintext,
    '2_kolo_hlasy' => $td[11]->plaintext,
    '2_kolo_procenta' => $td[12]->plaintext
  );
  scraperwiki::save_sqlite(array('obvod','cislo'),$data);
}

?>
<?php

//all senate candidates 2012

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/senat/se1111?xjazyk=CZ&xdatum=20121012&xv=1&xt=2';
$html = iconv("ISO-8859-2","UTF-8//IGNORE",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",0);

$trs = $table->find("tr");
array_shift($trs);
array_shift($trs);

foreach ($trs as $tr) {
  $td = $tr->find("td");
  $data = array(
    'obvod' => $td[0]->plaintext,
    'cislo' => $td[1]->plaintext,
    'name' => str_replace('&nbsp;',' ',$td[2]->plaintext),
    'age' => $td[3]->plaintext,
    'volebni_strana' => $td[4]->plaintext,
    'navrhujici_strana' => $td[5]->plaintext,
    'politicka_prislusnost' => $td[6]->plaintext,
    'povolani' => $td[7]->plaintext,
    'bydliste' => $td[8]->plaintext,
    '1_kolo_hlasy' => $td[9]->plaintext,
    '1_kolo_procenta' => $td[10]->plaintext,
    '2_kolo_hlasy' => $td[11]->plaintext,
    '2_kolo_procenta' => $td[12]->plaintext
  );
  scraperwiki::save_sqlite(array('obvod','cislo'),$data);
}

?>
<?php

//all senate candidates 2012

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/senat/se1111?xjazyk=CZ&xdatum=20121012&xv=1&xt=2';
$html = iconv("ISO-8859-2","UTF-8//IGNORE",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",0);

$trs = $table->find("tr");
array_shift($trs);
array_shift($trs);

foreach ($trs as $tr) {
  $td = $tr->find("td");
  $data = array(
    'obvod' => $td[0]->plaintext,
    'cislo' => $td[1]->plaintext,
    'name' => str_replace('&nbsp;',' ',$td[2]->plaintext),
    'age' => $td[3]->plaintext,
    'volebni_strana' => $td[4]->plaintext,
    'navrhujici_strana' => $td[5]->plaintext,
    'politicka_prislusnost' => $td[6]->plaintext,
    'povolani' => $td[7]->plaintext,
    'bydliste' => $td[8]->plaintext,
    '1_kolo_hlasy' => $td[9]->plaintext,
    '1_kolo_procenta' => $td[10]->plaintext,
    '2_kolo_hlasy' => $td[11]->plaintext,
    '2_kolo_procenta' => $td[12]->plaintext
  );
  scraperwiki::save_sqlite(array('obvod','cislo'),$data);
}

?>
<?php

//all senate candidates 2012

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/senat/se1111?xjazyk=CZ&xdatum=20121012&xv=1&xt=2';
$html = iconv("ISO-8859-2","UTF-8//IGNORE",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",0);

$trs = $table->find("tr");
array_shift($trs);
array_shift($trs);

foreach ($trs as $tr) {
  $td = $tr->find("td");
  $data = array(
    'obvod' => $td[0]->plaintext,
    'cislo' => $td[1]->plaintext,
    'name' => str_replace('&nbsp;',' ',$td[2]->plaintext),
    'age' => $td[3]->plaintext,
    'volebni_strana' => $td[4]->plaintext,
    'navrhujici_strana' => $td[5]->plaintext,
    'politicka_prislusnost' => $td[6]->plaintext,
    'povolani' => $td[7]->plaintext,
    'bydliste' => $td[8]->plaintext,
    '1_kolo_hlasy' => $td[9]->plaintext,
    '1_kolo_procenta' => $td[10]->plaintext,
    '2_kolo_hlasy' => $td[11]->plaintext,
    '2_kolo_procenta' => $td[12]->plaintext
  );
  scraperwiki::save_sqlite(array('obvod','cislo'),$data);
}

?>
