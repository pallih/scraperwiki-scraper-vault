<?php


require 'scraperwiki/simple_html_dom.php';

$initials = range('A', 'Z');
// add specific behaviour for C letter
foreach(range('A','Z') as $letter){
    array_push($initials, 'C'.$letter);
}

foreach ($initials as $initial) {
    $html = scraperWiki::scrape("http://tpweb.atc.bo.it/atc2/XSLT_TRIP_REQUEST2?place_origin=Bologna&type_origin=stop&name_origin=" . $initial);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("select[@name='name_origin'] option") as $option){
        $record = array(
           'busStop' => $option->plaintext, 
        );
        scraperwiki::save(array('busStop'),$record);
    }
}

?>
<?php


require 'scraperwiki/simple_html_dom.php';

$initials = range('A', 'Z');
// add specific behaviour for C letter
foreach(range('A','Z') as $letter){
    array_push($initials, 'C'.$letter);
}

foreach ($initials as $initial) {
    $html = scraperWiki::scrape("http://tpweb.atc.bo.it/atc2/XSLT_TRIP_REQUEST2?place_origin=Bologna&type_origin=stop&name_origin=" . $initial);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("select[@name='name_origin'] option") as $option){
        $record = array(
           'busStop' => $option->plaintext, 
        );
        scraperwiki::save(array('busStop'),$record);
    }
}

?>
