<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2002/ps111?xjazyk=CZ&xv=1&xt=1&xkstrana=0&xkraj=6';
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
    'tituly' => str_replace('&nbsp;',' ',$td[4]->plaintext),
    'vek' => $td[5]->plaintext,
    'navrhovana_strana' => $td[6]->plaintext,
    'politicka_prislusnost' => $td[7]->plaintext,
    'pocet_hlasu' => str_replace('&nbsp;',' ',$td[8]->plaintext),
    'procenta' => $td[9]->plaintext
  );
  scraperwiki::save_sqlite(array('cislo_volebni_strany','volebni_strana','poradove_cislo','jmeno_a_prijmeni','tituly','vek','navrhovana_strana','politicka_prislusnost','pocet_hlasu','procenta'),$data, $table_name="swdata");
}

?>