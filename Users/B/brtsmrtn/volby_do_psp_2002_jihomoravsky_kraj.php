<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2002/ps111?xjazyk=CZ&xv=1&xt=1&xkstrana=0&xkraj=11';
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
    'tituly' => str_replace('&nbsp;',' ',$td[4]->plaintext),
    'age' => $td[5]->plaintext,
    'navrhovana_strana' => $td[6]->plaintext,
    'politicka_prislusnost' => $td[7]->plaintext,
    'hlasy' => str_replace('&nbsp;',' ',$td[8]->plaintext),
    'procenta' => $td[9]->plaintext
  );
  scraperwiki::save_sqlite(array('cislo_volebni_strany','zkratka_volebni_strany','poradove_cislo','name','tituly','age','navrhovana_strana','politicka_prislusnost','hlasy','procenta'),$data, $table_name="swdata");
}

?><?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps2002/ps111?xjazyk=CZ&xv=1&xt=1&xkstrana=0&xkraj=11';
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
    'tituly' => str_replace('&nbsp;',' ',$td[4]->plaintext),
    'age' => $td[5]->plaintext,
    'navrhovana_strana' => $td[6]->plaintext,
    'politicka_prislusnost' => $td[7]->plaintext,
    'hlasy' => str_replace('&nbsp;',' ',$td[8]->plaintext),
    'procenta' => $td[9]->plaintext
  );
  scraperwiki::save_sqlite(array('cislo_volebni_strany','zkratka_volebni_strany','poradove_cislo','name','tituly','age','navrhovana_strana','politicka_prislusnost','hlasy','procenta'),$data, $table_name="swdata");
}

?>