<?php
require 'scraperwiki/simple_html_dom.php';

$ITERATIONS = 10;

for($i=0;$i<$ITERATIONS;$i++) {
    $html = scraperWiki::scrape("http://www.flickr.com/photos/?$i"); 

    $dom = new simple_html_dom();
    $indom = new simple_html_dom();

    $dom->load($html);
    foreach($dom->find("td#GoodStuff > div > p > a") as $data){ 
      if(preg_match('%^/photos/([^/]*)/?$%',$data->href, $matches)) {
        $inhtml = scraperWiki::scrape('http://www.flickr.com/'.$data->href.'/sets'); 
        $indom->load($inhtml);
        foreach($indom->find("div.Sets") as $set)  {
            $linkdata = $set->children(1)->children(0);
            $photos = $set->children(2)->children(0);
            $videos = $set->children(2)->children(1);
            $record = array(
                            'user' => $matches[1],
                            'url' => 'http://www.flickr.com/'.$linkdata->href,
                            'title' => $linkdata->title,
                            'photos_count' => str_replace(',','',$photos->plaintext),
                            'videos_count' => str_replace(',','',$videos->plaintext)
            );
            scraperwiki::save(array('url'), $record);
        }
      }
    }
}
    

?>
<?php
require 'scraperwiki/simple_html_dom.php';

$ITERATIONS = 10;

for($i=0;$i<$ITERATIONS;$i++) {
    $html = scraperWiki::scrape("http://www.flickr.com/photos/?$i"); 

    $dom = new simple_html_dom();
    $indom = new simple_html_dom();

    $dom->load($html);
    foreach($dom->find("td#GoodStuff > div > p > a") as $data){ 
      if(preg_match('%^/photos/([^/]*)/?$%',$data->href, $matches)) {
        $inhtml = scraperWiki::scrape('http://www.flickr.com/'.$data->href.'/sets'); 
        $indom->load($inhtml);
        foreach($indom->find("div.Sets") as $set)  {
            $linkdata = $set->children(1)->children(0);
            $photos = $set->children(2)->children(0);
            $videos = $set->children(2)->children(1);
            $record = array(
                            'user' => $matches[1],
                            'url' => 'http://www.flickr.com/'.$linkdata->href,
                            'title' => $linkdata->title,
                            'photos_count' => str_replace(',','',$photos->plaintext),
                            'videos_count' => str_replace(',','',$videos->plaintext)
            );
            scraperwiki::save(array('url'), $record);
        }
      }
    }
}
    

?>
