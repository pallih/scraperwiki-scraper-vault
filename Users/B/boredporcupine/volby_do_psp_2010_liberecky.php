<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.volby.cz/pls/ps2010/ps111?xjazyk=CZ&xkraj=7&xstrana=0&xv=1&xt=1';
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
    'cislo_volebni_strany' => $td[0]->plaintext,
    'volebni_strana' => $td[1]->plaintext,
    'poradove_cislo' => $td[2]->plaintext,
    'jmeno_a_prijmeni' => str_replace('&nbsp;',' ',$td[3]->plaintext),
    'vek' => $td[4]->plaintext,
    'navrhovana_strana' => $td[5]->plaintext,
    'politicka_prislusnost' => $td[6]->plaintext,
    'pocet_hlasu' => str_replace('&nbsp;',' ',$td[7]->plaintext),
    'procenta' => $td[8]->plaintext,
    'mandat' => str_replace('&nbsp;',' ',$td[9]->plaintext),
    'poradi' => $td[10]->plaintext
  );
  scraperwiki::save_sqlite(array('cislo_volebni_strany','volebni_strana','poradove_cislo','jmeno_a_prijmeni','vek','navrhovana_strana','politicka_prislusnost','pocet_hlasu','procenta','mandat','poradi'),$data, $table_name="swdata");
}

?>