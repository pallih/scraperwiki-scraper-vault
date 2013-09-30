<?php

$subjects = array(
//'advertising' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib21%2C1%2C0%2C6/mode=2',
'sains' => 'http://webopac.pnm.gov.my/search/query;jsessionid=DA7AC0C720E11F450B41741E2C1CE571?term_1=sains',

);


require 'scraperwiki/simple_html_dom.php';

foreach ($subjects AS $subject => $url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".briefcitTitle a") as $el){
    
        $item = scraperWiki::scrape("http://webopac.pnm.gov.my/".$el->href);
    
        $pdom = new simple_html_dom();
        $pdom->load($item);
        $p = $pdom->find('.bibDisplayPermLink a');
    
    
    
    
        $record = array(
            'subject_slug' => $subject,
            'title' => $el->plaintext, 
            'link' => "http://webopac.pnm.gov.my".$p[0]->href
        );
    
        $info = $pdom->find('.bibInfoEntry table tr');
        foreach ($info AS $tr) {
            $tds = $tr->find('td');
            $record[strtolower($tds[0]->plaintext)] = $tds[1]->plaintext;
    
        }
    
        scraperwiki::save(array('link'), $record);
    
    }
}

?>
<?php

$subjects = array(
//'advertising' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib21%2C1%2C0%2C6/mode=2',
'sains' => 'http://webopac.pnm.gov.my/search/query;jsessionid=DA7AC0C720E11F450B41741E2C1CE571?term_1=sains',

);


require 'scraperwiki/simple_html_dom.php';

foreach ($subjects AS $subject => $url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".briefcitTitle a") as $el){
    
        $item = scraperWiki::scrape("http://webopac.pnm.gov.my/".$el->href);
    
        $pdom = new simple_html_dom();
        $pdom->load($item);
        $p = $pdom->find('.bibDisplayPermLink a');
    
    
    
    
        $record = array(
            'subject_slug' => $subject,
            'title' => $el->plaintext, 
            'link' => "http://webopac.pnm.gov.my".$p[0]->href
        );
    
        $info = $pdom->find('.bibInfoEntry table tr');
        foreach ($info AS $tr) {
            $tds = $tr->find('td');
            $record[strtolower($tds[0]->plaintext)] = $tds[1]->plaintext;
    
        }
    
        scraperwiki::save(array('link'), $record);
    
    }
}

?>
