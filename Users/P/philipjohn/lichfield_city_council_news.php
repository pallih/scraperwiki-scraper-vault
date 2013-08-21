<?php

require 'scraperwiki/simple_html_dom.php'; // Hi Scraperwiki!

// Set the source and grab it
$url = "http://www.lichfield.gov.uk/news.ihtml";
$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);

foreach ($html->find("h3") as $n){
    $title = $n->innertext;
    $title = substr($title, strpos($title, '<br> ')+4);
    
    // Let's not let it go over 140 characters!
    if (strlen("Lichfield City Council News: $title") <= 140){
        $title = "Lichfield City Council News: $title";
    }
    else if (strlen("News: $title") <= 140){
        $title = "News: $title";
    } //otherwise it's left as just the headline

    scraperwiki::save(array('title','link','description', 'guid', 'date'), array('title'=>$title, 'link'=>$url, 'description'=>$title, 'guid'=>$url, 'date'=>date("Y-m-d H:i:s")));

}


?>
