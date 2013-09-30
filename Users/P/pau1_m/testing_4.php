<?php
# Blank PHP
    $sourcescraper = 'central_scotland_fire_incidents'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    print_r($keys);
    $keyindex = getenv("URLQUERY");
    //print_r($keyindex);
    $all_data = scraperwiki::getData($sourcescraper, $limit=10000); 
    //print_r($all_data);

    $is_malicious = FALSE;

    $results = array();


    $total_malicious = 0;
    $total_incidents = 0;

    foreach ($all_data as $item){
    $total_incidents++;

    $location = $item->location;
    $location = explode(',', $location);
    $location = trim($location[1]);

    

    $regex_malicious = '@malicious@';
    //$regex_false_alarm = '@false alarm@';

    $summary = $item->summary;


    $is_malicious = (preg_match ($regex_malicious , $summary)); //&& preg_match($regex_false_alarm, $summary));

    //$is_malicious = (preg_match ($regex_malicious , $summary) && preg_match($regex_false_alarm, $summary));

    $results[$location]['total']++;
    
    if ($is_malicious){
        $total_malicious++ ;   
        $results[$location]['malicious']++;
     };
};




$graph = array();


//sort out the percentages
foreach ($results as $key => $value){


//if there are malicious fires
    if ($results[$key]['malicious'] == TRUE) {
    
    $results[$key]['percentage'] = (double)(($results[$key]['malicious'] / $results[$key]['total'] ) * 100);

    };


    if ($results[$key]['percentage']){

    $graph[$key] = $results[$key]['percentage'];
 
     }; 


};
    

print_r($graph);

$total_percentage = ($total_malicious / $total_incidents) * 100;

print 'Percentage of malicious across all incindents ' . $total_percentage . '%';






?>  


    </script>        
<?php
# Blank PHP
    $sourcescraper = 'central_scotland_fire_incidents'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    print_r($keys);
    $keyindex = getenv("URLQUERY");
    //print_r($keyindex);
    $all_data = scraperwiki::getData($sourcescraper, $limit=10000); 
    //print_r($all_data);

    $is_malicious = FALSE;

    $results = array();


    $total_malicious = 0;
    $total_incidents = 0;

    foreach ($all_data as $item){
    $total_incidents++;

    $location = $item->location;
    $location = explode(',', $location);
    $location = trim($location[1]);

    

    $regex_malicious = '@malicious@';
    //$regex_false_alarm = '@false alarm@';

    $summary = $item->summary;


    $is_malicious = (preg_match ($regex_malicious , $summary)); //&& preg_match($regex_false_alarm, $summary));

    //$is_malicious = (preg_match ($regex_malicious , $summary) && preg_match($regex_false_alarm, $summary));

    $results[$location]['total']++;
    
    if ($is_malicious){
        $total_malicious++ ;   
        $results[$location]['malicious']++;
     };
};




$graph = array();


//sort out the percentages
foreach ($results as $key => $value){


//if there are malicious fires
    if ($results[$key]['malicious'] == TRUE) {
    
    $results[$key]['percentage'] = (double)(($results[$key]['malicious'] / $results[$key]['total'] ) * 100);

    };


    if ($results[$key]['percentage']){

    $graph[$key] = $results[$key]['percentage'];
 
     }; 


};
    

print_r($graph);

$total_percentage = ($total_malicious / $total_incidents) * 100;

print 'Percentage of malicious across all incindents ' . $total_percentage . '%';






?>  


    </script>        
