<?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperWiki::scrape("http://widget.kontan.co.id/v2/logammulia");

$dom->load($html);
$root = $dom->find("div.idr");
$emas = str_replace(".","",$root[1]->plaintext);
$perak = str_replace(".","",$root[2]->plaintext);
$message = scraperwiki::save_sqlite(array("id"),            
                array("id"=>1,
                        "emas"=>$emas,
                        "perak"=>$perak,
                    ));
print $emas;
print "\n".$perak;
?>
<?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperWiki::scrape("http://widget.kontan.co.id/v2/logammulia");

$dom->load($html);
$root = $dom->find("div.idr");
$emas = str_replace(".","",$root[1]->plaintext);
$perak = str_replace(".","",$root[2]->plaintext);
$message = scraperwiki::save_sqlite(array("id"),            
                array("id"=>1,
                        "emas"=>$emas,
                        "perak"=>$perak,
                    ));
print $emas;
print "\n".$perak;
?>
