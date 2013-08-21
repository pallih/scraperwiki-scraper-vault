<?php

require 'scraperwiki/simple_html_dom.php';

//URL Übersichtsseite Bundesländer
$url_uebersicht = "http://www.bundestag.de/bundestag/abgeordnete17/listeBundesland/index.html";
$html_uebersicht_content = scraperwiki::scrape($url_uebersicht);
$html = str_get_html($html_uebersicht_content);

$html_laenderliste = $html->find("ul.standardLinkliste",0);
print "Liste: " . $html_laenderliste . "\n";

$laender = array();
$MdB = array();
$counter_laender = 0;
$counter_MdB = 0;

//Länder-Schleife
foreach ($html_laenderliste->find("div.linkIntern a") as $el) { 
    $laender_url = "http://www.bundestag.de/bundestag/abgeordnete17/listeBundesland/" . $el->href;
    $laender[$counter_laender][0] = $laender_url;        //URL der Landes-Seite
    $laender[$counter_laender][1] = $el->innertext;      //Name des Landes

    print $laender[$counter_laender][1] . ": " . $laender[$counter_laender][0] . "\n";

    //Seite des Landes laden
    $html_land = str_get_html(scraperwiki::scrape($laender[$counter_laender][0]));

    //MdB-Schleife dieses Landes
    foreach ($html_land->find("div.linkIntern a") as $el_MdB) {
        $url_MdB = "http://www.bundestag.de/bundestag/abgeordnete17/" . substr($el_MdB->href, 3);

        list($nachname_MdB, $vorname_MdB, $partei_MdB) = explode(", ", $el_MdB->innertext);
        $nachname_MdB = strtok($nachname_MdB, " ");
        $titel_MdB = "";
        $dot_pos = strrpos ( $vorname_MdB , "." , -1 );    //Position des Punkts; Suche von hinten, ohne letztes Zeichen 
        if ( $dot_pos !== false) {
            $titel_MdB = substr($vorname_MdB, 0, $dot_pos+1);
            $vorname_MdB = substr($vorname_MdB, $dot_pos+2);           
        }
    
        //Seite dieses einzelnen MdB scrapen
        $html_MdB = str_get_html(scraperwiki::scrape($url_MdB));
        $html_biografie = $html_MdB->find("div.biografie",0);
        $startzeile = substr( $html_biografie, strpos ( $html_biografie , "Geboren am " )+11, strpos ( $html_biografie , ".", strpos ( $html_biografie , "Geboren am " )+16 )-strpos ( $html_biografie , "Geboren am " )-11);
        $satz = explode("; " , $startzeile);
        list($geburtstag_MdB, $geburtsort_MdB) = explode( " in ", $satz[0]);

    
        $MdB = array($counter_MdB => array("URL" => $url_MdB, "Nachname" => $nachname_MdB, "Vorname" => $vorname_MdB, "Titel" => $titel_MdB, "Geburtstag" => $geburtstag_MdB, "Partei" => $partei_MdB, "Bundesland"=> $laender[$counter_laender][1], "Geburtsort" => umlaute($geburtsort_MdB)));

        print "Nr. " . ($counter_MdB + 1) . ": ". $MdB[$counter_MdB]["Vorname"] . " " . $MdB[$counter_MdB]["Nachname"] . " (" . $MdB[$counter_MdB]["Partei"] . ")" . ", ". $MdB[$counter_MdB]["Geburtstag"]. ", ". $MdB[$counter_MdB]["Geburtsort"] . ", " . $MdB[$counter_MdB]["Bundesland"] . "\n";
        $counter_MdB = $counter_MdB + 1;        

    }

    $counter_laender = $counter_laender + 1; 
}




function umlaute($string){
  $upas = Array("&#xFC;" => "ü", "&uuml;" => "ü", "&#xE4;" => "ä" ,"&auml;" => "ä", "&#xF6;" => "ö", "&ouml;" => "ö", "&Auml;" => "Ä", "&Uuml;" => "Ü", "&Ouml;" => "Ö","&#xDF;" => "ß" , "&szlig;" => "ß");
  return strtr($string, $upas);
}

?>
