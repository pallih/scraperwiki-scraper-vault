<?php

$html = scraperWiki::scrape("http://www.viator.com/San-Francisco/d651-ttd");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='main-border-t']") as $data){
    $tds = $data->find("h2");
    if(count($tds)==1){
        $record = array(
            'country' => $tds[0]->plaintext//, 
         //   'years_in_school' => intval($tds[4]->plaintext)
        );
            scraperwiki::save(array('country'), $record);

    }
}


?>
<?php

$html = scraperWiki::scrape("http://www.viator.com/San-Francisco/d651-ttd");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='main-border-t']") as $data){
    $tds = $data->find("h2");
    if(count($tds)==1){
        $record = array(
            'country' => $tds[0]->plaintext//, 
         //   'years_in_school' => intval($tds[4]->plaintext)
        );
            scraperwiki::save(array('country'), $record);

    }
}


?>
