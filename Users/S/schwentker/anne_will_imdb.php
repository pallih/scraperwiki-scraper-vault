<?php

require 'scraperwiki/simple_html_dom.php';

//URL erste Episode
$url_adresse = "http://www.imdb.com/title/tt1106523/";
$html_content = scraperwiki::scrape($url_adresse);
$html = str_get_html($html_content);

$anzahl_episoden = $html->find("div.episode-nav a",0)->innertext;
$anzahl_episoden = substr($anzahl_episoden, 0, strpos($anzahl_episoden, " "));


for ($episode = 1; $episode <= $anzahl_episoden; $episode++) {

    $html_content = scraperwiki::scrape($url_adresse);
    $html = str_get_html($html_content);

    //Titel der Sendung ("Anne Will")
    $titel = $html->find("h2.tv_header a",0)->innertext;
    print "Sendung: " . $titel . "\n";

    //Nummer der Folge
    print "Nummer der Folge: " . $episode. "\n";

    //Thema der Folge
    $el = $html->find("h1.header",0)->innertext;
    $thema = umlaute(substr($el, 0, strpos($el, "<span")));
    print "Folge: " . $thema. "\n";

    //Datum der Folge
    $datum = trim($html->find("h1.header span",0)->innertext, "()");
    print "Datum: " . $datum . "\n";

    //Gäste
    print "Gäste:\n";
    $counter = 0;
    $gaeste = array_fill(0, 10, '');
    foreach ($html->find("td.name a") as $el) { 
        $gast = umlaute($el->innertext);

        if ($gast <> "Anne Will") {
            $gaeste[$counter] = $gast;
            $counter = $counter + 1;
        }
        print  $gast. "\n";
        
    }

    scraperwiki::save_sqlite(array("Nummer der Folge"),array("Sendung"=>$titel, "Nummer der Folge"=>$episode, "Thema"=>$thema, "Datum"=>$datum, "Anzahl Gäste"=>$counter, "Gast 1"=>$gaeste[0], "Gast 2"=>$gaeste[1], "Gast 3"=>$gaeste[2], "Gast 4"=>$gaeste[3], "Gast 5"=>$gaeste[4], "Gast 6"=>$gaeste[5], "Gast 7"=>$gaeste[6], "Gast 8"=>$gaeste[7], "Gast 9"=>$gaeste[8], "Gast 10"=>$gaeste[9]));

    //URL der nächsten Episode scrapen
    $el = $html->find("div.episode-nav",0);
    foreach ($el->children() as $child) {
        if ($child->innertext == "Next Episode")  $url_adresse = $child->href;
    }

    $url_adresse = "http://www.imdb.com" . $url_adresse . "/";   


}



function umlaute($string){
  $upas = Array("&#xFC;" => "ü", "&uuml;" => "ü", "&#xE4;" => "ä" ,"&auml;" => "ä", "&#xF6;" => "ö", "&ouml;" => "ö", "&Auml;" => "Ä", "&Uuml;" => "Ü", "&Ouml;" => "Ö","&#xDF;" => "ß" , "&szlig;" => "ß");
  return strtr($string, $upas);
}

?>
