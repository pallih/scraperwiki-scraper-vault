<?php

//$html = scraperWiki::scrape("http://www.fieb.org.br/guia/dados_industria.asp?industria=9642");
require 'scraperwiki/simple_html_dom.php'; 
///$dom = new simple_html_dom(); 
//$dom->load($html); 

//$links=$dom->find(".BtnSearchResultDetail a");
//We now have a array with all the links to go to :)


for($value = 1; $value<10000; $value++ ) {
 
$html = scraperWiki::scrape("http://www.fieb.org.br/guia/dados_industria.asp?industria=".$value);
$dom = new simple_html_dom();
$dom->load($html); 

$title= $dom->find("table",0);
//print $title->plaintext . "\n";

//$content=$dom->find(".keynote",0);
//print $content->plaintext . "\n";

$record = array(
                'teste' => utf8_encode ($title->plaintext)
                
            );

//print_r($record);

scraperwiki::save(array('teste'), $record); 

}
?><?php

//$html = scraperWiki::scrape("http://www.fieb.org.br/guia/dados_industria.asp?industria=9642");
require 'scraperwiki/simple_html_dom.php'; 
///$dom = new simple_html_dom(); 
//$dom->load($html); 

//$links=$dom->find(".BtnSearchResultDetail a");
//We now have a array with all the links to go to :)


for($value = 1; $value<10000; $value++ ) {
 
$html = scraperWiki::scrape("http://www.fieb.org.br/guia/dados_industria.asp?industria=".$value);
$dom = new simple_html_dom();
$dom->load($html); 

$title= $dom->find("table",0);
//print $title->plaintext . "\n";

//$content=$dom->find(".keynote",0);
//print $content->plaintext . "\n";

$record = array(
                'teste' => utf8_encode ($title->plaintext)
                
            );

//print_r($record);

scraperwiki::save(array('teste'), $record); 

}
?>