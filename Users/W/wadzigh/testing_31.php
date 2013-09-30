<?php
require "scraperwiki/simple_html_dom.php";
define("BASE_URL", "http://splitticket.moneysavingexpert.com/results.php?");


// Save a record to the data store.
function saveData($unique, $railway ) {
      scraperWiki::save_sqlite($unique, $railway );
}

function getLinks($page) {
    global $destination, $id, $from_city, $pisah;
    $id = 0;
  
            $source = scraperWiki::scrape($page);
            $html = new simple_html_dom();
            $html->load($source);
            $id = $id+1;
            $ticketvalues = $html->find("td[@class='ticketvalue']");
            $from_city= $ticketvalues[0]->plaintext;
            $destination= $ticketvalues[5]->plaintext;
            $pisah= $ticketvalues[2]->plaintext;
            
                         $railway = array(
                         "id"=>$id,
                         "from_city"=>$from_city,                             
                         "destination"=>$destination,
                         "pisah"=>$pisah
                     
                        );
         // Save the record.
        saveData(array("from_city","destination","pisah"), $railway );
   

}
getLinks("http://splitticket.moneysavingexpert.com/results.php?departure=NCL&arrival=LDS&railcard=&travellers=adult&type=walkonsingle&hour=18&minute=41");
?><?php
require "scraperwiki/simple_html_dom.php";
define("BASE_URL", "http://splitticket.moneysavingexpert.com/results.php?");


// Save a record to the data store.
function saveData($unique, $railway ) {
      scraperWiki::save_sqlite($unique, $railway );
}

function getLinks($page) {
    global $destination, $id, $from_city, $pisah;
    $id = 0;
  
            $source = scraperWiki::scrape($page);
            $html = new simple_html_dom();
            $html->load($source);
            $id = $id+1;
            $ticketvalues = $html->find("td[@class='ticketvalue']");
            $from_city= $ticketvalues[0]->plaintext;
            $destination= $ticketvalues[5]->plaintext;
            $pisah= $ticketvalues[2]->plaintext;
            
                         $railway = array(
                         "id"=>$id,
                         "from_city"=>$from_city,                             
                         "destination"=>$destination,
                         "pisah"=>$pisah
                     
                        );
         // Save the record.
        saveData(array("from_city","destination","pisah"), $railway );
   

}
getLinks("http://splitticket.moneysavingexpert.com/results.php?departure=NCL&arrival=LDS&railcard=&travellers=adult&type=walkonsingle&hour=18&minute=41");
?>