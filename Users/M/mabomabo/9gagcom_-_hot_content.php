<?php

require 'scraperwiki/simple_html_dom.php';

// content from homepage
$html_content = scraperwiki::scrape("http://9gag.com/");
$html = str_get_html($html_content);

// all items
foreach ($html->find("li.entry-item") as $el) {
    $el_html = str_get_html($el);
    
    // extract..
    $title = $el_html->find("div.sticky-items h1 a", 0)->innertext;
    $image_url = $el_html->find("div.content img", 0)->getAttribute("src");
    $url = $el_html->find("div.content a", 0)->getAttribute("href");
    $fb_count = (int) $el_html->find("span.facebook_share_count_inner", 0)->innertext;
    //$twitter_count = $el_html->find("span.b2-widget-val", 0)->innertext;    
    $loved_count = (int) $el_html->find("span.loved", 0)->innertext;

    if( preg_match("|nsfw-badge|", $el) )
        $nsfw = 1;
    else
        $nsfw = 0;

    // Image size
    $img = getimagesize($image_url);
    
    // Store data
    scraperwiki::save(array('url'), 
        array(  "url" => $url, 
                "title" => $title, 
                "image" => $image_url, 
                "image_width" => $img[0], 
                "image_height" => $img[1],
                "fb_count" => $fb_count,
                "nsfw" => $nsfw,
               // "twitter_count" =>  $twitter_count,
                "loved_count" => $loved_count) );
}


?>
