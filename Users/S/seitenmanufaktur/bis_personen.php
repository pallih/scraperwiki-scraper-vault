<?php

$baseurl = "http://bis.schwerin.de/";
$personen_url = 'http://bis.schwerin.de/kp0041.php';

require 'scraperwiki/simple_html_dom.php';

# Übersichtsseite laden
$html_content = scraperWiki::scrape($personen_url);
$html = str_get_html($html_content);

# Links zu Personen auslesen
foreach ($html->find("table.smc_page_kp0041_contenttable td a") as $el) {           
    $person = new stdClass;
    $person->bis_url = $baseurl . $el->href;
    $person->name = utf8_encode(html_entity_decode($el->plaintext));

    # Detailseite der Person laden
    $person_html_content =  scraperWiki::scrape($person->bis_url);
    $person_html = str_get_html($person_html_content);
    
    foreach ($person_html->find("table#smctablevorgang tr") as $detail) {
        if ($detail->find("td", 0)->plaintext == 'Ort:') {
            $person->ort = utf8_encode(html_entity_decode($detail->find("td", 1)->plaintext));
        }
        if ($detail->find("td", 0)->plaintext == 'Stra&szlig;e:') {
            $person->strasse = utf8_encode(html_entity_decode($detail->find("td", 1)->plaintext));
        }
        if ($detail->find("td", 0)->plaintext == 'Telefon dienstl.:') {
            $person->telefon_dienstl = $detail->find("td", 1)->plaintext;
        }
        if ($detail->find("td", 0)->plaintext == 'Telefon privat:') {
            $person->telefon_privat = $detail->find("td", 1)->plaintext;
        }
        if ($detail->find("td", 0)->plaintext == 'Fax dienstl.:') {
            $person->fax_dienstl = $detail->find("td", 1)->plaintext;
        }
        if ($detail->find("td", 0)->plaintext == 'Fax privat:') {
            $person->fax_dienstl = $detail->find("td", 1)->plaintext;
        }
        if ($detail->find("td", 0)->plaintext == 'Mobil dienstl.:') {
            $person->mobil_dienstl = $detail->find("td", 1)->plaintext;
        }
        if ($detail->find("td", 0)->plaintext == 'E-Mail:') {
            $person->email = $detail->find("td", 1)->plaintext;
        }
        if ($detail->find("td", 0)->plaintext == 'Internet:') {
            $person->internet = $detail->find("td", 1)->plaintext;
        }        
    };
    
    $images = $person_html->find("img.smcimgperson");
    if ($images[0]->src) {
        $person->bild = $baseurl . $images[0]->src;
    }

    foreach ($person_html->find("table.smc_page_kp0050_contenttable tr") as $gremium_html) {
        $gremium->person = $person->name;
        if (is_string($gremium_html->find("td", 0)->plaintext)) {
            print $gremium->name = utf8_encode(html_entity_decode($gremium_html->find("td", 0)->plaintext));
        }
        if (is_string($gremium_html->find("td", 1)->plaintext)) {
            $gremium->funktion = utf8_encode(html_entity_decode($gremium_html->find("td", 1)->plaintext));
        }
        if ($gremium->name != "") {
            scraperwiki::save_sqlite(array(), get_object_vars($gremium), 'GremienPersonen');
        }

        if (stripos($gremium->name, 'fraktion') !== false) {
            $person->fraktion = $gremium->name;
        }
    };

    scraperwiki::save_sqlite(array("name"), get_object_vars($person), 'Personen');

    $person_html->__destruct();
}
?>