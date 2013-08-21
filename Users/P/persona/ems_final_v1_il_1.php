<?php

require 'scraperwiki/simple_html_dom.php';

//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl(2);

//iterate through sources
foreach($sources as $page) {
    set_time_limit(0);
    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    $gotResults = 0;
    $onePage = 0;

    //Check for Next page tag
    foreach($dom->find("a class='toplink'[@->plaintext=='Next']") as $elm) {
        if ($elm->plaintext == "Next"){
            $gotResults++;
        }//endif
    }//end foreach

    //Check for One page results
    foreach($dom->find('td.pageLinks') as $rch) {
        $rch = substr($rch, -1, 2);
        $rch= $rch + 0;
        if ($rch < 25){
            $onePage++;        
        }//endif
    }//end foreach        

    $runPage = $gotResults + $onePage;
    if ($runPage > 0){    
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='3'] tr") as $data){  
            $tds = $data->find("td");
            //get the TD for every TR
            if(count($tds)==2){
                    //save the TD into a $record array
                    $record = array(
                        'Name'      => $tds[0]->plaintext, 
                        'Residence' => $tds[1]->plaintext
                    );
        
                //print for debugging
                print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'Name' is indexed
                scraperwiki::save(array('Name'), $record );
            }
    
        } //- end foreach
    } //- end if

} //- end foreach



/*
 * Build URLS and save to $sources array
 */
function buildUrl($length,$prefix = '') {
    global $sources;
    for($j = 97; $j < 123; $j++) {
        if ($length > 1) {
            buildUrl($length-1,$prefix . chr($j));
        } else {
            $last = $prefix . chr($j) . '';
            for ($i = 1; $i < 10; $i = ++$i){
                $page = '&page='. $i;              
                $fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=IN&last=' . '' . $last . '' . $page . chr(13) . chr(10);
                echo $fullUrl ;
                array_push($sources, $fullUrl ); //save url to array
            }
        }
    }
}

?>
