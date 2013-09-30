<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2006/ps111?xjazyk=CZ&xkraj=0&xstrana=0&xv=2&xt=1';
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
    'cislo_kraje' => $td[0]->plaintext,
    'kraj' => str_replace('&nbsp;',' ',$td[1]->plaintext),
    'cislo_volebni_strany' => $td[2]->plaintext,
    'volebni_strana' => $td[3]->plaintext,
    'poradove_cislo' => $td[4]->plaintext,
    'jmeno_a_prijmeni' => str_replace('&nbsp;',' ',$td[5]->plaintext),
    'vek' => $td[6]->plaintext,
    'navrhovana_strana' => $td[7]->plaintext,
    'politicka_prislusnost' => $td[8]->plaintext,
    'pocet_hlasu' => str_replace('&nbsp;',' ',$td[9]->plaintext),
    'procenta' => $td[10]->plaintext,
    'poradi' => str_replace('&nbsp;',' ',$td[11]->plaintext)
  );
  scraperwiki::save_sqlite(array('cislo_kraje','kraj','cislo_volebni_strany','volebni_strana','poradove_cislo','jmeno_a_prijmeni','vek','navrhovana_strana','politicka_prislusnost','pocet_hlasu','procenta','poradi'),$data, $table_name="swdata");
}

?><?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2006/ps111?xjazyk=CZ&xkraj=0&xstrana=0&xv=2&xt=1';
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
    'cislo_kraje' => $td[0]->plaintext,
    'kraj' => str_replace('&nbsp;',' ',$td[1]->plaintext),
    'cislo_volebni_strany' => $td[2]->plaintext,
    'volebni_strana' => $td[3]->plaintext,
    'poradove_cislo' => $td[4]->plaintext,
    'jmeno_a_prijmeni' => str_replace('&nbsp;',' ',$td[5]->plaintext),
    'vek' => $td[6]->plaintext,
    'navrhovana_strana' => $td[7]->plaintext,
    'politicka_prislusnost' => $td[8]->plaintext,
    'pocet_hlasu' => str_replace('&nbsp;',' ',$td[9]->plaintext),
    'procenta' => $td[10]->plaintext,
    'poradi' => str_replace('&nbsp;',' ',$td[11]->plaintext)
  );
  scraperwiki::save_sqlite(array('cislo_kraje','kraj','cislo_volebni_strany','volebni_strana','poradove_cislo','jmeno_a_prijmeni','vek','navrhovana_strana','politicka_prislusnost','pocet_hlasu','procenta','poradi'),$data, $table_name="swdata");
}

?>