<?php

# Blank PHP

$html = scraperWiki::scrape("http://www.idealsoftwares.com.br/indices/incc.html");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("th[@class='tabelatopo']") as $data){
    $ths = $data->find("th");
    if(count($ths)==12){
        $record = array(
            'year' => $ths[0]->plaintext, 
        );
        print json_encode($record) . "\n";
    }
}

scraperwiki::save(array('year'), $record);           


?>
<?php

# Blank PHP

$html = scraperWiki::scrape("http://www.idealsoftwares.com.br/indices/incc.html");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("th[@class='tabelatopo']") as $data){
    $ths = $data->find("th");
    if(count($ths)==12){
        $record = array(
            'year' => $ths[0]->plaintext, 
        );
        print json_encode($record) . "\n";
    }
}

scraperwiki::save(array('year'), $record);           


?>
