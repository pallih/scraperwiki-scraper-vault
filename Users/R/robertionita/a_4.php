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

        foreach($dom->find('/html/body/form/div/table/tbody/tr/td/table[2]') as $data){                     
            //echo "this is the value of data---- " . $data . "..................STOP";          

            $tds = $data->find('<td');
                //echo "this is the value of tds---- " . $tds ;
            
            $getID = $data->find('<td',15);
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
                        
                        'Denumire Comerciala' => $tds[1]->plaintext, 
                     //  'DCI' => $tds[3]->plaintext, 
                        'Forma Farmaceutica' => $tds[5]->plaintext, 
                        'Concentratia' => $tds[7]->plaintext, 
                        'Cod ATC' => $tds[9]->plaintext, 
                       // 'Actiune Terapeutica' => $tds[11]->plaintext, 
                       // 'Prescriptie' => $tds[13]->plaintext, 
                        'Ambalaj' => $tds[15]->plaintext, 
                        'Volum Ambalaj' => $tds[17]->plaintext, 
                        //'Valabilitate Ambalaj'=> $tds[19]->plaintext,  
                        'Cod CIM' => $tds[21]->plaintext, 
                        'Firm/Tar Producatoare APP' => $tds[23]->plaintext,  
                        'Firm/Tar Detinatoare APP'=> $tds[25]->plaintext, 
                        //'Nr./Data Ambalaj APP' => $tds[30]->plaintext, 
                        
                    );
        
                //print for debugging
                //print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'Name' is indexed
                scraperwiki::save(array('Cod CIM'), $record );
            }//- end if
    
        } //- end foreach
} //- end foreach

/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    for($i = 1; $i <= 38097; $i++) {        
        $fullUrl = 'http://193.169.156.200/app/nom1/anm_maint.asp?id=' . '' . $i . '' . chr(13) . chr(10);
        //echo $fullUrl ;
        array_push($sources, $fullUrl ); //save url to array
   }
}

?>