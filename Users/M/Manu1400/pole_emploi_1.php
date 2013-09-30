<?php
function save_key_value($key, $value, $count) {
    
    #if($count==2) {
        $recordb = array(
            'country' => $key, 
            'years_in_school' => $value
        );

    scraperwiki::save(array('country', 'years_in_school'), $recordb);
    #}
}

function decodeAccented($encodedValue, $options = array()) {
    $options += array(
        'quote'     => ENT_NOQUOTES,
        'encoding'  => 'UTF-8',
    );
    return preg_replace_callback(
        '/&\w(acute|uml|tilde);/',
        create_function(
            '$m',
            'return html_entity_decode($m[0], ' . $options['quote'] . ', "' .
            $options['encoding'] . '");'
        ),
        $encodedValue
    );
}

function chr_utf8($code) 
    { 
        if ($code < 0) return false; 
        elseif ($code < 128) return chr($code); 
        elseif ($code < 160) // Remove Windows Illegals Cars 
        { 
            if ($code==128) $code=8364; 
            elseif ($code==129) $code=160; // not affected 
            elseif ($code==130) $code=8218; 
            elseif ($code==131) $code=402; 
            elseif ($code==132) $code=8222; 
            elseif ($code==133) $code=8230; 
            elseif ($code==134) $code=8224; 
            elseif ($code==135) $code=8225; 
            elseif ($code==136) $code=710; 
            elseif ($code==137) $code=8240; 
            elseif ($code==138) $code=352; 
            elseif ($code==139) $code=8249; 
            elseif ($code==140) $code=338; 
            elseif ($code==141) $code=160; // not affected 
            elseif ($code==142) $code=381; 
            elseif ($code==143) $code=160; // not affected 
            elseif ($code==144) $code=160; // not affected 
            elseif ($code==145) $code=8216; 
            elseif ($code==146) $code=8217; 
            elseif ($code==147) $code=8220; 
            elseif ($code==148) $code=8221; 
            elseif ($code==149) $code=8226; 
            elseif ($code==150) $code=8211; 
            elseif ($code==151) $code=8212; 
            elseif ($code==152) $code=732; 
            elseif ($code==153) $code=8482; 
            elseif ($code==154) $code=353; 
            elseif ($code==155) $code=8250; 
            elseif ($code==156) $code=339; 
            elseif ($code==157) $code=160; // not affected 
            elseif ($code==158) $code=382; 
            elseif ($code==159) $code=376; 
        } 
        if ($code < 2048) return chr(192 | ($code >> 6)) . chr(128 | ($code & 63)); 
        elseif ($code < 65536) return chr(224 | ($code >> 12)) . chr(128 | (($code >> 6) & 63)) . chr(128 | ($code & 63)); 
        else return chr(240 | ($code >> 18)) . chr(128 | (($code >> 12) & 63)) . chr(128 | (($code >> 6) & 63)) . chr(128 | ($code & 63));
    } 

    // Callback for preg_replace_callback('~&(#(x?))?([^;]+);~', 'html_entity_replace', $str); 
    function html_entity_replace($matches) 
    { 
        if ($matches[2]) 
        { 
            return chr_utf8(hexdec($matches[3])); 
        } elseif ($matches[1]) 
        { 
            return chr_utf8($matches[3]); 
        } 
        switch ($matches[3]) 
        { 
            case "nbsp": return chr_utf8(160); 
            case "iexcl": return chr_utf8(161); 
            case "cent": return chr_utf8(162); 
            case "pound": return chr_utf8(163); 
            case "curren": return chr_utf8(164); 
            case "yen": return chr_utf8(165); 
            //case "eacute" : return chr_utf8(00E9);
            
            //... etc with all named HTML entities 
        } 
        return false; 
    } 
    
    function htmlentities2utf8 ($string) // because of the html_entity_decode() bug with UTF-8 
    { 
        $string = preg_replace_callback('~&(#(x?))?([^;]+);~', 'html_entity_replace', $string); 
        return $string; 
    } 

