<?php
require 'scraperwiki/simple_html_dom.php';
$urls = array(
    url1=>"https://play.google.com/store/apps/details?id=com.gameloft.android.ANMP.GloftG4HM",
    url2=>"https://play.google.com/store/apps/details?id=com.dotemu.anotherworld",
);

foreach($urls as $url){
    $purl = "http://nfriedly.com/px/poxy/index.php?q=" . $url;
    $html_content = scraperWiki::scrape($purl);
    $html = str_get_html($html_content);

    $price=$html->find('meta[itemprop="price"]');
    $image=$html->find('meta[itemprop="image"]');
    $name=$html->find('meta[itemprop="name"]');

    scraperwiki::save_sqlite(array("App"),array("App"=>$name[0]->content, "Price"=>$price[0]->content, "Image"=>$image[0]->content, "Url"=>$url));
}



?>
<?php
require 'scraperwiki/simple_html_dom.php';
$urls = array(
    url1=>"https://play.google.com/store/apps/details?id=com.gameloft.android.ANMP.GloftG4HM",
    url2=>"https://play.google.com/store/apps/details?id=com.dotemu.anotherworld",
);

foreach($urls as $url){
    $purl = "http://nfriedly.com/px/poxy/index.php?q=" . $url;
    $html_content = scraperWiki::scrape($purl);
    $html = str_get_html($html_content);

    $price=$html->find('meta[itemprop="price"]');
    $image=$html->find('meta[itemprop="image"]');
    $name=$html->find('meta[itemprop="name"]');

    scraperwiki::save_sqlite(array("App"),array("App"=>$name[0]->content, "Price"=>$price[0]->content, "Image"=>$image[0]->content, "Url"=>$url));
}



?>
