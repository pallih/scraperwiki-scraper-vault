<?php
# Scrape community kitchen information at #http://www.dccentralkitchen.org/dcck/kinc/Left_Navigation/Kitchens_Folder/CommunityKitchens.shtml

// Get the page.
$html = scraperwiki::scrape("http://www.dccentralkitchen.org/dcck/kinc/Left_Navigation/Kitchens_Folder/CommunityKitchens.shtml");

// Put the page into dom.
require  'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

// Set up kitchen data structure.
$kitchen = array();

// Find beginning of table.
$tablecontents = "";
    while ($tablecontents != "National Community Kitchens")
   // $tablecontents = $html->find('div[
    

   // foreach($dom->find('tr') as $kitchen){ 
        # Store data in the datastore
       // print $data->plaintext . "\n";
       // scraperwiki::save(array('data'), array('data' => $data->plaintext));
   // }
// Elise added the following 2 lines
foreach($dom->find('td') as $data) {
                     scraperwiki::save(array('table_cell'), array('table_cell' => $data->plaintext));
                 }             
?>