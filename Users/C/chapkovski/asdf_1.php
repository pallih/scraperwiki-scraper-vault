<?php
 require 'scraperwiki/simple_html_dom.php';
 $html = scraperWiki::scrape("http://www.ozon.ru/context/detail/id/1675437/");
// print $html . "\n"; 
 $dom = new simple_html_dom();
 $dom->load($html);
 $ret = $dom->find('div[class=item js_saleblock]'); 
 echo count($ret)."\n";
 foreach($ret as $element) {
    echo $element->innertext. "\n";
}
// print $ret[0];
?>
