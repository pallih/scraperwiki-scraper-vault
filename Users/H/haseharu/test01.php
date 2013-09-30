<?php
//using simple_html_dom.php
require 'scraperwiki/simple_html_dom.php';
$html = new simple_html_dom();
$html = file_get_html("https://nkp.iaea.org/INISMLThesaurus/en/ind.html");
foreach($html->find('body h2') as $data){
    $targetUrl ="https://nkp.iaea.org/INISMLThesaurus/en/". $data->find('a',0)->href;
    $htmlTree = new simple_html_dom();
    $htmlTree = file_get_html($targetUrl);
    foreach($htmlTree->find('body a') as $data2){
        $keyword = $data2->find('p',0)->plaintext;
        var_dump($keyword);
        $record = array('keyword' => $keyword);
        // scraping data can store at SQLite at the ScraperWiki
        scraperwiki::save(array('keyword'), $record); 
    }
}
?>
<?php
//using simple_html_dom.php
require 'scraperwiki/simple_html_dom.php';
$html = new simple_html_dom();
$html = file_get_html("https://nkp.iaea.org/INISMLThesaurus/en/ind.html");
foreach($html->find('body h2') as $data){
    $targetUrl ="https://nkp.iaea.org/INISMLThesaurus/en/". $data->find('a',0)->href;
    $htmlTree = new simple_html_dom();
    $htmlTree = file_get_html($targetUrl);
    foreach($htmlTree->find('body a') as $data2){
        $keyword = $data2->find('p',0)->plaintext;
        var_dump($keyword);
        $record = array('keyword' => $keyword);
        // scraping data can store at SQLite at the ScraperWiki
        scraperwiki::save(array('keyword'), $record); 
    }
}
?>
