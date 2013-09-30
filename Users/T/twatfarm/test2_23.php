<?php
require 'scraperwiki/simple_html_dom.php';
for ($page=1; $page<=28; $page++) {
    $html = scraperWiki::scrape("http://www.goodrunguide.co.uk/ClubDetails.asp?ClubID=$page");
die(var_dump($html));
     $dom = new simple_html_dom();
    $dom->load($html);
    $gyms =array();
 
        $link = $data->getAttribute('href');
        $html2 = scraperWiki::scrape($link);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
        $i = 0;
        foreach($dom2->find("table[class='tbllist'] tr td span") as $data2) {
            //hack my sack
            //if (stristr($data2->plaintext, 'Amateur Boxers') || !strlen($data2->plaintext) || stristr($data2->plaintext, 'casino')) {
            //    continue;
            //}
            
            if ($i == 0) {
                $record = array('title' => $data2->plaintext);
            } else {
                if (stristr($data2->plaintext, 'E-mail')) {
                    $record['email'] = $data2->children(0)->href;
                } else {
                    $items = explode(' :', $data2->plaintext);
                
                    $record[$items[0]] = $items[1];
                }
            }
            $i++;
        
    //scraperwiki::save_sqlite(array('title'), $record); 
    //$gyms[] = $record;
    }
}
//print_r($gyms);<?php
require 'scraperwiki/simple_html_dom.php';
for ($page=1; $page<=28; $page++) {
    $html = scraperWiki::scrape("http://www.goodrunguide.co.uk/ClubDetails.asp?ClubID=$page");
die(var_dump($html));
     $dom = new simple_html_dom();
    $dom->load($html);
    $gyms =array();
 
        $link = $data->getAttribute('href');
        $html2 = scraperWiki::scrape($link);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
        $i = 0;
        foreach($dom2->find("table[class='tbllist'] tr td span") as $data2) {
            //hack my sack
            //if (stristr($data2->plaintext, 'Amateur Boxers') || !strlen($data2->plaintext) || stristr($data2->plaintext, 'casino')) {
            //    continue;
            //}
            
            if ($i == 0) {
                $record = array('title' => $data2->plaintext);
            } else {
                if (stristr($data2->plaintext, 'E-mail')) {
                    $record['email'] = $data2->children(0)->href;
                } else {
                    $items = explode(' :', $data2->plaintext);
                
                    $record[$items[0]] = $items[1];
                }
            }
            $i++;
        
    //scraperwiki::save_sqlite(array('title'), $record); 
    //$gyms[] = $record;
    }
}
//print_r($gyms);