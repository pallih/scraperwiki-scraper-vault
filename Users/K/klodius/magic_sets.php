<?php
require 'scraperwiki/simple_html_dom.php'; 
$baseURL = "http://magiccards.info";

$html = scraperWiki::scrape($baseURL."/sitemap.html");          
$dom = new simple_html_dom();
$dom->load($html);

$tables = $dom->find("table");
$as = $tables[1]->find("ul ul li a");
echo "Sets: ".count($as)."\n";
$sets = array();
foreach ($as as $a) {
    $record = array( 'Name' => $a->plaintext, 'url' => $a->href);
    $sets[] = $record;
}


foreach ($sets as $set) {
    $cards = array();
    $html= scraperWiki::scrape($baseURL.$set['url']);
    $dom->load($html);

    $tables = $dom->find("table");
    if (count($tables)>3) {
        $trs = $tables[3]->find("tr");
    } else {
        $trs = $tables[2]->find("tr");
    }

    echo "Cards in Set: ".(count($trs)-1)."\n";
    
    for ($i=1;$i<count($trs);$i++) {
        $tds = $trs[$i]->find("td");
        $as = $trs[$i]->find("a");
        $cards[] = array( 'Name' => $as[0]->plaintext, 'url' => $as[0]->href,'type'=>$tds[2]->plaintext,'cost'=>$tds[3]->plaintext,'rarity'=>$tds[4]->plaintext,'set'=>$set['Name']);
    }
    scraperwiki::save_sqlite(array("url"),$cards);
}


?>
<?php
require 'scraperwiki/simple_html_dom.php'; 
$baseURL = "http://magiccards.info";

$html = scraperWiki::scrape($baseURL."/sitemap.html");          
$dom = new simple_html_dom();
$dom->load($html);

$tables = $dom->find("table");
$as = $tables[1]->find("ul ul li a");
echo "Sets: ".count($as)."\n";
$sets = array();
foreach ($as as $a) {
    $record = array( 'Name' => $a->plaintext, 'url' => $a->href);
    $sets[] = $record;
}


foreach ($sets as $set) {
    $cards = array();
    $html= scraperWiki::scrape($baseURL.$set['url']);
    $dom->load($html);

    $tables = $dom->find("table");
    if (count($tables)>3) {
        $trs = $tables[3]->find("tr");
    } else {
        $trs = $tables[2]->find("tr");
    }

    echo "Cards in Set: ".(count($trs)-1)."\n";
    
    for ($i=1;$i<count($trs);$i++) {
        $tds = $trs[$i]->find("td");
        $as = $trs[$i]->find("a");
        $cards[] = array( 'Name' => $as[0]->plaintext, 'url' => $as[0]->href,'type'=>$tds[2]->plaintext,'cost'=>$tds[3]->plaintext,'rarity'=>$tds[4]->plaintext,'set'=>$set['Name']);
    }
    scraperwiki::save_sqlite(array("url"),$cards);
}


?>
