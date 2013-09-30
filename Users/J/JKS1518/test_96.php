<?php
require 'scraperwiki/simple_html_dom.php';

$dbid = scraperwiki::get_var('dbid');
$dbid++;
$appid = scraperwiki::get_var('appid');
$appid++;

// Go through each app
for($appid; $appid <= 54038; $appid++) {

    $url = "http://appworld.blackberry.com/webstore/content/".$appid."/";

    $html = scraperWiki::scrape($url);          
    $dom = new simple_html_dom();
    $dom->load($html);

    $app = array();

$errorcheck = $dom->find("pre.apptitle");
if ($errorcheck != FALSE) {

    // database app id #
    $app['id'] = $dbid;

    // title
    $title = $dom->find("pre.apptitle");
    $app['title'] = trim(html_entity_decode($title[0]->plaintext));

    // description
    $desc = $dom->find("pre.appDescriptionText");
    $app['description'] = trim($desc[0]->plaintext);

    // vendor
    $vendor = $dom->find("span.sitelink");
    $app['vendor'] = trim(html_entity_decode($vendor[0]->plaintext));

    // icon
    $icon = $dom->find("div.awAppDetailIcon img");
    $app['icon'] = ($icon[0]->src) ? 'http://appworld.blackberry.com' . $icon[0]->src : '';

    // link
    $app['link'] = $url;

    // price
    $price = $dom->find("div.contentLic");
    $app['price'] = trim($price[0]->plaintext,"USD$");

    // breadcrumb
    $breadcrumb = $dom->find("div.breadcrumb a");
    $app['cat1'] = trim(html_entity_decode($breadcrumb[1]->plaintext));
    $app['cat2'] = trim(html_entity_decode($breadcrumb[2]->plaintext));
    if ($breadcrumb[3] == FALSE){
        $app['cat3'] = " ";}
    else {
        $app['cat3'] = trim(html_entity_decode($breadcrumb[3]->plaintext));}

    // rating
    $rating = $dom->find("div.awAppDetailsReviewsLinks img");
    $app['rating'] = trim($rating[0]->src, "/webstorimga.png");

    scraperwiki::save_sqlite(array('id'), $app);
    scraperwiki::save_var('dbid', $dbid);
    scraperwiki::save_var('appid', $appid);

$dbid++;
} else {}

}
?><?php
require 'scraperwiki/simple_html_dom.php';

$dbid = scraperwiki::get_var('dbid');
$dbid++;
$appid = scraperwiki::get_var('appid');
$appid++;

// Go through each app
for($appid; $appid <= 54038; $appid++) {

    $url = "http://appworld.blackberry.com/webstore/content/".$appid."/";

    $html = scraperWiki::scrape($url);          
    $dom = new simple_html_dom();
    $dom->load($html);

    $app = array();

$errorcheck = $dom->find("pre.apptitle");
if ($errorcheck != FALSE) {

    // database app id #
    $app['id'] = $dbid;

    // title
    $title = $dom->find("pre.apptitle");
    $app['title'] = trim(html_entity_decode($title[0]->plaintext));

    // description
    $desc = $dom->find("pre.appDescriptionText");
    $app['description'] = trim($desc[0]->plaintext);

    // vendor
    $vendor = $dom->find("span.sitelink");
    $app['vendor'] = trim(html_entity_decode($vendor[0]->plaintext));

    // icon
    $icon = $dom->find("div.awAppDetailIcon img");
    $app['icon'] = ($icon[0]->src) ? 'http://appworld.blackberry.com' . $icon[0]->src : '';

    // link
    $app['link'] = $url;

    // price
    $price = $dom->find("div.contentLic");
    $app['price'] = trim($price[0]->plaintext,"USD$");

    // breadcrumb
    $breadcrumb = $dom->find("div.breadcrumb a");
    $app['cat1'] = trim(html_entity_decode($breadcrumb[1]->plaintext));
    $app['cat2'] = trim(html_entity_decode($breadcrumb[2]->plaintext));
    if ($breadcrumb[3] == FALSE){
        $app['cat3'] = " ";}
    else {
        $app['cat3'] = trim(html_entity_decode($breadcrumb[3]->plaintext));}

    // rating
    $rating = $dom->find("div.awAppDetailsReviewsLinks img");
    $app['rating'] = trim($rating[0]->src, "/webstorimga.png");

    scraperwiki::save_sqlite(array('id'), $app);
    scraperwiki::save_var('dbid', $dbid);
    scraperwiki::save_var('appid', $appid);

$dbid++;
} else {}

}
?>