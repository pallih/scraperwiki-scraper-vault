<?php
# Scrape community kitchen information at #http://www.dccentralkitchen.org/dcck/kinc/Left_Navigation/Kitchens_Folder/CommunityKitchens.shtml

// Get the page.
$html = scraperwiki::scrape("http://www.dccentralkitchen.org/dcck/kinc/Left_Navigation/Kitchens_Folder/CommunityKitchens.shtml");

// Put the page into dom.
require  'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

$i = 0;
foreach($dom->find('table#table2 tr') as $row) {
    $j = 0;
    $record = array();
    foreach($row->find('td') as $column) {
       switch($j) {
            case 0:
                $record['name'] = $column->plaintext;
                $key_name = 'name';
                break;
            case 1:
                $record['link'] = $column->plaintext;
                $key_name = 'link';
                break;
            case 2:
                $record['contact'] = $column->plaintext;
                $key_name = 'contact';
                break;
            case 3:
                $record['location'] = $column->plaintext;
                $key_name = 'location';
                break;
        }    
        $j++; 
    }
    // Store data in the datastore

    scraperwiki::save(array('name','link', 'contact', 'location'), $record);
    $i++;
}

function clean_up($text) {
    return strip_tags($text);
}

?><?php
# Scrape community kitchen information at #http://www.dccentralkitchen.org/dcck/kinc/Left_Navigation/Kitchens_Folder/CommunityKitchens.shtml

// Get the page.
$html = scraperwiki::scrape("http://www.dccentralkitchen.org/dcck/kinc/Left_Navigation/Kitchens_Folder/CommunityKitchens.shtml");

// Put the page into dom.
require  'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

$i = 0;
foreach($dom->find('table#table2 tr') as $row) {
    $j = 0;
    $record = array();
    foreach($row->find('td') as $column) {
       switch($j) {
            case 0:
                $record['name'] = $column->plaintext;
                $key_name = 'name';
                break;
            case 1:
                $record['link'] = $column->plaintext;
                $key_name = 'link';
                break;
            case 2:
                $record['contact'] = $column->plaintext;
                $key_name = 'contact';
                break;
            case 3:
                $record['location'] = $column->plaintext;
                $key_name = 'location';
                break;
        }    
        $j++; 
    }
    // Store data in the datastore

    scraperwiki::save(array('name','link', 'contact', 'location'), $record);
    $i++;
}

function clean_up($text) {
    return strip_tags($text);
}

?>