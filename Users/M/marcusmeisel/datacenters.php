<?php

$html = scraperWiki::scrape("http://www.datacentermap.com/datacenters.html");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[class='lefttext'] div[class] a") as $data){ 
    $bs = $data->find("b");
    if(count($bs)==1){
        $input = $bs[0]->plaintext;
        $country = substr($input,0,strpos($input,' ('));
        $countryhtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/");
        $countrydom = new simple_html_dom();
        $countrydom->load($countryhtml);
        foreach($countrydom->find("div[class='lefttext'] div[class] a") as $countrydata){
            $bbs = $countrydata->find("b");
            if(count($bbs)==1){
                $countryinput = $bbs[0]->plaintext;
                //print "countryinput: ".$countryinput." ";
                $area = substr($countryinput,0,strpos($countryinput,' ('));
                if (strtolower($country)=='usa'){
                    $areahtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($area)."/");
                    $areadom = new simple_html_dom();
                    $areadom->load($areahtml);
                    $address=$area.', '.$country;
                    foreach($detailareadom->find("div[class='lefttext'] div[class~='DCColumn'] a[title]") as $detailareadata){
                        $datacenter = $detailareadata->plaintext;                        
                        $datacenterurl = $detailareadata->href;
                        $datacenterhtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($detailarea)."/".strtolower($datacenterurl));
                        $datacenterdom = new simple_html_dom();
                        $datacenterdom->load($datacenterhtml);
                        if (strcmp($detailarea,$area)!=0){
                            $address=$detailarea.', '.$address;
                        }
                        $datacenterstreet=" ";
                        $datacentercity=" ";
                        $datacenterpostal=" ";
                        foreach($datacenterdom->find("div[class='adr']") as $datacenterdata){                                                                                   
                            $dc = $datacenterdata->find("span[class='locality']");
                            if (count($dc)==1){
                                $datacentercity = $dc[0]->innertext;
                                if (strcmp($datacentercity,$detailarea)!=0){
                                    $address=$datacentercity.', '.$address;
                                }
                            }
                            $dc = $datacenterdata->find("span[class='postal-code']");
                            if (count($dc)==1){
                                $datacenterpostal = $dc[0]->innertext;
                                $address=$datacenterpostal.', '.$address;
                            }
                            $dc = $datacenterdata->find("div[class='street-address']");
                            if (count($dc)==1){
                                $datacenterstreet = $dc[0]->innertext;
                                $address=$datacenterstreet.', '.$address;
                            }
                        }
                        $locationarray = lookup(utf8_encode($address));
                        $record = array(
                            'country' => utf8_encode($country),
                            'area' => utf8_encode($area),
                            'detailarea' => utf8_encode($detailarea),
                            'datacenterCity' => utf8_encode($datacentercity),
                            'datacenterName' => utf8_encode($datacenter),
                            'postal-code' => utf8_encode($datacenterpostal),                                     
                            'street-address' => utf8_encode($datacenterstreet),
                            'latitude' => $locationarray['lat'],
                            'longitude' => $locationarray['long'],
                            'accuracy' => utf8_encode($locationarray['location_type']),
                        );
                        scraperwiki::save(array('country','area','detailarea','datacenterCity','datacenterName','postal-code','street-address','latitude','longitude','accuracy'), $record);
                    }
                }
                else {            
                    $detailarea=$area;
                    //print "datacenter: ".$datacenter.(strpos($countryinput,'(')+1)."-".(substr($countryinput, (strpos($countryinput,'(')+1),-1))." :";
                    $amount = intval(substr($countryinput, (strpos($countryinput,'(')+1),-1));
                    $detailareahtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($detailarea)."/");
                    $detailareadom = new simple_html_dom();
                    $detailareadom->load($detailareahtml);
                    foreach($detailareadom->find("div[class='lefttext'] div[class~='DCColumn'] a[title]") as $detailareadata){
                        $datacenter = $detailareadata->plaintext;                        
                        $datacenterurl = $detailareadata->href;
                        $datacenterhtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($detailarea)."/".strtolower($datacenterurl));
                        $datacenterdom = new simple_html_dom();
                        $datacenterdom->load($datacenterhtml);
                        $address=$area.', '.$country;
                        $datacenterstreet=" ";
                        $datacentercity=" ";
                        $datacenterpostal=" ";
                        foreach($datacenterdom->find("div[class='adr']") as $datacenterdata){                                                                                   
                            $dc = $datacenterdata->find("span[class='locality']");
                            if (count($dc)==1){
                                $datacentercity = $dc[0]->innertext;
                                if (strcmp($datacentercity,$detailarea)!=0){
                                    $address=$datacentercity.', '.$address;
                                }
                            }
                            $dc = $datacenterdata->find("span[class='postal-code']");
                            if (count($dc)==1){
                                $datacenterpostal = $dc[0]->innertext;
                                $address=$datacenterpostal.', '.$address;
                            }
                            $dc = $datacenterdata->find("div[class='street-address']");
                            if (count($dc)==1){
                                $datacenterstreet = $dc[0]->innertext;
                                $address=$datacenterstreet.', '.$address;
                            }
                        }
                        $locationarray = lookup(utf8_encode($address));
                        $record = array(
                            'country' => utf8_encode($country),
                            'area' => utf8_encode($area),
                            'detailarea' => utf8_encode($detailarea),
                            'datacenterCity' => utf8_encode($datacentercity),
                            'datacenterName' => utf8_encode($datacenter),
                            'postal-code' => utf8_encode($datacenterpostal),                                     
                            'street-address' => utf8_encode($datacenterstreet),
                            'latitude' => $locationarray['lat'],
                            'longitude' => $locationarray['long'],
                            'accuracy' => utf8_encode($locationarray['location_type'])
                        );
                        //print json_encode($record) . "\n";
                        scraperwiki::save(array('country','area','detailarea','datacenterCity','datacenterName','postal-code','street-address','latitude','longitude','accuracy'), $record);
                    }
                }
            }
        }
    }
}


