<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.movilesydispositivos.movistar.es/web/movistar/renueva-el-movil-particulares?p_p_id=MovistarMoviles_WAR_MovistarMovilesportlet_INSTANCE_u9P9&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=main&p_p_col_count=1&accion=&cantPaginas=3&comboNumero1=100&comboNumero2=100&idsCaracteristicasHidden=&idsComparadorHidden=&idsMarcasHidden=&numero=100&outlet=0&pag=1&palancaFiltro=&precio-modificador=0&precio-modificador=0&pregunta1=&pregunta1_a=0&pregunta1_b=0&pregunta2=&pregunta3=&puntos-modificador=0&textPag1=1&textPag2=1&tipoOferta=&urlCatalogo=renueva%20el%20movil%20particulares&urlComparador=");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('<li class="movil-listado">') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>