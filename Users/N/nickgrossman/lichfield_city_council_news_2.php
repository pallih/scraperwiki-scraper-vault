<?php

require 'scraperwiki/simple_html_dom.php'; // Hi Scraperwiki!

// Set the source and grab it
$url = "http://theslowhunch.net/tagged/hmm";
$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);

foreach ($html->find("article.post") as $post){

    $post_title = $post->find('h1.title a', 0)->plaintext;
    $post_url = $post->find('h1.title a', 0)->href;
    $post_content = $post->find('.caption', 0)->plaintext;
 
    if ($post_title) {
        scraperwiki::save(array('title','link','description', 'guid', 'date'), array('title'=>$post_title, 'link'=>$post_url, 'description'=>$post_content, 'guid'=>$post_url, 'date'=>date("Y-m-d H:i:s")));
    }

}


?>