function scrappe_offre($html, $referenceb){
$dom = new simple_html_dom();
$dom->load($html);
$div = $dom->find("div.tx-sqliwebServiceanpe-pi5");
$span = $dom->find("div.tx-sqliwebServiceanpe-pi5 span.texteANPEDetail");
$actualisation = $span[1]->plaintext;
$record = array();
//'NumOffre_et_description' => $dom->find("div.tx-sqliwebServiceanpe-pi5 h3")->plaintext, //005FZJB - testeur / testeuse informatique
foreach($span as $data){
    //$textb = html_entity_decode(htmlentities2utf8($data->plaintext) , ENT_COMPAT, "UTF-8");
#    $text = htmlspecialchars_decode($data->plaintext);
   # $text = $data->plaintext;
$text = htmlentities( (string) $data->plaintext, ENT_QUOTES, 'utf-8', FALSE);
#decodeAccented($encodedValue, $options = array())
#$text = decodeAccented($text);

    #$text = $tab[0];
    
    array_push($record, $text );
    #array_push($record, explode(' : ', $text, 2) );
    #$record[] = explode(' : ', $text, 2);
    $splited = array();
    $splited[] = explode(' : ', $text, 2);
    print_r($splited);
    $key = $splited[0][0];
    $value = $splited[0][1];
    
    if($key == "dur&eacute;e hebdomadaire de travail"){
        if($value == "35h hebdo")
            $value = "35h";
    }
    if($key == "type de contrat"){
        if($value == "contrat &agrave; dur&eacute;e ind&eacute;termin&eacute;e")
            $value = "CDI";
    }
    if($key == "permis"){
        if($value == "b - v&eacute;hicule l&eacute;ger (Exig&eacute;)")
            $value == "Permis B exigé";
    }
    if($key == "taille de l&#039;entreprise"){
        if($value == "100 &agrave; 199 salari&eacute;s")
            $value = "entre 100 et 200 salariés";
    }
    save_key_value($key, $value, count($splited[0]));
    if($key == "lieu de travail")  #"28 - nogent-le-phaye"
        {
        $lieu_travail = explode(' - ', $value, 2);
        $departement = $lieu_travail[0];
        $ville = ucfirst($lieu_travail[1]);
        save_key_value("departement", $departement, 2);
        save_key_value("ville", $ville, 2);
        save_key_value("map", "http://nominatim.openstreetmap.org/search/"+$ville+"?limit=1&format=html", 2);
        }
    #annuel de 20 000.00 à 34 000.00 euros sur 13 mois
    #if($key == "salaire indicatif")
    #    $value = "mensuel de 2 600 &agrave; 3 000 euros sur 13 mois mutuelle participation/action"
}
//'actualiseJJ' => intval($actualisation[29].$actualisation[30]), //01 ou 1 le premier janvier ?

print json_encode($record) . "\n";
#scraperwiki::save(array('contenu_offre'), $record);
#return $record;
}

/* $url = "http://www2.pole-emploi.fr/espacecandidat/nicola/LancerRechercheAvanceeMulti.do";
   $parameter = "?nomCommune:CHARTRES&communeChoisie=CHARTRES+%2828000%29&distance=10&codepostal=28000";
   $html = scraperWiki::scrape($url . $parameter);
   print $html . "\n"; */

/* Pre-scrapping */
$url_pre_scrapping = "http://www.handicapzero.org/index.php?id=19969";
$html = scraperWiki::scrape($url_pre_scrapping);

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("input") as $input){
    ;
}
$sess = $input->value;

$url = "http://www.handicapzero.org/index.php?id=19969";
$request_url = "http://www.handicapzero.org/index.php?tache=ResultatOffre&type_recherche=avance&sess=&id=19967&code_emploi_metier=m1805&int_rome=&lieu_travailD=28D&lieu_travailR=&lieu_travailP=&offre_emise=14&secteur_activite=&contrat=&salaire=&qualification=&nature_offre=&heure_par_semaine=&experience_fonction=&type_formation=&domaine_formation=&acces_th=2&mot_cle=mot+cl%C3%A9&Submit=rechercher&sess=" . $sess;
$html = scraperWiki::scrape($request_url);
#print $html . "\n";

