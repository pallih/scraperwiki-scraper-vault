<?php
define('BASE_URL', 'http://lain.gr.jp');
require 'scraperwiki/simple_html_dom.php';

$Url = "http://lain.gr.jp/voicedb/profile/list/cid/";

scraperwiki::save_sqlite(array("lain_actorid"),array("lain_actorid"=>"99999999", "updt"=>date("YmdHis")));

$arrActorUrl = GetActorList($Url);

foreach( $arrActorUrl as $ActorUrl){

    if(SelectActorData($ActorUrl)==0){
        echo "Get  " . $ActorUrl['name'] .", ". $ActorUrl['url'] . "\r\n";

        unset($arrActorData);
        $arrActorData = GetActorData($ActorUrl);
        SaveActorData($arrActorData);
    } else { 
        //echo "Skip " . $ActorUrl['name'] .", ". $ActorUrl['url'] . "\r\n";
    }
}

exit;

function SelectActorData($ActorUrl){

    $wDate = str_replace(array("-",":","T"),"",substr($ActorUrl['updt'],0,-6));
    $wDate = intval($wDate) + 1;

    $sql = "* from swdata where lain_actorid = '".$ActorUrl['id']."' and updt < '". $wDate ."'";
    //echo $sql . "\r\n";

    $value = scraperwiki::select($sql);
    //var_dump($value);
    //var_dump(count($value));

    return count($value);
}


function GetActorList($Url){

    $count = 0;
    for($i=1; $i<=10; $i++){
        $url_work = $Url . $i;
        echo "Get ". $url_work . "\r\n";

        $html = scraperWiki::scrape( $url_work );
        
        $dom = new simple_html_dom();
        $dom->load($html);

        foreach($dom->find('ul.listItems li') as $dom_list){
            foreach($dom_list->children() as $el){
                //print $el->tag . ":" . $el->innertext . "\n";
                switch($el->tag){
                    case "a":
                        if(strpos($el->href,'voicedb/profile/')>0){
                            $arrUrl[$count]['url'] = $el->href; 
                            $arrUrl[$count]['id'] = substr($el->href, strrpos($el->href, '/')+1);
                            $arrUrl[$count]['name'] = $el->plaintext;
                        }
                        break;
                    case "img":
                        $arrUrl[$count]['sex'] = $el->title; 
                        break;
                    case "data":
                        $arrUrl[$count]['updt'] = $el->value; 
                        break;
                    default:
                }
            }
            $count++;
        }
        //var_dump($arrUrl);
    }
    return $arrUrl;
}


function SaveActorData($ArrActorData){
    if(!array_key_exists("名前",$ArrActorData)){ return; }
    scraperwiki::save_sqlite(array("lain_actorid"),$ArrActorData);
}

function GetActorData($Urls){
    $url = BASE_URL . $Urls['url'];

    $html = scraperWiki::scrape( $url );
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $dom_db = $dom->find("div#db dl", 0);

    $ActorData['lain_actorid'] = $Urls['id'];
    $ActorData['url'] = $url;
    $ActorData['sex'] = $Urls['sex'];
    $ActorData['updt'] = str_replace(array("-",":","T"),"",substr($Urls['updt'],0,-6));

    foreach ($dom_db->children() as $el) {

        //delete column
        if($el->tag == "dt"){
            switch($el->innertext){
                case '年齢': continue 2;
                case '星座': continue 2;
                case '身長': continue 2;
                case '体重': continue 2;
                case 'タグ': continue 2;
                case '好きなもの': continue 2;
                case '嫌いなもの': continue 2;
                case '命日': continue 2;
                case '享年': continue 2;
                case '詳細': continue 2;
                case '特技': continue 2;
                case '趣味': continue 2;
                case 'ファンクラブ': continue 2;
                case 'トラックバックURL': continue 2;
                default:
            }
        }

        //print $el->tag . ":" . $el->innertext . "\n";

        //set data
        switch($el->tag){
            case "dt":
                $DtValue = $el->innertext;
                break;
            case "dd":
                if(isset($DtValue)){
                    $ActorData[$DtValue] = trim($el->plaintext);
                }
                unset($DtValue);
                break;
            default:
                unset($DtValue);
        }
    }
    return $ActorData;
}
?>
<?php
define('BASE_URL', 'http://lain.gr.jp');
require 'scraperwiki/simple_html_dom.php';

