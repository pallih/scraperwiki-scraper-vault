<?php
$url = "http://catalogue.library.manchester.ac.uk/items/1654645";
//$url = "http://prism.talis.com/brighton-ac/items/1019563";

$html = scraperWiki::scrape($url);           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$count = 0;

// get each item (tr) at each location (li)
foreach($dom->find("li.available") as $location){
    $locationname = $location->find("h3 span", 0)->plaintext;
    echo "Items at " . $locationname . "\n";
    foreach($location->find("tr") as $item) {
        // if this tr just contains table headings, skip to the next tr
        if ($item->first_child()->tag == 'th') { continue; }
        $count++; // number of items
        echo "Item number $count \n";
        $fieldcount = 0;
        $fieldname = array (0 => "Barcode", 1=> "Shelfmark", 2=>"Loan Type", 3=>"Status");
        // loop for each item field
        foreach ($item->find('td') as $itemdetail) {
            $name = $fieldname[$fieldcount];
            echo "$name : $itemdetail->plaintext \n";
            $fieldvalue[$name] = $itemdetail->plaintext; // add 'fieldname'=>'value' to array
            $fieldcount++; // when we loop again, use next field name
         }
         $fieldvalue['Location'] = $locationname;
         // save to db, key is the barcode   
         scraperwiki::save_sqlite(array ('Barcode'),$fieldvalue);
         $fieldvalue = "";
    } // endif each item
    
} // endif each location (that is available)

// do the same but for stuff that is unavailable TODO abstract this code to avoid duplicating it
// get each item (tr) at each location (li)
foreach($dom->find("li.unavailable") as $location){
    $locationname = $location->find("h3 span", 0)->plaintext;
    echo "Items at " . $locationname . "\n";
    foreach($location->find("tr") as $item) {
        // if this tr just contains table headings, skip to the next tr
        if ($item->first_child()->tag == 'th') { continue; }
        $count++; // number of items
        echo "Item number $count \n";
        $fieldcount = 0;
        $fieldname = array (0 => "Barcode", 1=> "Shelfmark", 2=>"Loan Type", 3=>"Status");
        // loop for each item field
        foreach ($item->find('td') as $itemdetail) {
            $name = $fieldname[$fieldcount];
            echo "$name : $itemdetail->plaintext \n";
            $fieldvalue[$name] = $itemdetail->plaintext; // add 'fieldname'=>'value' to array
            $fieldcount++; // when we loop again, use next field name
         }
         $fieldvalue['Location'] = $locationname;
         // save to db, key is the barcode   
         scraperwiki::save_sqlite(array ('Barcode'),$fieldvalue);
         $fieldvalue = "";
    } // end each item
    
} // end each location (that is unavailable)
echo "Total items $count";
?>
<?php
$url = "http://catalogue.library.manchester.ac.uk/items/1654645";
//$url = "http://prism.talis.com/brighton-ac/items/1019563";

$html = scraperWiki::scrape($url);           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$count = 0;

// get each item (tr) at each location (li)
foreach($dom->find("li.available") as $location){
    $locationname = $location->find("h3 span", 0)->plaintext;
    echo "Items at " . $locationname . "\n";
    foreach($location->find("tr") as $item) {
        // if this tr just contains table headings, skip to the next tr
        if ($item->first_child()->tag == 'th') { continue; }
        $count++; // number of items
        echo "Item number $count \n";
        $fieldcount = 0;
        $fieldname = array (0 => "Barcode", 1=> "Shelfmark", 2=>"Loan Type", 3=>"Status");
        // loop for each item field
        foreach ($item->find('td') as $itemdetail) {
            $name = $fieldname[$fieldcount];
            echo "$name : $itemdetail->plaintext \n";
            $fieldvalue[$name] = $itemdetail->plaintext; // add 'fieldname'=>'value' to array
            $fieldcount++; // when we loop again, use next field name
         }
         $fieldvalue['Location'] = $locationname;
         // save to db, key is the barcode   
         scraperwiki::save_sqlite(array ('Barcode'),$fieldvalue);
         $fieldvalue = "";
    } // endif each item
    
} // endif each location (that is available)

// do the same but for stuff that is unavailable TODO abstract this code to avoid duplicating it
// get each item (tr) at each location (li)
foreach($dom->find("li.unavailable") as $location){
    $locationname = $location->find("h3 span", 0)->plaintext;
    echo "Items at " . $locationname . "\n";
    foreach($location->find("tr") as $item) {
        // if this tr just contains table headings, skip to the next tr
        if ($item->first_child()->tag == 'th') { continue; }
        $count++; // number of items
        echo "Item number $count \n";
        $fieldcount = 0;
        $fieldname = array (0 => "Barcode", 1=> "Shelfmark", 2=>"Loan Type", 3=>"Status");
        // loop for each item field
        foreach ($item->find('td') as $itemdetail) {
            $name = $fieldname[$fieldcount];
            echo "$name : $itemdetail->plaintext \n";
            $fieldvalue[$name] = $itemdetail->plaintext; // add 'fieldname'=>'value' to array
            $fieldcount++; // when we loop again, use next field name
         }
         $fieldvalue['Location'] = $locationname;
         // save to db, key is the barcode   
         scraperwiki::save_sqlite(array ('Barcode'),$fieldvalue);
         $fieldvalue = "";
    } // end each item
    
} // end each location (that is unavailable)
echo "Total items $count";
?>
