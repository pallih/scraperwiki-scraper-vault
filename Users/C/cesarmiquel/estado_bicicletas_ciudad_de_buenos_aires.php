<?php

# Blank PHP
$url = "http://www.bicicletapublica.com.ar/mapa.aspx";

$pattern = '/span class="style1"\>([[:upper:][:space:]]*)(<br>[[:alnum:].:[:space:]]*)?\<\/span><br><span class="style2"\>Cant. Bicicletas disponibles: (\d+)\<\/span\>\<br\>\<\/div\>/';

$page = scraperwiki::scrape($url);

// remove accents
$page = str_replace('ó', 'o', $page);
$page = str_replace('á', 'a', $page);

preg_match_all( $pattern , $page , $matches );

// armarmos array con datos
$estaciones = $matches[1];
$estados    = $matches[2];
$cant_bicis = $matches[3];

$result = array();
foreach($estaciones as $i => $estacion) {
    $row = array(
        'nombre' => $estacion,
        'estado' => $estados[$i],
        'cant_bicis' => (int) $cant_bicis[$i]
    );
    scraperwiki::save_sqlite(array('nombre'), $row);
}

?>
