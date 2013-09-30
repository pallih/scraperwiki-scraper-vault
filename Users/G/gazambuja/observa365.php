<?php


#http://www.elobservador365.com.uy/index.php?option=com_virtuemart&category_id=19&page=shop.browse&Itemid=71&limitstart=0&limit=50
require 'scraperwiki/simple_html_dom.php';
 
for ($i = 20; $i <= 31; $i++) {
    $html_content = scraperwiki::scrape("http://www.elobservador365.com.uy/index.php?option=com_virtuemart&category_id={$i}&page=shop.browse&limitstart=0&limit=500");
    $html = str_get_html($html_content);
    
    $campo = $html->find("h3.categoryName", 0);
    $categoria = $campo->innertext;
    
    foreach ($html->find("div.leftPosition") as $fila) {
    
            $titulo = $fila->find("h2.browseProductTitle a[title]", 0)->title;

            $url = $fila->find("h2.browseProductTitle a[title]", 0)->href;
            $product_id = strstr($url, 'product_id=');
            $product_id = strstr($product_id, '&', true);
            $product_id = explode("=", $product_id);
            $product_id = $product_id[1];

            $itemid = strstr($url, 'product_id=');
            $itemid = strstr($itemid, '&', true);
            $itemid = explode("=", $itemid);
            $itemid = $itemid[1];
    
            $campo = $fila->find("p.texto_beneficio", 0);
            $beneficio = $campo->innertext;
    
            $campo = $fila->find("div.browseProductDescription", 0);
            $description = $campo->innertext;

            $subhtml_content = scraperwiki::scrape("http://www.elobservador365.com.uy{$url}");
            $subhtml = str_get_html($subhtml_content);
            
            $terminos = $subhtml->find("div.terminos_y_condiciones p", 0);
            if($terminos) $terminos = $terminos->innertext;
            else $terminos = '';

            $campo = $subhtml->find("div.browseProductImage img", 0);
            $imagen = $campo->src;

            $datos = $subhtml->find('div[style="float:right; width:250px; border-left: solid 1px #e8e8e8; padding-left:10px;"]', 0);
            if($datos) $valido = str_replace('<strong class="subtitulo">Válido hasta:</strong> <br /> ', '', $datos->innertext);
            else $valido = '';

            $registro = array (
                'empresa' => $titulo,
                'url' => $url,
                'categoria' => $categoria,
                'idCategoria' => $i,
                'idProduct' => $product_id,
                'idItem' => $itemid,
                'imagen' => $imagen,
                'beneficio' => $beneficio,
                'description' => $description,
                'terminos' => $terminos,
                'valido' => $valido
            );
    
            scraperwiki::save(array('idProduct'), $registro);
    
    }
}


?>
<?php


#http://www.elobservador365.com.uy/index.php?option=com_virtuemart&category_id=19&page=shop.browse&Itemid=71&limitstart=0&limit=50
require 'scraperwiki/simple_html_dom.php';
 
for ($i = 20; $i <= 31; $i++) {
    $html_content = scraperwiki::scrape("http://www.elobservador365.com.uy/index.php?option=com_virtuemart&category_id={$i}&page=shop.browse&limitstart=0&limit=500");
    $html = str_get_html($html_content);
    
    $campo = $html->find("h3.categoryName", 0);
    $categoria = $campo->innertext;
    
    foreach ($html->find("div.leftPosition") as $fila) {
    
            $titulo = $fila->find("h2.browseProductTitle a[title]", 0)->title;

            $url = $fila->find("h2.browseProductTitle a[title]", 0)->href;
            $product_id = strstr($url, 'product_id=');
            $product_id = strstr($product_id, '&', true);
            $product_id = explode("=", $product_id);
            $product_id = $product_id[1];

            $itemid = strstr($url, 'product_id=');
            $itemid = strstr($itemid, '&', true);
            $itemid = explode("=", $itemid);
            $itemid = $itemid[1];
    
            $campo = $fila->find("p.texto_beneficio", 0);
            $beneficio = $campo->innertext;
    
            $campo = $fila->find("div.browseProductDescription", 0);
            $description = $campo->innertext;

            $subhtml_content = scraperwiki::scrape("http://www.elobservador365.com.uy{$url}");
            $subhtml = str_get_html($subhtml_content);
            
            $terminos = $subhtml->find("div.terminos_y_condiciones p", 0);
            if($terminos) $terminos = $terminos->innertext;
            else $terminos = '';

            $campo = $subhtml->find("div.browseProductImage img", 0);
            $imagen = $campo->src;

            $datos = $subhtml->find('div[style="float:right; width:250px; border-left: solid 1px #e8e8e8; padding-left:10px;"]', 0);
            if($datos) $valido = str_replace('<strong class="subtitulo">Válido hasta:</strong> <br /> ', '', $datos->innertext);
            else $valido = '';

            $registro = array (
                'empresa' => $titulo,
                'url' => $url,
                'categoria' => $categoria,
                'idCategoria' => $i,
                'idProduct' => $product_id,
                'idItem' => $itemid,
                'imagen' => $imagen,
                'beneficio' => $beneficio,
                'description' => $description,
                'terminos' => $terminos,
                'valido' => $valido
            );
    
            scraperwiki::save(array('idProduct'), $registro);
    
    }
}


?>
