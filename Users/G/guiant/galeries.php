<?php

$html = scraperWiki::scrape("http://www.artbrussels.be/en/Galleries/Gallery");           

require 'scraperwiki/simple_html_dom.php';           

// get page
function loadPageGallery($url) {


    $htmlGallery = scraperWiki::scrape($url);           
            
    $domGallery = new simple_html_dom();
    $domGallery->load($htmlGallery);

    foreach($domGallery->find("div#contentDetail1") as $data){
            
                $title = $data->find("h3");
                $adressclass = $data->find('.adres');
                $urlandemail = $data->find('.adres a');
                $artists = $data->find('.artists');


                $contactName = explode("\n", $adressclass[0]->plaintext);
                list($contactNameGallery) = $contactName;

                $tels = explode("\n", $adressclass[4]->plaintext);
                list($tel1, $tel2) = $tels;

                $record = array(
                    'name' => $title[0]->plaintext,
                    'contact' => $contactNameGallery,
                    'url' => $urlandemail[0]->plaintext,
                    'email' => $urlandemail[1]->plaintext,
                    'address' => $adressclass[1]->plaintext,
                    'tel1' => $tel1,
                    'tel2' => $tel2,
                    'artists' => $artists[0]->plaintext
                );
        
                scraperwiki::save(array('name', 'contact', 'url', 'email', 'address', 'tel1', 'tel2', 'artists'), $record);
                //print_r($record);
    
    }


}

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div#contentHolder a") as $data){
        
           loadPageGallery($data->href);

}


?>
<?php

$html = scraperWiki::scrape("http://www.artbrussels.be/en/Galleries/Gallery");           

require 'scraperwiki/simple_html_dom.php';           

// get page
function loadPageGallery($url) {


    $htmlGallery = scraperWiki::scrape($url);           
            
    $domGallery = new simple_html_dom();
    $domGallery->load($htmlGallery);

    foreach($domGallery->find("div#contentDetail1") as $data){
            
                $title = $data->find("h3");
                $adressclass = $data->find('.adres');
                $urlandemail = $data->find('.adres a');
                $artists = $data->find('.artists');


                $contactName = explode("\n", $adressclass[0]->plaintext);
                list($contactNameGallery) = $contactName;

                $tels = explode("\n", $adressclass[4]->plaintext);
                list($tel1, $tel2) = $tels;

                $record = array(
                    'name' => $title[0]->plaintext,
                    'contact' => $contactNameGallery,
                    'url' => $urlandemail[0]->plaintext,
                    'email' => $urlandemail[1]->plaintext,
                    'address' => $adressclass[1]->plaintext,
                    'tel1' => $tel1,
                    'tel2' => $tel2,
                    'artists' => $artists[0]->plaintext
                );
        
                scraperwiki::save(array('name', 'contact', 'url', 'email', 'address', 'tel1', 'tel2', 'artists'), $record);
                //print_r($record);
    
    }


}

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div#contentHolder a") as $data){
        
           loadPageGallery($data->href);

}


?>
