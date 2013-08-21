<?php
require 'scraperwiki/simple_html_dom.php';     
$base_url = "http://comparecar.uol.com.br/GuiaCarros";

$brands = getBrands($base_url);

function getBrands($base_url) {
    $html = scraperWiki::scrape($base_url);     
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("div.box_selecao_itens_marcas");

    foreach ($rows as $row) {
        $brand_name = $row->find("a", 0)->title;
        print $brand_name . "\n";
    }
}