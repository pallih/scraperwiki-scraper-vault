<?php



$html = scraperWiki::scrape("http://www.xwordinfo.com/Crossword?date=11/08/2011");
# print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('div.letter') as $div_letter){
    // $div_letter->innerText = null;
    $div_letter->textContent = '';
}
echo $html->saveHTML();

// $html = $dom->writeHTML();

?>


