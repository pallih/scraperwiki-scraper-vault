<?php

require_once 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://news.nationalgeographic.com/news/archives/animals/");
$html_content = scraperwiki::scrape("http://news.nationalgeographic.com/news/archives/ancient-world/");
$html = str_get_html($html_content);
$dom = new simple_html_dom();
$dom->load($html);

$url_link_prev = "";

foreach($dom->find("div#content_mainA div.promo_collection ul.dividers li > a") as $data){ 
    $url_link = $data->href;
    if (($url_link != $url_link_prev) && (!strpos(($url_link),"/photogalleries/")) && (!strpos(($url_link),"/pictures/"))) {
        $url_link_prev = $url_link;
        $url_link = "http://news.nationalgeographic.com".$url_link;
 //       print $url_link." ----- ----- ----- ";
    $record = array('URL' => $url_link);
 //   print json_encode($record) . "\n";
    scraperwiki::save(array('URL'), $record);
    }
}

?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://news.nationalgeographic.com/news/archives/animals/");
$html_content = scraperwiki::scrape("http://news.nationalgeographic.com/news/archives/ancient-world/");
$html = str_get_html($html_content);
$dom = new simple_html_dom();
$dom->load($html);

$url_link_prev = "";

foreach($dom->find("div#content_mainA div.promo_collection ul.dividers li > a") as $data){ 
    $url_link = $data->href;
    if (($url_link != $url_link_prev) && (!strpos(($url_link),"/photogalleries/")) && (!strpos(($url_link),"/pictures/"))) {
        $url_link_prev = $url_link;
        $url_link = "http://news.nationalgeographic.com".$url_link;
 //       print $url_link." ----- ----- ----- ";
    $record = array('URL' => $url_link);
 //   print json_encode($record) . "\n";
    scraperwiki::save(array('URL'), $record);
    }
}

?>