function lookup($string){
 
   $string = str_replace (" ", "+", urlencode($string));
   $details_url = "http://maps.googleapis.com/maps/api/geocode/json?address=".$string."&sensor=false";
 
   $ch = curl_init();
   curl_setopt($ch, CURLOPT_URL, $details_url);
   curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
   $response = json_decode(curl_exec($ch), true);
 
   // If Status Code is ZERO_RESULTS, OVER_QUERY_LIMIT, REQUEST_DENIED or INVALID_REQUEST
   if ($response['status'] != 'OK') {
    return null;
   }
 
   //print_r($response);
   $geometry = $response['results'][0]['geometry'];
 
    //$longitude = $geometry['location']['lng'];
    //$latitude = $geometry['location']['lat'];
 
    $array = array(
        'lat' => $geometry['location']['lat'],
        'long' => $geometry['location']['lng'],
        'location_type' => $geometry['location_type'],
    );
 
    return $array;
 
}
?>

<?php

$html = scraperWiki::scrape("http://www.datacentermap.com/datacenters.html");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[class='lefttext'] div[class] a") as $data){ 
    $bs = $data->find("b");
    if(count($bs)==1){
        $input = $bs[0]->plaintext;
        $country = substr($input,0,strpos($input,' ('));
        $countryhtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/");
        $countrydom = new simple_html_dom();
        $countrydom->load($countryhtml);
        foreach($countrydom->find("div[class='lefttext'] div[class] a") as $countrydata){
            $bbs = $countrydata->find("b");
            if(count($bbs)==1){
                $countryinput = $bbs[0]->plaintext;
                //print "countryinput: ".$countryinput." ";
                $area = substr($countryinput,0,strpos($countryinput,' ('));
                if (strtolower($country)=='usa'){
                    $areahtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($area)."/");
                    $areadom = new simple_html_dom();
                    $areadom->load($areahtml);
                    $address=$area.', '.$country;
                    foreach($detailareadom->find("div[class='lefttext'] div[class~='DCColumn'] a[title]") as $detailareadata){
                        $datacenter = $detailareadata->plaintext;                        
                        $datacenterurl = $detailareadata->href;
                        $datacenterhtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($detailarea)."/".strtolower($datacenterurl));
                        $datacenterdom = new simple_html_dom();
                        $datacenterdom->load($datacenterhtml);
                        if (strcmp($detailarea,$area)!=0){
                            $address=$detailarea.', '.$address;
                        }
                        $datacenterstreet=" ";
                        $datacentercity=" ";
                        $datacenterpostal=" ";
                        foreach($datacenterdom->find("div[class='adr']") as $datacenterdata){                                                                                   
                            $dc = $datacenterdata->find("span[class='locality']");
                            if (count($dc)==1){
                                $datacentercity = $dc[0]->innertext;
                                if (strcmp($datacentercity,$detailarea)!=0){
                                    $address=$datacentercity.', '.$address;
                                }
                            }
                            $dc = $datacenterdata->find("span[class='postal-code']");
                            if (count($dc)==1){
                                $datacenterpostal = $dc[0]->innertext;
                                $address=$datacenterpostal.', '.$address;
                            }
                            $dc = $datacenterdata->find("div[class='street-address']");
                            if (count($dc)==1){
                                $datacenterstreet = $dc[0]->innertext;
                                $address=$datacenterstreet.', '.$address;
                            }
                        }
                        $locationarray = lookup(utf8_encode($address));
                        $record = array(
                            'country' => utf8_encode($country),
                            'area' => utf8_encode($area),
                            'detailarea' => utf8_encode($detailarea),
                            'datacenterCity' => utf8_encode($datacentercity),
                            'datacenterName' => utf8_encode($datacenter),
                            'postal-code' => utf8_encode($datacenterpostal),                                     
                            'street-address' => utf8_encode($datacenterstreet),
                            'latitude' => $locationarray['lat'],
                            'longitude' => $locationarray['long'],
                            'accuracy' => utf8_encode($locationarray['location_type']),
                        );
                        scraperwiki::save(array('country','area','detailarea','datacenterCity','datacenterName','postal-code','street-address','latitude','longitude','accuracy'), $record);
                    }
                }
                else {            
                    $detailarea=$area;
                    //print "datacenter: ".$datacenter.(strpos($countryinput,'(')+1)."-".(substr($countryinput, (strpos($countryinput,'(')+1),-1))." :";
                    $amount = intval(substr($countryinput, (strpos($countryinput,'(')+1),-1));
                    $detailareahtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($detailarea)."/");
                    $detailareadom = new simple_html_dom();
                    $detailareadom->load($detailareahtml);
                    foreach($detailareadom->find("div[class='lefttext'] div[class~='DCColumn'] a[title]") as $detailareadata){
                        $datacenter = $detailareadata->plaintext;                        
                        $datacenterurl = $detailareadata->href;
                        $datacenterhtml = scraperWiki::scrape("http://www.datacentermap.com/".strtolower($country)."/".strtolower($detailarea)."/".strtolower($datacenterurl));
                        $datacenterdom = new simple_html_dom();
                        $datacenterdom->load($datacenterhtml);
                        $address=$area.', '.$country;
                        $datacenterstreet=" ";
                        $datacentercity=" ";
                        $datacenterpostal=" ";
                        foreach($datacenterdom->find("div[class='adr']") as $datacenterdata){                                                                                   
                            $dc = $datacenterdata->find("span[class='locality']");
                            if (count($dc)==1){
                                $datacentercity = $dc[0]->innertext;
                                if (strcmp($datacentercity,$detailarea)!=0){
                                    $address=$datacentercity.', '.$address;
                                }
                            }
                            $dc = $datacenterdata->find("span[class='postal-code']");
                            if (count($dc)==1){
                                $datacenterpostal = $dc[0]->innertext;
                                $address=$datacenterpostal.', '.$address;
                            }
                            $dc = $datacenterdata->find("div[class='street-address']");
                            if (count($dc)==1){
                                $datacenterstreet = $dc[0]->innertext;
                                $address=$datacenterstreet.', '.$address;
                            }
                        }
                        $locationarray = lookup(utf8_encode($address));
                        $record = array(
                            'country' => utf8_encode($country),
                            'area' => utf8_encode($area),
                            'detailarea' => utf8_encode($detailarea),
                            'datacenterCity' => utf8_encode($datacentercity),
                            'datacenterName' => utf8_encode($datacenter),
                            'postal-code' => utf8_encode($datacenterpostal),                                     
                            'street-address' => utf8_encode($datacenterstreet),
                            'latitude' => $locationarray['lat'],
                            'longitude' => $locationarray['long'],
                            'accuracy' => utf8_encode($locationarray['location_type'])
                        );
                        //print json_encode($record) . "\n";
                        scraperwiki::save(array('country','area','detailarea','datacenterCity','datacenterName','postal-code','street-address','latitude','longitude','accuracy'), $record);
                    }
                }
            }
        }
    }
}


function lookup($string){
 
   $string = str_replace (" ", "+", urlencode($string));
   $details_url = "http://maps.googleapis.com/maps/api/geocode/json?address=".$string."&sensor=false";
 
   $ch = curl_init();
   curl_setopt($ch, CURLOPT_URL, $details_url);
   curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
   $response = json_decode(curl_exec($ch), true);
 
   // If Status Code is ZERO_RESULTS, OVER_QUERY_LIMIT, REQUEST_DENIED or INVALID_REQUEST
   if ($response['status'] != 'OK') {
    return null;
   }
 
   //print_r($response);
   $geometry = $response['results'][0]['geometry'];
 
    //$longitude = $geometry['location']['lng'];
    //$latitude = $geometry['location']['lat'];
 
    $array = array(
        'lat' => $geometry['location']['lat'],
        'long' => $geometry['location']['lng'],
        'location_type' => $geometry['location_type'],
    );
 
    return $array;
 
}
?>

