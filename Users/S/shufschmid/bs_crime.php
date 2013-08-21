<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.stawa.bs.ch/archiv?action=shownews&nid=8168");
$html = str_get_html($html_content);
for($zahl=8160;$zahl<8168;$zahl++){

    $html_content = scraperwiki::scrape("http://www.stawa.bs.ch/archiv?action=shownews&nid=".$zahl);
    $html = str_get_html($html_content);
    foreach ($html->find("div.lauftext b") as $el) {
        print $el->innertext . "\n";
    }
}
?>
