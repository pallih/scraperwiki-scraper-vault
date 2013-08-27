<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 9; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://wiki.open311.org/GeoReport_v2/Servers";

$link_list = get_link_list($url);

//$alldata = $link_list; 
$alldata = array();

$count = 1;
foreach ($link_list as $link) {
    
    //if(!strpos($link['services'], '.gov')) {
    //    continue;
    //}

    
    if ($run_environment == 'prod') {
        get_services($link);
    }
    else {
        $alldata[] = get_services($link);
    }

   $count++;
     if ($run_environment == 'dev' && $count > $max_records) break;

}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_link_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $content = $dom->find("table[class=wikitable]", 0);

    $count = 1;
    $endpoints = array();
    foreach($content->find("tr") as $row){
        
        //Skip first line
        if($count == 1) {
            $count++; 
            continue;    
        }

        $endpoint['jurisdiction']     = ($row->find("td", 0))                 ? trim($row->find("td", 0)->plaintext) : null;
        $endpoint['services']         = ($row->find("td", 6)->find("a", 0))     ? $row->find("td", 6)->find("a", 0)->href : null;    
        $endpoint['base_url']         = ($endpoint['services'])                 ? substr($endpoint['services'], 0, strpos($endpoint['services'], 'services.xml')) : null;

        // Make sure we get the correct URL for discovery
        if ($row->find("td", 4)->find("a", 0)) {
              foreach($row->find("td", 4)->find("a") as $link) {
                
                if(strtolower($link->plaintext) == 'xml') {
                    $endpoint['discovery'] = $link->href;
                }
                
            }
        }
        
        if(empty($endpoint['discovery'])) {
            $endpoint['discovery'] = null;
        }


        $endpoints[] = $endpoint;
        unset($endpoint);
        $count++;
    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $endpoints;

}



function get_services($link) {
    
    global $run_environment;
    global $max_records;

    $services_xml     = curl_data($link['services']);    
    

   // try {
   // 
   //     $dom = new DOMDocument;
   //     $dom->loadXML($services_xml);
   //     $services = simplexml_import_dom($dom);
   // 
   // }
   // catch (Exception $e) {
   //     
   //     $sample = substr($services_xml, 0, 25);
   //     $error = 'XML failed again for ' . $link['services'] . ' Sample: ' . $sample;
   //     throw new Exception( $error, 0, $e);   
   // }


   try {
   
    $services = new SimpleXMLElement($services_xml);

   }
   catch (Exception $e) {
       
       $sample = substr($services_xml, 0, 25);
       $error = 'XML failed for ' . $link['services'] . ' Sample: ' . $sample;
       throw new Exception( $error, 0, $e);   
   }





    // echo $services->service[0]->service_name;

    $services_output = array();

    foreach ($services as $service) {
            
        $service = object_to_array($service);            
            
        $service['endpoint_base'] = $link['base_url'];
        $service['endpoint_name'] = $link['jurisdiction'];  
        $service['discovery']       = $link['discovery'];      
        $service['url']           = $service['endpoint_base'] . 'services/' . $service['service_code'] . '.xml';    
        
        foreach($service as $key => $value) {
            
            if(empty($value)) $value = null;            
            $output[$key] = $value;
            
        }
        
        
        if ($run_environment == 'dev') {
            $services_output[] = $output;            
        } else {
            scraperwiki::save_sqlite(array('endpoint_base', 'service_code'), $output);            
        }

    }
    
    if ($run_environment == 'dev') {    
        return $services_output;
    } else {
        return true;    
    }

   
}



function curl_data($url) {
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $data=curl_exec($ch);
    curl_close($ch);

    return $data;    
}


function object_to_array($obj) {
    if(is_object($obj)) $obj = (array) $obj;
    if(is_array($obj)) {
    $new = array();
    foreach($obj as $key => $val) {
    $new[$key] = object_to_array($val);
    }
    }
    else $new = $obj;
    return $new;
}

function get_between($input, $start, $end)
{
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1));
  return $substr;
}


?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 9; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://wiki.open311.org/GeoReport_v2/Servers";

