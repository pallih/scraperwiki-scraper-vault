<?php
require 'scraperwiki/simple_html_dom.php';
define('BASE_URL', 'http://tabelog.com');

main();

function main(){

//    init();

    list($lastPrefecture, $lastCategoryCd, $lastPageNum) = _getLastPosition();

    $prefectureList = _getPrefectureList();
    $categoryList = _getCategoryList();
    foreach($prefectureList as $prefectureCd => $prefectureName){
        if($lastPrefecture && $prefectureCd != $lastPrefecture){
            continue;
        }
        foreach($categoryList as $categoryCd => $categoryName){
            
            if($lastCategoryCd){
                if($categoryCd != $lastCategoryCd){
                    continue;
                }
                $url = BASE_URL . '/' . $prefectureCd . '/' . $categoryCd . '/';
                if($lastPageNum){
                    $url .= $lastPageNum. '/';
                }
                _deleteLastData($url);

                $lastPrefecture = '';
                $lastCategoryCd = '';
                $lastPageNum = '';
            } else {
                $url = BASE_URL . '/' . $prefectureCd . '/' . $categoryCd . '/';
            }
            _parse($url, $prefectureCd, $prefectureName, $categoryCd, $categoryName);
        }
    }
}


function init(){
    scraperwiki::sqliteexecute("drop table if exists tabelog_landmark");

    $createTableSQL = <<<_END_SQL_
CREATE TABLE `tabelog_landmark` (
    `landmark_id` number,
    `category` string,
    `name` string,
    `kana` string,
    `prefecture` string,
    `addr1` string,
    `addr2` string,
    `addr3` string,
    `addr4` string,
    `station1` string,
    `station2` string,
    `station3` string,
    `url` string,
    `scrape_url` string,
    PRIMARY KEY(
        `landmark_id`
    )
)
_END_SQL_;

    scraperwiki::sqliteexecute($createTableSQL);
}

function _getLastPosition(){
    $existList = _getExistLandmark();
    $prefectureList = _getPrefectureList();
    end($prefectureList);

    $categoryList = _getCategoryList();

    $prefecture = '';
    $categoryCd = '';
    $pageNum = '';

    for($i = count($prefectureList); $i > 0; $i--){
        $pref = key($prefectureList);
        end($categoryList);
        for($j = count($categoryList); $j > 0; $j--){
            $cate = key($categoryList);
            if(isset($existList[$pref][$cate])){
                $prefecture = $pref;
                $categoryCd = $cate;
                $pageNum = $existList[$pref][$cate];
                break;
            }
            prev($categoryList);
        }
        if($prefecture){
            break;
        }
        prev($prefectureList);
    }

    return array($prefecture, $categoryCd, $pageNum);
}

function _deleteLastData($url){
    scraperwiki::sqliteexecute("delete from tabelog_landmark where scrape_url = '" . $url . "'");
}

function _parse($url, $prefectureCd, $prefectureName, $categoryCd, $categoryName){
    $page = $url;
    while($page){
        $page = _parsePage($page, $prefectureCd, $prefectureName, $categoryCd, $categoryName);
    }
}

