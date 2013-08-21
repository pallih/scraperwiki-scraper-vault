<?php
######################################
# Basic PHP scraper
######################################

$max = 159710;

for ($i=1; $i<=$max; $i++) {
    //
$html = scraperwiki::scrape('http://sarki.alternatifim.com/data.asp?ID=13914');


//    $html = scraperwiki::scrape('http://sarki.alternatifim.com/data.asp?ID='.$i);
    $html = oneline($html);

    preg_match_all('|<h1>(.*?)</h1>|',$html,$arr);
    $parts = explode(' - ',$arr[1][0]);

    preg_match_all('|<p id="sarkisozu">(.*?)</p>|',$html,$arr);
    $text = str_replace("<span style='color:#888888;font-size:0.75em'>[ kaynak: http://sarki.alternatifim.com/goster.asp?ac=".$i." ]</span>",'',$arr[1][0]);



if (trim($parts[0])!='' && trim($parts[1]) != '') {

    scraperwiki::save(array('id'), array('id' => "".$i,'artist' => clean($parts[0]),
                                             'song' => clean($parts[1]),'lyrics' =>addslashes($text)));    
   }
exit;
}

  

function clean($val) {
        $val = str_replace('&nbsp;',' ',$val);
        $val = str_replace('&amp;','&',$val);
        $val = html_entity_decode($val);
        $val = strip_tags($val);
        $val = trim($val);
        $val = utf8_decode($val);
        return($val);
    }
    
    function oneline($code) {
        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);
        return $code;
    }

?>