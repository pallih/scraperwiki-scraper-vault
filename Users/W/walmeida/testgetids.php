<?php

# Blank PHP
$html = scraperWiki::scrape("http://www.camara.gov.br/sitcamaraws/Proposicoes.asmx/ObterProposicaoPorID?idProp=25676");
echo $html;

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table tbody.coresAlternadas") as $data){
    $tds = $data->find("a");
    $record = array(
        'id' => $tds[0]->plaintext);
    //scraperwiki::save(array('id'), $record);
    print_r($record);
}

?>