$Url = "http://lain.gr.jp/voicedb/profile/list/cid/";

scraperwiki::save_sqlite(array("lain_actorid"),array("lain_actorid"=>"99999999", "updt"=>date("YmdHis")));

$arrActorUrl = GetActorList($Url);

foreach( $arrActorUrl as $ActorUrl){

    if(SelectActorData($ActorUrl)==0){
        echo "Get  " . $ActorUrl['name'] .", ". $ActorUrl['url'] . "\r\n";

        unset($arrActorData);
        $arrActorData = GetActorData($ActorUrl);
        SaveActorData($arrActorData);
    } else { 
        //echo "Skip " . $ActorUrl['name'] .", ". $ActorUrl['url'] . "\r\n";
    }
}

exit;

function SelectActorData($ActorUrl){

    $wDate = str_replace(array("-",":","T"),"",substr($ActorUrl['updt'],0,-6));
    $wDate = intval($wDate) + 1;

    $sql = "* from swdata where lain_actorid = '".$ActorUrl['id']."' and updt < '". $wDate ."'";
    //echo $sql . "\r\n";

    $value = scraperwiki::select($sql);
    //var_dump($value);
    //var_dump(count($value));

    return count($value);
}


function GetActorList($Url){

    $count = 0;
    for($i=1; $i<=10; $i++){
        $url_work = $Url . $i;
        echo "Get ". $url_work . "\r\n";

        $html = scraperWiki::scrape( $url_work );
        
        $dom = new simple_html_dom();
        $dom->load($html);

        foreach($dom->find('ul.listItems li') as $dom_list){
            foreach($dom_list->children() as $el){
                //print $el->tag . ":" . $el->innertext . "\n";
                switch($el->tag){
                    case "a":
                        if(strpos($el->href,'voicedb/profile/')>0){
                            $arrUrl[$count]['url'] = $el->href; 
                            $arrUrl[$count]['id'] = substr($el->href, strrpos($el->href, '/')+1);
                            $arrUrl[$count]['name'] = $el->plaintext;
                        }
                        break;
                    case "img":
                        $arrUrl[$count]['sex'] = $el->title; 
                        break;
                    case "data":
                        $arrUrl[$count]['updt'] = $el->value; 
                        break;
                    default:
                }
            }
            $count++;
        }
        //var_dump($arrUrl);
    }
    return $arrUrl;
}


function SaveActorData($ArrActorData){
    if(!array_key_exists("名前",$ArrActorData)){ return; }
    scraperwiki::save_sqlite(array("lain_actorid"),$ArrActorData);
}

function GetActorData($Urls){
    $url = BASE_URL . $Urls['url'];

    $html = scraperWiki::scrape( $url );
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $dom_db = $dom->find("div#db dl", 0);

    $ActorData['lain_actorid'] = $Urls['id'];
    $ActorData['url'] = $url;
    $ActorData['sex'] = $Urls['sex'];
    $ActorData['updt'] = str_replace(array("-",":","T"),"",substr($Urls['updt'],0,-6));

    foreach ($dom_db->children() as $el) {

        //delete column
        if($el->tag == "dt"){
            switch($el->innertext){
                case '年齢': continue 2;
                case '星座': continue 2;
                case '身長': continue 2;
                case '体重': continue 2;
                case 'タグ': continue 2;
                case '好きなもの': continue 2;
                case '嫌いなもの': continue 2;
                case '命日': continue 2;
                case '享年': continue 2;
                case '詳細': continue 2;
                case '特技': continue 2;
                case '趣味': continue 2;
                case 'ファンクラブ': continue 2;
                case 'トラックバックURL': continue 2;
                default:
            }
        }

        //print $el->tag . ":" . $el->innertext . "\n";

        //set data
        switch($el->tag){
            case "dt":
                $DtValue = $el->innertext;
                break;
            case "dd":
                if(isset($DtValue)){
                    $ActorData[$DtValue] = trim($el->plaintext);
                }
                unset($DtValue);
                break;
            default:
                unset($DtValue);
        }
    }
    return $ActorData;
}
?>
