<?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperWiki::scrape("http://pastipas.pertamina.com/lokasi.asp?pastipas=oke&propinsi=9999");

$dom->load($html);
$root = $dom->find("td.padlokasi");
$data = array();
foreach($root[4]->children as $child){
    $text = $child->plaintext;
    if(strpos($text,"Propinsi")!==false){
        $propinsi = trim(str_replace("Propinsi : ","",$text));
    }else if(strpos($text,"Kota") === 0){
        $kota = trim(str_replace("Kota : ","",$text));
    }else if($child->class=="link"){
        $ret = preg_split("/,/",$text);
        $no_spbu = trim($ret[0]);
        $text = str_replace($no_spbu,"",$text);

        $ret = preg_split("/\(/",$text);        
        $alamat = trim(str_replace(",","",$ret[0]));
        $alamat = str_replace("Jl ","",$alamat);
        $ref_gedung = trim(str_replace(")","",$ret[1]));
        $data[] = array("no_spbu"=>$no_spbu,
                        "propinsi"=>$propinsi,
                        "kota"=>$kota,"no_spbu"=>$no_spbu,
                        "alamat"=>utf8_encode($alamat),
                        "ref_gedung"=>utf8_encode($ref_gedung));
        
/*        $message = scraperwiki::save_sqlite(array("no_spbu"),            
                array("no_spbu"=>$no_spbu,
                        "propinsi"=>$propinsi,
                        "kota"=>$kota,"no_spbu"=>$no_spbu,
                        "alamat"=>utf8_encode($alamat),
                        "ref_gedung"=>utf8_encode($ref_gedung)
                    ));  */

    }
}


for($i=0;$i<count($data);$i++){
    /*$start =50;
    $stop = 150;
    if($i==$stop){
        break;
    }else if($i<$start){
        continue;
    }*/
        
    $item = $data[$i];
    $alamat = str_replace("-","",$item['alamat']);
    $kota = $item['kota'];
    $propinsi = $item['propinsi'];
    $address = urlencode("$alamat,$kota,$propinsi,indonesia");
    $address = str_replace("%C2","",$address);
    $address = str_replace("%96","",$address);
    $url = "http://maps.googleapis.com/maps/api/geocode/json?address=$address&sensor=false";

    $request = scraperWiki::scrape($url);
    $json = json_decode($request);

    //skip if geocode request fail
    if($json->status != "OK"){
        print "not ok \n";
    }else{
        print "ok \n";
        $latitude = $json->results[0]->geometry->location->lat;
        $longitude = $json->results[0]->geometry->location->lng;   
        $message = scraperwiki::save_sqlite(array("alamat"),            
                array("no_spbu"=>$item['no_spbu'],
                        "propinsi"=>$propinsi,
                        "kota"=>$kota,
                        "alamat"=>utf8_encode($alamat),
                        "ref_gedung"=>utf8_encode($ref_gedung),
                        "latitude"=>$latitude,
                        "longitude"=>$longitude,
                    ));
    }
}
?><?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperWiki::scrape("http://pastipas.pertamina.com/lokasi.asp?pastipas=oke&propinsi=9999");

$dom->load($html);
$root = $dom->find("td.padlokasi");
$data = array();
foreach($root[4]->children as $child){
    $text = $child->plaintext;
    if(strpos($text,"Propinsi")!==false){
        $propinsi = trim(str_replace("Propinsi : ","",$text));
    }else if(strpos($text,"Kota") === 0){
        $kota = trim(str_replace("Kota : ","",$text));
    }else if($child->class=="link"){
        $ret = preg_split("/,/",$text);
        $no_spbu = trim($ret[0]);
        $text = str_replace($no_spbu,"",$text);

        $ret = preg_split("/\(/",$text);        
        $alamat = trim(str_replace(",","",$ret[0]));
        $alamat = str_replace("Jl ","",$alamat);
        $ref_gedung = trim(str_replace(")","",$ret[1]));
        $data[] = array("no_spbu"=>$no_spbu,
                        "propinsi"=>$propinsi,
                        "kota"=>$kota,"no_spbu"=>$no_spbu,
                        "alamat"=>utf8_encode($alamat),
                        "ref_gedung"=>utf8_encode($ref_gedung));
        
/*        $message = scraperwiki::save_sqlite(array("no_spbu"),            
                array("no_spbu"=>$no_spbu,
                        "propinsi"=>$propinsi,
                        "kota"=>$kota,"no_spbu"=>$no_spbu,
                        "alamat"=>utf8_encode($alamat),
                        "ref_gedung"=>utf8_encode($ref_gedung)
                    ));  */

    }
}


for($i=0;$i<count($data);$i++){
    /*$start =50;
    $stop = 150;
    if($i==$stop){
        break;
    }else if($i<$start){
        continue;
    }*/
        
    $item = $data[$i];
    $alamat = str_replace("-","",$item['alamat']);
    $kota = $item['kota'];
    $propinsi = $item['propinsi'];
    $address = urlencode("$alamat,$kota,$propinsi,indonesia");
    $address = str_replace("%C2","",$address);
    $address = str_replace("%96","",$address);
    $url = "http://maps.googleapis.com/maps/api/geocode/json?address=$address&sensor=false";

    $request = scraperWiki::scrape($url);
    $json = json_decode($request);

    //skip if geocode request fail
    if($json->status != "OK"){
        print "not ok \n";
    }else{
        print "ok \n";
        $latitude = $json->results[0]->geometry->location->lat;
        $longitude = $json->results[0]->geometry->location->lng;   
        $message = scraperwiki::save_sqlite(array("alamat"),            
                array("no_spbu"=>$item['no_spbu'],
                        "propinsi"=>$propinsi,
                        "kota"=>$kota,
                        "alamat"=>utf8_encode($alamat),
                        "ref_gedung"=>utf8_encode($ref_gedung),
                        "latitude"=>$latitude,
                        "longitude"=>$longitude,
                    ));
    }
}
?>