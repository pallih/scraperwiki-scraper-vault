<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2002/ps111?xjazyk=CZ&xv=2&xt=1&xkstrana=0&xkraj=0';
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
    'kraj' => str_replace('&nbsp;',' ',$td[0]->plaintext),
    'cislo_volebni_strany' => $td[1]->plaintext,
    'volebni_strana' => $td[2]->plaintext,
    'poradove_cislo' => $td[3]->plaintext,
    'jmeno_a_prijmeni' => str_replace('&nbsp;',' ',$td[4]->plaintext),
    'tituly' => str_replace('&nbsp;',' ',$td[5]->plaintext),
    'vek' => $td[6]->plaintext,
    'navrhovana_strana' => $td[7]->plaintext,
    'politicka_prislusnost' => $td[8]->plaintext,
    'pocet_hlasu' => str_replace('&nbsp;',' ',$td[9]->plaintext),
    'procenta' => $td[10]->plaintext
  );
  scraperwiki::save_sqlite(array('kraj','cislo_volebni_strany','volebni_strana','poradove_cislo','jmeno_a_prijmeni','tituly','vek','navrhovana_strana','politicka_prislusnost','pocet_hlasu','procenta'),$data, $table_name="swdata");
}

?><?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2002/ps111?xjazyk=CZ&xv=2&xt=1&xkstrana=0&xkraj=0';
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
    'kraj' => str_replace('&nbsp;',' ',$td[0]->plaintext),
    'cislo_volebni_strany' => $td[1]->plaintext,
    'volebni_strana' => $td[2]->plaintext,
    'poradove_cislo' => $td[3]->plaintext,
    'jmeno_a_prijmeni' => str_replace('&nbsp;',' ',$td[4]->plaintext),
    'tituly' => str_replace('&nbsp;',' ',$td[5]->plaintext),
    'vek' => $td[6]->plaintext,
    'navrhovana_strana' => $td[7]->plaintext,
    'politicka_prislusnost' => $td[8]->plaintext,
    'pocet_hlasu' => str_replace('&nbsp;',' ',$td[9]->plaintext),
    'procenta' => $td[10]->plaintext
  );
  scraperwiki::save_sqlite(array('kraj','cislo_volebni_strany','volebni_strana','poradove_cislo','jmeno_a_prijmeni','tituly','vek','navrhovana_strana','politicka_prislusnost','pocet_hlasu','procenta'),$data, $table_name="swdata");
}

?>