$dom_page2 = new simple_html_dom();
$dom_page2->load($html);
/* Analyse des 20 premières offres éventuelles retournées */
foreach($dom_page2->find("ul.ANPE li") as $li){ //former : div[@align='left'] tr
    #print $li;
    $plaintext = $li->plaintext; //Utile pour visualiser le contenu
    #print $plaintext;
    $a = $li->find("a", 0);
    $href = $a->href;
    #print $href . "\n";
#   "index.php?id=19966&amp;idOffre=005FZJB&amp;fromPage=listeOffresSelection&amp;acces_th=2&amp;sess=20130524101216511479629910"
#   <a href="index.php?id=19966&amp;idOffre=005FZJB&amp;fromPage=listeOffresSelection&amp;acces_th=2&amp;sess=20130524101216511479629910" title="réf&nbsp;005FZJB : testeur / testeuse informatique">réf&nbsp;005FZJB</a>
    $reference = $href[27].$href[28].$href[29].$href[30].$href[31].$href[32].$href[33]; //idOffre
    print $reference . "\n";

    /* Scrapping de l'offre en question */
    $url_offre = "http://www.handicapzero.org/index.php?tache=Offre&idOffre=".$reference."&strReferences=".$reference."&fromPage=rechercheParRef&sess=&id=19966&reference=".$reference."&Submit=rechercher&sess=".$sess;
    $html = scraperWiki::scrape($url_offre);
    scrappe_offre($html, $reference);
    

    exit;

    #$record = array(
    #    'country' => $tds[0]->plaintext, 
    #    'years_in_school' => intval($tds[4]->plaintext)
    #    );
    #print json_encode($record) . "\n";
    #scraperwiki::save(array('country'), $record);
}

?>
<?php
function save_key_value($key, $value, $count) {
    
    #if($count==2) {
        $recordb = array(
            'country' => $key, 
            'years_in_school' => $value
        );

    scraperwiki::save(array('country', 'years_in_school'), $recordb);
    #}
}

function decodeAccented($encodedValue, $options = array()) {
    $options += array(
        'quote'     => ENT_NOQUOTES,
        'encoding'  => 'UTF-8',
    );
    return preg_replace_callback(
        '/&\w(acute|uml|tilde);/',
        create_function(
            '$m',
            'return html_entity_decode($m[0], ' . $options['quote'] . ', "' .
            $options['encoding'] . '");'
        ),
        $encodedValue
    );
}

