<?php  
for($year_id = 86; $year_id < 115; $year_id++){
    for($make_id = 1; $make_id < 60; $make_id++){
        $html = scraperWiki::scrape("http://www.automd.com/carpicker/get_models?year_id=$year_id&make_id=$make_id&iq=1");           
        //print $html . "\n";
    
        $keith = json_decode($html);
        //var_dump($keith->models);
    
        foreach($keith->models as $array){
            //var_dump($array);
            $data = array('year_id' => $year_id, 'make_id' => $make_id, 'model_id' => $array->model_id, 
                'model_name' => $array->model_name, 'active_model' => $array->active_model);   
            //var_dump($data);
            scraperwiki::save(array('year_id', 'make_id', 'model_id'), $data);  
        }
    }
}
?>
<?php  
for($year_id = 86; $year_id < 115; $year_id++){
    for($make_id = 1; $make_id < 60; $make_id++){
        $html = scraperWiki::scrape("http://www.automd.com/carpicker/get_models?year_id=$year_id&make_id=$make_id&iq=1");           
        //print $html . "\n";
    
        $keith = json_decode($html);
        //var_dump($keith->models);
    
        foreach($keith->models as $array){
            //var_dump($array);
            $data = array('year_id' => $year_id, 'make_id' => $make_id, 'model_id' => $array->model_id, 
                'model_name' => $array->model_name, 'active_model' => $array->active_model);   
            //var_dump($data);
            scraperwiki::save(array('year_id', 'make_id', 'model_id'), $data);  
        }
    }
}
?>
