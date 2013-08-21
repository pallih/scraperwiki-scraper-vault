<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.turispain.com/oficina-turismo");

$dom = new simple_html_dom();
$dom->load($html);

$arr = array(); 
$key = array();
$arrProv = array();
$i = 0;

//$arrOfi = array('id_municipio'=>$i, 'datos_oficina'=>'Comienzo del proceso');

foreach ($dom->find('div.oficina_comunidad a') as $enlace){
    //array_push($arr, $enlace->plaintext);
    array_push($arr, $enlace->href);
    $html = scraperwiki::scrape('http://www.turispain.com/' .$enlace->href );
    
    $domCo = new simple_html_dom();
    $domCo->load($html);

    foreach ($domCo->find('div.oficina_provincia a') as $enlaceProv){
        array_push($arrProv, $enlaceProv->href);
        $html = scraperwiki::scrape('http://www.turispain.com/' .$enlaceProv->href );
        $domProv = new simple_html_dom();
        $domProv->load($html);
        
        
        foreach ($domProv->find('div.oficina_datos') as $datosOficina){
            echo $i .';'. trim(str_replace('<br>', '',$datosOficina->plaintext));
            //$record = array('id_oficina' => $i,'datos_oficina' => $datosOficina->plaintext);
            //scraperwiki::save_sqlite(array('id_oficina'), $record);          
            //scraperwiki::save_sqlite(array('id_oficina'),array('id_oficina'=>$i, 'datos_oficina'=>$datosOficina->plaintext));          
            //scraperwiki::save(array('id_oficina'), $record);
            $i++; 

        }
    }
}


?>