function chr_utf8($code) 
    { 
        if ($code < 0) return false; 
        elseif ($code < 128) return chr($code); 
        elseif ($code < 160) // Remove Windows Illegals Cars 
        { 
            if ($code==128) $code=8364; 
            elseif ($code==129) $code=160; // not affected 
            elseif ($code==130) $code=8218; 
            elseif ($code==131) $code=402; 
            elseif ($code==132) $code=8222; 
            elseif ($code==133) $code=8230; 
            elseif ($code==134) $code=8224; 
            elseif ($code==135) $code=8225; 
            elseif ($code==136) $code=710; 
            elseif ($code==137) $code=8240; 
            elseif ($code==138) $code=352; 
            elseif ($code==139) $code=8249; 
            elseif ($code==140) $code=338; 
            elseif ($code==141) $code=160; // not affected 
            elseif ($code==142) $code=381; 
            elseif ($code==143) $code=160; // not affected 
            elseif ($code==144) $code=160; // not affected 
            elseif ($code==145) $code=8216; 
            elseif ($code==146) $code=8217; 
            elseif ($code==147) $code=8220; 
            elseif ($code==148) $code=8221; 
            elseif ($code==149) $code=8226; 
            elseif ($code==150) $code=8211; 
            elseif ($code==151) $code=8212; 
            elseif ($code==152) $code=732; 
            elseif ($code==153) $code=8482; 
            elseif ($code==154) $code=353; 
            elseif ($code==155) $code=8250; 
            elseif ($code==156) $code=339; 
            elseif ($code==157) $code=160; // not affected 
            elseif ($code==158) $code=382; 
            elseif ($code==159) $code=376; 
        } 
        if ($code < 2048) return chr(192 | ($code >> 6)) . chr(128 | ($code & 63)); 
        elseif ($code < 65536) return chr(224 | ($code >> 12)) . chr(128 | (($code >> 6) & 63)) . chr(128 | ($code & 63)); 
        else return chr(240 | ($code >> 18)) . chr(128 | (($code >> 12) & 63)) . chr(128 | (($code >> 6) & 63)) . chr(128 | ($code & 63));
    } 

    // Callback for preg_replace_callback('~&(#(x?))?([^;]+);~', 'html_entity_replace', $str); 
    function html_entity_replace($matches) 
    { 
        if ($matches[2]) 
        { 
            return chr_utf8(hexdec($matches[3])); 
        } elseif ($matches[1]) 
        { 
            return chr_utf8($matches[3]); 
        } 
        switch ($matches[3]) 
        { 
            case "nbsp": return chr_utf8(160); 
            case "iexcl": return chr_utf8(161); 
            case "cent": return chr_utf8(162); 
            case "pound": return chr_utf8(163); 
            case "curren": return chr_utf8(164); 
            case "yen": return chr_utf8(165); 
            //case "eacute" : return chr_utf8(00E9);
            
            //... etc with all named HTML entities 
        } 
        return false; 
    } 
    
    function htmlentities2utf8 ($string) // because of the html_entity_decode() bug with UTF-8 
    { 
        $string = preg_replace_callback('~&(#(x?))?([^;]+);~', 'html_entity_replace', $string); 
        return $string; 
    } 

function scrappe_offre($html, $referenceb){
$dom = new simple_html_dom();
$dom->load($html);
$div = $dom->find("div.tx-sqliwebServiceanpe-pi5");
$span = $dom->find("div.tx-sqliwebServiceanpe-pi5 span.texteANPEDetail");
$actualisation = $span[1]->plaintext;
$record = array();
//'NumOffre_et_description' => $dom->find("div.tx-sqliwebServiceanpe-pi5 h3")->plaintext, //005FZJB - testeur / testeuse informatique
foreach($span as $data){
    //$textb = html_entity_decode(htmlentities2utf8($data->plaintext) , ENT_COMPAT, "UTF-8");
#    $text = htmlspecialchars_decode($data->plaintext);
   # $text = $data->plaintext;
$text = htmlentities( (string) $data->plaintext, ENT_QUOTES, 'utf-8', FALSE);
#decodeAccented($encodedValue, $options = array())
#$text = decodeAccented($text);

    #$text = $tab[0];
    
    array_push($record, $text );
    #array_push($record, explode(' : ', $text, 2) );
    #$record[] = explode(' : ', $text, 2);
    $splited = array();
    $splited[] = explode(' : ', $text, 2);
    print_r($splited);
    $key = $splited[0][0];
    $value = $splited[0][1];
    
    if($key == "dur&eacute;e hebdomadaire de travail"){
        if($value == "35h hebdo")
            $value = "35h";
    }
    if($key == "type de contrat"){
        if($value == "contrat &agrave; dur&eacute;e ind&eacute;termin&eacute;e")
            $value = "CDI";
    }
    if($key == "permis"){
        if($value == "b - v&eacute;hicule l&eacute;ger (Exig&eacute;)")
            $value == "Permis B exigé";
    }
    if($key == "taille de l&#039;entreprise"){
        if($value == "100 &agrave; 199 salari&eacute;s")
            $value = "entre 100 et 200 salariés";
    }
    save_key_value($key, $value, count($splited[0]));
    if($key == "lieu de travail")  #"28 - nogent-le-phaye"
        {
        $lieu_travail = explode(' - ', $value, 2);
        $departement = $lieu_travail[0];
        $ville = ucfirst($lieu_travail[1]);
        save_key_value("departement", $departement, 2);
        save_key_value("ville", $ville, 2);
        save_key_value("map", "http://nominatim.openstreetmap.org/search/"+$ville+"?limit=1&format=html", 2);
        }
    #annuel de 20 000.00 à 34 000.00 euros sur 13 mois
    #if($key == "salaire indicatif")
    #    $value = "mensuel de 2 600 &agrave; 3 000 euros sur 13 mois mutuelle participation/action"
}
//'actualiseJJ' => intval($actualisation[29].$actualisation[30]), //01 ou 1 le premier janvier ?

print json_encode($record) . "\n";
#scraperwiki::save(array('contenu_offre'), $record);
#return $record;
}

