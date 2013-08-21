<?php

require 'scraperwiki/simple_html_dom.php';

$domain = "http://www.yomiuri.co.jp";
$htmlTop = scraperWiki::scrape("${domain}/gourmet/drink/");

$dom = new simple_html_dom();
$dom->load($htmlTop);
$obj = $dom->find("table.layout td.c50 div.cont-s",0);

$title = "";
$record = "";
$urlDetail = "";
foreach ($obj->nodes as $k => $v) {
    $attr = $v->attr;
    if (isset($attr['class'])) {
        if ($attr['class'] == "headline-def") {
            $title = $v->outertext();
            if (preg_match("/<a .*?href=(?:\"|')(.+?)(?:\"|').*?>(.+?)<\/a>/", $v->outertext(), $matched)) {
                $title = "<div class=\"kijititle\">" . $matched[2] . "</div>";
                $urlDetail = $matched[1];                
            }
        } elseif ($attr['class'] == "lead-def") {
            if (preg_match("/<a .*?href=(?:\"|')(.+?)(?:\"|').*?>(.+?) *<\/a>/", $v->outertext(), $matched)) {
            $tmp = preg_replace("/<a .*?>.+? *<\/a>/","",  $v->outertext());                
            $tmp = preg_replace("/<span +class=(\"|')date.+? *<\/span>/","",  $tmp);                
            $record = str_replace($attr['class'], "news_body", $tmp);
            }
        }
    }
}

$htmlDetial = "";
if ($urlDetail) {
    $htmlDetail =  scraperWiki::scrape("${domain}${urlDetail}");
    $dom = new simple_html_dom();
    $dom->load($htmlDetail);
    $obj = $dom->find("div.article-def",0);
    $record = "<div class=\"kiji\">";
    foreach ($obj->nodes as $v) {
        
        $v = preg_replace("/<!\-\-.*?\-\->/","", $v->outertext());
        $v = preg_replace("/(<p>|<\/p>)/", "", $v);
        $v = preg_replace("/<a .*?<\/a>/", "", $v);
$v = strip_tags($v);
        if (strlen(trim($v)) == 0) continue;
        if (preg_match("/<h1/", $v)) continue;
        if (preg_match("/<div +class=(\"|')date/", $v)) continue;
        if (preg_match("/<div +class=(\"|')cl/", $v)) continue;
        $record.= $v . "\n";
    }
    $record .="</div>";
}

$title = mb_convert_encoding($title, "utf8", "sjis-win");
$record = mb_convert_encoding($record, "utf8", "sjis-win");
$record = $title.$record;
//echo $title;
//echo "\n";
//echo $record;
$date = date('Y/m/d H:i:s');
scraperwiki::save_sqlite(array("id"), array("id"=>"1","date"=>$date,"news"=>$record));
?>