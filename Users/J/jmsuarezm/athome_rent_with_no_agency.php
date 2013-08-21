<?php
require 'scraperwiki/simple_html_dom.php';
ini_set('max_execution_time', 1200);
setlocale(LC_ALL, 'fr_FR.UTF8');

$counter = 0;
//the first time, set manually the first page
$value = "/recherche/resultats/tr/rt/w/d,Luxembourg%7CBelair,Limpertsberg,Rollingergrund,Merl%3Ba,Bertrange%3Ba,Strassen/ig/h,f";
//while $value is not blank
while ($value != "") {
    $htmlCentre = scraperWiki::scrape("http://www.athome.lu" . $value);
    $domCentre = new simple_html_dom();
    $domCentre->load($htmlCentre);
    //find the announces in the current page and store the records
    findAnnounces ($domCentre, $counter);
    //look for the next page link
    $value = "";
    foreach($domCentre->find('.next') as $data){
        $value = $data->href;
    }
}

//if there are no records, insert a blank record
/*
if ($counter == 0){
    $record=array();
    $record["id"] = 0;
    $record["url"] = "No records for today :(";
    $record["submitter"] = 0;
    //save the record
    scraperwiki::save(array('id'), $record);
}
*/

/***************** Functions *********************/
function findAnnounces($strDataDom, &$counter){
    //for each page, there are up to 10 records, each of them marked with DOM class 'plus'
    foreach($strDataDom->find('.plus') as $data){
        $value = $data->href;
        //is it a valid URL for an announce?
        if (strrpos ($value , "www.athome.lu/")){
            //go into the announce
            $htmlContent = scraperWiki::scrape($value);
            //look for the start of the json record wich has all the information of the announce
            //and manually trim it to the correct json format
            $strStart = strpos($htmlContent, "initGoogleMap");
            $strEnd = strpos($htmlContent, "#containerGoogleMap");
    
            $strData = substr ($htmlContent, $strStart, $strEnd - $strStart - 6);     
            $strData = ltrim($strData, "initGoogleMap([");
            //is it UTF format? just in case we convert it   
            $strDataUTF = iconv('UTF-8', 'ASCII//TRANSLIT', $strData);
            //the function will transfor the string into a json object and store it in the database
            storeJson($strDataUTF, $value, $counter);
        }
    }
}

/*************************************************/
function storeJson($strData, $url, &$counter){
    $record=array();
    //ads we have already seen and discard
    //reviewed on 13/05/2013
    $dislike = array("2526433", "2514611", "2351993", "2221553", "1893755", "427350", "2530587", "2560145", "2560055", "2555105", "978951", "2595253", "2567675", "91864", "2549179", "2584447", "2610713", "1794045", "2615221", "2637917", "2639393");
    //decode the string
    $jsonVar = json_decode($strData);
    //if the decode ended with no error
    if (json_last_error() === JSON_ERROR_NONE) {
        $sumbitter = $jsonVar -> submitter;
        if ($sumbitter == "websubmitter"){
            if (!in_array($jsonVar -> id, $dislike )){
                $record["id"] = $jsonVar -> id;
                $record["url"] = $url;
                $record["submitter"] = $sumbitter;
                //save the record
                scraperwiki::save(array('id'), $record);
                $counter = 1;
            }
        }
    }    
} 

?>