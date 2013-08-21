<?php
// たまに取り逃がしますが、原因不明です・・・


require 'scraperwiki/simple_html_dom.php';
define('TARGET_URL', "http://www.iwanami.co.jp/meigen/heute.html");
define('TARGET_ENCODING', 'Shift_JIS');

//test2();exit();


$html = scraperWiki::scrape(TARGET_URL);
$dom = new simple_html_dom();
$dom->load($html);

$data = $dom->find("td[@class='bg_frame']");
if( isset($data[0]) ){
    $meigen = (string) str_get_html( $data[0] );
    $meigen = mb_convert_encoding($meigen, "UTF-8", TARGET_ENCODING);

  // 日時
    $datetime = get_current_datetime();
    $jdatetime = gmdate("Y年m月d日", time()+9*3600);
    
  // URLの相対パスを絶対パスに変換
    $meigen = PathReplace::toAbsolutePath( TARGET_URL, $meigen );
    
  // 表示
    print $jdatetime ."\r\n";
    print $meigen ."\r\n";

    $record = array('date'=>$datetime, 'meigen'=>($meigen), 'title'=>"岩波 きょうの名言 @{$jdatetime}" , 'link'=>TARGET_URL, 'description'=>$meigen);
    scraperwiki::save(array('date', 'meigen', 'title', 'link', 'description'), $record);
}

function get_current_datetime()
{
    return gmdate('Y-m-d H:i:s', time() + 9*3600);
}

function text_normalization( $text )
{
//    preg_replace('/(?:src="([^"]*)"|href="([^"]*)")/imu', );
    
//    return html_entity_decode($text, ENT_COMPAT | ENT_HTML401, 'UTF-8');
}

function get_last_nippo()
{
    try {
        foreach( scraperwiki::select('* from swdata ORDER BY date desc limit 1') as $data ) {
            return $data['description'];
        }
        return false;
    } catch(Exception $e) {
        return '';
    }
}



function test2()
{
    echo get_last_nippo();
}


function test()
{
    $baseurl = 'http://www.insightnet.co.jp/';
    $html = <<<_EOT_
<div id="nippo"> <div class="nippoTop"> 
<img src="images/nippo_logo.png" alt="STAFFにっぽー" title="STAFFにっぽー" /> </div> 
<div class="nippoMiddle"> <p class="photo"><img src="images/koshi_photo/abu.jpg" alt="日報フォト" width="200" height="140" title="日報フォト" /></p> 
<p>&nbsp;</p> 
<p>７月７日は中学時代の「プチ同窓会」でした。 その中に、母校である中学校へ数学教師として凱旋している子がいました。 なんでしょう、「なんだか誇らしい」気分です！<br /> </p> <p class="tanto">担当・阿武</p> </div> 
<div class="mottoBottom"></div> </div>
_EOT_;
    echo PathReplace::toAbsolutePath($baseurl, $html);
}

class PathReplace
{
    static function toAbsolutePath( $baseurl, $html )
    {
        return preg_replace('/(href|src)\s*=\s*("[^\\"]*"|\'[^\\\']*\')/e', 'self::expand_links("$baseurl","$1","$2")', $html);
    }
    
    static function expand_links($baseurl, $elem, $link) {
        $link = trim($link, '\'\"');
        $top = self::is_root_reference($link)
             ? self::rootname($baseurl)
             : ( self::str_right($baseurl,1)=='/' ? $baseurl : dirname($baseurl).'/' );
        return("{$elem}=\"{$top}{$link}\"");
    }
    
    // リンクがルートパスへの参照をしているか調べる
    static function is_root_reference($link)
    {
        return (self::str_left($link,1) == '/');
    }
    // URLのドメイン名までの部分を取得
    static function rootname($url)
    {
        return preg_match('/^([a-z]{2,10}:\/\/[^\/]+)/i', $url, $r) ? $r[1] : '';
    }
    // 文字列を右側から指定数切り取って返す。ExcelのRIGHT関数と同様。
    static function str_right( $string, $n )
    {
        return substr($string, strlen($string) -$n, $n);
    }
    // 文字列を左側から指定数切り取って返す。ExcelのLEFT関数と同様。
    static function str_left( $string, $n )
    {
        return substr($string, 0, $n);
    }
}

?>

