<?php  
$makes = array("26"=>"Acura", "33"=>"Audi", "9"=>"BMW", "16"=>"Buick", "17"=>"Cadillac", "18"=>"Chevrolet",
    "11"=>"Chrysler", "12"=>"Dodge", "44"=>"FIAT", "23"=>"Ford", "19"=>"GMC", "20"=>"Geo", "27"=>"Honda",
    "42"=>"Hummer", "3"=>"Hyundai", "31"=>"Infiniti", "10"=>"Isuzu", "7"=>"Jaguar", "14"=>"Jeep", "39"=>"Kia", 
    "4"=>"Land Rover", "35"=>"Lexus", "24"=>"Lincoln", "37"=>"Mazda", "28"=>"Mercedes-Benz", "25"=>"Mercury",
    "41"=>"Mini", "32"=>"Mitsubishi", "30"=>"Nissan", "21"=>"Oldsmobile", "15"=>"Plymouth", "22"=>"Pontiac", 
    "2"=>"Porsche", "46"=>"Ram","29"=>"Saab", "38"=>"Saturn", "43"=>"Scion","45"=>"Smart", "5"=>"Subaru",
    "1"=>"Suzuki", "36"=>"Toyota", "34"=>"Volkswagen", "8"=>"Volvo");

$year_id = 2013;

while($year_id > 1985){
    foreach($makes as $num => $make){
        //print "http://repairpal.com/car_chooser/models_for_year.json?car_year=$year_id&car_brand_id=$num\n";
        $html = scraperWiki::scrape("http://repairpal.com/car_chooser/models_for_year.json?car_year=$year_id&car_brand_id=$num");           
        //print $html . "\n";
        
        if($html != null){ 
            $models = json_decode($html);
            //var_dump($models);

            if($models != null){ 
                //var_dump($models);
    
                foreach($models as $model){
                    //print $year_id . "," . $array->make_id . "," . $array->make_name . "," . $array->active_make . "\n";
                    //var_dump($model);
                    //{"car_model_id":237,"name":"4Runner","car_type_id":5113,"slug":"toyota-4runner-2007"}        
                    $data = array('year'=> $year_id, 'make' => $num, 'make_name' => $make, 'car_model_id' => $model->car_model_id, 'name' => $model->name, 
                        'car_type_id' => $model->car_type_id);   
                    //var_dump($data);
                    scraperwiki::save(array('year', 'make', 'make_name', 'car_model_id', 'car_type_id'), $data);  
                } 
            }
        }
    }
    $year_id--;
}
?>
