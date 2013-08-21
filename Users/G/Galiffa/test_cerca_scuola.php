<?php
    // TEST PER SCUOLE ITALIANE

    /*
    URL per dettaglio scuola:
    http://cercalatuascuola.istruzione.it/scuolaInChiaro/home/start.do?p1=CHAA01801V&p2=201112
    */

    $regioni = array() ;
    $province = array() ;
    $comuni = array() ;
    $scuole = array() ;

    require 'scraperwiki/simple_html_dom.php';
    
    function getRegioni()
    {
        $html = scraperWiki::scrape("http://cercalatuascuola.istruzione.it/cercalatuascuola/ricercaAvanzata/start.do");
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("option [select#codiceRegione]") as $data)
        {
            // $a = $data->find("a") ;
            if($data->value != "")
            {
                $id = substr($data->value,0,2) ;
                $regioni = array(
                'regione' => $data->plaintext,
                'id' => $id 
                );

                getProvinceByRegione($id) ;
            }
        }
    }


    function getProvinceByRegione($p_regioneID="")
    {
        $html = scraperWiki::scrape("http://cercalatuascuola.istruzione.it/cercalatuascuola/jsp/common/caricaProvincia.jsp?codiceRegione=" . $p_regioneID);
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("option") as $data)
        {
            // $a = $data->find("a") ;
            if($data->value != "")
            {
                $id = substr($data->value,0,2) ;
                $province = array(
                'provincia' => $data->plaintext,
                'id' => $id,
                'regione' => $p_regioneID
                );

                getComuniByProvincia($id,$p_regioneID) ;
            }
        }
    }

   
    
    function getComuniByProvincia($p_provinciaID="",$p_regioneID="")
    {
        $html = scraperWiki::scrape("http://cercalatuascuola.istruzione.it/cercalatuascuola/jsp/common/caricaComune.jsp?codiceProvincia=" . $p_provinciaID);
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("option") as $data)
        {
            // $a = $data->find("a") ;
            if($data->value != "")
            {
                $id = substr($data->value,0,2) ;
                $comuni = array(
                'comune' => $data->plaintext,
                'id' => $id,
                'provincia' => $p_provinciaID,
                'regione' => $p_regioneID
                );

                // scraperwiki::save(array('id'), $comuni);
            }
        }
    }
    

    
   getRegioni();


?>
