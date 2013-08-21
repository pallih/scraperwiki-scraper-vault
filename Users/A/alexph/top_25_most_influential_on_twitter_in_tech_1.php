<?php
require 'scraperwiki/simple_html_dom.php';

$html  = file_get_html('http://wefollow.com/twitter/tech');

foreach($html->find('div#results div.result_row') as $el) {
    $rank      = substr($el->children(0)->plaintext, 1);
    $handle    = '@'.$el->children(2)->children(0)->plaintext;
    $tagline   = $el->children(2)->children(1)->plaintext;
    $followers = preg_replace('/[,a-z\s]+/', '', $el->children(3)->children(0)->plaintext);
    $trend     = preg_replace('/[,\sA-Z]/', '', $el->children(3)->children(1)->plaintext);

    $record = array(
        'rank'      => $rank,
        'handle'    => $handle,
        'tagline'   => $tagline,
        'followers' => $followers,
        'trend'     => $trend
    );

    scraperwiki::save(array('rank'), $record);
}
?>