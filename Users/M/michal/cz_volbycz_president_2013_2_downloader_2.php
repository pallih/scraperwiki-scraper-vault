<?php

//get all towns' htmls (obce)
//like http://www.volby.cz/pls/prez2013/pe311?xjazyk=CZ&xnumnuts=2107&xobec=536041

//temp
/*scraperwiki::save_var('last_town_code',0);                                               //********************************
die();*/
/*$rows = scraperwiki::select("count(*) from `swdata` where town_code>'599999'");
foreach ($rows as $row) {
 print_r($row);
}
scraperwiki::sqliteexecute("delete from `swdata` where town_code>'599999'");
scraperwiki::sqlitecommit();
die();*/


$election_link = 'http://www.volby.cz/pls/prez2013/';                                               //********************************

$last_town_code = scraperwiki::get_var('last_town_code',0);

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_volbycz_president_2013_1", "src");                                               //********************************
$rows = scraperwiki::select("* from src.town where town_code>'{$last_town_code}' order by town_code");

foreach ($rows as $row) {
  $url = $election_link . $row['link'];
  $html = str_replace('ISO-8859-2','UTF-8',str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url))));
  $data = $row;
  $data['html'] = $html;
  scraperwiki::save_sqlite(array('town_code'),$data);
  scraperwiki::save_var('last_town_code',$data['town_code']);
}
scraperwiki::save_var('last_town_code',0); 
?>
<?php

//get all towns' htmls (obce)
//like http://www.volby.cz/pls/prez2013/pe311?xjazyk=CZ&xnumnuts=2107&xobec=536041

//temp
/*scraperwiki::save_var('last_town_code',0);                                               //********************************
die();*/
/*$rows = scraperwiki::select("count(*) from `swdata` where town_code>'599999'");
foreach ($rows as $row) {
 print_r($row);
}
scraperwiki::sqliteexecute("delete from `swdata` where town_code>'599999'");
scraperwiki::sqlitecommit();
die();*/


$election_link = 'http://www.volby.cz/pls/prez2013/';                                               //********************************

$last_town_code = scraperwiki::get_var('last_town_code',0);

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_volbycz_president_2013_1", "src");                                               //********************************
$rows = scraperwiki::select("* from src.town where town_code>'{$last_town_code}' order by town_code");

foreach ($rows as $row) {
  $url = $election_link . $row['link'];
  $html = str_replace('ISO-8859-2','UTF-8',str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url))));
  $data = $row;
  $data['html'] = $html;
  scraperwiki::save_sqlite(array('town_code'),$data);
  scraperwiki::save_var('last_town_code',$data['town_code']);
}
scraperwiki::save_var('last_town_code',0); 
?>
