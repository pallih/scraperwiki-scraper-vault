<?php

$html = scraperWiki::scrape("http://www.regmovies.com/nowshowing/opencaptionedshowtimes.aspx");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

$state = "stateProv";

foreach ($dom->find("table.theatresByState tr") as $row) {

    # Need to figure out how/when to change states so that we can properly scrap data.

    switch ($state) {
        case "stateProv":
            $stateProv = $row->find("td.stateTransparentRow div.hdrTransparentBlock h1", 0);
            
            if ($stateProv != null) {
                $stateCode = $stateProv->plaintext;
        
                $record = array(
                    'state' => $stateCode
                );
        
                scraperwiki::save(array('state'), $record);
            }
            break;

        case "theatres":
            
            break;
    }
}
?>
<?php

$html = scraperWiki::scrape("http://www.regmovies.com/nowshowing/opencaptionedshowtimes.aspx");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

$state = "stateProv";

foreach ($dom->find("table.theatresByState tr") as $row) {

    # Need to figure out how/when to change states so that we can properly scrap data.

    switch ($state) {
        case "stateProv":
            $stateProv = $row->find("td.stateTransparentRow div.hdrTransparentBlock h1", 0);
            
            if ($stateProv != null) {
                $stateCode = $stateProv->plaintext;
        
                $record = array(
                    'state' => $stateCode
                );
        
                scraperwiki::save(array('state'), $record);
            }
            break;

        case "theatres":
            
            break;
    }
}
?>
