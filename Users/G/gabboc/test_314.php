<?php
include 'http://www.direttagoal.it/livesport/matchdetail/6432271';
require 'scraperwiki/simple_html_dom.php';

$html_content = scraperWiki::scrape("http://www.direttagoal.it/livesport/matchdetail/6432271");
$html = str_get_html($html_content);
foreach ($html->find("div.cronacacontainer tr") as $el) {
 $el1 = $el->find("td",2); 
   print $el1 . "\n";

}

?>
