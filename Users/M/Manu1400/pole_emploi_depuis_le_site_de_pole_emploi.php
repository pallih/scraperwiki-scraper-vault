<?php
function scrape_with_header ($url, $session) {
    $curl = curl_init ($url ) ;
    curl_setopt ($curl, CURLOPT_RETURNTRANSFER, true) ;
    //curl_setopt($curl, CURLOPT_POST,true);
    curl_setopt( $curl, CURLOPT_ENCODING, "ISO-8859-1" ); 
    curl_setopt($curl, CURLOPT_HTTPHEADER, array(
    'Connection: keep-alive',
'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
'Accept-Encoding: gzip,deflate,sdch',
'Accept-Language: fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
#"'Cookie: xtvrn=$475540$; JSESSIONID=RknC8LMyT2ngpGHcCSmZc2FdKCh122kk2QhhwKWrTlsN41xs5jsC!1494859989'
    'Cookie: xtvrn=$475540$; JSESSIONID='.$session
    ));
    $res  = curl_exec ($curl) ;
    curl_close ($curl) ;
    print $res;
    return   $res;
}

function requete(){

$c = curl_init();
/*On indique à curl quelle url on souhaite télécharger*/
curl_setopt($c, CURLOPT_URL, "http://www.google.com");
/*On indique à curl de nous retourner le contenu de la requête plutôt que de l'afficher*/
curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
/*On indique à curl de retourner les headers http de la réponse dans la chaine de retour*/
curl_setopt($c, CURLOPT_HEADER, true);
/*On indique à curl de suivre les redirections par le header http location*/
curl_setopt($c, CURLOPT_FOLLOWLOCATION, true);
/*On execute la requete*/
$output = curl_exec($c);
/*On a une erreur alors on la leve*/
if($output === false)
{
    trigger_error('Erreur curl : '.curl_error($c),E_USER_WARNING);
}
/*Si tout c'est bien passé on affiche le contenu de la requête*/
else
{
    var_dump($output);
}
/*On ferme la ressource*/ 
curl_close($c);
}

function read_header($url, $str) {
    echo 'Header : '.$str."\n";
    return strlen($str);
}

function requete_b($site='http://www.google.com') {
$url = curl_init();
curl_setopt($url, CURLOPT_URL, $site);
curl_setopt($url, CURLOPT_RETURNTRANSFER, true);
curl_setopt($url, CURLOPT_HEADER, true);
curl_setopt($url, CURLOPT_HEADERFUNCTION, 'read_header');
$page = curl_exec($url);
curl_close($url);
}

function scrappe_pole_emploi($html, $reference){
    $dom = new simple_html_dom();
    $dom->load($html);
    print_r($dom->plaintext);
    #$metier = $dom->find("span");
    #print_r($metier);
    #print trim($metier[0]->textplain);
    
    
    #save_key_value("reference", $reference, 2);
}

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

function scrappe_offre($html, $referenceb){
$dom = new simple_html_dom();
$dom->load($html);
$div = $dom->find("div.tx-sqliwebServiceanpe-pi5");
$span = $dom->find("div.tx-sqliwebServiceanpe-pi5 span.texteANPEDetail");
$actualisation = $span[1]->plaintext;
$record = array();
//'NumOffre_et_description' => $dom->find("div.tx-sqliwebServiceanpe-pi5 h3")->plaintext, //005FZJB - testeur / testeuse informatique

foreach($span as $data){
$text = htmlentities( (string) $data->plaintext, ENT_QUOTES, 'utf-8', FALSE);
    
    array_push($record, $text );
    #array_push($record, explode(' : ', $text, 2) );
    #$record[] = explode(' : ', $text, 2);
    $splited = array();
    $splited[] = explode(' : ', $text, 2);
    #print_r($splited);
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
}

}

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
foreach($dom_page2->find("ul.ANPE li") as $li){
    $a = $li->find("a", 0);
    $href = $a->href;
    $reference = $href[27].$href[28].$href[29].$href[30].$href[31].$href[32].$href[33]; //idOffre

    /* Scrapping de l'offre en question */
    $url_offre = "http://www.handicapzero.org/index.php?tache=Offre&idOffre=".$reference."&strReferences=".$reference."&fromPage=rechercheParRef&sess=&id=19966&reference=".$reference."&Submit=rechercher&sess=".$sess;
    $html = scraperWiki::scrape($url_offre);
    #scrappe_offre($html, $reference);

    /* Pré-scrapping 2 */
/*
Set-Cookie: Apache=10.10.225.10.1369752126491931; path=/; domain=.anpe.fr
Set-Cookie: JSESSIONID=RkCpLFL3hflHBd80wnvbCvz9Zyd5dNjhprdM1qsZwxTFNmHhHq4S!1398971125; path=/
*/
#requete();
 file_get_contents("http://www2.pole-emploi.fr/espacecandidat/nicola/InitialiserCriteresPartenaire.do");
var_dump($http_response_header);
$cookie = "";
foreach($http_response_header as $ligne){
    $analyse_entete = explode(':', $ligne, 2);
    if($analyse_entete[0] == "Set-Cookie")
        $cookie = $analyse_entete[1];
    }
$cookie = explode("=", $cookie);
$cookie = explode(";", $cookie[1]);
$JSESSIONID = $cookie[0];
#Cookie: JSESSIONID=RkdNbZfRRvLdpMYHX6Pkbm5nkv0Yym4MRXptdJbnqCX49Qx45xvb!-1636119155


    #iso-8859-1
   
    $html_pole_emploi = scrape_with_header("http://www2.pole-emploi.fr/espacecandidat/nicola/AfficherOffre.do?reference=".$reference.";jsessionid=".$JSESSIONID, $JSESSIONID);    
 #$html_pole_emploi = iconv("ISO-8859-1","UTF-8//IGNORE",$html_pole_emploi);
    #print $html_pole_emploi;
    scrappe_pole_emploi($html_pole_emploi, $reference); #todo : transformer $reference en un vrai string


    exit; #TODO : Commenter exit
}
?>