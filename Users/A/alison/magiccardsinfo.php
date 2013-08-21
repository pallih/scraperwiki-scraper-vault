<?php

require 'scraperwiki/simple_html_dom.php';
 
// Get most of the data from the spoiler page (everything except the collector's number)
$html_content = scraperwiki::scrape("http://magiccards.info/query?q=%2B%2Be%3Adka%2Fen&v=spoiler&s=issue");
$html = str_get_html($html_content);

$html_el = $html->find("html body", 0);
$raw = str_get_html($html_el->children(6));

$data = array();

echo("starting up...\n");

//$item = $raw->find("td[width='25%']",2);
foreach ($raw->find("td[width='25%']") as $item)
{
    $record = array();
    $record["name"] = trim($item->children(0)->first_child()->plaintext);

    $t = explode(", ", $item->children(1)->plaintext);
    $record["set"] = trim($t[0]);
    $record["rarity"] = trim($t[1]);

    $t = explode(",", $item->children(2)->plaintext);
    $record["type"] = trim($t[0]);
    $t[1] = trim($t[1]);
    $i = strpos($t[1], '(');
    $record["cost"] = trim(substr($t[1], 0, $i));
    $record["converted_cost"] = trim(substr($t[1], $i), "()");
    
    $record["text"] = trim(preg_replace("/<[^>]*>/", "", str_replace("<br>", "\n", $item->children(3)->innertext)));

    $record["flavour"] = trim(preg_replace("/<[^>]*>/", "", str_replace("<br>", "\n", $item->children(4)->innertext)));

    $record["artist"] = trim(str_replace("Illus. ", "", $item->children(5)->plaintext));

    $record["setNo"] = "0a";

    $data[$record["name"]."_".$record["set"]] = $record;
}

echo("first page complete...\n");

// Add in the collectors number from the list page
$html_content = scraperwiki::scrape("http://magiccards.info/query?q=%2B%2Be%3Adka%2Fen&v=list&s=issue");
$html = str_get_html($html_content);

$html_el = $html->find("html body", 0);
$raw = str_get_html($html_el->children(6));

//$item = $raw->find("tr[class]",2);
foreach ($raw->find("tr[class]") as $item)
{
    $record = array();
    $record["setNo"] = trim($item->children(0)->plaintext);
    $record["name"] = trim($item->children(1)->plaintext);
    $record["set"] = trim($item->children(6)->plaintext);
    
    $data[$record["name"]."_".$record["set"]]["setNo"] = $record["setNo"];
}    

echo("second page complete...\n");

foreach ($data as $k => $record)
    @scraperwiki::save(array('name', 'set'), $record);

?>
