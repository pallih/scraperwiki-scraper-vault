<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
// $url = "http://mappings.dbpedia.org/index.php/Mapping_nl";
// $url = "http://mappings.dbpedia.org/index.php/Mapping_ru";
// $allurls[] = "http://mappings.dbpedia.org/index.php?title=Special:AllPages&from=Infobox+river&namespace=204";
$allurls = array();
$allurls[] = "http://mappings.dbpedia.org/index.php/Special:AllPages/Mapping_tr:";
$string = "";
$string .= '<?xml version="1.0" encoding="UTF-8"?><mediawiki xmlns="http://www.mediawiki.org/xml/export-0.6/">';

foreach ($allurls as $url) {
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
    
    $i = 0;
    foreach ($html->find("table.mw-allpages-table-chunk td a") as $el) {
        $i++;
        $template = "http://mappings.dbpedia.org/index.php?title=%s&action=edit";
        // echo $el->href."\n";
        if (preg_match("/(Mapping_..:.*)$/", $el->href, $ris)) {
            $title = $ris[1];
            $string .= "<page><title>".str_replace("_", " ", $title)."</title>";
            $string .= "<revision><text>";
            $url = sprintf($template, $title);
            $html_content = scraperwiki::scrape($url);
            $html_in = str_get_html($html_content);
            foreach ($html_in->find("#wpTextbox1") as $el_in) {
                $string .= "{$el_in->innertext}";
            }
            $string .= "</text></revision>";
            $string .= "</page>";
        }
    }
}

$string .= "</mediawiki>";

echo "\n";
echo $string;

//$record = array("id" => $string, "text" => $string);
//scraperwiki::save(array("id"), $record);

