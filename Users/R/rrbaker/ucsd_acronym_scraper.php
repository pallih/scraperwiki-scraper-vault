<?php



$html = scraperWiki::scrape("http://libguides.ucsd.edu/content.php?pid=275227&sid=2268671");

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div.innerbox_1 tr") as $data){
    $tds = $data->find("td");
    $uri = $data->find("a", 0);
    $record = array();

    if(count($tds)==2){
        $nyms = array(
            'acronym' => $tds[0]->plaintext,
            'stands_for' => $tds[1]->plaintext
        );
    }

    if($uri) {
        $links = array(
            'uri' => $uri->href
        );
    }
    
    $results = array_merge($nyms, $links);
    json_encode($results) . "\n";
    scraperwiki::save_sqlite(array("acronym"),array("acronym"=>$nyms['acronym'],"stands_for"=>$nyms['stands_for'],"uri"=>"$uri"));
}

?>
