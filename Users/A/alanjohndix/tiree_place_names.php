<?php

// data from tireeplacenames.org gathered by John Holiday - just testing ScrapperWiki

$AtoZurl = "http://www.tireeplacenames.org/place-names-a-z/";

$html = scraperWiki::scrape($AtoZurl);

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$count = 0;
foreach($dom->find("div.azindex li") as $data){
    //echo $count . "\n";
    $link = $data->find("a[@href]");
    $head = $data->find("span[@class='head']");
    $subhead = $data->find("span[@class='subhead']");

    if ( ! ( $link && $head && $subhead ) ) {
        continue;
    }

    $record = array(
        'link' => $link[0]->href,
//        'head' => utf8_encode( $head[0]->plaintext ),
//        'subhead' => utf8_encode( $subhead[0]->plaintext ),
        'head' =>  $head[0]->plaintext ,
        'subhead' =>  $subhead[0]->plaintext ,
    );
    //print_r($record);
    $count++;
    //if ( $count  < 1233 ) continue;
    echo $count  . ": " . $record['head']. " " . (mb_check_encoding($record['head'],'UTF-8')?'YES':'NO') . " " .  mb_detect_encoding($head[0]->plaintext). " " .  mb_detect_encoding($record['head']). " link:" . json_encode($link[0]->href). " subhead:" . json_encode($subhead[0]->plaintext). " head:" . json_encode($head[0]->plaintext) . /*" " . bin2hex($head[0]->plaintext) . */ "\n";
    if ( $record['head'] ) {
        scraperwiki::save(array('head','subhead'), $record);
    }
//break;
    //if ( $count  >= 1233 ) break;
}


?>
<?php

// data from tireeplacenames.org gathered by John Holiday - just testing ScrapperWiki

$AtoZurl = "http://www.tireeplacenames.org/place-names-a-z/";

$html = scraperWiki::scrape($AtoZurl);

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$count = 0;
foreach($dom->find("div.azindex li") as $data){
    //echo $count . "\n";
    $link = $data->find("a[@href]");
    $head = $data->find("span[@class='head']");
    $subhead = $data->find("span[@class='subhead']");

    if ( ! ( $link && $head && $subhead ) ) {
        continue;
    }

    $record = array(
        'link' => $link[0]->href,
//        'head' => utf8_encode( $head[0]->plaintext ),
//        'subhead' => utf8_encode( $subhead[0]->plaintext ),
        'head' =>  $head[0]->plaintext ,
        'subhead' =>  $subhead[0]->plaintext ,
    );
    //print_r($record);
    $count++;
    //if ( $count  < 1233 ) continue;
    echo $count  . ": " . $record['head']. " " . (mb_check_encoding($record['head'],'UTF-8')?'YES':'NO') . " " .  mb_detect_encoding($head[0]->plaintext). " " .  mb_detect_encoding($record['head']). " link:" . json_encode($link[0]->href). " subhead:" . json_encode($subhead[0]->plaintext). " head:" . json_encode($head[0]->plaintext) . /*" " . bin2hex($head[0]->plaintext) . */ "\n";
    if ( $record['head'] ) {
        scraperwiki::save(array('head','subhead'), $record);
    }
//break;
    //if ( $count  >= 1233 ) break;
}


?>
