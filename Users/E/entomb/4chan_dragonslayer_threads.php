<?php
//4chan dragon raid thead finder.

$url = "http://api.4chan.org/b/catalog.json";

$json = scraperWiki::scrape($url);           
$catalog = json_decode($json);
$result = array();

foreach($catalog as $page){
    foreach($page->threads as $thread){
        if(!isset($thread->com)) continue;
        $text = strtolower($thread->com);

            if(strpos($text,'dragon')!==false
            || strpos($text,'if your id')!==false
            || strpos($text,'dragonslayer')!==false
            ){
                $result[] = $thread;
            }

    }
}

foreach($result as $row){
    scraperwiki::save_sqlite(array('no'), $row);
}


?>
<?php
//4chan dragon raid thead finder.

$url = "http://api.4chan.org/b/catalog.json";

$json = scraperWiki::scrape($url);           
$catalog = json_decode($json);
$result = array();

foreach($catalog as $page){
    foreach($page->threads as $thread){
        if(!isset($thread->com)) continue;
        $text = strtolower($thread->com);

            if(strpos($text,'dragon')!==false
            || strpos($text,'if your id')!==false
            || strpos($text,'dragonslayer')!==false
            ){
                $result[] = $thread;
            }

    }
}

foreach($result as $row){
    scraperwiki::save_sqlite(array('no'), $row);
}


?>
