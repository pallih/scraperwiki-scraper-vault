<?php

//Get simple_html_dom.php
require 'scraperwiki/simple_html_dom.php';

//Get the pages - $wiki is the page from Wikipedia detailing MPs elected in the 2010 election...
$wiki = scraperWiki::scrape("http://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_United_Kingdom_general_election,_2010");                    
$wiki_dom = new simple_html_dom();
$wiki_dom->load($wiki);

//... And here's Guido's list.
$guido = scraperWiki::scrape("http://order-order.com/2013/09/13/list-of-shame-every-mp-who-employs-a-family-member/");                    
$guido_dom = new simple_html_dom();
$guido_dom->load($guido);

$list = array();

foreach($guido_dom->find("div[@class='post-body'] div p strong") as $guido_data){
    $string = $guido_data->plaintext;
    $list[] = rtrim($string, ":");
}

foreach($wiki_dom->find("table[@class='wikitable'] tr") as $wiki_data){
    $wiki_tds = $wiki_data->find("td");
    if(isset($wiki_tds[4])){
        $MP_long = $wiki_tds[4]->plaintext;
        $MP = explode("&#160;", $MP_long);
        if(isset($MP[1])){
            $party_code = $MP[1];
            if($party_code == "(C)"){
                $party = "Con";
            } else if($party_code == "(L)"){
                $party = "Lab";
            } else if ($party_code == "(SNP)"){
                $party = "SNP";
            } else if ($party_code == "(PC)"){
                $party = "Plaid Cymru";
            } else if ($party_code == "(LD)") {
                $party = "LDem"; 
            } else if ($party_code == "(APIN)") {
                $party = "Alliance Party"; 
            } else if ($party_code == "(SF)"){
                $party = "SF";
            } else if ($party_code == "(SDLP)") {
                $party = "SDLP";
            } else if ($party_code == "(G)") {
                $party = "Green";
            } else {
                $party = "Unknown"; 
            }
        }
    }

        if(isset($MP[1])){
            
            $sir = strpos($MP[0], "Sir");

            if($sir !== false){
                $MP[0] = substr($MP[0],4);
            }

            if(in_array($MP[0],$list)){
                $record = array(
                        'MP' => $MP[0],
                        'CONSTITUENCY' => $wiki_tds[0]->plaintext,
                        'PARTY' => $party
            );
        
            scraperwiki::save(array('MP'), $record);           

            }
        }
    }

?>