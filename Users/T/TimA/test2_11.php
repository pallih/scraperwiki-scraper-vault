<?php

$html = scraperWiki::scrape("http://www.regmovies.com/nowshowing/opencaptionedshowtimes.aspx");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$dom->find("table.theatresByState");

foreach ($dom->find("td.stateTransparentRow div.hdrTransparentBlock h1") as $stateHeaders) {

    $record = array(
        'state' => $stateHeaders->plaintext
    );
    scraperwiki::save(array('state'), $record);

}


?>
<?php

$html = scraperWiki::scrape("http://www.regmovies.com/nowshowing/opencaptionedshowtimes.aspx");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$dom->find("table.theatresByState");

foreach ($dom->find("td.stateTransparentRow div.hdrTransparentBlock h1") as $stateHeaders) {

    $record = array(
        'state' => $stateHeaders->plaintext
    );
    scraperwiki::save(array('state'), $record);

}


?>
