<?php

set_time_limit(0);
print "Hello, coding in the cloud!\n";  

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$detail_dom = new simple_html_dom();

$date = "2007-04-01 00:00:00";
$time = strtotime($date);

while($time < time())
{
    echo date("m-Y", $time)."\n";
    $url = "http://www.killerstartups.com/archives/".date("Y", $time)."/".date("m", $time)."/";

    $html = scraperWiki::scrape($url);
    
    $dom->load($html);
    foreach($dom->find("ul.contArchives li a") as $a){
    
        $detail_html = scraperWiki::scrape("http://www.killerstartups.com".$a->href);
        $detail_dom->load($detail_html);
        
        $info = $detail_dom->find("div.descriptionBanner", 0);
        $link = $detail_dom->find("p.linkSite a", 0);

        $url_info = parse_url($link->href);
        $domain = preg_replace("#^www\.#is", "", $url_info['host']);

        $record = array(
            'domain' => trim($domain),
            'title' => trim($a->plaintext),
            'description' => $info->plaintext,
        );
        //print_r($record);
        scraperwiki::save(array('domain'), $record);
        
        usleep(500000); // 0.5s
    }

    $time = strtotime($date."+1 month");
    $date = date("Y-m-d H:i:s", $time);
}

$dom->clear(); 
$detail_dom->clear();
unset($dom, $detail_dom);

?><?php

set_time_limit(0);
print "Hello, coding in the cloud!\n";  

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$detail_dom = new simple_html_dom();

$date = "2007-04-01 00:00:00";
$time = strtotime($date);

while($time < time())
{
    echo date("m-Y", $time)."\n";
    $url = "http://www.killerstartups.com/archives/".date("Y", $time)."/".date("m", $time)."/";

    $html = scraperWiki::scrape($url);
    
    $dom->load($html);
    foreach($dom->find("ul.contArchives li a") as $a){
    
        $detail_html = scraperWiki::scrape("http://www.killerstartups.com".$a->href);
        $detail_dom->load($detail_html);
        
        $info = $detail_dom->find("div.descriptionBanner", 0);
        $link = $detail_dom->find("p.linkSite a", 0);

        $url_info = parse_url($link->href);
        $domain = preg_replace("#^www\.#is", "", $url_info['host']);

        $record = array(
            'domain' => trim($domain),
            'title' => trim($a->plaintext),
            'description' => $info->plaintext,
        );
        //print_r($record);
        scraperwiki::save(array('domain'), $record);
        
        usleep(500000); // 0.5s
    }

    $time = strtotime($date."+1 month");
    $date = date("Y-m-d H:i:s", $time);
}

$dom->clear(); 
$detail_dom->clear();
unset($dom, $detail_dom);

?>