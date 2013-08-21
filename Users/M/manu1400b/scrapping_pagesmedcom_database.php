<?php
/* Scrapping PagesMed.com database
 * @Author : Manu1400b
 */
// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';
$cle = 1;
$nombre_de_page_a_scrapper = 52077; //Modifier en conséquence le numéro MAX des pages à scrapper avec http://www.pagesmed.com/fr/recherche?page=1&query%5Bkeywords%5D=

for($page_souhaite = 1; $page_souhaite <= $nombre_de_page_a_scrapper; $page_souhaite++) {
    $url = "http://www.pagesmed.com/fr/recherche?page=".$page_souhaite."&query%5Bkeywords%5D=";
    
    $html = scraperwiki::scrape($url);
    //print $html;
    print "\n\nEND OF HTML\n\n"; 
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach ($dom->find('article.vcard') as $vcard){
    
    $nom = array();
    $street_adress = array(); 
    $locality = array();
    $postalcode = array();
    $telephone = array();
    $fax = array();
    $profession = array();

    $values = $vcard->find('span.tel span.value');
    if(isset($values[0]))
        array_push($telephone, str_replace(' ','',$values[0]->plaintext));
    if(isset($values[1]))
        array_push($fax, str_replace(' ','',$values[1]->plaintext));

    foreach ($vcard->find('header h3.fn a') as $a)
    array_push($nom, $a->plaintext);

    foreach ($vcard->find('p.street-address') as $p)
    array_push($street_adress, $p->plaintext);

    foreach ($vcard->find('span.postal-code') as $span)
    array_push($postalcode, $span->plaintext);

    foreach ($vcard->find('span.locality') as $span)
    array_push($locality, $span->plaintext);

    foreach ($vcard->find('p.position') as $p)
    array_push($profession, $p->plaintext);

    scraperwiki::save(array("a"),array("a"=>$cle, "nom"=>$nom[0], "profession"=>$profession[0], "telephone"=>$telephone[0], "fax"=>$fax[0], "adresse"=>$street_adress[0], "codepostal"=>$postalcode[0], "ville"=>$locality[0]));  
    $cle++;
}
/*
print_r($street_adress);
#print_r($telephone);
print_r($profession);
*/
unset($html, $dom);
#set_time_limit(...); #remet le compteur à zéro
}

/*
echo "telephone\n";
print_r($telephone);
echo "fax\n";
print_r($fax);
echo "nom\n";
print_r($nom);
*/
?>