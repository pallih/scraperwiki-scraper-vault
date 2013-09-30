<?php

require 'scraperwiki/simple_html_dom.php';
$lastpage = 110;
$links = array();
$url = "http://www.eparlimen.com/home/signup/";

for ($page=0; $page <= $lastpage; $page+=10) {

    $html = scraperWiki::scrape("http://www.eparlimen.com/home/signup/$page");
    $dom = new simple_html_dom();
    $dom->load($html);

    $anchors = $dom->find("div.sidebar a");

    foreach ($anchors as $anchor) {

        if (stristr($anchor->href, "view")) {

            # Hack for the shitty relative non-properly-entitized-urls
            $links[] = array("url"=>"https://www.eparlimen.com".str_replace(" ", "%20", $anchor->href));

        }
    }
}

scraperwiki::save_sqlite(array("url"), $links, "eparlimen_constituencies_links");

?>
<?php

require 'scraperwiki/simple_html_dom.php';
$lastpage = 110;
$links = array();
$url = "http://www.eparlimen.com/home/signup/";

for ($page=0; $page <= $lastpage; $page+=10) {

    $html = scraperWiki::scrape("http://www.eparlimen.com/home/signup/$page");
    $dom = new simple_html_dom();
    $dom->load($html);

    $anchors = $dom->find("div.sidebar a");

    foreach ($anchors as $anchor) {

        if (stristr($anchor->href, "view")) {

            # Hack for the shitty relative non-properly-entitized-urls
            $links[] = array("url"=>"https://www.eparlimen.com".str_replace(" ", "%20", $anchor->href));

        }
    }
}

scraperwiki::save_sqlite(array("url"), $links, "eparlimen_constituencies_links");

?>
