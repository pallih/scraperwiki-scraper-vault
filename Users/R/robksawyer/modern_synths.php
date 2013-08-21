<?php
//This scraper holds modern synths.

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

$modernSynthData = file_get_contents("https://docs.google.com/spreadsheet/pub?hl=en_US&hl=en_US&key=0Aht1e-sbjyvPdHJmaUIzTEctZl8tc2tVWjdjYnFpOGc&single=true&gid=0&output=csv"); 
$modernSynthData = csv_to_array($modernSynthData);
//print_r($modernSynthData);

$synths = array();
$counter = 0;
foreach($modernSynthData as $synth){
    if(!empty($synth)){
        $synths[$counter]['manufacturer'] = $synth['Manufacturer'];
        $synths[$counter]['name'] = $synth['Synth Name'];
        $synths[$counter]['url'] = $synth['Source URL'];
        $synths[$counter]['images'] = $synth['Images'];
        $counter++;
    }
}

print_r($synths);

if(!empty($synths)){
    scraperwiki::save_var('total_results', count($synths));           
    print scraperWiki::get_var('total_results');
    
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url','images'), $synths);
    print strval($saveMessage);
}else{
    $info = scraperwiki::table_info($name="swdata");
    if(!empty($info)){
        scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
    }
}

// 
// Convert csv file to associative array: 
// 

function csv_to_array($input, $delimiter=',') { 
    $header = null; 
    $data = array(); 
    $csvData = str_getcsv($input, "\n"); 
    
    foreach($csvData as $csvLine){ 
        if(is_null($header)) $header = explode($delimiter, $csvLine); 
        else{ 
            
            $items = explode($delimiter, $csvLine); 
            
            for($n = 0, $m = count($header); $n < $m; $n++){ 
                $prepareData[$header[$n]] = $items[$n]; 
            } 
            
            $data[] = $prepareData; 
        } 
    } 
    
    return $data; 
} 

?>
