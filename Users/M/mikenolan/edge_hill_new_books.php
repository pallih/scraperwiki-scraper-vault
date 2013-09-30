<?php

$subjects = array(
'advertising' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib21%2C1%2C0%2C6/mode=2',
'animation' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib22%2C1%2C0%2C49/mode=2',
'biology' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib23%2C1%2C0%2C7/mode=2',
'business' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib24%2C1%2C0%2C6/mode=2',
'computing' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib25%2C1%2C0%2C10/mode=2',
'creativewriting' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib26%2C1%2C0%2C5/mode=2',
'dance' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib27%2C1%2C0%2C12/mode=2',
'design' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib28%2C1%2C0%2C14/mode=2',
'english' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib29%2C1%2C0%2C8/mode=2',
'film' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib30%2C1%2C0%2C3/mode=2',
'geography' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib31%2C1%2C0%2C49/mode=2',
'health' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib32%2C1%2C0%2C75/mode=2',
'history' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib33%2C1%2C0%2C29/mode=2',
'law' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib34%2C1%2C0%2C7/mode=2',
'media' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib35%2C1%2C0%2C9/mode=2',
'music' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib36%2C1%2C0%2C51/mode=2',
'psychology' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib37%2C1%2C0%2C28/mode=2',
'socialsciences' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib38%2C1%2C0%2C1/mode=2',
'socialwork' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib39%2C1%2C0%2C4/mode=2',
'sport' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib40%2C1%2C0%2C51/mode=2',
'education' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib41%2C1%2C0%2C22/mode=2',
);


require 'scraperwiki/simple_html_dom.php';

foreach ($subjects AS $subject => $url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".briefcitTitle a") as $el){
    
        $item = scraperWiki::scrape("http://library.edgehill.ac.uk/".$el->href);
    
        $pdom = new simple_html_dom();
        $pdom->load($item);
        $p = $pdom->find('.bibDisplayPermLink a');
    
    
    
    
        $record = array(
            'subject_slug' => $subject,
            'title' => $el->plaintext, 
            'link' => "http://library.edgehill.ac.uk".$p[0]->href,
            'dateadded' => microtime(true)
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
'advertising' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib21%2C1%2C0%2C6/mode=2',
'animation' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib22%2C1%2C0%2C49/mode=2',
'biology' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib23%2C1%2C0%2C7/mode=2',
'business' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib24%2C1%2C0%2C6/mode=2',
'computing' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib25%2C1%2C0%2C10/mode=2',
'creativewriting' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib26%2C1%2C0%2C5/mode=2',
'dance' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib27%2C1%2C0%2C12/mode=2',
'design' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib28%2C1%2C0%2C14/mode=2',
'english' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib29%2C1%2C0%2C8/mode=2',
'film' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib30%2C1%2C0%2C3/mode=2',
'geography' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib31%2C1%2C0%2C49/mode=2',
'health' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib32%2C1%2C0%2C75/mode=2',
'history' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib33%2C1%2C0%2C29/mode=2',
'law' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib34%2C1%2C0%2C7/mode=2',
'media' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib35%2C1%2C0%2C9/mode=2',
'music' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib36%2C1%2C0%2C51/mode=2',
'psychology' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib37%2C1%2C0%2C28/mode=2',
'socialsciences' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib38%2C1%2C0%2C1/mode=2',
'socialwork' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib39%2C1%2C0%2C4/mode=2',
'sport' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib40%2C1%2C0%2C51/mode=2',
'education' => 'http://library.edgehill.ac.uk/search~S1?/ftlist^bib41%2C1%2C0%2C22/mode=2',
);


require 'scraperwiki/simple_html_dom.php';

foreach ($subjects AS $subject => $url) {

    $html = scraperWiki::scrape($url);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".briefcitTitle a") as $el){
    
        $item = scraperWiki::scrape("http://library.edgehill.ac.uk/".$el->href);
    
        $pdom = new simple_html_dom();
        $pdom->load($item);
        $p = $pdom->find('.bibDisplayPermLink a');
    
    
    
    
        $record = array(
            'subject_slug' => $subject,
            'title' => $el->plaintext, 
            'link' => "http://library.edgehill.ac.uk".$p[0]->href,
            'dateadded' => microtime(true)
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
