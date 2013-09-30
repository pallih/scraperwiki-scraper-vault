<?php

function endsWith($haystack, $needle)
{
    $length = strlen($needle);
    if ($length == 0) {
        return true;
    }

    return (substr($haystack, -$length) === $needle);
}

require 'scraperwiki/simple_html_dom.php'; 
$baseURL = "http://magiccards.info";

$html = scraperWiki::scrape($baseURL."/query?q=is%3Avanilla&v=list&s=cname");          
$dom = new simple_html_dom();
$dom->load($html);
$tables = $dom->find("table");
$trs = $tables[3]->find("tr");
echo "Vanilla Cards: ".(count($trs)-1)."\n";
for ($i=1;$i<count($trs);$i++) {
    //echo $trs[$i]."\n";
    $tds = $trs[$i]->find("td");
    $as = $trs[$i]->find("a");
    //echo "found stuff";
    $cardhtml = scraperWiki::scrape($baseURL.$as[0]->href);
    $dom = new simple_html_dom();
    $dom->load($cardhtml);
    $images = $dom->find("img");
    $imageURL;
    foreach ($images as $image) {
        if (endsWith($image->src,".jpg")) {
            $imageURL = $image->src;
        }
    }
    
    $cards[] = array( 'Name' => $as[0]->plaintext, 'url' => $as[0]->href,'image'=>$imageURL,'type'=>$tds[2]->plaintext,'cost'=>$tds[3]->plaintext,'rarity'=>$tds[4]->plaintext);
}
scraperwiki::save_sqlite(array("url"),$cards);

?>
<?php

function endsWith($haystack, $needle)
{
    $length = strlen($needle);
    if ($length == 0) {
        return true;
    }

    return (substr($haystack, -$length) === $needle);
}

require 'scraperwiki/simple_html_dom.php'; 
$baseURL = "http://magiccards.info";

$html = scraperWiki::scrape($baseURL."/query?q=is%3Avanilla&v=list&s=cname");          
$dom = new simple_html_dom();
$dom->load($html);
$tables = $dom->find("table");
$trs = $tables[3]->find("tr");
echo "Vanilla Cards: ".(count($trs)-1)."\n";
for ($i=1;$i<count($trs);$i++) {
    //echo $trs[$i]."\n";
    $tds = $trs[$i]->find("td");
    $as = $trs[$i]->find("a");
    //echo "found stuff";
    $cardhtml = scraperWiki::scrape($baseURL.$as[0]->href);
    $dom = new simple_html_dom();
    $dom->load($cardhtml);
    $images = $dom->find("img");
    $imageURL;
    foreach ($images as $image) {
        if (endsWith($image->src,".jpg")) {
            $imageURL = $image->src;
        }
    }
    
    $cards[] = array( 'Name' => $as[0]->plaintext, 'url' => $as[0]->href,'image'=>$imageURL,'type'=>$tds[2]->plaintext,'cost'=>$tds[3]->plaintext,'rarity'=>$tds[4]->plaintext);
}
scraperwiki::save_sqlite(array("url"),$cards);

?>