/* $url = "http://www2.pole-emploi.fr/espacecandidat/nicola/LancerRechercheAvanceeMulti.do";
   $parameter = "?nomCommune:CHARTRES&communeChoisie=CHARTRES+%2828000%29&distance=10&codepostal=28000";
   $html = scraperWiki::scrape($url . $parameter);
   print $html . "\n"; */

/* Pre-scrapping */
$url_pre_scrapping = "http://www.handicapzero.org/index.php?id=19969";
$html = scraperWiki::scrape($url_pre_scrapping);

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("input") as $input){
    ;
}
$sess = $input->value;

$url = "http://www.handicapzero.org/index.php?id=19969";
$request_url = "http://www.handicapzero.org/index.php?tache=ResultatOffre&type_recherche=avance&sess=&id=19967&code_emploi_metier=m1805&int_rome=&lieu_travailD=28D&lieu_travailR=&lieu_travailP=&offre_emise=14&secteur_activite=&contrat=&salaire=&qualification=&nature_offre=&heure_par_semaine=&experience_fonction=&type_formation=&domaine_formation=&acces_th=2&mot_cle=mot+cl%C3%A9&Submit=rechercher&sess=" . $sess;
$html = scraperWiki::scrape($request_url);
#print $html . "\n";

$dom_page2 = new simple_html_dom();
$dom_page2->load($html);
/* Analyse des 20 premières offres éventuelles retournées */
foreach($dom_page2->find("ul.ANPE li") as $li){ //former : div[@align='left'] tr
    #print $li;
    $plaintext = $li->plaintext; //Utile pour visualiser le contenu
    #print $plaintext;
    $a = $li->find("a", 0);
    $href = $a->href;
    #print $href . "\n";
#   "index.php?id=19966&amp;idOffre=005FZJB&amp;fromPage=listeOffresSelection&amp;acces_th=2&amp;sess=20130524101216511479629910"
#   <a href="index.php?id=19966&amp;idOffre=005FZJB&amp;fromPage=listeOffresSelection&amp;acces_th=2&amp;sess=20130524101216511479629910" title="réf&nbsp;005FZJB : testeur / testeuse informatique">réf&nbsp;005FZJB</a>
    $reference = $href[27].$href[28].$href[29].$href[30].$href[31].$href[32].$href[33]; //idOffre
    print $reference . "\n";

    /* Scrapping de l'offre en question */
    $url_offre = "http://www.handicapzero.org/index.php?tache=Offre&idOffre=".$reference."&strReferences=".$reference."&fromPage=rechercheParRef&sess=&id=19966&reference=".$reference."&Submit=rechercher&sess=".$sess;
    $html = scraperWiki::scrape($url_offre);
    scrappe_offre($html, $reference);
    

    exit;

    #$record = array(
    #    'country' => $tds[0]->plaintext, 
    #    'years_in_school' => intval($tds[4]->plaintext)
    #    );
    #print json_encode($record) . "\n";
    #scraperwiki::save(array('country'), $record);
}

?>
