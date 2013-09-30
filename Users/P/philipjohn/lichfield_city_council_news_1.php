<?php

require 'scraperwiki/simple_html_dom.php'; // Hi Scraperwiki!

// Set the source and grab it
$url = "http://lichfield.keepsblogging.com/blog--catid12";
$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);

foreach ($html->find("div.cat_items a") as $n){
    
    // Get the title
    $title = $n->children(0)->children(0)->innertext;
    //$title = substr($title, strpos($title, ' - ')+3);
    
    // Let's not let it go over 140 characters!
    if (strlen("Field of the Dead: $title") <= 140){
        $title = "Field of the Dead: $title";
    }

    // Get the date from the title
    /*$date = $n->children(0)->children(0)->innertext;
    $date = substr($date, 0, strpos($date, ' - '));
    //die(var_dump($date));
    $date = date("Y-m-d H:i:s", $date);*/

    // Get the permalink
    $link = $n->href;
    $link = "http://lichfield.keepsblogging.com".$link;

    scraperwiki::save(array('title','link','description', 'guid', 'date'), array('title'=>$title, 'link'=>$link, 'description'=>$title, 'guid'=>$url, 'date'=>date("Y-m-d H:i:s")));

}


?>
<?php

require 'scraperwiki/simple_html_dom.php'; // Hi Scraperwiki!

// Set the source and grab it
$url = "http://lichfield.keepsblogging.com/blog--catid12";
$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);

foreach ($html->find("div.cat_items a") as $n){
    
    // Get the title
    $title = $n->children(0)->children(0)->innertext;
    //$title = substr($title, strpos($title, ' - ')+3);
    
    // Let's not let it go over 140 characters!
    if (strlen("Field of the Dead: $title") <= 140){
        $title = "Field of the Dead: $title";
    }

    // Get the date from the title
    /*$date = $n->children(0)->children(0)->innertext;
    $date = substr($date, 0, strpos($date, ' - '));
    //die(var_dump($date));
    $date = date("Y-m-d H:i:s", $date);*/

    // Get the permalink
    $link = $n->href;
    $link = "http://lichfield.keepsblogging.com".$link;

    scraperwiki::save(array('title','link','description', 'guid', 'date'), array('title'=>$title, 'link'=>$link, 'description'=>$title, 'guid'=>$url, 'date'=>date("Y-m-d H:i:s")));

}


?>
