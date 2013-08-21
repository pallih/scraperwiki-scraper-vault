<?php
require 'scraperwiki/simple_html_dom.php';           

function scrapeIdeeLab() {
    $html = scraperWiki::scrape("http://ideelab.wordpress.com/category/uudis/");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('div.status-publish') as $data){
        $newsTitle = $data->find('div.posttitle h2.pagetitle');
    //    print($newsTitle[0]->plaintext."\n");
        $newsBody = $data->find('div.entry');
    //    print($newsBody[0]->plaintext."\n");
        $record = array(
               'title' => $newsTitle[0]->plaintext,
               'newsbody' => $newsBody[0]->plaintext);
                scraperwiki::save(array('title', 'newsbody'), $record);
        }
}

function scrapeArengufond() {
    $html = scraperWiki::scrape("http://www.arengufond.ee/news/");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('div.template') as $data){
    //print($data);
        $newsTitle = $data->find('h2');
        if (count($newsTitle)>0) { print($newsTitle[0]->plaintext."\n"); }
        $newsBody = $data->find('td');
        //print($newsBody[0]->plaintext."\n");
        /* $record = array(
               'title' => $newsTitle[0]->plaintext,
               'newsbody' => $newsBody[0]->plaintext);
                scraperwiki::save(array('title', 'newsbody'), $record);*/
        }
}
//scrapeIdeeLab();
scrapeArengufond();

?>
