<?php

// The Scraper https://scraperwiki.com/scrapers/dzi_-_german_non_profit_companys/edit/#
// Scrapes http://www.dzi.de/spenderberatung/das-spenden-siegel/liste-aller-spenden-siegel-organisationen-a-z/
// From A-Z to generate a list of all NGOS and their detail URL
//
// This Scraper will take the list and get the details for each NGO


require_once 'scraperwiki/simple_html_dom.php';

// Load the List of NGOs
scraperwiki::attach("dzi_-_german_non_profit_companys", "ngolist");            
$ngos = scraperwiki::select("* FROM ngolist.ngos"); 

foreach ($ngos as $ngo){
    $details = scrapeDetails($ngo);
    saveNgo($details);
}

function saveNgo($ngo){
    scraperwiki::save_sqlite(array("name"),$ngo, "ngodetails");
}

/*
 Takes the url of a ngo and scrapes the details
*/
function scrapeDetails($ngo){
    $html_content = scraperwiki::scrape($ngo["url"]);
    $dom = new simple_html_dom();
    $dom->load($html_content);      

    $infosWeWant = array('Telefon', 'Rechtsform', 'Steuerstatus', 'Weltanschauliche Ausrichtung','Anzahl Mitarbeiter', 'Gesamteinnahmen:', 'Davon Sammlungseinnahmen', 'Bezugsjahr:');    


    // Scrape Details from all paragraphs
    $paragraphs = $dom->find('p');
    foreach($paragraphs as $p){

            if (strstr($p->plaintext, "Website")){
                $ngo["website"] = $p->find('a',0)->href;
            }

            if (strstr($p->plaintext, "Email")){
                $ngo["email"] = $p->find('a',0)->plaintext;
            }
            
            foreach ($infosWeWant as $key => $info){
                $res = extractInfo($p, $info);
                if ($res) {
                    $ngo[$info] = $res;
                    //Do not search for this info again
                    unset($infosWeWant[$key]);
                }
            }
   
    }
    print_r($ngo);
    return $ngo;
  
}

function extractInfo($p, $infoName){
    $res = false;
    if (strstr($p->plaintext, $infoName)){
               $res = trim(str_replace($infoName, "", $p->plaintext));
    }
    return $res;
}

?>
