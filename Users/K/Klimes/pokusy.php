<?php
# Blank PHP
//scraperwiki::sqliteexecute("create table Volby ('obec' string, 'kandidatka' string, `kandidat` string, 'vek' int, 'navrhujici' string, 'prislusnost' string, 'hlasy' int, 'poradi' int)");           
//scraperwiki::sqliteexecute("insert into Volby values (?,?,?,?,?,?,?)", array('CSSD', 'hello', 45, 'CSSD', 'Cssd', 1259, 1));
//scraperwiki::sqliteexecute("insert or replace into ttt values (:xx, :yy)", array("xx"=>10, "yy"=>"again"));
$html = scraperWiki::scrape("http://www.volby.cz/pls/kv2010/kv21111?xjazyk=CZ&xid=0&xv=23&xdz=4&xnumnuts=1100&xobec=554782&xstrana=0");           
//print $html . "\n";
        
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

print "Encoding: " . mb_check_encoding($html, 'UTF-8');
  
//scraperwiki::sqliteexecute("insert into ttt values (?,?)", array(9, 'hello'));
//scraperwiki::sqliteexecute("insert or replace into ttt values (:xx, :yy)", array("xx"=>10, "yy"=>"again"));

//scraperwiki::sqlitecommit();           

?>
<?php
# Blank PHP
//scraperwiki::sqliteexecute("create table Volby ('obec' string, 'kandidatka' string, `kandidat` string, 'vek' int, 'navrhujici' string, 'prislusnost' string, 'hlasy' int, 'poradi' int)");           
//scraperwiki::sqliteexecute("insert into Volby values (?,?,?,?,?,?,?)", array('CSSD', 'hello', 45, 'CSSD', 'Cssd', 1259, 1));
//scraperwiki::sqliteexecute("insert or replace into ttt values (:xx, :yy)", array("xx"=>10, "yy"=>"again"));
$html = scraperWiki::scrape("http://www.volby.cz/pls/kv2010/kv21111?xjazyk=CZ&xid=0&xv=23&xdz=4&xnumnuts=1100&xobec=554782&xstrana=0");           
//print $html . "\n";
        
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

print "Encoding: " . mb_check_encoding($html, 'UTF-8');
  
//scraperwiki::sqliteexecute("insert into ttt values (?,?)", array(9, 'hello'));
//scraperwiki::sqliteexecute("insert or replace into ttt values (:xx, :yy)", array("xx"=>10, "yy"=>"again"));

//scraperwiki::sqlitecommit();           

?>
