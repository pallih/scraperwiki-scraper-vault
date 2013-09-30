<?php
require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();
date_default_timezone_set('UTC');

$ITERATIONS = 10;

for($i=0; $i<$ITERATIONS;$i++) {

    $html = scraperWiki::scrape('http://picasaweb.google.com/lh/explore?'.$i);
    preg_match_all ('%https://picasaweb\.google\.com/[a-zA-Z0-9._]*/[a-zA-Z0-9._]*#[0-9]*%', $html, $matches);
    foreach($matches[0] as $url) {
      $parts = preg_split('%[/#]%', $url);
      $user = $parts[3];
      $html = scraperWiki::scrape("http://picasaweb.google.com/$user/");
      $dom->load($html);
      foreach($dom->find("div#lhid_albums div a") as $albums) {
        $info = $albums->find("p");
        $title = $info[0]->plaintext;
        $desc = $info[1]->plaintext;
        $date = strftime("%Y-%m-%d",strtotime($info[2]->plaintext));
        $photos = preg_split('/:/',$info[3]->plaintext);
        $photos = trim($photos[1]);
        if($photos && $title != "Profile Photos" && $title != "Photos from posts") {
           $entry = (array(
                          'user' => $user,
                          'url' => $albums->href,
                          'title'=>$title,
                          'description' => $desc,
                          'date' => $date,
                          'photo_count'=>$photos));
        }
        scraperwiki::save_sqlite(array("url"),$entry);
      }
    }
}
?>
<?php
require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();
date_default_timezone_set('UTC');

$ITERATIONS = 10;

for($i=0; $i<$ITERATIONS;$i++) {

    $html = scraperWiki::scrape('http://picasaweb.google.com/lh/explore?'.$i);
    preg_match_all ('%https://picasaweb\.google\.com/[a-zA-Z0-9._]*/[a-zA-Z0-9._]*#[0-9]*%', $html, $matches);
    foreach($matches[0] as $url) {
      $parts = preg_split('%[/#]%', $url);
      $user = $parts[3];
      $html = scraperWiki::scrape("http://picasaweb.google.com/$user/");
      $dom->load($html);
      foreach($dom->find("div#lhid_albums div a") as $albums) {
        $info = $albums->find("p");
        $title = $info[0]->plaintext;
        $desc = $info[1]->plaintext;
        $date = strftime("%Y-%m-%d",strtotime($info[2]->plaintext));
        $photos = preg_split('/:/',$info[3]->plaintext);
        $photos = trim($photos[1]);
        if($photos && $title != "Profile Photos" && $title != "Photos from posts") {
           $entry = (array(
                          'user' => $user,
                          'url' => $albums->href,
                          'title'=>$title,
                          'description' => $desc,
                          'date' => $date,
                          'photo_count'=>$photos));
        }
        scraperwiki::save_sqlite(array("url"),$entry);
      }
    }
}
?>
