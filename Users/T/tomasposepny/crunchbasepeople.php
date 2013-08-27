<?php

require 'scraperwiki/simple_html_dom.php';   

$html_content = scraperwiki::scrape("http://www.crunchbase.com/people/recently-added.rss");
$html = str_get_html($html_content);

$people_array = $html->find("channel > item");
    
foreach($people_array as $person) {
    $title = $person->find("title", 0)->plaintext;
    $link = $person->find("guid", 0)->plaintext;
    $date = date_parse(trim(substr($person->find("pubDate", 0)->plaintext,5,-13)));

    $html_content = scraperwiki::scrape($link);
    $detail_html = str_get_html($html_content);
    $twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
    if(isset($twitter)) {
        $twitter = trim($twitter->plaintext);
    }

    //prepare tweet text
    $tweet_text = null;
    if(!is_null($twitter)) {
        $tweet_text = "Newly listed investor to watch - " . $twitter; 
    }
    
    
    $new_person = array('name' => $title, 
                        'link' => $link, 
                        'twitter' => $twitter, 
                        'day' => $date['day'],
                        'month' => $date['month'],
                        'year' => $date['year'],
                        'tweet' => $tweet_text);
    
    scraperwiki::save(array("name", "link"), $new_person);
}


?>
<?php

require 'scraperwiki/simple_html_dom.php';   

$html_content = scraperwiki::scrape("http://www.crunchbase.com/people/recently-added.rss");
$html = str_get_html($html_content);

$people_array = $html->find("channel > item");
    
foreach($people_array as $person) {
    $title = $person->find("title", 0)->plaintext;
    $link = $person->find("guid", 0)->plaintext;
    $date = date_parse(trim(substr($person->find("pubDate", 0)->plaintext,5,-13)));

    $html_content = scraperwiki::scrape($link);
    $detail_html = str_get_html($html_content);
    $twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
    if(isset($twitter)) {
        $twitter = trim($twitter->plaintext);
    }

    //prepare tweet text
    $tweet_text = null;
    if(!is_null($twitter)) {
        $tweet_text = "Newly listed investor to watch - " . $twitter; 
    }
    
    
    $new_person = array('name' => $title, 
                        'link' => $link, 
                        'twitter' => $twitter, 
                        'day' => $date['day'],
                        'month' => $date['month'],
                        'year' => $date['year'],
                        'tweet' => $tweet_text);
    
    scraperwiki::save(array("name", "link"), $new_person);
}


?>
<?php

require 'scraperwiki/simple_html_dom.php';   

$html_content = scraperwiki::scrape("http://www.crunchbase.com/people/recently-added.rss");
$html = str_get_html($html_content);

$people_array = $html->find("channel > item");
    
foreach($people_array as $person) {
    $title = $person->find("title", 0)->plaintext;
    $link = $person->find("guid", 0)->plaintext;
    $date = date_parse(trim(substr($person->find("pubDate", 0)->plaintext,5,-13)));

    $html_content = scraperwiki::scrape($link);
    $detail_html = str_get_html($html_content);
    $twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
    if(isset($twitter)) {
        $twitter = trim($twitter->plaintext);
    }

    //prepare tweet text
    $tweet_text = null;
    if(!is_null($twitter)) {
        $tweet_text = "Newly listed investor to watch - " . $twitter; 
    }
    
    
    $new_person = array('name' => $title, 
                        'link' => $link, 
                        'twitter' => $twitter, 
                        'day' => $date['day'],
                        'month' => $date['month'],
                        'year' => $date['year'],
                        'tweet' => $tweet_text);
    
    scraperwiki::save(array("name", "link"), $new_person);
}


?>