$link_list = get_link_list($url);

//$alldata = $link_list; 
$alldata = array();

$count = 1;
foreach ($link_list as $link) {
    
    //if(!strpos($link['services'], '.gov')) {
    //    continue;
    //}

    
    if ($run_environment == 'prod') {
        get_services($link);
    }
    else {
        $alldata[] = get_services($link);
    }

   $count++;
     if ($run_environment == 'dev' && $count > $max_records) break;

}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_link_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $content = $dom->find("table[class=wikitable]", 0);

    $count = 1;
    $endpoints = array();
    foreach($content->find("tr") as $row){
        
        //Skip first line
        if($count == 1) {
            $count++; 
            continue;    
        }

        $endpoint['jurisdiction']     = ($row->find("td", 0))                 ? trim($row->find("td", 0)->plaintext) : null;
        $endpoint['services']         = ($row->find("td", 6)->find("a", 0))     ? $row->find("td", 6)->find("a", 0)->href : null;    
        $endpoint['base_url']         = ($endpoint['services'])                 ? substr($endpoint['services'], 0, strpos($endpoint['services'], 'services.xml')) : null;

        // Make sure we get the correct URL for discovery
        if ($row->find("td", 4)->find("a", 0)) {
              foreach($row->find("td", 4)->find("a") as $link) {
                
                if(strtolower($link->plaintext) == 'xml') {
                    $endpoint['discovery'] = $link->href;
                }
                
            }
        }
        
        if(empty($endpoint['discovery'])) {
            $endpoint['discovery'] = null;
        }


        $endpoints[] = $endpoint;
        unset($endpoint);
        $count++;
    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $endpoints;

}



function get_services($link) {
    
    global $run_environment;
    global $max_records;

    $services_xml     = curl_data($link['services']);    
    

   // try {
   // 
   //     $dom = new DOMDocument;
   //     $dom->loadXML($services_xml);
   //     $services = simplexml_import_dom($dom);
   // 
   // }
   // catch (Exception $e) {
   //     
   //     $sample = substr($services_xml, 0, 25);
   //     $error = 'XML failed again for ' . $link['services'] . ' Sample: ' . $sample;
   //     throw new Exception( $error, 0, $e);   
   // }


   try {
   
    $services = new SimpleXMLElement($services_xml);

   }
   catch (Exception $e) {
       
       $sample = substr($services_xml, 0, 25);
       $error = 'XML failed for ' . $link['services'] . ' Sample: ' . $sample;
       throw new Exception( $error, 0, $e);   
   }





    // echo $services->service[0]->service_name;

    $services_output = array();

    foreach ($services as $service) {
            
        $service = object_to_array($service);            
            
        $service['endpoint_base'] = $link['base_url'];
        $service['endpoint_name'] = $link['jurisdiction'];  
        $service['discovery']       = $link['discovery'];      
        $service['url']           = $service['endpoint_base'] . 'services/' . $service['service_code'] . '.xml';    
        
        foreach($service as $key => $value) {
            
            if(empty($value)) $value = null;            
            $output[$key] = $value;
            
        }
        
        
        if ($run_environment == 'dev') {
            $services_output[] = $output;            
        } else {
            scraperwiki::save_sqlite(array('endpoint_base', 'service_code'), $output);            
        }

    }
    
    if ($run_environment == 'dev') {    
        return $services_output;
    } else {
        return true;    
    }

   
}



function curl_data($url) {
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $data=curl_exec($ch);
    curl_close($ch);

    return $data;    
}


function object_to_array($obj) {
    if(is_object($obj)) $obj = (array) $obj;
    if(is_array($obj)) {
    $new = array();
    foreach($obj as $key => $val) {
    $new[$key] = object_to_array($val);
    }
    }
    else $new = $obj;
    return $new;
}

function get_between($input, $start, $end)
{
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1));
  return $substr;
}


?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 9; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);     
    require 'scraperwiki.php';
}

require 'scraperwiki/simple_html_dom.php';


$url = "http://wiki.open311.org/GeoReport_v2/Servers";

$link_list = get_link_list($url);

