<?php

require 'scraperwiki/simple_html_dom.php';    

class PFParser {
    
    var $mainUrl = 'http://www.e-pagofacil.com.ar/espanol/site/donde_pago.php';

    var $locUrl = 'http://www.e-pagofacil.com.ar/espanol/site/donde_pago.php?provincia={provincia}';

    var $prov = array();

    var $suc = array();

    function init() {
        $this->prov = array();
        $this->loc = array();  

        $this->parseProv();

        $this->parseLoc();
    }

    function parseProv(){
        $html_content = scraperwiki::scrape($this->mainUrl);

        $html = str_get_html($html_content);
    
        foreach ($html->find("#provincia option") as $el) {
            
            if($el->value != 'XX'){
                $p['id'] = $el->value;
                $p['nombre'] = $el->innertext;
                $this->prov[$p['id']] = $p['nombre'];
                scraperwiki::save_sqlite(array("id"=>$p['id']), $p, "provincia");
            }
 
        }
        
        $html->__destruct();
    }
    
    function parseLoc(){
        foreach ($this->prov as $id => $nombre) {
            
            $html_content = scraperwiki::scrape(str_replace('{provincia}',$id,$this->locUrl));

            $html = str_get_html($html_content);
        
            echo count($html->find("#localidad option"));

            foreach ($html->find("#localidad option") as $el) {
       
                if($el->value != 'XX'){
                    $l['id'] = $el->value;
                    $l['provincia'] = $nombre;
                    $l['id_provincia'] = $id;
                    $l['nombre'] = $el->innertext;
                    scraperwiki::save_sqlite(array("id"=>$l['id']), $l, "localidad");
                }
             
            }

            $html->__destruct();
            
        }

    }

}

$parser = new PFParser();

$parser->init();


?>
