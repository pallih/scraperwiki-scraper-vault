<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';

$url = "http://www.yokohama-arena.co.jp/event/calendar/";

$html = scraperWiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);

//var_dump($html);exit;

// simple_html_dom_node->find() メソッドの引数にhtmlタグを指定すると、返り値が配列になり、
// その指定したhtmlタグが存在するだけ、配列の要素(simple_html_dom_node オブジェクト)を作成する。
$calendar = $dom->find("#calendar");
//$cal = $calender[0]->innertext;
$dom2 = new simple_html_dom();
$dom2->load($calendar[0]->innertext);

echo $calendar[0]->innertext;exit;

foreach ($dom2->find("tr") as $trs){
    foreach ($trs->find("th") as $ths){
        if ($ths->plaintext=="7"){
            echo $trs->innertext;
            exit;
        }
    }
    continue;
    foreach ($trs->find("td") as $tds){
        echo $tds->plaintext. "-";
        
    }
    echo "\n";
}
exit;


$cnt=1;
//foreach( $dom->find("table[@id='calendar']") as $data){
foreach( $dom->find("#calendar") as $data){
    //$ths = $data->find("th");
    //$tds = $data->find("td");
    foreach ($data->find("tr") as $trs){
        foreach ($trs->find("th") as $ths){
            //var_dump(get_class($ths));exit;
            echo $trs->children[0]->innertext . "\n";
            //scraperwiki::save($record['day'], $record); 
        }
    }
    //echo $ths[0]->plaintext."a->";
    //echo count($ths->children)+count($tds->children)."\n";
    //var_dump($data->save());exit;
    
    //var_dump(get_class_methods(get_class($dom)));
    //var_dump($data->children());
    continue;
    /*
    $record = array(
        'day' => $ths[0]->plaintext, 
        'youbi' => $ths[1]->plaintext,
        'name' => $tds[0]->plaintext,
         'sp' => $tds[1]->plaintext,
        'start' => $tds[2]->plaintext,
         'end' => $tds[3]->plaintext,
        'toi' => $tds[4]->plaintext
        );
    print_r($record);
    scraperwiki::save($record['day'], $record);     
    */
}
?>
<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';

$url = "http://www.yokohama-arena.co.jp/event/calendar/";

$html = scraperWiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);

//var_dump($html);exit;

// simple_html_dom_node->find() メソッドの引数にhtmlタグを指定すると、返り値が配列になり、
// その指定したhtmlタグが存在するだけ、配列の要素(simple_html_dom_node オブジェクト)を作成する。
$calendar = $dom->find("#calendar");
//$cal = $calender[0]->innertext;
$dom2 = new simple_html_dom();
$dom2->load($calendar[0]->innertext);

echo $calendar[0]->innertext;exit;

foreach ($dom2->find("tr") as $trs){
    foreach ($trs->find("th") as $ths){
        if ($ths->plaintext=="7"){
            echo $trs->innertext;
            exit;
        }
    }
    continue;
    foreach ($trs->find("td") as $tds){
        echo $tds->plaintext. "-";
        
    }
    echo "\n";
}
exit;


$cnt=1;
//foreach( $dom->find("table[@id='calendar']") as $data){
foreach( $dom->find("#calendar") as $data){
    //$ths = $data->find("th");
    //$tds = $data->find("td");
    foreach ($data->find("tr") as $trs){
        foreach ($trs->find("th") as $ths){
            //var_dump(get_class($ths));exit;
            echo $trs->children[0]->innertext . "\n";
            //scraperwiki::save($record['day'], $record); 
        }
    }
    //echo $ths[0]->plaintext."a->";
    //echo count($ths->children)+count($tds->children)."\n";
    //var_dump($data->save());exit;
    
    //var_dump(get_class_methods(get_class($dom)));
    //var_dump($data->children());
    continue;
    /*
    $record = array(
        'day' => $ths[0]->plaintext, 
        'youbi' => $ths[1]->plaintext,
        'name' => $tds[0]->plaintext,
         'sp' => $tds[1]->plaintext,
        'start' => $tds[2]->plaintext,
         'end' => $tds[3]->plaintext,
        'toi' => $tds[4]->plaintext
        );
    print_r($record);
    scraperwiki::save($record['day'], $record);     
    */
}
?>
