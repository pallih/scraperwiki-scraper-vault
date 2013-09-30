<?php
error_reporting(0);

require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape('http://www.nona.dti.ne.jp/d-space/');
$html = mb_convert_encoding($html, "UTF-8", "SJIS");

$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find('td.cb500 a') as $td){ //リンク
    $all_href[] = $td->href;
}
foreach($all_href as $val){
    if(strpos($val, "http") !== FALSE ){
        $href[] = $val;
    }
}
foreach ($dom->find('td.cb500') as $td){//テキスト
    //echo $td->plaintext."\n";
    $plaintext[] = $td->plaintext;
}
$text = array();
foreach($plaintext as $val){
    $explode_text = explode("\n", $val);
    $text = array_merge($text, $explode_text );
}

$del_chk = "/発売情報ログ　発売予定表/";
$p_date = "dummy";
$i = 0;

foreach($text as $val){
    // mm.dd hh:mm を YYYY-mm-ddThh:mm:ss+09:00 形式に変換
    $time_reg        = "/(\d\d)\.(\d\d)\s(\d\d):(\d\d)/";
    $no_time_reg = "/(\d\d)\.(\d\d)\s\*\*:\*\*/";
    if(preg_match($time_reg, $val, $match)){
            $p_month = $match[1];
            $p_day   = $match[2];
            $p_hour  = $match[3];
            $p_min   = $match[4];
            $p_id    = date("Y").$p_month.$p_day.$p_hour.$p_min;
            $p_date = date("Y")."-".$p_month."-".$p_day."T".$p_hour.":".$p_min.":00+09:00";
            $date_chk = TRUE;
    }elseif(preg_match($no_time_reg, $val, $match)) { //**:**を23:59に整形
            $p_month = $match[1];
            $p_day   = $match[2];
            $p_hour  = "23";
            $p_min   = "59";
            $p_id    = date("Y").$p_month.$p_day.$p_hour.$p_min;
            $p_date = date("Y")."-".$p_month."-".$p_day."T".$p_hour.":".$p_min.":00+09:00";
            $date_chk = TRUE;

    }elseif(strpos($val, "更新情報ログ") === FALSE){
        $val = html_entity_decode(rtrim($val), ENT_QUOTES, "UTF-8");
        if($date_chk === TRUE){
            $id_num = 0;
        }else{
            //$id_num = 0;
        }
        $item[] = array("text" =>$val,"date" => $p_date, "href" => $href[$i++], 'uniq_id' => $p_id.$id_num++);
        $date_chk = FALSE;

        if(preg_match($del_chk , $val, $match)){ //ここで発売日変更情報を削除
            echo "clear\n";
            $item = null;
            $i = 0;
        }
    }
}

foreach($item as $key => $val){
    $data = array(array("id"=>$key, "text" => $val['text'], "href" => $val['href'], "date" => $val['date'], "uniq" => $val['uniq_id']));
    scraperwiki::save_sqlite(array("id"), $data); 
}

//var_dump($item); 
//echo count($item);
//echo count($href);
//exit;
<?php
error_reporting(0);

require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape('http://www.nona.dti.ne.jp/d-space/');
$html = mb_convert_encoding($html, "UTF-8", "SJIS");

$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find('td.cb500 a') as $td){ //リンク
    $all_href[] = $td->href;
}
foreach($all_href as $val){
    if(strpos($val, "http") !== FALSE ){
        $href[] = $val;
    }
}
foreach ($dom->find('td.cb500') as $td){//テキスト
    //echo $td->plaintext."\n";
    $plaintext[] = $td->plaintext;
}
$text = array();
foreach($plaintext as $val){
    $explode_text = explode("\n", $val);
    $text = array_merge($text, $explode_text );
}

$del_chk = "/発売情報ログ　発売予定表/";
$p_date = "dummy";
$i = 0;

foreach($text as $val){
    // mm.dd hh:mm を YYYY-mm-ddThh:mm:ss+09:00 形式に変換
    $time_reg        = "/(\d\d)\.(\d\d)\s(\d\d):(\d\d)/";
    $no_time_reg = "/(\d\d)\.(\d\d)\s\*\*:\*\*/";
    if(preg_match($time_reg, $val, $match)){
            $p_month = $match[1];
            $p_day   = $match[2];
            $p_hour  = $match[3];
            $p_min   = $match[4];
            $p_id    = date("Y").$p_month.$p_day.$p_hour.$p_min;
            $p_date = date("Y")."-".$p_month."-".$p_day."T".$p_hour.":".$p_min.":00+09:00";
            $date_chk = TRUE;
    }elseif(preg_match($no_time_reg, $val, $match)) { //**:**を23:59に整形
            $p_month = $match[1];
            $p_day   = $match[2];
            $p_hour  = "23";
            $p_min   = "59";
            $p_id    = date("Y").$p_month.$p_day.$p_hour.$p_min;
            $p_date = date("Y")."-".$p_month."-".$p_day."T".$p_hour.":".$p_min.":00+09:00";
            $date_chk = TRUE;

    }elseif(strpos($val, "更新情報ログ") === FALSE){
        $val = html_entity_decode(rtrim($val), ENT_QUOTES, "UTF-8");
        if($date_chk === TRUE){
            $id_num = 0;
        }else{
            //$id_num = 0;
        }
        $item[] = array("text" =>$val,"date" => $p_date, "href" => $href[$i++], 'uniq_id' => $p_id.$id_num++);
        $date_chk = FALSE;

        if(preg_match($del_chk , $val, $match)){ //ここで発売日変更情報を削除
            echo "clear\n";
            $item = null;
            $i = 0;
        }
    }
}

foreach($item as $key => $val){
    $data = array(array("id"=>$key, "text" => $val['text'], "href" => $val['href'], "date" => $val['date'], "uniq" => $val['uniq_id']));
    scraperwiki::save_sqlite(array("id"), $data); 
}

//var_dump($item); 
//echo count($item);
//echo count($href);
//exit;
