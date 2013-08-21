<?php

// The source
// It's aggregate financial data for charities split by major source of income
$html = scraperWiki::scrape("http://www.charitycommission.gov.uk/ShowCharity/RegisterOfCharities/SectorData/CharitiesByIncomeCategory.aspx");

// fire up the dom...
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

// find some data:

// The date first:
$date = $dom->find("#ctl00_MainContent_pageTitle");
if (!$date) {
    echo 'ERROR - no date found';
    exit;
}
// This is horrid.  The substr is to get rid of the dash that doesn't seem
// to go by any other means...
$date = substr(str_replace("Charities by income category ", "", $date[0]->innertext()), 5);
$date = date_create($date);

// Check if there's already data:
try {
    $alreadyDataForDate = scraperwiki::select("* from swdata where `date` = '" . $date->format(DATE_ISO8601) . "'");
    var_dump($alreadyDataForDate);
        if ($alreadyDataForDate) {
            // don't need to do it again
            exit;
        }
} catch (Exception $e) {
    // Table doesn't exist, we can carry on.
}



$ret = array();
// Now get some data
// tables have ids like: ctl00_MainContent_sdtcByIncCatPer90_gvTable
for ($centile = 70; $centile <= 90; $centile += 10) {
    foreach (array('Total', 'Avg', 'Per') as $calcType) {

        $tableid = "ctl00_MainContent_sdtcByIncCat" . $calcType . $centile . "_gvTable";
        $table = $dom->find("#" . $tableid);

        // now look through the rows
        if ($table && $table[0] && $table[0]->id) {
            $cells= $table[0]->find("tr.DeHighlightRow td");
            echo " found " . count($cells) . "\r\n";
            foreach ($cells as $cell) {
                $dataRow = array();
                // the rowclass and cellclass attributes tell us pretty well what we've got:
                $dataRow['incomeType'] = str_replace(array("class_data_", "Label"), "", $cell->rowclass);
                $dataRow['label'] = str_replace(array("class_data_", "Label"), "", $cell->colclass);
                // clean up the value so we've got just numbers
                $dataRow['value'] = preg_replace("/([^0-9.])/", "", $cell->innertext());
                // the rest:
                $dataRow['centile'] = $centile;
                $dataRow['calculationType'] = $calcType;
                $dataRow['date'] = $date;

                if ($dataRow['value']) {
                    scraperwiki::save(array('date', 'centile', 'calculationType', 'incomeType', 'label'), $dataRow);
                    $ret[] = $dataRow;
                }

            }
        }

    }
}



?>
