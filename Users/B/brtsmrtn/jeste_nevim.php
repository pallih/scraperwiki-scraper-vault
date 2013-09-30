<?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/kv1994/kv22?xjazyk=CZ&xid=1&xv=21';
$html = iconv("ISO-8859-2","UTF-8//IGNORE",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",0);

$trs = $table->find("tr");
array_shift($trs);
$trst = $table->find("tr");
array_shift($trst);

$kraj = "";
foreach ($trs as $tr) {
    $tdh = $tr->find("td, 1");
    if (!$tdh) {
      foreach ($trs as $tr) {
        $td = $tr->find("td");
        $kraj = str_replace('&nbsp;',' ',$td[0]->plaintext);
      }  
    } else { 
        foreach ($trs as $tr) {
          $td = $tr->find("td");
          $data = array(
            'kraj' => $kraj,
            'kod' => $td[0]->plaintext,
            'mesto' => str_replace('&nbsp;',' ',$td[1]->plaintext),
            'odkaz' => $td[2]->plaintext
          );
        }      
      }
      scraperwiki::save_sqlite(array('kraj','kod','mesto','odkaz'),$data, $table_name="swdata");
}
?><?php

require 'scraperwiki/simple_html_dom.php';

$url = 'http://volby.cz/pls/kv1994/kv22?xjazyk=CZ&xid=1&xv=21';
$html = iconv("ISO-8859-2","UTF-8//IGNORE",scraperwiki::scrape($url));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",0);

$trs = $table->find("tr");
array_shift($trs);
$trst = $table->find("tr");
array_shift($trst);

$kraj = "";
foreach ($trs as $tr) {
    $tdh = $tr->find("td, 1");
    if (!$tdh) {
      foreach ($trs as $tr) {
        $td = $tr->find("td");
        $kraj = str_replace('&nbsp;',' ',$td[0]->plaintext);
      }  
    } else { 
        foreach ($trs as $tr) {
          $td = $tr->find("td");
          $data = array(
            'kraj' => $kraj,
            'kod' => $td[0]->plaintext,
            'mesto' => str_replace('&nbsp;',' ',$td[1]->plaintext),
            'odkaz' => $td[2]->plaintext
          );
        }      
      }
      scraperwiki::save_sqlite(array('kraj','kod','mesto','odkaz'),$data, $table_name="swdata");
}
?>