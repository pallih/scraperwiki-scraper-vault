<?php  
require 'scraperwiki/simple_html_dom.php';   

scraperwiki::attach("rp_models", "src");            
foreach(scraperwiki::select("* from src.swdata") as $car_type_array){
    //print_r($car_type_array['car_type_id']);
 
    $car_type_id = $car_type_array['car_type_id'];
    $html = scraperWiki::scrape("http://repairpal.com/estimator/ajax_load_service_types_list?car_type_id=$car_type_id "); 
    //print $html . "\n";
     
    $dom = new simple_html_dom();
    $dom->load($html); 
    $previous_car;
    //<a href="#" class="service_type_item" data-keywords="5,000 mile service" data-service="145">5,000 Mile Service</a>
    $tds = $dom->find("td[@class='service_list_block_column']");
    //print "tds count = " . count($tds) . "\n";
    foreach($tds as $td_single){
        $as = $td_single->find("a");
        //print "as count = " . count($as) . "\n";
        foreach($as as $a_single){
    
            $x = new SimpleXMLElement($a_single);
            //var_dump($x);
    
            $service = array();
            $service['car_type_id'] = $car_type_id;
            $service['car_trim_type'] = "";
            foreach($x->attributes() as $a => $b){
                if($a == "data-cartrimtype"){
                    $service['id'] = $previous_car;
                    $service['car_trim_type'] = (string)$b;
                    $service['name'] = (string)$x;
                }
                if($a == "data-keywords") $service['name'] = (string)$b;
                if($a == "data-service"){
                    $service['id'] = (string)$b;
                    $previous_car = (string)$b;
                }
                //print $a . " = " . $b . "\n";
            }
            //print "name = ". $service['name'] . ", id = " . $service['id'] . "\n";
            //var_dump($service);
            scraperwiki::save(array('car_type_id', 'name', 'id', 'car_trim_type'), $service);  
        }
    }
}
?>
<?php  
require 'scraperwiki/simple_html_dom.php';   

scraperwiki::attach("rp_models", "src");            
foreach(scraperwiki::select("* from src.swdata") as $car_type_array){
    //print_r($car_type_array['car_type_id']);
 
    $car_type_id = $car_type_array['car_type_id'];
    $html = scraperWiki::scrape("http://repairpal.com/estimator/ajax_load_service_types_list?car_type_id=$car_type_id "); 
    //print $html . "\n";
     
    $dom = new simple_html_dom();
    $dom->load($html); 
    $previous_car;
    //<a href="#" class="service_type_item" data-keywords="5,000 mile service" data-service="145">5,000 Mile Service</a>
    $tds = $dom->find("td[@class='service_list_block_column']");
    //print "tds count = " . count($tds) . "\n";
    foreach($tds as $td_single){
        $as = $td_single->find("a");
        //print "as count = " . count($as) . "\n";
        foreach($as as $a_single){
    
            $x = new SimpleXMLElement($a_single);
            //var_dump($x);
    
            $service = array();
            $service['car_type_id'] = $car_type_id;
            $service['car_trim_type'] = "";
            foreach($x->attributes() as $a => $b){
                if($a == "data-cartrimtype"){
                    $service['id'] = $previous_car;
                    $service['car_trim_type'] = (string)$b;
                    $service['name'] = (string)$x;
                }
                if($a == "data-keywords") $service['name'] = (string)$b;
                if($a == "data-service"){
                    $service['id'] = (string)$b;
                    $previous_car = (string)$b;
                }
                //print $a . " = " . $b . "\n";
            }
            //print "name = ". $service['name'] . ", id = " . $service['id'] . "\n";
            //var_dump($service);
            scraperwiki::save(array('car_type_id', 'name', 'id', 'car_trim_type'), $service);  
        }
    }
}
?>
