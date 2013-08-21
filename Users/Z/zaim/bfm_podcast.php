<?php

error_reporting(0);


##
## Functions
##

function getAudioURL ($url) {
  $html = file_get_contents($url);
  $dom  = new DOMDocument();
  $dom->loadHTML($html);
  $tag  = $dom->getElementById("podcast-download");
  if ($tag) {
    $url = $tag->getAttribute("href");
    echo "... $url\n";
    return $url;
  }
  return null;
}


##
## Main
##

// Config
$RSS_URL = "http://www.bfm.my/Podcast-RSS.html";

// Open RSS
echo "Opening RSS File\n";
$rss = file_get_contents($RSS_URL);

// Create DOM
echo "Reading DOM\n";
$dom = new DOMDocument();
$dom->loadXML($rss);

// Get items
$items = $dom->getElementsByTagName('item');

// Get audio file for each URL
foreach ($items as $item) {
  $tag = $item->getElementsByTagName('link');
  if ($tag->length) {
    $url = $tag->item(0)->textContent;
    echo $url . "\n";
    getAudioURL($url);
  }
}

?>