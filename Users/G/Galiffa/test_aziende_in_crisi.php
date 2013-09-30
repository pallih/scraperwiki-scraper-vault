<?php
    //Scraper che recupera tutti gli ID dei comuni pugliesi in merito alla raccolta rifiuti

    $comuni = array() ;

    require 'scraperwiki/simple_html_dom.php';
    

    function getItems()
    {
        $html = scraperWiki::scrape("http://racconta.repubblica.it/aziende-in-crisi-2012/database.php");
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("DIV.element") as $data)
        {
            echo "ABC" ;
            //$link = $data->href ;
            //$ato = str_replace ("ato.php?ato=","" ,$link) ;
            // getCitieListByATO($ato) ;
        }
        
    }

    function getCitieListByATO($p_atoCODE="")
    {
        $html = scraperWiki::scrape("http://www.rifiutiebonifica.puglia.it/dettaglio_differenziata.php?ato=" . $p_atoCODE . "&data=12");
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("table tr") as $data){
            $tds = $data->find("td");
            $a = $data->find("a") ;
        
            if(isset($a[0]))
            {
                $link = $a[0]->href ;
                $link = str_replace ("dettaglio_trasmissione.php?IdComune=","" ,$link) ;
                $position = strrpos($link,"&");
                $id = substr($link,0,$position) ;
                $ato = $p_atoCODE ;
                $comuni = array(
                'comune' => $tds[0]->plaintext, 
                'id' => $id
                );
                scraperwiki::save(array('id'), $comuni);
            }
        }
    }
    
   getItems();

?>
<?php
    //Scraper che recupera tutti gli ID dei comuni pugliesi in merito alla raccolta rifiuti

    $comuni = array() ;

    require 'scraperwiki/simple_html_dom.php';
    

    function getItems()
    {
        $html = scraperWiki::scrape("http://racconta.repubblica.it/aziende-in-crisi-2012/database.php");
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("DIV.element") as $data)
        {
            echo "ABC" ;
            //$link = $data->href ;
            //$ato = str_replace ("ato.php?ato=","" ,$link) ;
            // getCitieListByATO($ato) ;
        }
        
    }

    function getCitieListByATO($p_atoCODE="")
    {
        $html = scraperWiki::scrape("http://www.rifiutiebonifica.puglia.it/dettaglio_differenziata.php?ato=" . $p_atoCODE . "&data=12");
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("table tr") as $data){
            $tds = $data->find("td");
            $a = $data->find("a") ;
        
            if(isset($a[0]))
            {
                $link = $a[0]->href ;
                $link = str_replace ("dettaglio_trasmissione.php?IdComune=","" ,$link) ;
                $position = strrpos($link,"&");
                $id = substr($link,0,$position) ;
                $ato = $p_atoCODE ;
                $comuni = array(
                'comune' => $tds[0]->plaintext, 
                'id' => $id
                );
                scraperwiki::save(array('id'), $comuni);
            }
        }
    }
    
   getItems();

?>
