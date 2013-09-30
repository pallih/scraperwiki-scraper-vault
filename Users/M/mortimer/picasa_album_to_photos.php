<?php
require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("picasa_explore_album_scraper", "albums");
$users = scraperwiki::select("distinct user from albums.swdata limit 2");

foreach($users as $u) {
$urls = scraperwiki::select("url from albums.swdata where user='".$u['user']."' order by random() limit 1");
foreach($urls as $ur) {
$album_url = preg_replace('/https/','http', $ur['url']);
$html = scraperWiki::scrape($album_url);

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("link[@rel='alternate']") as $data){
    $rss_url = $data->href;
    if(preg_match('#^.*/albumid/([^?]*)\??.*$#', $data->href, $matches)) {
        $album_id = $matches[1];
        
$rss_album = scraperWiki::scrape($rss_url);

$splits = preg_split('#</?entry#', $rss_album);

foreach($splits as $entry) {
if(preg_match_all("|<([^>]+)>(.*)</\\1>|U", $entry, $matches)) {
print $matches[0][0];
}
}

    }
}


}
}


?>
<?php
require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("picasa_explore_album_scraper", "albums");
$users = scraperwiki::select("distinct user from albums.swdata limit 2");

foreach($users as $u) {
$urls = scraperwiki::select("url from albums.swdata where user='".$u['user']."' order by random() limit 1");
foreach($urls as $ur) {
$album_url = preg_replace('/https/','http', $ur['url']);
$html = scraperWiki::scrape($album_url);

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("link[@rel='alternate']") as $data){
    $rss_url = $data->href;
    if(preg_match('#^.*/albumid/([^?]*)\??.*$#', $data->href, $matches)) {
        $album_id = $matches[1];
        
$rss_album = scraperWiki::scrape($rss_url);

$splits = preg_split('#</?entry#', $rss_album);

foreach($splits as $entry) {
if(preg_match_all("|<([^>]+)>(.*)</\\1>|U", $entry, $matches)) {
print $matches[0][0];
}
}

    }
}


}
}


?>
