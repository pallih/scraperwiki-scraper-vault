<?php

# Blank PHP
# http://www.midiproperty.com/properties-in-france/Languedoc-Roussillon/LE-CAP-DAGDE/Apartment/3414820113/

$host = "http://www.agence-centrale-immobilier.com/";
$firstSearchURL = "annonces/____Vente/acheter.html";

require 'scraperwiki/simple_html_dom.php';

listPage($host, $firstSearchURL);

function listPage($host, $searchURL)
{
    $html_content = scraperwiki::scrape($host . $searchURL);
    $html = str_get_html($html_content);
    
    $pageCount = 0;
       
    foreach ($html->find("div.photo ul.thumb a") as $el) 
    {
        $propPage = str_replace("../", "/", $el->href);
       // echo "\nPAGE :" . $propPage;
        $property = listProperty($host, $propPage);
        //scraperwiki::save_sqlite(array('property'), array('property' => json_encode($property))); 
        scraperwiki::save_sqlite(array('property'), $property); 
       // scraperwiki::save_sqlite(array("a"),array("a"=>1, "bbb"=>"Hi there"));

        exit;
    }

    foreach ($html->find("a.pageResults") as $el) 
    {
        if(trim($el->plaintext) == "Suivante")
        {
            $nextPage = $el->href;
            //echo "\nSEARCH : " . $nextPage;
            listPage($host, $nextPage);
            break;
        }
    }
}

function listProperty($host, $searchURL)
{
    $property = array();
    $html_content = scraperwiki::scrape($host . $searchURL);
    $html = str_get_html($html_content);

    //$el = $html->find("div.bien_description h3");
    //print_r($el);
    //$property['description'] = $el;
    
    foreach ($html->find("ul.galerie_photo a") as $el)
    {
        $imageURL = $el->href;
        $property['images'][] = $imageURL;
        //echo "\nIMAGE : " . $imageURL;
    }

    usleep(1000000);
    //echo "\n";
    //print json_encode($property);
    $property = array('property' => json_encode($property));
    return $property;
}

//class="pageResults" title=" Page Suivante "
//$el = $html->find("a.pageresults",0);
//print $el . "\n";

?>
