<?php
/*https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=*/

error_reporting(0);

require 'scraperwiki/simple_html_dom.php';

//stores list of urls
$sources = array(
); 

//build urls and save to $sources
buildUrl();

//iterate through sources
foreach($sources as $page) {
    set_time_limit(0);
    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);

$store_arr = array();
$counter = 0;      

    foreach($dom->find('<font face=') as $tds){ 
//echo $tds->plaintext . chr(13) . chr(10);
    
    $result = $tds->plaintext;
    $store_arr[$counter++] = $result;

//echo 'Result: ' . $result . chr(13) . chr(10);

    } //- end foreach

$ScrapedPages++;

echo $ScrapedPages;
    
    if ( $store_arr[5] == 'Cert.&nbsp;Status'){
        echo ' - NO RECORD' . chr(13) . chr(10);
    }
    if($store_arr[5]!= 'Cert.&nbsp;Status'){
        echo ' - RECORD!  PSID: ' . $store_arr[5] . chr(13) . chr(10);
        $final_arr = array(
            'PSID' => $store_arr[5],
            'FName' => $store_arr[7],
            'MName' => $store_arr[8],
            'LName' => $store_arr[9],
            'City' => $store_arr[12],
            'County' => $store_arr[14],
            'PStatus' => $store_arr[16],
            
            'CertNum1' => $store_arr[21],        
            'CertName1' => $store_arr[22],
            'CertStatus1' => $store_arr[24],
            'CertIssueDate1' => $store_arr[25],
            'CertExpDate1' => $store_arr[26],
            
            'CertNum2' => $store_arr[27],        
            'CertName2' => $store_arr[28],
            'CertStatus2' => $store_arr[30],
            'CertIssueDate2' => $store_arr[31],
            'CertExpDate2' => $store_arr[32],
            
            'CertNum3' => $store_arr[33],        
            'CertName3' => $store_arr[34],
            'CertStatus3' => $store_arr[36],
            'CertIssueDate3' => $store_arr[37],
            'CertExpDate3' => $store_arr[38],
            
            'CertNum4' => $store_arr[39],        
            'CertName4' => $store_arr[40],
            'CertStatus4' => $store_arr[42],
            'CertIssueDate4' => $store_arr[43],
            'CertExpDate4' => $store_arr[44],
            
            'CertNum5' => $store_arr[45],        
            'CertName5' => $store_arr[46],
            'CertStatus5' => $store_arr[48],
            'CertIssueDate5' => $store_arr[49],
            'CertExpDate5' => $store_arr[50],
            
            'CertNum6' => $store_arr[51],        
            'CertName6' => $store_arr[52],
            'CertStatus6' => $store_arr[54],
            'CertIssueDate6' => $store_arr[55],
            'CertExpDate6' => $store_arr[56],
            
            'CertNum7' => $store_arr[57],        
            'CertName7' => $store_arr[58],
            'CertStatus7' => $store_arr[60],
            'CertIssueDate7' => $store_arr[61],
            'CertExpDate7' => $store_arr[62],
            
            'CertNum8' => $store_arr[63],        
            'CertName8' => $store_arr[64],
            'CertStatus8' => $store_arr[66],
            'CertIssueDate8' => $store_arr[67],
            'CertExpDate8' => $store_arr[68],
            
            'CertNum9' => $store_arr[69],        
            'CertName9' => $store_arr[70],
            'CertStatus9' => $store_arr[72],
            'CertIssueDate9' => $store_arr[73],
            'CertExpDate9' => $store_arr[74],
                
            'CertNum10' => $store_arr[75],        
            'CertName10' => $store_arr[76],
            'CertStatus10' => $store_arr[78],
            'CertIssueDate10' => $store_arr[79],
            'CertExpDate10' => $store_arr[80],
            
            'CertNum11' => $store_arr[81],        
            'CertName11' => $store_arr[82],
            'CertStatus11' => $store_arr[84],
            'CertIssueDate11' => $store_arr[85],
            'CertExpDate11' => $store_arr[86],
            
            'CertNum12' => $store_arr[87],        
            'CertName12' => $store_arr[88],
            'CertStatus12' => $store_arr[90],
            'CertIssueDate12' => $store_arr[91],
            'CertExpDate12' => $store_arr[92],
            
    //        'CertNum13' => $store_arr[21],        
    //        'CertName13' => $store_arr[22],
    //        'CertStatus13' => $store_arr[24],
    //        'CertIssueDate13' => $store_arr[25],
    //        'CertExpDate13' => $store_arr[26],
            
    //        'CertNum14' => $store_arr[27],        
    //        'CertName14' => $store_arr[28],
    //        'CertStatus14' => $store_arr[30],
    //        'CertIssueDate14' => $store_arr[31],
    //        'CertExpDate14' => $store_arr[32]
        );

//print_r($store_arr);
//print_r($final_arr); 

        scraperwiki::save(array('PSID'), $final_arr );
    }

    $dom->clear();  
    unset($dom);

} //- end foreach

/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    for($i = 10605; $i <= 300000; $i++) {        
    //for($i = 99000; $i <= 100000; $i++) {        
        $fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=' . '' . $i . '' . chr(13) . chr(10);
echo $fullUrl ;
        array_push($sources, $fullUrl ); //save url to array
    }
}

?>
<?php
/*https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=*/

error_reporting(0);

