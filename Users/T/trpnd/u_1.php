<?php

require 'scraperwiki/simple_html_dom.php';
//mb_language("Japanese");

scraperwiki::attach("swdata");
scraperwiki::sqliteexecute(
    "delete from swdata"
);

for ($i = 1; $i < 20; $i++) {

    $html = scraperWiki::scrape("http://smocca.jp/search/results?air_conditionings%5B%5D=4&area%5Bmax%5D=&area%5Bmin%5D=&built_year=&chinryou%5Binclude_kanrihi%5D=true&chinryou%5Bmax%5D=35000&chinryou%5Bmin%5D=&city_ids%5B%5D=14151&city_ids%5B%5D=14152&city_ids%5B%5D=14153&facilities%5B%5D=16&locations%5B%5D=2&locations%5B%5D=16&per_page=15&prefecture=kanagawa&q=&reikin=true&walk_min=&x=142&y=16&page=$i");

    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("td.routeAddress") as $data){
        $tds = $data->parent()->find("td");
        $record = array(
            'route' => $tds[0]->innertext, //路線/最寄駅
            'Address' => $tds[0]->innertext, //所在地
            'url' => $tds[0]->find("a",0)->href,
            'link' => $tds[0]->innertext, 
            'distance' => $tds[1]->plaintext, //徒歩 バス
            'layout' => $tds[2]->plaintext,   //間取り 専有面積
            'year' => $tds[3]->plaintext,     //築年数 方位
            'room' => $tds[4]->plaintext,     //種別 所在階 部屋番号
            'charge' => $tds[5]->plaintext,   //賃料 管理費等
            'initial' => $tds[6]->plaintext,  //敷金 礼金
            'photo' => $tds[7]->innertext     //物件写真・間取り図
        );
        $record = str_replace("/bukken/","http://smocca.jp/bukken/",$record);
        $record = preg_replace("/\/top.+?\?url=/i","",$record);
        $record = preg_replace("/\.(jpg)\?.+?\"/i",".$1\"",$record);
        $record = preg_replace("/\.(gif)\?.+?\"/i",".$1\"",$record);
        $record = preg_replace("/\.(jpg)&.+?\"/i",".$1\"",$record);
        $record = preg_replace("/\.(gif)&.+?\"/i",".$1\"",$record);

        $record['route'] = preg_replace("/<a href=.+?>(.+?)<.+/i","$1",$record['route']);
        $record['Address'] = preg_replace("/.+<br \/>(.+?)<.+/i","$1",$record['Address']);

        scraperwiki::save(array('url'), $record);
    }
    $dom->__destruct();
}


?>
<?php

require 'scraperwiki/simple_html_dom.php';
//mb_language("Japanese");

scraperwiki::attach("swdata");
scraperwiki::sqliteexecute(
    "delete from swdata"
);

for ($i = 1; $i < 20; $i++) {

    $html = scraperWiki::scrape("http://smocca.jp/search/results?air_conditionings%5B%5D=4&area%5Bmax%5D=&area%5Bmin%5D=&built_year=&chinryou%5Binclude_kanrihi%5D=true&chinryou%5Bmax%5D=35000&chinryou%5Bmin%5D=&city_ids%5B%5D=14151&city_ids%5B%5D=14152&city_ids%5B%5D=14153&facilities%5B%5D=16&locations%5B%5D=2&locations%5B%5D=16&per_page=15&prefecture=kanagawa&q=&reikin=true&walk_min=&x=142&y=16&page=$i");

    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("td.routeAddress") as $data){
        $tds = $data->parent()->find("td");
        $record = array(
            'route' => $tds[0]->innertext, //路線/最寄駅
            'Address' => $tds[0]->innertext, //所在地
            'url' => $tds[0]->find("a",0)->href,
            'link' => $tds[0]->innertext, 
            'distance' => $tds[1]->plaintext, //徒歩 バス
            'layout' => $tds[2]->plaintext,   //間取り 専有面積
            'year' => $tds[3]->plaintext,     //築年数 方位
            'room' => $tds[4]->plaintext,     //種別 所在階 部屋番号
            'charge' => $tds[5]->plaintext,   //賃料 管理費等
            'initial' => $tds[6]->plaintext,  //敷金 礼金
            'photo' => $tds[7]->innertext     //物件写真・間取り図
        );
        $record = str_replace("/bukken/","http://smocca.jp/bukken/",$record);
        $record = preg_replace("/\/top.+?\?url=/i","",$record);
        $record = preg_replace("/\.(jpg)\?.+?\"/i",".$1\"",$record);
        $record = preg_replace("/\.(gif)\?.+?\"/i",".$1\"",$record);
        $record = preg_replace("/\.(jpg)&.+?\"/i",".$1\"",$record);
        $record = preg_replace("/\.(gif)&.+?\"/i",".$1\"",$record);

        $record['route'] = preg_replace("/<a href=.+?>(.+?)<.+/i","$1",$record['route']);
        $record['Address'] = preg_replace("/.+<br \/>(.+?)<.+/i","$1",$record['Address']);

        scraperwiki::save(array('url'), $record);
    }
    $dom->__destruct();
}


?>
