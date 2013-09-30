<?php

require 'scraperwiki/simple_html_dom.php';

//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl(1);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    //$gotResults = 0;
    //$onePage = 0;

    //Check for Next page tag
    //foreach($dom->find("a class='toplink'[@->plaintext=='Next']") as $elm) {
    //    if ($elm->plaintext == "Next"){
    //        $gotResults++;
    //    }//endif
    //}//end foreach

    //Check for One page results
    //foreach($dom->find('<table border="0" cellspacing="0" cellpadding="0" class="middle"> tr') as $onePg) {
    //    $tds = $onePg->find("td");
        //get the TD for every TR
    //    if(count($tds)==4){
                            //if ($onePg->plaintext == "1"){        
    //        $onePage++;     
    //    }//endif
    //}//end foreach        

    //$runPage = $gotResults + $onePage;
    //if ($runPage > 0){    
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='4'] tr") as $data){  
            $tds = $data->find("td");
            //get the TD for every TR
            if(count($tds)==7){
                    //save the TD into a $record array
                    $record = array(
                        'Num' => $tds[0]->plaintext, 
                        'ID' => $tds[1]->plaintext,
                        'LName' => $tds[2]->plaintext, 
                        'FName' => $tds[3]->plaintext,
                        'Org' => $tds[4]->plaintext, 
                        'CountyCode' => $tds[5]->plaintext,
                        'MuniCode' => $tds[6]->plaintext
                    );
        
                //print for debugging
                print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'LName' is indexed
                scraperwiki::save(array('LName'), $record );
            }
    
        } //- end foreach
    //} //- end if

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
            for ($i = 1; $i < 5; $i = ++$i){
                $page = '&showpage='. $i;              
                $fullUrl = 'https://www.njoemscert.com/extCertView/index.cfm?fuseaction=SearchUsers&Search=Search&vchLastName=' . '' . $last . '' . $page . chr(13) . chr(10);
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
buildUrl(1);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    //$gotResults = 0;
    //$onePage = 0;

    //Check for Next page tag
    //foreach($dom->find("a class='toplink'[@->plaintext=='Next']") as $elm) {
    //    if ($elm->plaintext == "Next"){
    //        $gotResults++;
    //    }//endif
    //}//end foreach

    //Check for One page results
    //foreach($dom->find('<table border="0" cellspacing="0" cellpadding="0" class="middle"> tr') as $onePg) {
    //    $tds = $onePg->find("td");
        //get the TD for every TR
    //    if(count($tds)==4){
                            //if ($onePg->plaintext == "1"){        
    //        $onePage++;     
    //    }//endif
    //}//end foreach        

    //$runPage = $gotResults + $onePage;
    //if ($runPage > 0){    
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='4'] tr") as $data){  
            $tds = $data->find("td");
            //get the TD for every TR
            if(count($tds)==7){
                    //save the TD into a $record array
                    $record = array(
                        'Num' => $tds[0]->plaintext, 
                        'ID' => $tds[1]->plaintext,
                        'LName' => $tds[2]->plaintext, 
                        'FName' => $tds[3]->plaintext,
                        'Org' => $tds[4]->plaintext, 
                        'CountyCode' => $tds[5]->plaintext,
                        'MuniCode' => $tds[6]->plaintext
                    );
        
                //print for debugging
                print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'LName' is indexed
                scraperwiki::save(array('LName'), $record );
            }
    
        } //- end foreach
    //} //- end if

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
            for ($i = 1; $i < 5; $i = ++$i){
                $page = '&showpage='. $i;              
                $fullUrl = 'https://www.njoemscert.com/extCertView/index.cfm?fuseaction=SearchUsers&Search=Search&vchLastName=' . '' . $last . '' . $page . chr(13) . chr(10);
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
buildUrl(1);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    //$gotResults = 0;
    //$onePage = 0;

    //Check for Next page tag
    //foreach($dom->find("a class='toplink'[@->plaintext=='Next']") as $elm) {
    //    if ($elm->plaintext == "Next"){
    //        $gotResults++;
    //    }//endif
    //}//end foreach

    //Check for One page results
    //foreach($dom->find('<table border="0" cellspacing="0" cellpadding="0" class="middle"> tr') as $onePg) {
    //    $tds = $onePg->find("td");
        //get the TD for every TR
    //    if(count($tds)==4){
                            //if ($onePg->plaintext == "1"){        
    //        $onePage++;     
    //    }//endif
    //}//end foreach        

    //$runPage = $gotResults + $onePage;
    //if ($runPage > 0){    
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='4'] tr") as $data){  
            $tds = $data->find("td");
            //get the TD for every TR
            if(count($tds)==7){
                    //save the TD into a $record array
                    $record = array(
                        'Num' => $tds[0]->plaintext, 
                        'ID' => $tds[1]->plaintext,
                        'LName' => $tds[2]->plaintext, 
                        'FName' => $tds[3]->plaintext,
                        'Org' => $tds[4]->plaintext, 
                        'CountyCode' => $tds[5]->plaintext,
                        'MuniCode' => $tds[6]->plaintext
                    );
        
                //print for debugging
                print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'LName' is indexed
                scraperwiki::save(array('LName'), $record );
            }
    
        } //- end foreach
    //} //- end if

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
            for ($i = 1; $i < 5; $i = ++$i){
                $page = '&showpage='. $i;              
                $fullUrl = 'https://www.njoemscert.com/extCertView/index.cfm?fuseaction=SearchUsers&Search=Search&vchLastName=' . '' . $last . '' . $page . chr(13) . chr(10);
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
buildUrl(1);

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    //$gotResults = 0;
    //$onePage = 0;

    //Check for Next page tag
    //foreach($dom->find("a class='toplink'[@->plaintext=='Next']") as $elm) {
    //    if ($elm->plaintext == "Next"){
    //        $gotResults++;
    //    }//endif
    //}//end foreach

    //Check for One page results
    //foreach($dom->find('<table border="0" cellspacing="0" cellpadding="0" class="middle"> tr') as $onePg) {
    //    $tds = $onePg->find("td");
        //get the TD for every TR
    //    if(count($tds)==4){
                            //if ($onePg->plaintext == "1"){        
    //        $onePage++;     
    //    }//endif
    //}//end foreach        

    //$runPage = $gotResults + $onePage;
    //if ($runPage > 0){    
        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='4'] tr") as $data){  
            $tds = $data->find("td");
            //get the TD for every TR
            if(count($tds)==7){
                    //save the TD into a $record array
                    $record = array(
                        'Num' => $tds[0]->plaintext, 
                        'ID' => $tds[1]->plaintext,
                        'LName' => $tds[2]->plaintext, 
                        'FName' => $tds[3]->plaintext,
                        'Org' => $tds[4]->plaintext, 
                        'CountyCode' => $tds[5]->plaintext,
                        'MuniCode' => $tds[6]->plaintext
                    );
        
                //print for debugging
                print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'LName' is indexed
                scraperwiki::save(array('LName'), $record );
            }
    
        } //- end foreach
    //} //- end if

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
            for ($i = 1; $i < 5; $i = ++$i){
                $page = '&showpage='. $i;              
                $fullUrl = 'https://www.njoemscert.com/extCertView/index.cfm?fuseaction=SearchUsers&Search=Search&vchLastName=' . '' . $last . '' . $page . chr(13) . chr(10);
                echo $fullUrl ;
                array_push($sources, $fullUrl ); //save url to array
            }
        }
    }
}

?>
