<?php
require 'scraperwiki/simple_html_dom.php';
$page_counter = 0;

//initial value of variable-table name
//scraperwiki::save_var('which-table', "1"); 
//disable after first run

$oldnap = scraperwiki::get_var('which-table');

if ($oldnap == "1")
    {
    scraperwiki::save_var('which-table', "2"); 
    }
    else
    {
    scraperwiki::save_var('which-table', "1"); 
    }

$current = "swdata" . $oldnap;
print "Writing table: " . $current . "\n";

do { 
$kovetkezo = "";
$page_counter++;
$pageurl = "http://www.hasznaltauto.hu/talalatilista/auto/YHUQECPJ75JDSHH4K11URJIL5UM5ZJ67OJ0PSDARHGCQOAM901FIFTJ117ST1HZ508UQIHTYLS04GGOQJWA9WSRZWSFHQTUKOPY2GKPLULCZGKD479JY3IPMERARL1J9HFGYQ12RUA692DHRT071D83FDDERAH5HL528M7LK8HZQR4ILRLOD6FKZ7QZEK7P5KFTJJAZI6R1YEG3KK5QPYDMRE6OERT170MUJUQMP9Y7MSZKYU58F9FSCYA1GM1TWJS96RGAI5CIPZCM20REO47E15K4ZP1M3CF8FOG3MOCGU93088QKU33WAPEQLT1STGHGGUAET3KLJ0CHTOY6Z5YK2U2OE0185S/page{$page_counter}";
 
$html_content = scraperWiki::scrape($pageurl);

$html = str_get_html($html_content);
foreach ($html->find("div.talalati_lista") as $talalat) {  
    foreach ($talalat->find("h2 a") as $el) {

    $url = $el->href;
    $kod = substr($url, -7); 
    }

    scraperWiki::save_sqlite(   
            array('id'),
            array(
                'id' => $kod,
                'url' => $url
            ),
            $table_name=$current
        );
    }
    foreach ($html->find("div.oldalszamozas a[title=Következő]") as $kovetkezo) {
//    print $page_counter . "\n";
    }

//} while ($page_counter != 10);
 } while ($kovetkezo != "");
?>
