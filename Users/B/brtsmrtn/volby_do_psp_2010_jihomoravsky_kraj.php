<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2010/ps111?xjazyk=CZ&xkraj=11&xstrana=0&xv=1&xt=1';
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
    'zkratka_volebni_strany' => $td[1]->plaintext,
    'poradove_cislo' => $td[2]->plaintext,
    'name' => str_replace('&nbsp;',' ',$td[3]->plaintext),
    'age' => $td[4]->plaintext,
    'navrhovana_strana' => $td[5]->plaintext,
    'politicka_prislusnost' => $td[6]->plaintext,
    'hlasy' => str_replace('&nbsp;',' ',$td[7]->plaintext),
    'procenta' => $td[8]->plaintext,
    'mandat' => str_replace('&nbsp;',' ',$td[9]->plaintext),
    'poradi' => $td[10]->plaintext
  );
  scraperwiki::save_sqlite(array('cislo_volebni_strany','zkratka_volebni_strany','poradove_cislo','name','age','navrhovana_strana','politicka_prislusnost','hlasy','procenta','mandat','poradi'),$data, $table_name="swdata");
}

?>