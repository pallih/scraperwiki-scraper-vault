<?php  
$year_id = 114;

while($year_id > 85){
    $html = scraperWiki::scrape("http://www.automd.com/carpicker/get_makes?year_id=$year_id");           
    //print $html . "\n";

    $keith = json_decode($html);
    //var_dump($keith->make_years);

    foreach($keith->make_years as $array){
        //print $year_id . "," . $array->make_id . "," . $array->make_name . "," . $array->active_make . "\n";
        //var_dump($array);
        $data = array('year_id' => $year_id, 'make_id' => $array->make_id, 
            'make_name ' => $array->make_name , 'active_make ' => $array->active_make);   
        //var_dump($data);
        scraperwiki::save(array('year_id', 'make_id'), $data);  
    }
    $year_id--;
}
?>