function _parsePage($url, $prefectureCd, $prefectureName, $categoryCd, $categoryName){
    $html = file_get_html($url);
    if(!$html){
        return false;
    }
    $regex = BASE_URL . '/' . $prefectureCd . '/([^/]+)/';
    
    $divList = $html->find('div[class=info]');
    if(!$divList){
        return false;
    }

    $record = array();
    for($i = 0; $i < count($divList); $i++){
        $link = $divList[$i]->find('div[class=mname] a', 0);
        if(!preg_match("|$regex|", $link, $matches)){
            continue;
        }

        $landmark_id = $matches[1];
        $kana = $divList[$i]->find('div[class=mname] span', 0);
        $kana = (isset($kana) && $kana->plaintext)? $kana->plaintext : '';    
        $kana = preg_replace('/^（/', '', $kana);
        $kana = preg_replace('/）$/', '', $kana);

        $ddList = $divList[$i]->find('div[class=info-ex] dl[class=item clearfix] dd');

        // 住所情報取得
        $addr = $ddList[0]->find('a');
        $addr1 = ($addr && isset($addr[0]))? $addr[0]->plaintext : '';
        $addr2 = ($addr && isset($addr[1]))? $addr[1]->plaintext : '';
        $addr3 = ($addr && isset($addr[2]))? $addr[2]->plaintext : '';
        $addr4 = $ddList[0]->plaintext;

        // 最寄り駅情報取得
        $station = $ddList[1]->find('a');
        $station1 = ($station && isset($station[0]))? $station[0]->plaintext : '';
        $station2 = ($station && isset($station[1]))? $station[1]->plaintext : '';
        $station3 = ($station && isset($station[2]))? $station[2]->plaintext : '';

        $record[] = array(
            'landmark_id' => $matches[1],
            'category' => $categoryName,
            'name' => $link->plaintext,
            'kana' => $kana,
            'prefecture' => $prefectureCd,
            'addr1' => $addr1,
            'addr2' => $addr2,
            'addr3' => $addr3,
            'addr4' => $addr4,
            'station1' => $station1,
            'station2' => $station2,
            'station3' => $station3,
            'url' => $link->href,
            'scrape_url' => $url,
        );
    }

    // DB書き込み
    if(!empty($record)){
        scraperwiki::save_sqlite(array('landmark_id'), $record, 'tabelog_landmark');
        $record = null;
    }

    // ページング判定
    $nextLink = $html->find('div[class=page-move] a[class=next]', 0);
    if($nextLink){
        return BASE_URL . $nextLink->href;
    }

    return false;
}

function _getExistLandmark(){
    $data = scraperwiki::select(           
        "scrape_url from tabelog_landmark where prefecture = 'akita' group by scrape_url" 
    );

    $landmark = array();
    foreach($data as $row){
        $regex = BASE_URL . '/(\w+)/(\w+)/((\w+)/)?';
        if(preg_match("|$regex|", $row['scrape_url'], $matches)){
            if(!isset($landmark[$matches[1]])){
                $landmark[$matches[1]] = array();
            }

            if(!isset($landmark[$matches[1]][$matches[2]])){
                $landmark[$matches[1]][$matches[2]] = 0;
            }

            if(isset($matches[4]) && $landmark[$matches[1]][$matches[2]] < $matches[4]){
                $landmark[$matches[1]][$matches[2]] = $matches[4];
            }
        }
    }
    return $landmark;
}


function _getPrefectureList(){
    return array(
/*
        'hokkaido'  => '北海道',
        'aomori'    => '青森',
*/
        'akita'     => '秋田',
/*
        'yamagata'  => '山形',
        'iwate'     => '岩手',
        'miyagi'    => '宮城',
        'fukushima' => '福島',
        'tokyo'     => '東京',
        'kanagawa'  => '神奈川',
        'saitama'   => '埼玉',
        'chiba'     => '千葉',
        'tochigi'   => '栃木',
        'ibaraki'   => '茨城',
        'gunma'     => '群馬',
        'aichi'     => '愛知',
        'gifu'      => '岐阜',
        'shizuoka'  => '静岡',
        'mie'       => '三重',
        'niigata'   => '新潟',
        'yamanashi' => '山梨',
        'nagano'    => '長野',
        'ishikawa'  => '石川',
        'toyama'    => '富山',
        'fukui'     => '福井',
        'osaka'     => '大阪',
        'hyogo'     => '兵庫',
        'kyoto'     => '京都',
        'shiga'     => '滋賀',
        'nara'      => '奈良',
        'wakayama'  => '和歌山',
        'okayama'   => '岡山',
        'hiroshima' => '広島',
        'tottori'   => '鳥取',
        'shimane'   => '島根',
        'yamaguchi' => '山口',
        'kagawa'    => '香川',
        'tokushima' => '徳島',
        'ehime'     => '愛媛',
        'kochi'     => '高知',
        'fukuoka'   => '福岡',
        'saga'      => '佐賀',
        'nagasaki'  => '長崎',
        'kumamoto'  => '熊本',
        'oita'      => '大分',
        'miyazaki'  => '宮崎',
        'kagoshima' => '鹿児島',
        'okinawa'   => '沖縄',
*/
    );
}

function _getCategoryList(){
    return array(
        'P01' => '商業施設・ショッピングモール',
        'P02' => '空港・駅構内',
        'P03' => 'ホテル・旅館',
        'P04' => '遊園地・テーマパーク',
        'P05' => '道の駅・サービスエリア',
        'P06' => 'レジャー施設',
        'P07' => '学術施設',
        'P08' => '病院',
        'P09' => 'その他施設・ビル',
    );
}
?>
