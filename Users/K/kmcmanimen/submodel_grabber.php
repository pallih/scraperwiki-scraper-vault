<?php  
for($year_id = 86; $year_id < 115; $year_id++){
    for($make_id = 1; $make_id < 60; $make_id++){
        for($model_id=0; $model_id < 1000; $model_id++){
            $html = scraperWiki::scrape("http://www.automd.com/carpicker/get_submodels?year_id=107&make_id=7&model_id=$model_id&iq=1");           
            //print $html . "\n";
        
            $keith = json_decode($html);
            //var_dump($keith->models);
        
            foreach($keith->submodels as $array){
                //var_dump($array);
                $data = array('year_id' => $year_id, 'make_id' => $make_id, 'model_id' => $model_id, 
                    'submodel_id' => $array->submodel_id, 'submodel_name' => $array->submodel_name);   
                //var_dump($data);
                scraperwiki::save(array('year_id', 'make_id', 'model_id', 'submodel_id'), $data);  
            }
        }
    }
}
?>
<?php  
for($year_id = 86; $year_id < 115; $year_id++){
    for($make_id = 1; $make_id < 60; $make_id++){
        for($model_id=0; $model_id < 1000; $model_id++){
            $html = scraperWiki::scrape("http://www.automd.com/carpicker/get_submodels?year_id=107&make_id=7&model_id=$model_id&iq=1");           
            //print $html . "\n";
        
            $keith = json_decode($html);
            //var_dump($keith->models);
        
            foreach($keith->submodels as $array){
                //var_dump($array);
                $data = array('year_id' => $year_id, 'make_id' => $make_id, 'model_id' => $model_id, 
                    'submodel_id' => $array->submodel_id, 'submodel_name' => $array->submodel_name);   
                //var_dump($data);
                scraperwiki::save(array('year_id', 'make_id', 'model_id', 'submodel_id'), $data);  
            }
        }
    }
}
?>
