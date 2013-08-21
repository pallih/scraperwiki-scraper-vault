<?php
function scrappe_offre($html, $reference){
$dom = new simple_html_dom();
$dom->load($html);
$div = $dom->find("div.tx-sqliwebServiceanpe-pi5");
$span = $dom->find("div.tx-sqliwebServiceanpe-pi5 span.texteANPEDetail");
$actualisation = $span[1]->plaintext;
foreach($span as $data){
    $tds = $data->find("td");
    $record = array(
        //'NumOffre_et_description' => $dom->find("div.tx-sqliwebServiceanpe-pi5 h3")->plaintext, //005FZJB - testeur / testeuse informatique
        'actualiseJJ' => intval($actualisation[29].$actualisation[30]), //01 ou 1 le premier janvier ?
        'actualise le' => $actualisation,
        'type_contrat' => $span[5]->plaintext,
        'analyse_type_contrat' => "",
        'experiance' => $span[6]->plaintext
    );
    print json_encode($record) . "\n";
    #scraperwiki::save(array('contenu_offre'), $record);
}

#return ;
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
