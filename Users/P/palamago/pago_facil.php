<?php

require 'scraperwiki/simple_html_dom.php';    

class PFParser {
    
    var $sucUrl = 'http://www.e-pagofacil.com.ar/espanol/site/donde_pago.php?accion=listado&localidad={localidad}&provincia={provincia}';

    var $detUrl = 'http://www.e-pagofacil.com.ar/espanol/site/donde_pago.php?accion=detalle&id={sucursal}';

    var $geoUrl = 'http://maps.google.com/maps/api/geocode/json?address={direccion},{localidad},{provincia},Argentina&sensor=false';

    function init() {

        $this->parseSuc();

    }

    function parseSuc(){
   
        scraperwiki::attach("sucursales_pago_facil");            
        $localidades = scraperwiki::select("* from sucursales_pago_facil.localidad");

        foreach ($localidades as $l) {

            //Obtengo el id de la sucursal
            $html_content = scraperwiki::scrape(str_replace(array('{localidad}','{provincia}'),array($l['id'],$l['id_provincia']),$this->sucUrl));
            $html = str_get_html($html_content);
            $table = $html->find('.DondePago2Listado table');
            
            $temp = array();

            foreach ($table[0]->find('td') as $el) {
               
                if($el->plaintext!='no disponible'){
   
                    if($el->height == '15'){
                        //completo nombre
                        $id = $this->parseId($el);                    
                        $temp[$id] = array();
                        $temp[$id]['id'] = $id;
                        $nombre = $el->find('a');
                        $nombre = $nombre[0]->innertext;
                        $temp[$id]['nombre'] = $nombre;
    
                    } else if ($el->width == '300'){
                        //completo dire
                        $id = $this->parseId($el);
                        $direccion = $el->find('a');
                        $direccion = $direccion[0]->innertext;
                        $temp[$id]['direccion'] = $direccion;
                        $temp[$id]['provincia'] = $l['provincia'];
                        $temp[$id]['localidad'] = $l['nombre'];
                        $temp[$id]['id_localidad'] = $l['id'];
                        $temp[$id]['id_provincia'] = $l['id_provincia'];
    
                        $url = str_replace(array('{direccion}','{localidad}','{provincia}'),array($direccion,$l['nombre'],$l['provincia']),$this->geoUrl);
    
                        $ch = curl_init();
                        curl_setopt($ch, CURLOPT_URL, str_replace(' ','+',$url));
                        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
                        curl_setopt($ch, CURLOPT_PROXYPORT, 3128);
                        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
                        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
                        $response = curl_exec($ch);
                        curl_close($ch);
                        $response_a = json_decode($response);
    
                        $response_a = $response_a->results[0]->geometry->location;
                        
                        $temp[$id]['lat'] = $response_a->lat;
                        $temp[$id]['lng'] = $response_a->lng;
                        
                        //scraperwiki::save_sqlite(array("id"=>$id), $temp[$id], "sucursal");
                    
                        $this->parseDetails($temp[$id]);
        
                        unset($temp[$id]);
    
                    }

                }
             
            }
 
        }

        $html->__destruct();

    }

    function parseId($el){
        $a = $el->find('a');
        $id = $a[0]->href;            
        $id = explode('&id=',$id);
        return $id[1];
    }

    //Detalle de la sucursal

    function parseDetails($l){

        $html_content = scraperwiki::scrape(str_replace('{sucursal}',$l['id'],$this->detUrl));

        $html = str_get_html($html_content);
        $table = $html->find('.DondePago3 table');
        $table = $table[0];
        $table = $table->find('tr [height="15"]'); 
        $table = $table[0];

        $r = $table->find('p');
        $r = $r[0]->plaintext;

        $r = explode("Rubro:",$r);
        $r = $r[1];
        $r = explode("> Localidad:",$r);
        $r = trim($r[0]);  

        $l['rubro'] = str_replace('BANCARIASCENTROS','BANCARIAS CENTROS ',$r);            

        $h = $table->find('h1');
        $h = $h[0]->plaintext;

        $l['horario'] = $h;

        scraperwiki::save_sqlite(array("id"=>$l['id']), $l, "sucursal");
        
        $html->__destruct();
    
    }

}

$parser = new PFParser();

