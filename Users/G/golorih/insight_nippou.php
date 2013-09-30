<?php
require 'scraperwiki/simple_html_dom.php';
define('TARGET_URL', "http://www.insightnet.co.jp/index.html");
define('TARGET_ENCODING', 'UTF-8');

//test2();exit();


$html = scraperWiki::scrape(TARGET_URL);
$dom = new simple_html_dom();
$dom->load($html);

$data = $dom->find("div[@id='nippo']");
if( isset($data[0]) ){
    $nippo = (string) str_get_html( $data[0] );
    
  // 担当者名
    if( $tanto = $dom->find("p[@class='tanto']") ) {
        $tanto = $tanto[0]->plaintext;
    } else {
        $tanto = '';
    }

  // 日時
    $datetime = get_current_datetime();
    
  // URLの相対パスを絶対パスに変換
    // $nippo = PathReplace::toAbsolutePath( TARGET_URL, $nippo );        // 2012/9/27 元々絶対パスを使用するようにしたためコメントアウト
    
  // 表示
    print $datetime ."\r\n";
    print $tanto ."\r\n";
    print $nippo ."\r\n";

  // 記録
    if(get_last_nippo() == $nippo) {
        print "前回と同じデータでした。記録せずに終了します。\r\n";
    } else {
        print "前回と異なるデータでした。記録します。\r\n";
        $record = array('date'=>$datetime, 'tanto'=>($tanto), 'title'=>$tanto, 'link'=>TARGET_URL, 'description'=>$nippo);
        scraperwiki::save(array('date', 'tanto', 'title', 'link', 'description'), $record);
    }
}

function get_current_datetime()
{
    return date('Y-m-d H:i:s');
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
<?php
require 'scraperwiki/simple_html_dom.php';
define('TARGET_URL', "http://www.insightnet.co.jp/index.html");
define('TARGET_ENCODING', 'UTF-8');

//test2();exit();


$html = scraperWiki::scrape(TARGET_URL);
$dom = new simple_html_dom();
$dom->load($html);

$data = $dom->find("div[@id='nippo']");
if( isset($data[0]) ){
    $nippo = (string) str_get_html( $data[0] );
    
  // 担当者名
    if( $tanto = $dom->find("p[@class='tanto']") ) {
        $tanto = $tanto[0]->plaintext;
    } else {
        $tanto = '';
    }

  // 日時
    $datetime = get_current_datetime();
    
  // URLの相対パスを絶対パスに変換
    // $nippo = PathReplace::toAbsolutePath( TARGET_URL, $nippo );        // 2012/9/27 元々絶対パスを使用するようにしたためコメントアウト
    
  // 表示
    print $datetime ."\r\n";
    print $tanto ."\r\n";
    print $nippo ."\r\n";

  // 記録
    if(get_last_nippo() == $nippo) {
        print "前回と同じデータでした。記録せずに終了します。\r\n";
    } else {
        print "前回と異なるデータでした。記録します。\r\n";
        $record = array('date'=>$datetime, 'tanto'=>($tanto), 'title'=>$tanto, 'link'=>TARGET_URL, 'description'=>$nippo);
        scraperwiki::save(array('date', 'tanto', 'title', 'link', 'description'), $record);
    }
}

function get_current_datetime()
{
    return date('Y-m-d H:i:s');
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
