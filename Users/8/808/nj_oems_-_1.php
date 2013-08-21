<?php

require 'scraperwiki/simple_html_dom.php';

//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl();

//iterate through sources
foreach($sources as $page) {
    set_time_limit(0);
    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
        //find the table of persons and iterate through each TR

        foreach($dom->find('//*[@id="mediumsmall"]/table/tbody/tr/*[@id="mediumsmall"]/table') as $data){                
            //echo "this is the value of data---- " . $data . "..................STOP";          

            $tds = $data->find('<td.white');
                //echo "this is the value of tds---- " . $tds ;
            
            $getID = $data->find('<td.white',15);
            //$getID = $getID->plaintext;
            if($getID == '')
                {
                //echo $getID;
                }
            else
                {
                //echo $getID; 

                //get the TD for every TR
                //save the TD into a $record array                
                $record = array(
                        'FNamelbl' => $tds[0]->plaintext, 
                        'FName' => $tds[1]->plaintext, 
                        'LNamelbl' => $tds[2]->plaintext,
                        'LName' => $tds[3]->plaintext,
                        'MIlbl' => $tds[4]->plaintext,
                        'MI' => $tds[5]->plaintext,
                        'Genderlbl' => $tds[6]->plaintext, 
                        'Gender' => $tds[7]->plaintext, 
                        'Citylbl' => $tds[8]->plaintext,
                        'City' => $tds[9]->plaintext,
                        'Statelbl' => $tds[10]->plaintext,
                        'State' => $tds[11]->plaintext,
                        'MuniCodelbl' => $tds[12]->plaintext,
                        'MuniCode' => $tds[13]->plaintext, 
                        'IDNumlbl' => $tds[14]->plaintext,
                        'IDNum' => $tds[15]->plaintext,
                        'EMT-Blbl' => $tds[16]->plaintext,
                        'CertStauslbl' => $tds[17]->plaintext,
                        'CertStaus' => $tds[18]->plaintext,
                        'InitCertlbl' => $tds[19]->plaintext, 
                        'InitCert' => $tds[20]->plaintext, 
                        'CertStartDatelbl' => $tds[21]->plaintext,
                        'CertStartDate' => $tds[22]->plaintext,
                        'CertExpDatelbl' => $tds[23]->plaintext, 
                        'CertExpDate' => $tds[24]->plaintext,
                        'ParaCertlbl' => $tds[25]->plaintext,
                        'PCertStauslbl' => $tds[26]->plaintext,
                        'PCertStaus' => $tds[27]->plaintext,
                        'PInitCertlbl' => $tds[28]->plaintext, 
                        'PInitCert' => $tds[29]->plaintext, 
                        'PCertStartDatelbl' => $tds[30]->plaintext,
                        'PCertStartDate' => $tds[31]->plaintext,
                        'PCertExpDatelbl' => $tds[32]->plaintext, 
                        'PCertExpDate' => $tds[33]->plaintext
                    );
        
                //print for debugging
                //print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'Name' is indexed
                scraperwiki::save_sqlLite(array('LName'), $record );
            }//- end if
    
        } //- end foreach
} //- end foreach

/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    for($i = 90844; $i <= 90850; $i++) {        
        $fullUrl = 'https://www.njoemscert.com/extCertView/index.cfm?fuseaction=UserDetail&intuserid=' . '' . $i . '' . chr(13) . chr(10);
        //echo $fullUrl ;
        array_push($sources, $fullUrl ); //save url to array
   }
}

?>
