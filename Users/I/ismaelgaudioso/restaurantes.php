<?php

require 'scraperwiki/simple_html_dom.php';  

$restaurantes = array();

for($i=1;$i<=6;$i++){   
    print("Página: ".$i."\n");   
    $html = scraperWiki::scrape("http://www.comermuybien.com/listado.php?pagina=".$i."&merindad=1");
    $dom = new simple_html_dom(); 
    $dom->load($html); 
    foreach($dom->find("div.ico strong a") as $data){ 
        $url_rest = "http://www.comermuybien.com/".$data->href;
        $html_rest = scraperWiki::scrape($url_rest);
        $dom_rest = new simple_html_dom(); 
        $dom_rest -> load($html_rest);
        $nombre_rest = $dom_rest->find("div.datos h2 strong",0)->innertext;
        
        $datos_rest = $dom_rest->find("div.datos p");
    
        $posicion_corte = strpos($datos_rest[0]->innertext,"</strong>")+9;
        $direccion_rest = substr($datos_rest[0]->innertext,$posicion_corte);
        
        $posicion_corte = strpos($datos_rest[1]->innertext,"</strong>")+9;
        $telefono_rest = substr($datos_rest[1]->innertext,$posicion_corte,9);
    
        $posicion_corte = strpos($datos_rest[1]->innertext,"e-mail:</strong>")+16;
        if($posicion_corte > 16){
            $email_rest = substr($datos_rest[1]->innertext,$posicion_corte);
        }else{
            $email_rest = "";
        }

        $iframe = $dom_rest->find("div.TabbedPanelsContent iframe");
        $posicion_corte = strpos($iframe[0]->src,"ll=")+3;
        $coords_rest = substr($iframe[0]->src,$posicion_corte);
        $posicion_corte = strpos($coords_rest,"&");
        $coords_rest = substr($coords_rest,0,$posicion_corte);
        $coords = explode(",",$coords_rest);

        $lat_rest = $coords[0];
        $lon_rest = $coords[1];
        
        $web_rest = $dom_rest->find("span.url a.external");
        if($web_rest)
            $web_rest = $web_rest[0]->href;
        else
            $web_rest = "";

        $type_rest = $dom_rest->find("div.col_02 p");
        $type_rest = $type_rest[0]->innertext;

        $desc_rest = $dom_rest->find("div.col_02");
        $posicion_corte = strpos($desc_rest[1]->innertext,"Descripci")+54;
        $desc_rest = strip_tags(substr($desc_rest[1]->innertext,$posicion_corte));
        $desc_rest = $type_rest . " - " . $desc_rest;
    
        $restaurante = array(
            "nombre"=>utf8_encode($nombre_rest),
            "direccion"=>utf8_encode($direccion_rest),
            "telefono"=>$telefono_rest,
            //"web"=>$web_rest,
            //"email"=>$email_rest,
            "descripcion"=>utf8_encode($desc_rest),
            "lattitude"=>$lat_rest,
            "longitude"=>$lon_rest     
        );

        
    
        $restaurantes[] = $restaurante;
        $dom_rest->__destruct();
    }    
    $dom->__destruct();
}
scraperwiki::save(array('nombre'), $restaurantes); 

?>
<?php

require 'scraperwiki/simple_html_dom.php';  

$restaurantes = array();

for($i=1;$i<=6;$i++){   
    print("Página: ".$i."\n");   
    $html = scraperWiki::scrape("http://www.comermuybien.com/listado.php?pagina=".$i."&merindad=1");
    $dom = new simple_html_dom(); 
    $dom->load($html); 
    foreach($dom->find("div.ico strong a") as $data){ 
        $url_rest = "http://www.comermuybien.com/".$data->href;
        $html_rest = scraperWiki::scrape($url_rest);
        $dom_rest = new simple_html_dom(); 
        $dom_rest -> load($html_rest);
        $nombre_rest = $dom_rest->find("div.datos h2 strong",0)->innertext;
        
        $datos_rest = $dom_rest->find("div.datos p");
    
        $posicion_corte = strpos($datos_rest[0]->innertext,"</strong>")+9;
        $direccion_rest = substr($datos_rest[0]->innertext,$posicion_corte);
        
        $posicion_corte = strpos($datos_rest[1]->innertext,"</strong>")+9;
        $telefono_rest = substr($datos_rest[1]->innertext,$posicion_corte,9);
    
        $posicion_corte = strpos($datos_rest[1]->innertext,"e-mail:</strong>")+16;
        if($posicion_corte > 16){
            $email_rest = substr($datos_rest[1]->innertext,$posicion_corte);
        }else{
            $email_rest = "";
        }

        $iframe = $dom_rest->find("div.TabbedPanelsContent iframe");
        $posicion_corte = strpos($iframe[0]->src,"ll=")+3;
        $coords_rest = substr($iframe[0]->src,$posicion_corte);
        $posicion_corte = strpos($coords_rest,"&");
        $coords_rest = substr($coords_rest,0,$posicion_corte);
        $coords = explode(",",$coords_rest);

        $lat_rest = $coords[0];
        $lon_rest = $coords[1];
        
        $web_rest = $dom_rest->find("span.url a.external");
        if($web_rest)
            $web_rest = $web_rest[0]->href;
        else
            $web_rest = "";

        $type_rest = $dom_rest->find("div.col_02 p");
        $type_rest = $type_rest[0]->innertext;

        $desc_rest = $dom_rest->find("div.col_02");
        $posicion_corte = strpos($desc_rest[1]->innertext,"Descripci")+54;
        $desc_rest = strip_tags(substr($desc_rest[1]->innertext,$posicion_corte));
        $desc_rest = $type_rest . " - " . $desc_rest;
    
        $restaurante = array(
            "nombre"=>utf8_encode($nombre_rest),
            "direccion"=>utf8_encode($direccion_rest),
            "telefono"=>$telefono_rest,
            //"web"=>$web_rest,
            //"email"=>$email_rest,
            "descripcion"=>utf8_encode($desc_rest),
            "lattitude"=>$lat_rest,
            "longitude"=>$lon_rest     
        );

        
    
        $restaurantes[] = $restaurante;
        $dom_rest->__destruct();
    }    
    $dom->__destruct();
}
scraperwiki::save(array('nombre'), $restaurantes); 

?>
