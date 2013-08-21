<?php  
require 'scraperwiki/simple_html_dom.php';   

//scraperwiki::attach("rp_models", "src");            
//foreach(scraperwiki::select("* from src.swdata") as $car_type_array){
    //print_r($car_type_array['car_type_id']);
 
    //$car_type_id = $car_type_array['car_type_id'];
    //$html = scraperWiki::scrape("http://repairpal.com/estimator/";

  
    $cmd = 'curl "http://repairpal.com/estimator/results" -H "Cookie: uid=CnrDzFE+W0k0ckaZBWluAg==; __gads=ID=2fefb8788247fd0d:T=1363041223:S=ALNI_MbEELB_ADvDJgUXe38_LBqJENWY0w; __g_c=a%3A0%7Cb%3A2%7Cc%3A180889854511767%7Cd%3A4%7Ce%3A0.04%7Cf%3A1%7Ch%3A0; __g_u=180889854511767_4_0.04_1_5_1365889162653_0; _rp_produ_v2=BAh7CkkiD3Nlc3Npb25faWQGOgZFRkkiJWY0N2NhN2M5MTcwZDFiYWYwNGE0OGQyNjhhMWVlMjhmBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUFWc1Z1djNNVnhyMXRiYzlLVU9UQWtJT2kyK1I2SEdsbUpLS21VVXFRQVU9BjsARkkiFWFkZHJlc3NhYmxlX3VzZXIGOwBGewc6DWZyb21femlwVDoKdmFsdWVJIgx0b3BzaG9wBjsARkkiG3NlcnZpY2VfZXN0aW1hdG9yX2Zvcm0GOwBGew06EGNhcl90eXBlX2lkaQLcEToRY2FyX2JyYW5kX2lkaSk6EWNhcl9tb2RlbF9pZGkCRgI6DWNhcl95ZWFyaQLWBzoNemlwX2NvZGVJIhYxOTA2MyAtIE1lZGlhLCBQQQY7AFQ6FWNhcl90cmltX3R5cGVfaWRpAkkEOhRzZXJ2aWNlX3R5cGVfaWRpZToQdGlyZV9vcHRpb25JIgAGOwBUSSIaZGlyZWN0b3J5X3NlYXJjaF9mb3JtBjsARnsJOgxzb3J0X2J5Og5yZWxldmFuY2U6DWRpc3RhbmNlaQ86DGFkZHJlc3NJIhYxOTA2MyAtIE1lZGlhLCBQQQY7AFQ6FGNhcl9icmFuZF9uYW1lc0kiC1RveW90YQY7AFQ%3D--178a9298b2776209878172c67d59a5871d21394e; ab=A; __utma=48183460.1025026868.1363041151.1365182624.1365457163.6; __utmb=48183460.2.10.1365457163; __utmc=48183460; __utmz=48183460.1363041151.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=48183460.|4=TestGroup=A=1" -H "Origin: http://repairpal.com" -H "Accept-Encoding: gzip,deflate,sdch" -H "Host: repairpal.com" -H "Accept-Language: en-US,en;q=0.8" -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31" -H "Content-Type: application/x-www-form-urlencoded" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" -H "Cache-Control: max-age=0" -H "Referer: http://repairpal.com/estimator" -H "Connection: keep-alive" -H "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3" --data "utf8=%E2%9C%93&authenticity_token=AVsVuv3MVxr1tbc9KUOTAkIOi2%2BR6HGlmJKKmUUqQAU%3D&service_estimator_form%5Bcar_brand_id%5D=36&service_estimator_form%5Bcar_year%5D=2006&service_estimator_form%5Bcar_model_id%5D=582&service_estimator_form%5Bcar_type_id%5D=4572&car_slug=toyota-highlander-2006&service_estimator_form%5Bzip_code%5D=19063&service_estimator_form%5Bservice_type%5D=Thermostat+Replacement+-+3.3L+V6&service_estimator_form%5Bservice_type_id%5D=96&service_estimator_form%5Bcar_trim_type_id%5D=1097&service_estimator_form%5Btire_option%5D="';
    exec($cmd,$html);
    var_dump($html);
     
    /*$dom = new simple_html_dom();
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
}*/
?>
