<?php
require 'scraperwiki/simple_html_dom.php';  

$htmlGEN = scraperWiki::scrape("http://www.turismocehegin.es/listaalojamientos.php?idtipo=3");           

         
$dom = new simple_html_dom();
$dom->load($htmlGEN );
foreach($dom->find("div.botoninfo a") as $data){
    echo $data->href;
    
    $htmlAlojamiento = scraperWiki::scrape("http://www.turismocehegin.es/" .$data->href);
    $domAlo = new simple_html_dom();
    $domAlo->load($htmlAlojamiento);
    if (count($domAlo) > 0){
        foreach($domAlo->find("table.tabladetalle tr") as $tabla){
            
        }
    }
    //$a = $data->children(1);
    //echo $a;
    /*if(count($tds)==12){
        $record = array(
            'country' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
        print json_encode($record) . "\n";
    }*/
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';  

$htmlGEN = scraperWiki::scrape("http://www.turismocehegin.es/listaalojamientos.php?idtipo=3");           

         
$dom = new simple_html_dom();
$dom->load($htmlGEN );
foreach($dom->find("div.botoninfo a") as $data){
    echo $data->href;
    
    $htmlAlojamiento = scraperWiki::scrape("http://www.turismocehegin.es/" .$data->href);
    $domAlo = new simple_html_dom();
    $domAlo->load($htmlAlojamiento);
    if (count($domAlo) > 0){
        foreach($domAlo->find("table.tabladetalle tr") as $tabla){
            
        }
    }
    //$a = $data->children(1);
    //echo $a;
    /*if(count($tds)==12){
        $record = array(
            'country' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
        print json_encode($record) . "\n";
    }*/
}

?>
