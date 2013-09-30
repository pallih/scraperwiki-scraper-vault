<?php

require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('Europe/Athens');
$z = 1; /* Sivunumero */
$rowTotal = 0;
$c = "Jyväskylä"; // Kaupunki (pakko syöttää)
$s = ""; // Katu
$r = "1"; // Asunnon koko: 1 = yksiö, 2 = kaksio, jne. 0 = ei määritelty
$amin = ""; //asunnon minimikoko neliömetreissä
$amax = ""; // asunnon maksimikoko neliometreissa
$time = date('l jS \of F Y h:i:s A');

function scrape_page() {
    $row = 0;
    $html = scraperWiki::scrape("http://asuntojen.hintatiedot.fi/haku/?c=".$GLOBALS['c']."&s=".$GLOBALS['s']."&r=".$GLOBALS['r']."&amin=".$GLOBALS['amin']."&amax=".$GLOBALS['amax']."&z=".$GLOBALS['z']);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("tr") as $data){
        $tds = $data->find("td");
        if(count($tds) > 8){
            $row++;
            $GLOBALS['rowTotal']++;
            $apt = array("Uniikkiavain"=>$GLOBALS['rowTotal'], "Kaupunginosa"=> $tds[0]->plaintext, "Myyntihinta"=> $tds[3]->plaintext, "Neliohinta" => $tds[4]->plaintext, "Tyyppi"=> $tds[1]->plaintext, "Koko" => $tds[2]->plaintext);
            scraperwiki::save_sqlite(null,$apt,$table_name=$GLOBALS['c']." ".$GLOBALS['time'] );
            print $GLOBALS['rowTotal']."\n";
            print $row.". Sijainti: ". $tds[0]->plaintext ." Hinta: " . $tds[3]->plaintext ." Tyyppi: " . $tds[1]->plaintext . " Koko: " . $tds[2]->plaintext . " Neliöhinta: " . $tds[4]->plaintext . "€" . "\n";
        }
    }

    if($row==50) {
        print("Vielä jatkuu, haetaan seuraava sivu..."."\n");
        $GLOBALS['z']++;
        scrape_page();
    }
    else {
    
        print("Skrääpiminen suoritettu."."\n");
        print("Sivuja yhteensä: ".$GLOBALS['z']."\n");
        print("Rivejä yhteensä: ".$GLOBALS['rowTotal']."\n");
    }
}

scrape_page();

?>
<?php

require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('Europe/Athens');
$z = 1; /* Sivunumero */
$rowTotal = 0;
$c = "Jyväskylä"; // Kaupunki (pakko syöttää)
$s = ""; // Katu
$r = "1"; // Asunnon koko: 1 = yksiö, 2 = kaksio, jne. 0 = ei määritelty
$amin = ""; //asunnon minimikoko neliömetreissä
$amax = ""; // asunnon maksimikoko neliometreissa
$time = date('l jS \of F Y h:i:s A');

function scrape_page() {
    $row = 0;
    $html = scraperWiki::scrape("http://asuntojen.hintatiedot.fi/haku/?c=".$GLOBALS['c']."&s=".$GLOBALS['s']."&r=".$GLOBALS['r']."&amin=".$GLOBALS['amin']."&amax=".$GLOBALS['amax']."&z=".$GLOBALS['z']);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("tr") as $data){
        $tds = $data->find("td");
        if(count($tds) > 8){
            $row++;
            $GLOBALS['rowTotal']++;
            $apt = array("Uniikkiavain"=>$GLOBALS['rowTotal'], "Kaupunginosa"=> $tds[0]->plaintext, "Myyntihinta"=> $tds[3]->plaintext, "Neliohinta" => $tds[4]->plaintext, "Tyyppi"=> $tds[1]->plaintext, "Koko" => $tds[2]->plaintext);
            scraperwiki::save_sqlite(null,$apt,$table_name=$GLOBALS['c']." ".$GLOBALS['time'] );
            print $GLOBALS['rowTotal']."\n";
            print $row.". Sijainti: ". $tds[0]->plaintext ." Hinta: " . $tds[3]->plaintext ." Tyyppi: " . $tds[1]->plaintext . " Koko: " . $tds[2]->plaintext . " Neliöhinta: " . $tds[4]->plaintext . "€" . "\n";
        }
    }

    if($row==50) {
        print("Vielä jatkuu, haetaan seuraava sivu..."."\n");
        $GLOBALS['z']++;
        scrape_page();
    }
    else {
    
        print("Skrääpiminen suoritettu."."\n");
        print("Sivuja yhteensä: ".$GLOBALS['z']."\n");
        print("Rivejä yhteensä: ".$GLOBALS['rowTotal']."\n");
    }
}

scrape_page();

?>