require 'scraperwiki/simple_html_dom.php';

//stores list of urls
$sources = array(
); 

//build urls and save to $sources
buildUrl();

//iterate through sources
foreach($sources as $page) {
    set_time_limit(0);
    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);

$store_arr = array();
$counter = 0;      

    foreach($dom->find('<font face=') as $tds){ 
//echo $tds->plaintext . chr(13) . chr(10);
    
    $result = $tds->plaintext;
    $store_arr[$counter++] = $result;

//echo 'Result: ' . $result . chr(13) . chr(10);

    } //- end foreach

$ScrapedPages++;

echo $ScrapedPages;
    
    if ( $store_arr[5] == 'Cert.&nbsp;Status'){
        echo ' - NO RECORD' . chr(13) . chr(10);
    }
    if($store_arr[5]!= 'Cert.&nbsp;Status'){
        echo ' - RECORD!  PSID: ' . $store_arr[5] . chr(13) . chr(10);
        $final_arr = array(
            'PSID' => $store_arr[5],
            'FName' => $store_arr[7],
            'MName' => $store_arr[8],
            'LName' => $store_arr[9],
            'City' => $store_arr[12],
            'County' => $store_arr[14],
            'PStatus' => $store_arr[16],
            
            'CertNum1' => $store_arr[21],        
            'CertName1' => $store_arr[22],
            'CertStatus1' => $store_arr[24],
            'CertIssueDate1' => $store_arr[25],
            'CertExpDate1' => $store_arr[26],
            
            'CertNum2' => $store_arr[27],        
            'CertName2' => $store_arr[28],
            'CertStatus2' => $store_arr[30],
            'CertIssueDate2' => $store_arr[31],
            'CertExpDate2' => $store_arr[32],
            
            'CertNum3' => $store_arr[33],        
            'CertName3' => $store_arr[34],
            'CertStatus3' => $store_arr[36],
            'CertIssueDate3' => $store_arr[37],
            'CertExpDate3' => $store_arr[38],
            
            'CertNum4' => $store_arr[39],        
            'CertName4' => $store_arr[40],
            'CertStatus4' => $store_arr[42],
            'CertIssueDate4' => $store_arr[43],
            'CertExpDate4' => $store_arr[44],
            
            'CertNum5' => $store_arr[45],        
            'CertName5' => $store_arr[46],
            'CertStatus5' => $store_arr[48],
            'CertIssueDate5' => $store_arr[49],
            'CertExpDate5' => $store_arr[50],
            
            'CertNum6' => $store_arr[51],        
            'CertName6' => $store_arr[52],
            'CertStatus6' => $store_arr[54],
            'CertIssueDate6' => $store_arr[55],
            'CertExpDate6' => $store_arr[56],
            
            'CertNum7' => $store_arr[57],        
            'CertName7' => $store_arr[58],
            'CertStatus7' => $store_arr[60],
            'CertIssueDate7' => $store_arr[61],
            'CertExpDate7' => $store_arr[62],
            
            'CertNum8' => $store_arr[63],        
            'CertName8' => $store_arr[64],
            'CertStatus8' => $store_arr[66],
            'CertIssueDate8' => $store_arr[67],
            'CertExpDate8' => $store_arr[68],
            
            'CertNum9' => $store_arr[69],        
            'CertName9' => $store_arr[70],
            'CertStatus9' => $store_arr[72],
            'CertIssueDate9' => $store_arr[73],
            'CertExpDate9' => $store_arr[74],
                
            'CertNum10' => $store_arr[75],        
            'CertName10' => $store_arr[76],
            'CertStatus10' => $store_arr[78],
            'CertIssueDate10' => $store_arr[79],
            'CertExpDate10' => $store_arr[80],
            
            'CertNum11' => $store_arr[81],        
            'CertName11' => $store_arr[82],
            'CertStatus11' => $store_arr[84],
            'CertIssueDate11' => $store_arr[85],
            'CertExpDate11' => $store_arr[86],
            
            'CertNum12' => $store_arr[87],        
            'CertName12' => $store_arr[88],
            'CertStatus12' => $store_arr[90],
            'CertIssueDate12' => $store_arr[91],
            'CertExpDate12' => $store_arr[92],
            
    //        'CertNum13' => $store_arr[21],        
    //        'CertName13' => $store_arr[22],
    //        'CertStatus13' => $store_arr[24],
    //        'CertIssueDate13' => $store_arr[25],
    //        'CertExpDate13' => $store_arr[26],
            
    //        'CertNum14' => $store_arr[27],        
    //        'CertName14' => $store_arr[28],
    //        'CertStatus14' => $store_arr[30],
    //        'CertIssueDate14' => $store_arr[31],
    //        'CertExpDate14' => $store_arr[32]
        );

//print_r($store_arr);
//print_r($final_arr); 

        scraperwiki::save(array('PSID'), $final_arr );
    }

    $dom->clear();  
    unset($dom);

} //- end foreach

/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    for($i = 10605; $i <= 300000; $i++) {        
    //for($i = 99000; $i <= 100000; $i++) {        
        $fullUrl = 'https://myoracle.in.gov/reports/rwservlet?acadisepnhtml&report=acadis_person_detail.rdf&p_personid=' . '' . $i . '' . chr(13) . chr(10);
echo $fullUrl ;
        array_push($sources, $fullUrl ); //save url to array
    }
}

?>
