<?php

require 'scraperwiki/simple_html_dom.php';

$overview = scraperWiki::scrape("http://noetv-austria.liga.nu/cgi-bin/WebObjects/TennisLeagueAustria.woa/2/wa/teamPortrait?team=241283&championship=N%C3%96TV+2013+MI&group=95321");
$base_url = "http://noetv-austria.liga.nu";

$dom = new simple_html_dom();
$dom->load($overview);

$ergebnisse = array();

foreach($dom->find("table[@class='result-set'] tr") as $data){
    $tds = $data->find("td");

    if(count($tds) == 6){
        $a = $tds[5]->find("a");
        $ergebnisse[] = scrapeErgebnis($base_url . $a[0]->href);
    }
}

print json_encode($ergebnisse);

function scrapeErgebnis($url){
    global $ergebnisse;
    $url = urldecode($url);
    $url = str_replace("&amp;", "&", $url);
    $url = str_replace(" ", "+", $url);
    $ergebnis = scraperWiki::scrape($url);

    $domErg = new simple_html_dom();
    $domErg->load($ergebnis);

    $summary = array();
    $summary["Einzel"] = array();
    $summary["Doppel"] = array();

    $state = 0;
    $header = 0;
    $spiel = 1;
    foreach($domErg->find("table[@class='result-set'] tr") as $data){
        if($data->class == "table-split"){ $state++; $header=0; $spiel = 1; continue; }
        if($state == 1){
            if($header == 0){
                $ths = $data->find("th");
                $heim = $ths[0]->plaintext;
                $gast = $ths[1]->plaintext;
                $summary["Heim"] = $heim;
                $summary["Gast"] = $gast;
                $summary["Spiel"] = $heim . " - " . $gast;
                $header++;
            }else{
                $tds = $data->find("td");
                if(count($tds) != 10){ continue; }
                $summary["Einzel"]["Spiel".$spiel] = array();
                $sheim = $tds[1]->plaintext;
                $sheim = trim(substr($sheim, 0, strpos($sheim, "(")));
                $sgast = $tds[3]->plaintext;
                $sgast = trim(substr($sgast, 0, strpos($sgast, "(")));
                $summary["Einzel"]["Spiel".$spiel]["Spieler-Heim"] = $sheim;
                $summary["Einzel"]["Spiel".$spiel]["Spieler-Gast"] = $sgast;

                $s1 = explode(":", $tds[4]->plaintext);
                $s2 = explode(":", $tds[5]->plaintext);
                $s3 = explode(":", $tds[6]->plaintext);
                
                if(count($s1) != 2){ $s1[0] = "";  $s1[1] = ""; }
                if(count($s2) != 2){ $s2[0] = "";  $s2[1] = ""; }
                if(count($s3) != 2){ $s3[0] = "";  $s3[1] = ""; }

                $summary["Einzel"]["Spiel".$spiel]["Satz1-Heim"] = trim($s1[0]);
                $summary["Einzel"]["Spiel".$spiel]["Satz1-Gast"] = trim($s1[1]);
                $summary["Einzel"]["Spiel".$spiel]["Satz2-Heim"] = trim($s2[0]);
                $summary["Einzel"]["Spiel".$spiel]["Satz2-Gast"] = trim($s2[1]);
                $summary["Einzel"]["Spiel".$spiel]["Satz3-Heim"] = trim($s3[0]);
                $summary["Einzel"]["Spiel".$spiel]["Satz3-Gast"] = trim($s3[1]);
                $spiel++;
            }
        }else if($state == 2){
            if($header == 0){ $header++; continue; }else{
                $tds = $data->find("td");
                if(count($tds) != 12){ continue; }
                $sheim = explode("\n", $tds[2]->plaintext);
                $sheim1 = trim(substr($sheim[0], 0, strpos($sheim[0], "(")));
                $sheim2 = trim(substr($sheim[1], 0, strpos($sheim[1], "(")));
                $sgast = explode("\n", $tds[5]->plaintext);
                $sgast1 = trim(substr($sgast[0], 0, strpos($sgast[0], "(")));
                $sgast2 = trim(substr($sgast[1], 0, strpos($sgast[1], "(")));
                $summary["Doppel"]["Spiel".$spiel]["Spieler1-Heim"] = $sheim1;
                $summary["Doppel"]["Spiel".$spiel]["Spieler2-Heim"] = $sheim2;
                $summary["Doppel"]["Spiel".$spiel]["Spieler1-Gast"] = $sgast1;
                $summary["Doppel"]["Spiel".$spiel]["Spieler2-Gast"] = $sgast2;

                $s1 = explode(":", $tds[6]->plaintext);
                $s2 = explode(":", $tds[7]->plaintext);
                $s3 = explode(":", $tds[8]->plaintext);
                
                if(count($s1) != 2){ $s1[0] = "";  $s1[1] = ""; }
                if(count($s2) != 2){ $s2[0] = "";  $s2[1] = ""; }
                if(count($s3) != 2){ $s3[0] = "";  $s3[1] = ""; }

                $summary["Doppel"]["Spiel".$spiel]["Satz1-Heim"] = trim($s1[0]);
                $summary["Doppel"]["Spiel".$spiel]["Satz1-Gast"] = trim($s1[1]);
                $summary["Doppel"]["Spiel".$spiel]["Satz2-Heim"] = trim($s2[0]);
                $summary["Doppel"]["Spiel".$spiel]["Satz2-Gast"] = trim($s2[1]);
                $summary["Doppel"]["Spiel".$spiel]["Satz3-Heim"] = trim($s3[0]);
                $summary["Doppel"]["Spiel".$spiel]["Satz3-Gast"] = trim($s3[1]);
                $spiel++;
            }
        }
    }
    return $summary;
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$overview = scraperWiki::scrape("http://noetv-austria.liga.nu/cgi-bin/WebObjects/TennisLeagueAustria.woa/2/wa/teamPortrait?team=241283&championship=N%C3%96TV+2013+MI&group=95321");
$base_url = "http://noetv-austria.liga.nu";

$dom = new simple_html_dom();
$dom->load($overview);

$ergebnisse = array();

foreach($dom->find("table[@class='result-set'] tr") as $data){
    $tds = $data->find("td");

    if(count($tds) == 6){
        $a = $tds[5]->find("a");
        $ergebnisse[] = scrapeErgebnis($base_url . $a[0]->href);
    }
}

print json_encode($ergebnisse);

function scrapeErgebnis($url){
    global $ergebnisse;
    $url = urldecode($url);
    $url = str_replace("&amp;", "&", $url);
    $url = str_replace(" ", "+", $url);
    $ergebnis = scraperWiki::scrape($url);

    $domErg = new simple_html_dom();
    $domErg->load($ergebnis);

    $summary = array();
    $summary["Einzel"] = array();
    $summary["Doppel"] = array();

    $state = 0;
    $header = 0;
    $spiel = 1;
    foreach($domErg->find("table[@class='result-set'] tr") as $data){
        if($data->class == "table-split"){ $state++; $header=0; $spiel = 1; continue; }
        if($state == 1){
            if($header == 0){
                $ths = $data->find("th");
                $heim = $ths[0]->plaintext;
                $gast = $ths[1]->plaintext;
                $summary["Heim"] = $heim;
                $summary["Gast"] = $gast;
                $summary["Spiel"] = $heim . " - " . $gast;
                $header++;
            }else{
                $tds = $data->find("td");
                if(count($tds) != 10){ continue; }
                $summary["Einzel"]["Spiel".$spiel] = array();
                $sheim = $tds[1]->plaintext;
                $sheim = trim(substr($sheim, 0, strpos($sheim, "(")));
                $sgast = $tds[3]->plaintext;
                $sgast = trim(substr($sgast, 0, strpos($sgast, "(")));
                $summary["Einzel"]["Spiel".$spiel]["Spieler-Heim"] = $sheim;
                $summary["Einzel"]["Spiel".$spiel]["Spieler-Gast"] = $sgast;

                $s1 = explode(":", $tds[4]->plaintext);
                $s2 = explode(":", $tds[5]->plaintext);
                $s3 = explode(":", $tds[6]->plaintext);
                
                if(count($s1) != 2){ $s1[0] = "";  $s1[1] = ""; }
                if(count($s2) != 2){ $s2[0] = "";  $s2[1] = ""; }
                if(count($s3) != 2){ $s3[0] = "";  $s3[1] = ""; }

                $summary["Einzel"]["Spiel".$spiel]["Satz1-Heim"] = trim($s1[0]);
                $summary["Einzel"]["Spiel".$spiel]["Satz1-Gast"] = trim($s1[1]);
                $summary["Einzel"]["Spiel".$spiel]["Satz2-Heim"] = trim($s2[0]);
                $summary["Einzel"]["Spiel".$spiel]["Satz2-Gast"] = trim($s2[1]);
                $summary["Einzel"]["Spiel".$spiel]["Satz3-Heim"] = trim($s3[0]);
                $summary["Einzel"]["Spiel".$spiel]["Satz3-Gast"] = trim($s3[1]);
                $spiel++;
            }
        }else if($state == 2){
            if($header == 0){ $header++; continue; }else{
                $tds = $data->find("td");
                if(count($tds) != 12){ continue; }
                $sheim = explode("\n", $tds[2]->plaintext);
                $sheim1 = trim(substr($sheim[0], 0, strpos($sheim[0], "(")));
                $sheim2 = trim(substr($sheim[1], 0, strpos($sheim[1], "(")));
                $sgast = explode("\n", $tds[5]->plaintext);
                $sgast1 = trim(substr($sgast[0], 0, strpos($sgast[0], "(")));
                $sgast2 = trim(substr($sgast[1], 0, strpos($sgast[1], "(")));
                $summary["Doppel"]["Spiel".$spiel]["Spieler1-Heim"] = $sheim1;
                $summary["Doppel"]["Spiel".$spiel]["Spieler2-Heim"] = $sheim2;
                $summary["Doppel"]["Spiel".$spiel]["Spieler1-Gast"] = $sgast1;
                $summary["Doppel"]["Spiel".$spiel]["Spieler2-Gast"] = $sgast2;

                $s1 = explode(":", $tds[6]->plaintext);
                $s2 = explode(":", $tds[7]->plaintext);
                $s3 = explode(":", $tds[8]->plaintext);
                
                if(count($s1) != 2){ $s1[0] = "";  $s1[1] = ""; }
                if(count($s2) != 2){ $s2[0] = "";  $s2[1] = ""; }
                if(count($s3) != 2){ $s3[0] = "";  $s3[1] = ""; }

                $summary["Doppel"]["Spiel".$spiel]["Satz1-Heim"] = trim($s1[0]);
                $summary["Doppel"]["Spiel".$spiel]["Satz1-Gast"] = trim($s1[1]);
                $summary["Doppel"]["Spiel".$spiel]["Satz2-Heim"] = trim($s2[0]);
                $summary["Doppel"]["Spiel".$spiel]["Satz2-Gast"] = trim($s2[1]);
                $summary["Doppel"]["Spiel".$spiel]["Satz3-Heim"] = trim($s3[0]);
                $summary["Doppel"]["Spiel".$spiel]["Satz3-Gast"] = trim($s3[1]);
                $spiel++;
            }
        }
    }
    return $summary;
}

?>
