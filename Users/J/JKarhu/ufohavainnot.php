<?php

require 'scraperwiki/simple_html_dom.php';
$stmp = date('l jS \of F Y h:i:s A');
$row = 0;
$html = scraperWiki::scrape("http://www.suomenufotutkijat.fi/ufodb/ufoselaa.php");
$tags = array("<td width=\"25%\">","</td>");
$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find("tr") as $data){


    if ($i < 6) { //Poistaa taulukon ensimmäiset, turhat rivit

        $i++;

    }

    else {

        $tds = $data->find("td");

        if (count($tds) == 3) {

            // Jaetaan paikkatiedot        
    
            $p = explode("<br>", $tds[2]);
    
            if (count($p) == 1) {
                
                $str = "ei tiedossa";
                $city = utf8_encode(str_replace($GLOBALS['tags'], "", $p[0]));
    
            }
    
            else if (count($p) == 2) {
                
                $str = utf8_encode(str_replace($GLOBALS['tags'], "", $p[0]));
                $city = utf8_encode(str_replace($GLOBALS['tags'], "", $p[1]));
    
            }
    
            else {
    
                $str = "ei tiedossa";
                $city = "ei tiedossa";
    
            }
    
            // Jaetaan aikatiedot
    
            $t = explode("<br>", $tds[1]);
    
            if (count($t) == 1) {
                
                $date = utf8_encode(str_replace($GLOBALS['tags'], "", $t[0]));
                $time = "ei tiedossa";
    
            }
    
            else if (count($t) == 2) {
                
                $date = utf8_encode(str_replace($GLOBALS['tags'], "", $t[0]));
                $time = utf8_encode(str_replace($GLOBALS['tags'], "", $t[1]));
    
    
            }
    
            else {
    
                $date = "ei tiedossa";
                $time = "ei tiedossa";
    
            }

            $ufo = array("Havainto"=> $tds[0]->plaintext,"Pvm"=> $date, "Aika"=> $time, "Katu_tai_alue"=> $str, "Kaupunki"=>$city);
            scraperwiki::save_sqlite(null, $ufo,$table_name=$GLOBALS['stmp']);
            $GLOBALS['row']++;

            print $GLOBALS['row']. " " . $str . " --- " . $city . " ---" . $date . " --- " . $time . "\n";

        }

    }

}

?>
