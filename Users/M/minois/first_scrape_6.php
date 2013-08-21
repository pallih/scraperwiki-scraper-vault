<?php
require 'scraperwiki/simple_html_dom.php';
define('BASE_URL', 'http://baito.mynavi.jp/sitemap/landmark/');

main();

function init(){
    scraperwiki::sqliteexecute("drop table if exists mynavi_landmark");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `mynavi_landmark` (
    `prefecture_id` number, 
    `landmark_id` number,
    `index_name` string,
    `prefecture_name` string, 
    `landmark_name` string, 
    PRIMARY KEY(
        `prefecture_id`, `landmark_id`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);

}

function main(){
    init();
    $urls = _getPrefectureUrls();
    foreach($urls as $prefectureCd => $url){
        _parse($prefectureCd, $url);
    }
}

function _getPrefectureUrls(){
    $html = file_get_html(BASE_URL);

    $urls = array();
    $links = $html->find('div[id="dsitemap-wrap01"] ul li a');
    foreach($links as $link){
        if(preg_match('|http://baito\.mynavi\.jp/sitemap/\w+/landmark/(\d+)/|', $link->href, $matches)){
            $urls[$matches[1]] = $link->href;
        }
    }
    return $urls;
}

function _parse($prefectureCd, $url){

    $html = file_get_html($url);
    
    // 都道府県
    $h1 = $html->find('h1 strong', 0);
    $prefecture = str_replace('のスポット', '', $h1->plaintext);

    // インデックス名称(あかさたな・・・)
    $indexes = $html->find('div[id=lstIndex] dl dt');

    // ランドマーク
    $record = array();
    $ddList = $html->find('div[id=lstIndex] dl dd');
    for($i = 0; $i < count($indexes); $i++){
        $index = str_replace('行', '', $indexes[$i]->plaintext);
        $links = $ddList[$i]->find('a');
        foreach($links as $link){
            if(preg_match('|http://baito\.mynavi\.jp/landmark/(\d+)/|', $link, $matches)){
                $record[] = array(
                    'prefecture_id' => $prefectureCd,
                    'landmark_id' => $matches[1],
                    'index_name' => $index,
                    'prefecture_name' => $prefecture, 
                    'landmark_name' => $link->plaintext,
                );
            }
        }
    }

    scraperwiki::save_sqlite(array('prefecture_id', 'landmark_id'), $record, 'mynavi_landmark');
}

?>
