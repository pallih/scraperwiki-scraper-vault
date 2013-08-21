<?php
require 'scraperwiki/simple_html_dom.php';
    //  The following is a list of Exchange SAUIDs gleaned from SamKnows

$codes = array( );
 $html_content= scraperWiki::scrape("http://www.dft.gov.uk/fyn/practical.php?directory=true");
 $html = str_get_html($html_content);
foreach ($html->find(".nav-list a") as $row) {
    
        $codes[] = $row->innertext;
 }

//print_r($codes) ;     
$i = 1;

 foreach($codes as $code) {

    echo "Loading " . $code . "...";
    $html_content= scraperWiki::scrape("http://www.dft.gov.uk/fyn/practical.php?directory=true&county=" . $code);
    echo "Loaded";
    $html = str_get_html($html_content);
    $line = array();
    
    foreach ($html->find(".row-fluid .span8 h3") as $row) {
    
            print $row->innertext. "\n";

            $line["ID"] = $i;
            $line["Loction"] = $row->innertext;
            $line["County"] = $code;
             scraperwiki::save(array("ID"),$line);
            $i++;
     }      
   
  

} 

?>