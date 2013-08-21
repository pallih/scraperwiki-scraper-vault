<?php
mail('alquiler@yanoo.com', 'scrapper', 'ksafg fksa jfgksajf kasjf gksfj hkf sdjkg');
exit;
require 'scraperwiki/simple_html_dom.php';           

#$html = scraperWiki::scrape("https://www.bankiahabitat.es/compra/vivienda/todos/madrid/listado");   
$base_url = "https://www.bankiahabitat.es";
$html = scraperWiki::scrape($base_url . "/compra/vivienda/todos/madrid/norte/localidad/280060001/listado");

#preg_match_all('#<a class="i-profile-thumb" .+? href="(.+?\?ref.+?)">#',$html_data, $results_url);
#<td headers="direccion
preg_match_all('#<td headers="direccion inmueble(.+?)<div id="datosMantenimientoBusqueda." class="oculto">#sm',$html, $matches);
//print_r($matches);


$dom = new simple_html_dom();
$dom->load($html);
$title = $dom->find("title", 0)->plaintext;
#print $title . "\n";
#$html = $dom->find('table.tabla-resultadosBusqueda tr',0);


#---

$html_el = $dom->find("table.tabla-resultadosBusqueda tbody",0);           
foreach ($html_el->children() as $child1) {
    print $child1->tag . "\n";
    foreach ($child1->children() as $child2) {
        print "-- " . $child2->tag . " ";
        print json_encode($child2->attr) . "\n";
    }
}
print "otra cosa\n\n\n\n";

$html_el = $dom->find("table.tabla-resultadosBusqueda");           
foreach ($html_el as $child1) {
    print $child1 . "\n";
}

#----
exit;
foreach($dom->find("table.tabla-resultadosBusqueda tr") as $tr){
    #$tds = $data->find("td");
print $tr->plaintext;
}

print $html;
exit;
$address = $dom->find('table td[headers=direccion]', 0);
print $address . "\n";

exit;
$first_result = $dom->find("table.tabla-resultadosBusqueda tr td#inmueble0 a.mantieneBusqueda", 0)->href;
#$first_result = $first_result->href;
print $base_url . $first_result . "\n";
$html = scraperWiki::scrape($base_url . $first_result);   
#print $html;
$dom->load($html);
$title = $dom->find("title", 0)->plaintext;
print $title . "\n";

#$next_page = $dom->find("a.siguiente", 0)->href;
$next_page = $dom->find("div.contenido_tr div.mv-c09 div#fichaProducto", 0);
print $next_page ."\n";
print $base_url . $next_page;
  #preg_match_all('#<a class="i-profile-thumb" .+? href="(.+?\?ref.+?)">#',$html_data, $results_url);

preg_match('#<a class="siguiente mantieneBusqueda datosEn_datosMantenimientoBusquedaSiguiente" href="(.+?)">Anuncio siguiente</a>#', $html, $matches);
print "\nPos: ". strpos($html,'11500300')."\n";

print_r($matches);

#//*[@id="fichaProducto"]/div[1]/p/a


#foreach($dom->find("table.tabla-resultadosBusqueda tr td#inmueble0 a.mantieneBusqueda") as $first_result){
#    $tds = $data->find("td");
#    if(count($tds)==12){
#        $record = array(
#            'country' => $tds[0]->plaintext, 
#            'years_in_school' => intval($tds[4]->plaintext)
#        );
#        scraperwiki::save(array('country'), $record);     }
#}
?>
