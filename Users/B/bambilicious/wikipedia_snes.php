<?php

require 'scraperwiki/simple_html_dom.php';

$pages = array(
"http://en.wikipedia.org/wiki/List_of_Super_Nintendo_Entertainment_System_games_(A-M)",
"http://en.wikipedia.org/wiki/List_of_Super_Nintendo_Entertainment_System_games_(N-Z)"
);
foreach ($pages as $page) {
    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom(); $dom->load($html);
    foreach ($dom->find("table.wikitable tr") as $data) {
        $tds = $data->find("td");
        if (count($tds) >= 5) {
        $regions = implode(',', explode(' ', $tds[5]->plaintext));
        $record = array(
            'console' => 'SNES',
            'title' => $tds[0]->plaintext,
            #'alternative titles' => $alt,
            'developer' => $tds[3]->plaintext,
            'release' => date('Y-m-d', strtotime($tds[2]->plaintext)),
            'publisher' => $tds[4]->plaintext,
            'regions' => $regions,
        );
        scraperwiki::save(array('title'), $record);
        }
    }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$pages = array(
"http://en.wikipedia.org/wiki/List_of_Super_Nintendo_Entertainment_System_games_(A-M)",
"http://en.wikipedia.org/wiki/List_of_Super_Nintendo_Entertainment_System_games_(N-Z)"
);
foreach ($pages as $page) {
    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom(); $dom->load($html);
    foreach ($dom->find("table.wikitable tr") as $data) {
        $tds = $data->find("td");
        if (count($tds) >= 5) {
        $regions = implode(',', explode(' ', $tds[5]->plaintext));
        $record = array(
            'console' => 'SNES',
            'title' => $tds[0]->plaintext,
            #'alternative titles' => $alt,
            'developer' => $tds[3]->plaintext,
            'release' => date('Y-m-d', strtotime($tds[2]->plaintext)),
            'publisher' => $tds[4]->plaintext,
            'regions' => $regions,
        );
        scraperwiki::save(array('title'), $record);
        }
    }
}

?>
