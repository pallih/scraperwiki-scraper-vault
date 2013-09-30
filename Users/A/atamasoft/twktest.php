<?php
require 'scraperwiki/simple_html_dom.php';           
//require 'simplehtmldom_1_5/simple_html_dom.php';           

function filter($s)
{
    // @see http://jp2.php.net/trim
    $s = preg_replace('/^\s+/', '', $s);
    $s = preg_replace('/\s+$/', '', $s);
    $s = mb_convert_kana($s, 'KVa');
    return $s;
}

$url = 'http://www1.plala.or.jp/an/sq/sq/sqq.htm';
$html = scraperWiki::scrape($url);
//$html = file_get_contents('sqq.html');
$html = mb_convert_encoding($html, 'UTF-8', 'Shift_JIS');
// print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);
$records = array();
foreach ($dom->find('table') as $data)
{
    $text = $data->plaintext;
    // echo $text;
    if (mb_strpos($text, '開催日') === false)
        continue;

    $date = preg_replace('/^開催日:\s*/u', '', filter($data->find('td', 0)->plaintext));
    $date = preg_replace('/\([^)]*\)/u', '', $date);
    
    $updated_at = preg_replace('/更新/u', '', filter($data->find('td', 1)->plaintext));
    $updated_at = str_replace('/', '-', $updated_at);
    $updated_at .= ' 00:00:00';
    
    $title = preg_replace('/^大会名:\s*/u', '', filter($data->find('td', 2)->plaintext));
    
    $anchors = $data->find('a');

    $record = array(
        'date' => $date,
        'updated_at' => $updated_at,
        'title' => $title,
        'description' => $date . $title,
        'place' => preg_replace('/会場:\s*/u', '', filter($data->find('td', 3)->plaintext)),
        'sponsor' => preg_replace('/主催:\s*/u', '', filter($data->find('td', 4)->plaintext)),
        'html' => $data->innertext,
    );
    if (count($anchors))
        $record['url'] = $anchors[count($anchors)-1]->href;

    $records[] = $record;
    scraperwiki::save(array('date', 'title'), $record);  
}

//foreach ($records as $record)
//     print_r($record);
<?php
require 'scraperwiki/simple_html_dom.php';           
//require 'simplehtmldom_1_5/simple_html_dom.php';           

function filter($s)
{
    // @see http://jp2.php.net/trim
    $s = preg_replace('/^\s+/', '', $s);
    $s = preg_replace('/\s+$/', '', $s);
    $s = mb_convert_kana($s, 'KVa');
    return $s;
}

$url = 'http://www1.plala.or.jp/an/sq/sq/sqq.htm';
$html = scraperWiki::scrape($url);
//$html = file_get_contents('sqq.html');
$html = mb_convert_encoding($html, 'UTF-8', 'Shift_JIS');
// print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);
$records = array();
foreach ($dom->find('table') as $data)
{
    $text = $data->plaintext;
    // echo $text;
    if (mb_strpos($text, '開催日') === false)
        continue;

    $date = preg_replace('/^開催日:\s*/u', '', filter($data->find('td', 0)->plaintext));
    $date = preg_replace('/\([^)]*\)/u', '', $date);
    
    $updated_at = preg_replace('/更新/u', '', filter($data->find('td', 1)->plaintext));
    $updated_at = str_replace('/', '-', $updated_at);
    $updated_at .= ' 00:00:00';
    
    $title = preg_replace('/^大会名:\s*/u', '', filter($data->find('td', 2)->plaintext));
    
    $anchors = $data->find('a');

    $record = array(
        'date' => $date,
        'updated_at' => $updated_at,
        'title' => $title,
        'description' => $date . $title,
        'place' => preg_replace('/会場:\s*/u', '', filter($data->find('td', 3)->plaintext)),
        'sponsor' => preg_replace('/主催:\s*/u', '', filter($data->find('td', 4)->plaintext)),
        'html' => $data->innertext,
    );
    if (count($anchors))
        $record['url'] = $anchors[count($anchors)-1]->href;

    $records[] = $record;
    scraperwiki::save(array('date', 'title'), $record);  
}

//foreach ($records as $record)
//     print_r($record);
