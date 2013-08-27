<?php
/*https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=*/

error_reporting(0);

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
            
        foreach($dom->find('<font face=') as $data){
        
        // Remove/Replace spaces and &nbsp ** still testing
        //$data = preg_replace("/\s|&nbsp;/",'',$data);
        //echo $data->plaintext . chr(13) . chr(10);    
        
        $tds = $data->plaintext;
        echo $tds . chr(13) . chr(10);;
        
        //echo "This is tds-1:   " . $tds[1]->plaintext . chr(13) . chr(10);
        //echo "----- data = " . $tds. chr(13) . chr(10);          

            //$tds = $data->find('<TD ');
            //echo "this is the value of tds---- " . $tds ;
            
            //$getID = ''text;
            //$getID = $getID->innertext;
            //if($getID == '')
            //    {
                //echo $getID;
            //    }
            //else
            //    {
                //echo $getID; 

                //get the TD for every TR
                //save the TD into a $record array                


               $record = array(
                        'PSIDlbl' => $tds[4]->plaintext,
                        'PSID' => $tds[5]->plaintext, 
                        'FNamelbl' => $tds[6]->plaintext, 
                        'FName' => $tds[7]->plaintext, 

                        'MName' => $tds[8]->plaintext,

                        'LName' => $tds[10]->plaintext,
                        'Citylbl' => $tds[11]->plaintext, 
                        'City' => $tds[12]->plaintext, 
                        'Citylbl' => $tds[8]->plaintext,
                        'City' => $tds[9]->plaintext,
                        'Countylbl' => $tds[10]->plaintext,
                        'County' => $tds[11]->plaintext,
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

                
                print_r ($record);
        
                //print for debugging
                //print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'PSID' is indexed
                //scraperwiki::save_sqlite(array("PSID"),$record );
            //}//- end if
    
        } //- end foreach
} //- end foreach

/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    //for($i = 0; $i <= 300000; $i++) {        
        //$fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=' . '' . $i . '' . chr(13) . chr(10);
        //echo $fullUrl ;
        //array_push($sources, $fullUrl ); //save url to array
       $fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=154354';
       array_push($sources, $fullUrl );
    //}
}

?>
<?php
/*https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=*/

error_reporting(0);

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
            
        foreach($dom->find('<font face=') as $data){
        
        // Remove/Replace spaces and &nbsp ** still testing
        //$data = preg_replace("/\s|&nbsp;/",'',$data);
        //echo $data->plaintext . chr(13) . chr(10);    
        
        $tds = $data->plaintext;
        echo $tds . chr(13) . chr(10);;
        
        //echo "This is tds-1:   " . $tds[1]->plaintext . chr(13) . chr(10);
        //echo "----- data = " . $tds. chr(13) . chr(10);          

            //$tds = $data->find('<TD ');
            //echo "this is the value of tds---- " . $tds ;
            
            //$getID = ''text;
            //$getID = $getID->innertext;
            //if($getID == '')
            //    {
                //echo $getID;
            //    }
            //else
            //    {
                //echo $getID; 

                //get the TD for every TR
                //save the TD into a $record array                


               $record = array(
                        'PSIDlbl' => $tds[4]->plaintext,
                        'PSID' => $tds[5]->plaintext, 
                        'FNamelbl' => $tds[6]->plaintext, 
                        'FName' => $tds[7]->plaintext, 

                        'MName' => $tds[8]->plaintext,

                        'LName' => $tds[10]->plaintext,
                        'Citylbl' => $tds[11]->plaintext, 
                        'City' => $tds[12]->plaintext, 
                        'Citylbl' => $tds[8]->plaintext,
                        'City' => $tds[9]->plaintext,
                        'Countylbl' => $tds[10]->plaintext,
                        'County' => $tds[11]->plaintext,
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

                
                print_r ($record);
        
                //print for debugging
                //print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'PSID' is indexed
                //scraperwiki::save_sqlite(array("PSID"),$record );
            //}//- end if
    
        } //- end foreach
} //- end foreach

/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    //for($i = 0; $i <= 300000; $i++) {        
        //$fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=' . '' . $i . '' . chr(13) . chr(10);
        //echo $fullUrl ;
        //array_push($sources, $fullUrl ); //save url to array
       $fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=154354';
       array_push($sources, $fullUrl );
    //}
}

?>
<?php
/*https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=*/

error_reporting(0);

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
            
        foreach($dom->find('<font face=') as $data){
        
        // Remove/Replace spaces and &nbsp ** still testing
        //$data = preg_replace("/\s|&nbsp;/",'',$data);
        //echo $data->plaintext . chr(13) . chr(10);    
        
        $tds = $data->plaintext;
        echo $tds . chr(13) . chr(10);;
        
        //echo "This is tds-1:   " . $tds[1]->plaintext . chr(13) . chr(10);
        //echo "----- data = " . $tds. chr(13) . chr(10);          

            //$tds = $data->find('<TD ');
            //echo "this is the value of tds---- " . $tds ;
            
            //$getID = ''text;
            //$getID = $getID->innertext;
            //if($getID == '')
            //    {
                //echo $getID;
            //    }
            //else
            //    {
                //echo $getID; 

                //get the TD for every TR
                //save the TD into a $record array                


               $record = array(
                        'PSIDlbl' => $tds[4]->plaintext,
                        'PSID' => $tds[5]->plaintext, 
                        'FNamelbl' => $tds[6]->plaintext, 
                        'FName' => $tds[7]->plaintext, 

                        'MName' => $tds[8]->plaintext,

                        'LName' => $tds[10]->plaintext,
                        'Citylbl' => $tds[11]->plaintext, 
                        'City' => $tds[12]->plaintext, 
                        'Citylbl' => $tds[8]->plaintext,
                        'City' => $tds[9]->plaintext,
                        'Countylbl' => $tds[10]->plaintext,
                        'County' => $tds[11]->plaintext,
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

                
                print_r ($record);
        
                //print for debugging
                //print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'PSID' is indexed
                //scraperwiki::save_sqlite(array("PSID"),$record );
            //}//- end if
    
        } //- end foreach
} //- end foreach

/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    //for($i = 0; $i <= 300000; $i++) {        
        //$fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=' . '' . $i . '' . chr(13) . chr(10);
        //echo $fullUrl ;
        //array_push($sources, $fullUrl ); //save url to array
       $fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=154354';
       array_push($sources, $fullUrl );
    //}
}

?>
