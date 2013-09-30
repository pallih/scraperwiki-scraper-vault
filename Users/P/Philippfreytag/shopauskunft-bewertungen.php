<?php
require 'scraperwiki/simple_html_dom.php';  
$url = "https://www.shopauskunft.de/bewertung/ReifenDirektde--S-13779.spg-#aa#.html";
$limit = 100;

for($i = 1;$i <= $limit; $i++){
$page_url = str_replace("#aa#",$i,$url);
print $page_url. "\n";
$shop = scraperwiki::scrape($page_url);         
$dom = new simple_html_dom();
$dom->load($shop);
foreach($dom->find("td.text a") as $href){
    $urlcomment = $href->href;
    $commentsite = scraperwiki::scrape($urlcomment);
    $dom_comment = new simple_html_dom();
    $dom_comment->load($commentsite);
    $commenttr = $dom_comment->find("tr.datarow");
    $commenttd = $commenttr[0]->find("td.text");
    $kommentar = $commenttd[0]->plaintext;
  
    $record = array(
    'urlcomment' => $urlcomment,
    'kommentar' => $kommentar
     );
     scraperwiki::save(array('urlcomment', 'kommentar'), $record);
}
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';  
$url = "https://www.shopauskunft.de/bewertung/ReifenDirektde--S-13779.spg-#aa#.html";
$limit = 100;

for($i = 1;$i <= $limit; $i++){
$page_url = str_replace("#aa#",$i,$url);
print $page_url. "\n";
$shop = scraperwiki::scrape($page_url);         
$dom = new simple_html_dom();
$dom->load($shop);
foreach($dom->find("td.text a") as $href){
    $urlcomment = $href->href;
    $commentsite = scraperwiki::scrape($urlcomment);
    $dom_comment = new simple_html_dom();
    $dom_comment->load($commentsite);
    $commenttr = $dom_comment->find("tr.datarow");
    $commenttd = $commenttr[0]->find("td.text");
    $kommentar = $commenttd[0]->plaintext;
  
    $record = array(
    'urlcomment' => $urlcomment,
    'kommentar' => $kommentar
     );
     scraperwiki::save(array('urlcomment', 'kommentar'), $record);
}
}

?>