//$alldata = $link_list; 
$alldata = array();

$count = 1;
foreach ($link_list as $link) {
    
    //if(!strpos($link['services'], '.gov')) {
    //    continue;
    //}

    
    if ($run_environment == 'prod') {
        get_services($link);
    }
    else {
        $alldata[] = get_services($link);
    }

   $count++;
     if ($run_environment == 'dev' && $count > $max_records) break;

}


// if testing
if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($alldata);
}



function get_link_list($url) {
        
    global $run_environment;
    global $max_records;

    $html = scraperWiki::scrape($url);    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $content = $dom->find("table[class=wikitable]", 0);

    $count = 1;
    $endpoints = array();
    foreach($content->find("tr") as $row){
        
        //Skip first line
        if($count == 1) {
            $count++; 
            continue;    
        }

        $endpoint['jurisdiction']     = ($row->find("td", 0))                 ? trim($row->find("td", 0)->plaintext) : null;
        $endpoint['services']         = ($row->find("td", 6)->find("a", 0))     ? $row->find("td", 6)->find("a", 0)->href : null;    
        $endpoint['base_url']         = ($endpoint['services'])                 ? substr($endpoint['services'], 0, strpos($endpoint['services'], 'services.xml')) : null;

        // Make sure we get the correct URL for discovery
        if ($row->find("td", 4)->find("a", 0)) {
              foreach($row->find("td", 4)->find("a") as $link) {
                
                if(strtolower($link->plaintext) == 'xml') {
                    $endpoint['discovery'] = $link->href;
                }
                
            }
        }
        
        if(empty($endpoint['discovery'])) {
            $endpoint['discovery'] = null;
        }


        $endpoints[] = $endpoint;
        unset($endpoint);
        $count++;
    }  

    // Clear memory
    $dom->__destruct();
    $content->__destruct();

     return $endpoints;

}



function get_services($link) {
    
    global $run_environment;
    global $max_records;

    $services_xml     = curl_data($link['services']);    
    

   // try {
   // 
   //     $dom = new DOMDocument;
   //     $dom->loadXML($services_xml);
   //     $services = simplexml_import_dom($dom);
   // 
   // }
   // catch (Exception $e) {
   //     
   //     $sample = substr($services_xml, 0, 25);
   //     $error = 'XML failed again for ' . $link['services'] . ' Sample: ' . $sample;
   //     throw new Exception( $error, 0, $e);   
   // }


   try {
   
    $services = new SimpleXMLElement($services_xml);

   }
   catch (Exception $e) {
       
       $sample = substr($services_xml, 0, 25);
       $error = 'XML failed for ' . $link['services'] . ' Sample: ' . $sample;
       throw new Exception( $error, 0, $e);   
   }





    // echo $services->service[0]->service_name;

    $services_output = array();

    foreach ($services as $service) {
            
        $service = object_to_array($service);            
            
        $service['endpoint_base'] = $link['base_url'];
        $service['endpoint_name'] = $link['jurisdiction'];  
        $service['discovery']       = $link['discovery'];      
        $service['url']           = $service['endpoint_base'] . 'services/' . $service['service_code'] . '.xml';    
        
        foreach($service as $key => $value) {
            
            if(empty($value)) $value = null;            
            $output[$key] = $value;
            
        }
        
        
        if ($run_environment == 'dev') {
            $services_output[] = $output;            
        } else {
            scraperwiki::save_sqlite(array('endpoint_base', 'service_code'), $output);            
        }

    }
    
    if ($run_environment == 'dev') {    
        return $services_output;
    } else {
        return true;    
    }

   
}



function curl_data($url) {
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $data=curl_exec($ch);
    curl_close($ch);

    return $data;    
}


function object_to_array($obj) {
    if(is_object($obj)) $obj = (array) $obj;
    if(is_array($obj)) {
    $new = array();
    foreach($obj as $key => $val) {
    $new[$key] = object_to_array($val);
    }
    }
    else $new = $obj;
    return $new;
}

function get_between($input, $start, $end)
{
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1));
  return $substr;
}


?>