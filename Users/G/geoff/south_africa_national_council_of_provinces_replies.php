<?php
require 'scraperwiki/simple_html_dom.php';

function get_date($when) {           
    return $when->format(DATE_ISO8601); 
}

function scrapepage($url) {
    $html = scraperWiki::scrape($url);                
    $dom = new simple_html_dom();
    $dom->load($html);
    $rows = $dom->find("table table table table table table tr");
    
    foreach ($rows as $row) {
        $tds=$row->find('td');
        if ($tds[0]->height==30) {
            $document=array();
            $document['name']=$tds[0]->plaintext;
            if ($tds[2]->plaintext=='-') $document['date']='';
            else $document['date']=get_date(date_create($tds[2]->plaintext));
            $document['house']=$tds[4]->plaintext;
            $document['language']=$tds[6]->plaintext;
            $link=$tds[8]->find('a');
            $img=$tds[8]->find('img');
            $document['url']='http://www.parliament.gov.za/live/'.$link[0]->href;
            if ($img[0]->src=='images/icon_word.gif') $type='.doc';
            if ($img[0]->src=='images/icon_pdf.gif') $type='.pdf';
            $document['type']=$type;
            scraperwiki::save(array('url'), $document); 
            //print_r($document);
            //print $row->plaintext;
        }
    }

    //find next page to scrape
    $links=$dom->find("table[style=height:26px] a");
    foreach ($links as $link) {
        if ($link->plaintext=='Next') {
            scrapepage('http://www.parliament.gov.za/live/'.$link->href);
        }
    }
}

scrapepage('http://www.parliament.gov.za/live/content.php?Category_ID=249');
?>
