<?php

require 'scraperwiki/simple_html_dom.php';  

$lista_precios = array();

for($i=1001;$i<=1379;$i++){   
    print("Página: ".$i."\n");   
    $html = scraperWiki::scrape("http://motos.honda.com.co/resultadosBusquedaRedDistribucion/precios.php?pagesNum=1384&pageNum=".$i);
    $dom = new simple_html_dom();
    $dom->load($html);

foreach($dom->find('tr') as $data){

        $ref = $data->children(0)->innertext;
        $desc =  $data->children(1)->innertext;
        $precio =  $data->children(2)->innertext;
        $modelo =  $data->children(3)->innertext;

    $lista_precio = array(
       "ref" => $ref,
       "desc" => $desc,
       "precio" =>intval(str_replace(",","",(str_replace("$","",$precio)))),
       "modelo" => $modelo
    );

    $lista_precios[] = $lista_precio;
  }
  $dom->__destruct();
}

scraperwiki::save(array("ref"), $lista_precios);

?>
<?php

require 'scraperwiki/simple_html_dom.php';  

$lista_precios = array();

for($i=1001;$i<=1379;$i++){   
    print("Página: ".$i."\n");   
    $html = scraperWiki::scrape("http://motos.honda.com.co/resultadosBusquedaRedDistribucion/precios.php?pagesNum=1384&pageNum=".$i);
    $dom = new simple_html_dom();
    $dom->load($html);

foreach($dom->find('tr') as $data){

        $ref = $data->children(0)->innertext;
        $desc =  $data->children(1)->innertext;
        $precio =  $data->children(2)->innertext;
        $modelo =  $data->children(3)->innertext;

    $lista_precio = array(
       "ref" => $ref,
       "desc" => $desc,
       "precio" =>intval(str_replace(",","",(str_replace("$","",$precio)))),
       "modelo" => $modelo
    );

    $lista_precios[] = $lista_precio;
  }
  $dom->__destruct();
}

scraperwiki::save(array("ref"), $lista_precios);

?>
