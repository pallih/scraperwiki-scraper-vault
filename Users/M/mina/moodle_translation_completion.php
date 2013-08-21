<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://download.moodle.org/langpack/2.6/?lang=en");
$html = str_get_html($html_content);

foreach ($html->find("table.generaltable tr") as $i => $row) {
    if ( $i > 0 ) {
        $language = $row->find("td.c0", 0)->plaintext;
        if ( strpos($row->find("td.c4", 0)->innertext, "span") !== false ) {
            $rawtext = $row->find("td.c4 span", 0)->plaintext;
            $progress = substr($rawtext, strpos($rawtext, "%")+1);
            eval('$percentage = '. $progress .';');
        } else {
            $percentage = 0;
            $progress = "- : " . $row->find("td.c4", 0)->plaintext;
        }
        //print($percentage . " " . $progress . "\n");
        //if ($i == 20) { break; }
        scraperwiki::save_sqlite(array("Language"), array("Language" => $language, "Percentage completion" => $percentage, "Progress" => $progress));
    }
}

$html->__destruct();

?>