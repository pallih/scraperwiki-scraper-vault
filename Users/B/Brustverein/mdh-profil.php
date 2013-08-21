<?php

require 'scraperwiki/simple_html_dom.php';


$html_content_s = scraperwiki::scrape("http://www.mydirtyhobby.com/?ac=search&ac2=umgebung&plz=2#type|1|ac|search|anf|"."15"."|ac2|umgebung|plz|2|gender|F|module|get");
print "Lade Seite: http://www.mydirtyhobby.com/?ac=search&ac2=umgebung&plz=2#type|1|ac|search|anf|".$seite*$offset."|ac2|umgebung|plz|2|gender|F|module|get\n";

$html_s = str_get_html($html_content_s);

foreach ($html_s->find("div.amateurs_block .am_name_block a") as $el_s) {

preg_match ('/"(.*?)"/',$el_s,$el_URL);
preg_match ('/u_id=(.*?)"/',$el_s,$el_ID);
$URL = "http://www.mydirtyhobby.com/".$el_URL[1];
$ID = $el_ID[1];

print $URL." - ".$ID."\n";

$html_content = scraperwiki::scrape($URL);
$html = str_get_html($html_content);

$index = 0;

foreach ($html->find("div.vipbadge_block h1 span") as $screenName) {
    $screenName = str_replace('<span>',NULL,$screenName);
    $screenName = str_replace('</span>',NULL,$screenName);
//    print $screenName."\n";
}
foreach ($html->find("#prof_bildl1 img") as $profilBild) {
    $profilBild = str_replace('<img id="prof_bild1" src="',NULL,$profilBild);
    $profilBild = str_replace('" alt="" border="0">',NULL,$profilBild);
//    print $profilBild."\n";
}


foreach ($html->find("div.xtabl td") as $el) {
    if (stripos($el, 'clear.gif')) $el=NULL;
    $el = str_replace('<td class="ytab1b">',NULL,$el);
    $el = str_replace('<td class="ytab2b">',NULL,$el);
    $el = str_replace('<td class="ytab1a">',NULL,$el);
    $el = str_replace('<td class="ytab2a">',NULL,$el);
    $el = str_replace('... / <img src="http://cdn1.e5.mydirtyhobby.com/u/images/flag_de.gif" title="Deutschland">',NULL,$el);
    $el = str_replace('</td>',"",$el);

  if ($el) {
    $index++;
    $data[$index] = $el;
//    print $index." - ".$data[$index] . "\n";
    }
}
        
    for ($i=0; $i<=count($data); $i++) {
        switch ($data[$i]) {
            case "Vorname":
                $vorname = html_entity_decode($data[$i+1]);
                break;
            case "Geschlecht":
                $geschlecht = $data[$i+1];
                break;
            case "Alter":
                $alter = $data[$i+1];
                break;
            case "PLZ / Land":
                $plz = $data[$i+1];
                break;
            case "Sternzeichen":
                $sternzeichen = $data[$i+1];
                break;
            case "Gr&ouml;&szlig;e":
                $groesse = $data[$i+1];
                break;
            case "Augenfarbe":
                $augenfarbe = $data[$i+1];
                break;
            case "Haarfarbe":
                $haarfarbe = $data[$i+1];
                break;
            case "Gewicht":
                $gewicht = $data[$i+1];
                break;
            case "K&ouml;rbchengr&ouml;&szlig;e":
                preg_match("/[0-9]*/", $data[$i+1], $BHUmfang);
                preg_match("/[a-zA-Z]/", $data[$i+1], $BHCup);
                $BHCup[0] = strtoupper ($BHCup[0]);
                break;
            case "Intimrasur":
                $intimrasur = $data[$i+1];
                break;
            case "Piercing":
                $piercing = $data[$i+1];
                break;
            case "Tattoos":
                $tattoos = $data[$i+1];
                break;
            case "Beruf":
                $beruf = $data[$i+1];
                break;
            case "Aussehen":
                $aussehen = $data[$i+1];
                break;
            case "Familienstand":
                $familienstand = $data[$i+1];
                break;
            case "Sexuelle Orientierung":
                $orientierung = $data[$i+1];
                break;
            case "Ich suche":
                $ichSuche = $data[$i+1];
                break;
            case "Ich bin interessiert an":
                $interesse = $data[$i+1];
                break;
            case "Sexuelle Vorlieben":
                $vorlieben = $data[$i+1];
                break;
    }
}

$record = array(
    'ID' => $ID,
    'ScreenName' => $screenName,
    'Geschlecht'=> $geschlecht,
    'ProfilBild' => $profilBild,
    'Vorname' => $vorname,
    'Alter'=> intval($alter),
    'PLZ'=> intval($plz),
    'Sternzeichen'=> $sternzeichen,
    'Groesse'=> intval($groesse),
    'Augenfarbe'=> $augenfarbe,
    'Haarfarbe'=> $haarfarbe,
    'Gewicht'=> intval($gewicht),
    'BHUmfang' => intval($BHUmfang[0]),
    'BHCup'=> $BHCup[0],
    'Intimrasur'=> $intimrasur,
    'Piercing'=> $piercing,
    'Tattoos'=> $tattoos,
    'Beruf'=> $beruf,
    'Aussehen'=> $aussehen,
    'Familienstand'=> $familienstand,
    'Orientierung'=> $orientierung,
    'IchSuche'=> $ichSuche,
    'Interesse'=> $interesse,
    'Vorlieben' => $vorlieben,
//    'Angemeldet' => $angemeldet,
//    'Online' => $online,
//    'Galerien' => $galerien,
//    'Videos' => $videos,
//    'Upload' => $upload
    );

//print_r($record);
scraperwiki::save(array('ID'), $record);
}
?>