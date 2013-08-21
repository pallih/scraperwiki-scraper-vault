<?php

require 'scraperwiki/simple_html_dom.php';

define('URL_BASE','http://baseball.yahoo.co.jp');


echo "start\r\n";

$url = "http://baseball.yahoo.co.jp/npb/teams/";
$urlMemberList = GetMemberListUrl($url);
$urlPlayerList = GetPlayerListUrl($urlMemberList);
//var_dump($urlPlayerList);

foreach($urlPlayerList as $urlPlayer){
    //$urlPlayer = 'http://baseball.yahoo.co.jp/npb/player/1200046/';
    unset($PlayerData);
    echo URL_BASE . $urlPlayer . "\r\n";
    $PlayerData = GetPlayerData(URL_BASE . $urlPlayer);
    SavePlayerData($PlayerData);
    //break;
}
echo "end\r\n";
exit;



function SavePlayerData($ArrData){

    if(!array_key_exists("pTeam",$ArrData)){ return; }

    scraperwiki::save_sqlite(array("pTeam","pNumber"),$ArrData);
    //var_dump($ArrData);

}


function GetPlayerListUrl($ArrUrl){

    foreach($ArrUrl as $url){
        $html = scraperWiki::scrape( URL_BASE . $url );
    
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find('a') as $pageUrl){
            if(strpos($pageUrl->href, "player/")>0){
                $arrListUrl[] = $pageUrl->href;
            }
        }
    }
    return $arrListUrl;
}


function GetMemberListUrl($url){

    $html = scraperWiki::scrape( $url );

    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find('a') as $pageUrl){
        if(strpos($pageUrl->href, "memberlist?type")>0){
            //echo $pageUrl->href . "\r\n";
            $arrListUrl[] = $pageUrl->href;
        }
    }
    return $arrListUrl;
}


function GetPlayerData($url){

    $html = scraperWiki::scrape( $url );

    $dom = new simple_html_dom();
    $dom->load($html);

    //set date format   
    $wDate = $dom->find('div.NpbFl',0)->plaintext;
    $wDate = str_replace(array("年","月"),"-",$wDate);
    $wDate = str_replace("時",":",$wDate);
    $wDate = str_replace(array("日","分","更新"),"",$wDate);
    $arrDate = date_parse_from_format("Y-n-j H:i",$wDate);
    $arrPlayer['pUpdate'] = sprintf("%04d-%02d-%02d %02d:%02d:00", 
                                        $arrDate["year"], $arrDate["month"], $arrDate["day"], 
                                        $arrDate["hour"], $arrDate["minute"]);

   
    foreach($dom->find('.NpbTeamTop') as $PlayerHeader){
        //echo $PlayerHeader->innertext . "\r\n";

        if(array_key_exists('pTeam',$arrPlayer)){  break; }

        $PlayerDom = new simple_html_dom();
        $PlayerDom->load($PlayerHeader->innertext);

        //Get Baseball Team name
        $arrPlayer['pTeam'] = $PlayerDom->find('a', 0)->plaintext;

        $arrPlayer['pNameFull'] = $PlayerDom->find('h1', 0)->innertext;
        $arrPlayer['pNameFull'] = mb_substr($arrPlayer['pNameFull'], 0, mb_strpos($arrPlayer['pNameFull'],'<span>'));
        
        if(mb_strpos($arrPlayer['pNameFull'],"　")>0){
            $playerName = explode("　", $arrPlayer['pNameFull'], 2);
            //var_dump($playerName);
            $arrPlayer['pNameLast'] = $playerName[0];
            $arrPlayer['pNameFirst'] = $playerName[1];
        } else {
            $arrPlayer['pNameLast'] = $arrPlayer['pNameFull'];
            $arrPlayer['pNameFirst'] = "";
        }

        $arrPlayer['pNumber'] = $PlayerDom->find('em', 0)->innertext;

        $arrPlayer['pKanaFull'] = $PlayerDom->find('span', 0)->innertext;
        $arrPlayer['pKanaFull'] = str_replace(array('（','）'),"", $arrPlayer['pKanaFull']);

        if(mb_strpos($arrPlayer['pKanaFull'],"　")>0){
            $playerName = explode("　", $arrPlayer['pKanaFull'], 2);
            //var_dump($playerName);
            $arrPlayer['pKanaLast'] = $playerName[0];
            $arrPlayer['pKanaFirst'] = $playerName[1];
        } else {
            $arrPlayer['pKanaLast'] = $arrPlayer['pKanaFull'];
            $arrPlayer['pKanaFirst'] = "";
        }

        $arrPlayer['pPosition'] = $PlayerDom->find('span.position', 0)->innertext;
        $arrPlayer['pUrl'] = $url;
    }

    //var_dump($arrPlayer);
    return $arrPlayer;
}

?>
