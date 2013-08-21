<?php
require 'scraperwiki/simple_html_dom.php';

function get_http_response_code($url) {
    $headers = get_headers($url);
    return substr($headers[0], 9, 3);
}


$pattern=Array("/ä/","/ö/","/ü/","/Ä/","/Ö/","/Ü/","/ß/","/ /");
$replace=Array("ae","oe","ue","Ae","Oe","Ue","ss","");


$i=0;
$ortsteile=array();
$indexarray=array("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T","U","V","W","XYZ");
//$indexarray=array("B");
foreach ($indexarray as $index) {
    echo $index;
    $html = scraperWiki::scrape("http://www.unterfranken-in-zahlen.de/uiz-aktuell/01/010701-".$index.".htm");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('td[colspan=4]') as $row) {
        $ots=$row->plaintext;
        $ot=explode(",",$ots);
        foreach ($ot as $o) {
            $original=$o;
            $ot_words=Array();
            $words=explode(" ",trim($o));
            foreach ($words as $w) {
                if (!strpos($w,".")) $ot_words[]=trim($w);
            }
            $o=implode(" ",$ot_words);
            $ot_trans=preg_replace($pattern,$replace,$o);
            if(get_http_response_code("http://graph.facebook.com/".$ot_trans)!="404"){
  
                $json_fb = file_get_contents("http://graph.facebook.com/".$ot_trans);
                $json=json_decode($json_fb);
                if ($json->first_name==true) $json=false; 
            } else {
                $json=false;
            }
//print_r($json);            
           if ($json) { $record=array("id" => $i, "name" => utf8_encode($o), "name_trans" => utf8_encode($ot_trans),"name_original" => utf8_encode($original), "fb_link" => $json->link, "website" => $json->website, "about" => $json->about, "likes" => $json->likes);
             scraperwiki::save(array('id'),$record);
}
            $i++;
        
        }
    }
}


?>
