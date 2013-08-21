<?php
/**
 * Get the new Charity Commission overview data in a nice format and 
 * store it so we have time-series...
 */


// Get the page:
$html = scraperWiki::scrape("http://www.charitycommission.gov.uk/ShowCharity/RegisterOfCharities/SectorData/SectorOverview.aspx");

// Find the data:
$data = array();
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

if(!function_exists('cleanupCCdata')) {
    function cleanupCCdata ($domEl) {
        return str_replace(array(','), '', $domEl->plaintext);
    }
}

// How many charities:
$sections = $dom->find("#ctl00_MainContent_ucNumberCharitiesChart_ucLegend_tbl td.DataColumnCSS");
$data['numMainCharities'] = cleanupCCdata($sections[0]);
$data['numLinkedCharities'] = cleanupCCdata($sections[1]);
$data['numTotalCharities'] = cleanupCCdata($sections[2]);
$data['date'] = date_create();
// sanity check
if ((int)$data['numTotalCharities'] != ((int)$data['numMainCharities'] + (int)$data['numLinkedCharities'])) {
    echo 'ERROR - not adding up';
} else {

    scraperwiki::save(array('date'), $data);

    //$saved = scraperwiki::select("* from swdata where `date` = '" . date('Y-m-d') . "'");
    //var_dump($saved);

}
?>
