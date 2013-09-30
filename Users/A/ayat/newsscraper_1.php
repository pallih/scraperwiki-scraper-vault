<?php

$html = scraperWiki::scrape("http://www.shorouknews.com/columns/fahmy-howaidy");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$dd=array();
foreach($dom->find('.LsitingContent-right a') as $data){
    print $data . "\n";
      $title = $data->plaintext;
    $link =$data->href;
    print $title ." " . $link . "\n";
     $record = array(
            'title' => $title, 
            'link' => $link
        );
    $dd[]=$record;
   
}
 scraperwiki::save_sqlite(array('title'), $dd, 'articles');

/*
$html = scraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'country' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
    scraperwiki::save(array('country'), $record);
        print json_encode($record) . "\n";
    }
}

*/

?>
<?php

$html = scraperWiki::scrape("http://www.shorouknews.com/columns/fahmy-howaidy");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$dd=array();
foreach($dom->find('.LsitingContent-right a') as $data){
    print $data . "\n";
      $title = $data->plaintext;
    $link =$data->href;
    print $title ." " . $link . "\n";
     $record = array(
            'title' => $title, 
            'link' => $link
        );
    $dd[]=$record;
   
}
 scraperwiki::save_sqlite(array('title'), $dd, 'articles');

/*
$html = scraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'country' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
    scraperwiki::save(array('country'), $record);
        print json_encode($record) . "\n";
    }
}

*/

?>
