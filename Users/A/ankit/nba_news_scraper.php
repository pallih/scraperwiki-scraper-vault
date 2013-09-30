<?php

require 'scraperwiki/simple_html_dom.php'; 

$url = 'http://www.nba.com/news/';
$html = file_get_html($url);


foreach($html->find('a') as $key)
{      
    $key->href = 'http://www.nba.com'.$key->href ;    
}

foreach($html->find('div[id=nbaNewsStories]') as $key)
{
    echo ($key->innertext) . "<br />";
}

?>
