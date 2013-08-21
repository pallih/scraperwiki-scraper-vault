<?php
require 'scraperwiki/simple_html_dom.php';

define('URL_NEW','http://com.nicovideo.jp/com_new');
define('URL_BASE','http://com.nicovideo.jp/community/');
define('PRE_COM_NO','co');

$MaxCoNo = GetMaxCoNumber();
scraperwiki::save_var('cno_max', $MaxCoNo);
//$MaxCoNo = 10;
$MaxDbCoNo = scraperwiki::get_var('cno_dbmax');
scraperwiki::save_var('cno_dbmax_old', $MaxDbCoNo );
//$MaxDbCoNo = 1; // RUN for first time.

$MaxCoNo = 50000; //it's workaround.

echo $MaxDbCoNo . "->" . $MaxCoNo . "\r\n";

for( $iCom=$MaxDbCoNo; $iCom<=$MaxCoNo; $iCom++){
    unset($ComData);

    $ComData = GetCommunityData($iCom);
    echo $ComData['cid']."/".$ComData['ctype']."\r\n";
    //var_dump($ComData);

    SaveCommunityData($ComData);
    if($iCom % 50 ==0) scraperwiki::save_var('cno_dbmax', $iCom);
    //break;
}
exit;

function SaveCommunityData($ArrComData){

    if(!array_key_exists("cid",$ArrComData)){ return; }
    scraperwiki::save_sqlite(array("cid"),$ArrComData);
}

function GetMaxCoNumber(){
    $html = scraperWiki::scrape( URL_NEW );
    
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("div.com_frm a") as $el){
        $wCoNo = $el->href;
        break;
    }
    return substr($wCoNo, strrpos($wCoNo, '/co')+3);
}

function GetCommunityData($ComNo){

    $url = URL_BASE . PRE_COM_NO . $ComNo;

    $html = scraperWiki::scrape( $url );
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $ComData['cid'] = PRE_COM_NO . $ComNo;
    $ComData['cno'] = (int) $ComNo;

    $sErrDesc = trim($dom->find("p.error_description",0)->plaintext);

    switch($sErrDesc){
        case is_null($sErrDesc):
            $strHtml = $dom->find('div#community_prof_frm2',0)->innertext;
            $ComData = GetCommunityDataOpen($strHtml, $ComData);
            break;

        case is_int(strpos($sErrDesc,'コミュニティメンバーではありません。')): //クローズコミュ
            $ComData['ctype'] = 'close';
            $ComData['cname'] = trim($dom->find("strong", 0)->plaintext);
            break;

        case is_int(strpos($sErrDesc,'お探しのコミュニティは存在しないか')): //削除済み
            $ComData['ctype'] = 'delete';
            break;

        default:
    }

    return $ComData;
}

function GetCommunityDataOpen(&$Html, &$ComData){

    $dom_com = new simple_html_dom();
    $dom_com->load($Html);

    //base data
    $ComData['cname'] = $dom_com->find('h1#community_name',0)->plaintext;
    $ComData['getday'] = date(DATE_ATOM);

    unset($key);
    foreach($dom_com->find("div.r p") as $el){

        $dom_value = new simple_html_dom();
        $dom_value->load($el->innertext);

        switch($el->innertext){
            case (strpos($el->innertext,'開設日：')===0): 
                $ComData['openday'] = $dom_value->find('strong',0)->plaintext; 
                $ComData['openday'] = str_replace(array('年','月','日'),array('-','-',''),$ComData['openday']);
                break;
            case (strpos($el->innertext,'オーナー：')===0): 
                $ComData['owner_id'] = $dom_value->find('a',0)->href; 
                $ComData['owner_id'] = (int) substr($ComData['owner_id'], strrpos($ComData['owner_id'], '/')+1);

                $ComData['owner_name'] = $dom_value->find('strong',0)->plaintext; 
                break;
            default:
        }
        
    }

    //img tags
    foreach($dom_com->find("img") as $el){
        switch($el->src){
            case (strpos($el->src,'type_open.gif')<>FALSE): $ComData['ctype'] = 'open'; break;
            case (strpos($el->src,'type_close.gif')<>FALSE): $ComData['ctype'] = 'close'; break;
            case (strpos($el->src,'type_open_official.gif')<>FALSE): $ComData['ctype'] = 'open official'; break;
            case (strpos($el->src,'icon.nimg.jp/community')<>FALSE): $ComData['clogoimg'] = $el->src; break;
            default:
                //echo $el->src . "\r\n";
        }
    }

    unset($key);
    foreach($dom_com->find("tr[valign=top] td") as $el){

        if(!isset($key)){
            switch($el->plaintext){
                case 'レベル：': $key = 'lv'; break;
                case 'メンバー：': $key = 'member'; break;
                case '設定：': $key = 'setting'; break;
                case '登録タグ：': $key = 'tags'; break;
                case '累計来場者数：': $key = 'viewer'; break;
                case '獲得した特権：': $key = 'special'; break;
                case '投稿動画：': $key = 'moviecount'; break;
                default:
                    echo $el->tag ."/". $el->plaintext . "\r\n";
            }
        } else {
            $dom_value = new simple_html_dom();
            $dom_value->load($el->innertext);

            unset($value);
            unset($type);
            switch($key){
                case 'lv': 
                case 'member': 
                case 'viewer': 
                case 'moviecount': 
                    $value = $dom_value->find('strong',0)->plaintext; 
                    $type = "i";
                    break;
                case 'setting': 
                    foreach($dom_value->find("div.comsetting span") as $elValue){
                        //echo $key . ", " . $elValue->tag ."/". $elValue->outertext. "\r\n";

                        switch($elValue->outertext){
                            case (strpos($elValue->outertext,'auto_accept')<>FALSE):
                                $key = 'auto_accept';
                                $ComData[$key] = GetSettingValue($elValue->outertext);
                                break;

                            case (strpos($elValue->outertext,'userinfo_required')<>FALSE):
                                $key = 'userinfo_required';
                                $ComData[$key] = GetSettingValue($elValue->outertext);
                                break;

                            case (strpos($elValue->outertext,'privvideo_post')<>FALSE):
                                $key = 'privvideo_post';
                                $ComData[$key] = GetSettingValue($elValue->outertext);
                                break;

                            case (strpos($elValue->outertext,'privuser_auth')<>FALSE):
                                $key = 'privuser_auth';
                                $ComData[$key] = GetSettingValue($elValue->outertext);
                                break;

                            case (strpos($elValue->outertext,'privlive_broadcast')<>FALSE):
                                $key = 'privlive_broadcast';
                                $ComData[$key] = GetSettingValue($elValue->outertext);
                                break;

                            default:
                                echo $key . ", " . $elValue->tag ."/". $elValue->outertext. "\r\n";
                        }
                        unset($key);
                        unset($value);
                    }
                    break;
                case 'tags':
                    foreach($dom_value->find("a") as $elValue){
                        $value = $value . $elValue->plaintext . "\t";
                    }
                    break;
                case 'special': 
                    //$value = $el->plaintext; 
                    break;
                default:
                    echo $key . ", " . $el->tag ."/". $el->innertext. "\r\n";
            }
            if(isset($value)){
                switch($type){
                    case 'i':
                        $ComData[$key] = (int) $value; 
                        break;
                    default:
                        $ComData[$key] = trim($value);
                }
            }
            unset($key);
        }
    }

    return $ComData;

}

function GetSettingValue($ElValue){

    if(strpos($ElValue, ' on')>0) {
        $value = 'on';
    } else {
        $value = 'off';
    }
    return $value;
}
?>
