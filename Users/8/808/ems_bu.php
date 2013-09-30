<?php

require 'scraperwiki/simple_html_dom.php';


//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl(2);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    $pageErrorCount = 0;

    //determin if there are page errors
    foreach($dom->find("<div[@class='bodya_warn'] tr") as $data0){  
        $pageErrorCount++;
    }
    

    if ($pageErrorCount == 0) {
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='3'] tr") as $data){  
        
            //TODO: Strip-out "Name" column header
            //TODO: Residence is displaying in the json_encode, but not on the Data tab??
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
            for ($i = 1; $i < 2; $i = ++$i){
                $page = '&page='. $i;              
                $fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
                echo $fullUrl ;
                array_push($sources, $fullUrl ); //save url to array
            }
        }
    }
}



?>
<?php

require 'scraperwiki/simple_html_dom.php';


//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl(2);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    $pageErrorCount = 0;

    //determin if there are page errors
    foreach($dom->find("<div[@class='bodya_warn'] tr") as $data0){  
        $pageErrorCount++;
    }
    

    if ($pageErrorCount == 0) {
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='3'] tr") as $data){  
        
            //TODO: Strip-out "Name" column header
            //TODO: Residence is displaying in the json_encode, but not on the Data tab??
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
            for ($i = 1; $i < 2; $i = ++$i){
                $page = '&page='. $i;              
                $fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
                echo $fullUrl ;
                array_push($sources, $fullUrl ); //save url to array
            }
        }
    }
}



?>
<?php

require 'scraperwiki/simple_html_dom.php';


//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl(2);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    $pageErrorCount = 0;

    //determin if there are page errors
    foreach($dom->find("<div[@class='bodya_warn'] tr") as $data0){  
        $pageErrorCount++;
    }
    

    if ($pageErrorCount == 0) {
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='3'] tr") as $data){  
        
            //TODO: Strip-out "Name" column header
            //TODO: Residence is displaying in the json_encode, but not on the Data tab??
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
            for ($i = 1; $i < 2; $i = ++$i){
                $page = '&page='. $i;              
                $fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
                echo $fullUrl ;
                array_push($sources, $fullUrl ); //save url to array
            }
        }
    }
}



?>
<?php

require 'scraperwiki/simple_html_dom.php';


//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl(2);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    $pageErrorCount = 0;

    //determin if there are page errors
    foreach($dom->find("<div[@class='bodya_warn'] tr") as $data0){  
        $pageErrorCount++;
    }
    

    if ($pageErrorCount == 0) {
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='3'] tr") as $data){  
        
            //TODO: Strip-out "Name" column header
            //TODO: Residence is displaying in the json_encode, but not on the Data tab??
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
            for ($i = 1; $i < 2; $i = ++$i){
                $page = '&page='. $i;              
                $fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
                echo $fullUrl ;
                array_push($sources, $fullUrl ); //save url to array
            }
        }
    }
}



?>
