<?php
require 'scraperwiki/simple_html_dom.php';
define('BASE_URL', 'http://j-sen.jp/guide_area%d.htm');

main();

function init(){
    scraperwiki::sqliteexecute("drop table if exists jsen_area");
    scraperwiki::sqliteexecute("CREATE TABLE `jsen_area` (`prefecture` string, `larea` string, `count` number, PRIMARY KEY(`prefecture`, `larea`))");
}

function main(){
    init();
    for($i=1; $i <= 47; $i++){
        _parse(sprintf(BASE_URL, $i));
    }
}

function _parse($url){
    $html = file_get_html($url);
    
    $form = $html->find('form[@id="searchForm"]', 0);
    
    // 都道府県
    $h3 = $form->find('h3[@class="guideTTLh3"]',0);
    $larea = $h3->plaintext;
    
    // 市区町村
    $ul = $form->find('ul[@class="guideList4"]', 0);
    $li = $ul->find('li');
    $record = array();
    foreach($li as $l){
        if(preg_match('/<a href=[^>]+>(.*)<\/a>\((\d+)\)/', $l, $matches)){
            $record[] = array(
                'prefecture' => $larea,
                'larea' => $matches[1],
                'count' => $matches[2],
            );
        }
    }
    scraperwiki::save_sqlite(array('prefecture', 'larea'), $record, 'jsen_area');
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';
define('BASE_URL', 'http://j-sen.jp/guide_area%d.htm');

main();

function init(){
    scraperwiki::sqliteexecute("drop table if exists jsen_area");
    scraperwiki::sqliteexecute("CREATE TABLE `jsen_area` (`prefecture` string, `larea` string, `count` number, PRIMARY KEY(`prefecture`, `larea`))");
}

function main(){
    init();
    for($i=1; $i <= 47; $i++){
        _parse(sprintf(BASE_URL, $i));
    }
}

function _parse($url){
    $html = file_get_html($url);
    
    $form = $html->find('form[@id="searchForm"]', 0);
    
    // 都道府県
    $h3 = $form->find('h3[@class="guideTTLh3"]',0);
    $larea = $h3->plaintext;
    
    // 市区町村
    $ul = $form->find('ul[@class="guideList4"]', 0);
    $li = $ul->find('li');
    $record = array();
    foreach($li as $l){
        if(preg_match('/<a href=[^>]+>(.*)<\/a>\((\d+)\)/', $l, $matches)){
            $record[] = array(
                'prefecture' => $larea,
                'larea' => $matches[1],
                'count' => $matches[2],
            );
        }
    }
    scraperwiki::save_sqlite(array('prefecture', 'larea'), $record, 'jsen_area');
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';
define('BASE_URL', 'http://j-sen.jp/guide_area%d.htm');

main();

function init(){
    scraperwiki::sqliteexecute("drop table if exists jsen_area");
    scraperwiki::sqliteexecute("CREATE TABLE `jsen_area` (`prefecture` string, `larea` string, `count` number, PRIMARY KEY(`prefecture`, `larea`))");
}

function main(){
    init();
    for($i=1; $i <= 47; $i++){
        _parse(sprintf(BASE_URL, $i));
    }
}

function _parse($url){
    $html = file_get_html($url);
    
    $form = $html->find('form[@id="searchForm"]', 0);
    
    // 都道府県
    $h3 = $form->find('h3[@class="guideTTLh3"]',0);
    $larea = $h3->plaintext;
    
    // 市区町村
    $ul = $form->find('ul[@class="guideList4"]', 0);
    $li = $ul->find('li');
    $record = array();
    foreach($li as $l){
        if(preg_match('/<a href=[^>]+>(.*)<\/a>\((\d+)\)/', $l, $matches)){
            $record[] = array(
                'prefecture' => $larea,
                'larea' => $matches[1],
                'count' => $matches[2],
            );
        }
    }
    scraperwiki::save_sqlite(array('prefecture', 'larea'), $record, 'jsen_area');
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';
define('BASE_URL', 'http://j-sen.jp/guide_area%d.htm');

main();

function init(){
    scraperwiki::sqliteexecute("drop table if exists jsen_area");
    scraperwiki::sqliteexecute("CREATE TABLE `jsen_area` (`prefecture` string, `larea` string, `count` number, PRIMARY KEY(`prefecture`, `larea`))");
}

function main(){
    init();
    for($i=1; $i <= 47; $i++){
        _parse(sprintf(BASE_URL, $i));
    }
}

function _parse($url){
    $html = file_get_html($url);
    
    $form = $html->find('form[@id="searchForm"]', 0);
    
    // 都道府県
    $h3 = $form->find('h3[@class="guideTTLh3"]',0);
    $larea = $h3->plaintext;
    
    // 市区町村
    $ul = $form->find('ul[@class="guideList4"]', 0);
    $li = $ul->find('li');
    $record = array();
    foreach($li as $l){
        if(preg_match('/<a href=[^>]+>(.*)<\/a>\((\d+)\)/', $l, $matches)){
            $record[] = array(
                'prefecture' => $larea,
                'larea' => $matches[1],
                'count' => $matches[2],
            );
        }
    }
    scraperwiki::save_sqlite(array('prefecture', 'larea'), $record, 'jsen_area');
}

?>