$parser->init();


?>
<?php

require 'scraperwiki/simple_html_dom.php';    

class PFParser {
    
    var $sucUrl = 'http://www.e-pagofacil.com.ar/espanol/site/donde_pago.php?accion=listado&localidad={localidad}&provincia={provincia}';

    var $detUrl = 'http://www.e-pagofacil.com.ar/espanol/site/donde_pago.php?accion=detalle&id={sucursal}';

    var $geoUrl = 'http://maps.google.com/maps/api/geocode/json?address={direccion},{localidad},{provincia},Argentina&sensor=false';

    function init() {

        $this->parseSuc();

    }

    function parseSuc(){
   
        scraperwiki::attach("sucursales_pago_facil");            
        $localidades = scraperwiki::select("* from sucursales_pago_facil.localidad");

        foreach ($localidades as $l) {

            //Obtengo el id de la sucursal
            $html_content = scraperwiki::scrape(str_replace(array('{localidad}','{provincia}'),array($l['id'],$l['id_provincia']),$this->sucUrl));
            $html = str_get_html($html_content);
            $table = $html->find('.DondePago2Listado table');
            
            $temp = array();

            foreach ($table[0]->find('td') as $el) {
               
                if($el->plaintext!='no disponible'){
   
                    if($el->height == '15'){
                        //completo nombre
                        $id = $this->parseId($el);                    
                        $temp[$id] = array();
                        $temp[$id]['id'] = $id;
                        $nombre = $el->find('a');
                        $nombre = $nombre[0]->innertext;
                        $temp[$id]['nombre'] = $nombre;
    
                    } else if ($el->width == '300'){
                        //completo dire
                        $id = $this->parseId($el);
                        $direccion = $el->find('a');
                        $direccion = $direccion[0]->innertext;
                        $temp[$id]['direccion'] = $direccion;
                        $temp[$id]['provincia'] = $l['provincia'];
                        $temp[$id]['localidad'] = $l['nombre'];
                        $temp[$id]['id_localidad'] = $l['id'];
                        $temp[$id]['id_provincia'] = $l['id_provincia'];
    
                        $url = str_replace(array('{direccion}','{localidad}','{provincia}'),array($direccion,$l['nombre'],$l['provincia']),$this->geoUrl);
    
                        $ch = curl_init();
                        curl_setopt($ch, CURLOPT_URL, str_replace(' ','+',$url));
                        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
                        curl_setopt($ch, CURLOPT_PROXYPORT, 3128);
                        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
                        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
                        $response = curl_exec($ch);
                        curl_close($ch);
                        $response_a = json_decode($response);
    
                        $response_a = $response_a->results[0]->geometry->location;
                        
                        $temp[$id]['lat'] = $response_a->lat;
                        $temp[$id]['lng'] = $response_a->lng;
                        
                        //scraperwiki::save_sqlite(array("id"=>$id), $temp[$id], "sucursal");
                    
                        $this->parseDetails($temp[$id]);
        
                        unset($temp[$id]);
    
                    }

                }
             
            }
 
        }

        $html->__destruct();

    }

    function parseId($el){
        $a = $el->find('a');
        $id = $a[0]->href;            
        $id = explode('&id=',$id);
        return $id[1];
    }

    //Detalle de la sucursal

    function parseDetails($l){

        $html_content = scraperwiki::scrape(str_replace('{sucursal}',$l['id'],$this->detUrl));

        $html = str_get_html($html_content);
        $table = $html->find('.DondePago3 table');
        $table = $table[0];
        $table = $table->find('tr [height="15"]'); 
        $table = $table[0];

        $r = $table->find('p');
        $r = $r[0]->plaintext;

        $r = explode("Rubro:",$r);
        $r = $r[1];
        $r = explode("> Localidad:",$r);
        $r = trim($r[0]);  

        $l['rubro'] = str_replace('BANCARIASCENTROS','BANCARIAS CENTROS ',$r);            

        $h = $table->find('h1');
        $h = $h[0]->plaintext;

        $l['horario'] = $h;

        scraperwiki::save_sqlite(array("id"=>$l['id']), $l, "sucursal");
        
        $html->__destruct();
    
    }

}

$parser = new PFParser();

$parser->init();


?>
