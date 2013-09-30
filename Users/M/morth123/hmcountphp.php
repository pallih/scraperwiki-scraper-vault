<?php
// A scraper for airline information from PHL.org

require 'scraperwiki/simple_html_dom.php'; 
$html_content = scraperwiki::scrape("http://www.hm.com/gb/subdepartment/sale?Nr=4294944772"); 
$html = str_get_html($html_content);

foreach ($html->find("dl.settings dd") as $el) {  }

$record = array( 'hmcount1' => $el->innertext, 'hmcount2' => $el->innertext);
//$record = ( 'hmcount1' => $el->innertext);

print $record . "\n";
 print json_encode($record) . "\n";

//scraperwiki::save('hmcount1', $record); 
//scraperwiki::sqliteexecute("delete from swdata"); 
scraperwiki::sqliteexecute("drop table if exists swdata"); 
//scraperwiki::sqliteexecute("drop table if exists hmcount_new"); 

scraperwiki::save_var('last_page', (integer)$el->innertext); print scraperwiki::get_var('last_page');

?>
<?php
// A scraper for airline information from PHL.org

require 'scraperwiki/simple_html_dom.php'; 
$html_content = scraperwiki::scrape("http://www.hm.com/gb/subdepartment/sale?Nr=4294944772"); 
$html = str_get_html($html_content);

foreach ($html->find("dl.settings dd") as $el) {  }

$record = array( 'hmcount1' => $el->innertext, 'hmcount2' => $el->innertext);
//$record = ( 'hmcount1' => $el->innertext);

print $record . "\n";
 print json_encode($record) . "\n";

//scraperwiki::save('hmcount1', $record); 
//scraperwiki::sqliteexecute("delete from swdata"); 
scraperwiki::sqliteexecute("drop table if exists swdata"); 
//scraperwiki::sqliteexecute("drop table if exists hmcount_new"); 

scraperwiki::save_var('last_page', (integer)$el->innertext); print scraperwiki::get_var('last_page');

?>
