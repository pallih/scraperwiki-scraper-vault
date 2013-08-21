<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/ps1996/u321?xpl=0&xtr=1&xvstrana=00&xkraj=37';
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
    'hlasy' => str_replace('&nbsp;',' ',$td[5]->plaintext),
    'procenta' => $td[6]->plaintext,
    'mandat' => str_replace('&nbsp;',' ',$td[7]->plaintext),
    'poradi' => $td[8]->plaintext
  );
  scraperwiki::save_sqlite(array('cislo_volebni_strany','zkratka_volebni_strany','poradove_cislo','name','age','hlasy','procenta','mandat','poradi'),$data, $table_name="swdata");
}

?>