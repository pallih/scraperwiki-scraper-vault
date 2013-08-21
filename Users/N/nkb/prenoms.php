<?php

require_once 'scraperwiki/simple_html_dom.php';  

$last_id = 0;

$last_id_array = scraperwiki::sqliteexecute("select max(id) from swdata");

if ($last_id_array)
    $last_id = $last_id_array->data[0][0];

if ($last_id<10){

    $last_id = 11;

}

if ($last_id>10){

    for ($num = $last_id; $num<=$last_id+100; $num++){
    
        $html = scraperWiki::scrape("http://www.journaldesfemmes.com/prenoms/prenom/". $num ."/");
        $dom = new simple_html_dom();
    
        $dom->load($html);
    
        foreach($dom->find("#tableau_graphique td img[alt]") as $data){
            
            $alt = $data->alt;
            $pattern = "/(\d*) (.*?) en (\d{4})/";
            if(preg_match($pattern, $alt, $match)){
                $quantite = $match[1];
                $prenom = $match[2];
                $annee = $match[3];
                
                if ($quantite>0){

                    $triple = array(
                        "id" => $num,
                        "prenom" => $prenom,
                        "annee" => $annee,
                        "quantite" => $quantite
                    );
                    
                    scraperwiki::save_sqlite(array("id", "annee"), $triple);  
                } 
            }
        }
    }

}

?>
