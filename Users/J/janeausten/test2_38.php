<?php

require 'scraperwiki/simple_html_dom.php';

    $venues = array(18523,7417);

for ($i = 0; $i <= 1; $i++) {
    
    //scrape the page HTML and convert into string
    $html_content = scraperwiki::scrape("http://www.musicborn.com/profile.php?id=".$venues[$i]);
    $html = str_get_html($html_content);
    $delete = array('<div class="content">','<b>','</b>','</div>');
    $separate = '<br />';

    //within the HTML, find the name of the entry
    $basicsrc = $html->find('div.col2 div.content', 0);
    $basictrim1 = str_replace($delete,"",$basicsrc);
    $basictrim2 = str_replace($separate,"| ",$basictrim1);
    $facebook= html_entity_decode($html->find('div#pageTitle a', 0)->href);
    //print the content to see if it works
    print $basictrim2 . "\n";
    print $facebook;

}

?>