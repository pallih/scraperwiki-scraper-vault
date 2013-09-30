<?php

set_time_limit(0);

require 'scraperwiki/simple_html_dom.php';

$query_clues = array_merge(range(0, 9), range('a', 'z'));

$queue = array();
foreach ($query_clues as $clue) {
  $queue[] = "http://www.truelocal.com.au/search/$clue/queensland";
}

while (!empty($queue)) {
  $url = array_shift($queue);

  print $url ."\n";

  $html = scraperWiki::scrape($url);

  $dom = new simple_html_dom();
  $dom->load($html);

  foreach ($dom->find('#search-results #search .search-item') as $data) {
    list($latitude, $longitude) = explode(',', $data->getAttribute('data-listing-latlng'));
    $listingid = $$data->getAttribute('data-listing-id');
    
    $data_selector = '.media-content .media .media-content';

    $name = $data->find($name_selector .' .name');
    $address = $data->find($data_selector .' .address');
    $phone = $data->find($data_selector .' .phone .tl-phone-full');

    $record = array(
      'listingid' => $listingid,
      'name' => !empty($name[0]) ? htmlspecialchars_decode($name[0]->plaintext, ENT_QUOTES) : '',
      'address' => !empty($address[0]) ? htmlspecialchars_decode($address[0]->plaintext, ENT_QUOTES) : '',
      'phone' => !empty($phone[0]) ? $phone[0]->plaintext : '',
      'longitutde' => $longitude,
      'latitude' => $latitude,
      'url' => $url,
    );
print_r($record);
//    scraperwiki::save(array('listingid'), $record);
  }

  $next = $dom->find('#search-results #pagination .last a');

print $next[0]->plaintext;

  if (!empty($next[0]) && $next[0]->plaintext == 'next') {
    $full_url = 'http://www.truelocal.com.au/'. $next[0]->getAttribute('href');
    array_unshift($queue, $full_url);
  }

  $dom->__destruct();
}
<?php

set_time_limit(0);

require 'scraperwiki/simple_html_dom.php';

$query_clues = array_merge(range(0, 9), range('a', 'z'));

$queue = array();
foreach ($query_clues as $clue) {
  $queue[] = "http://www.truelocal.com.au/search/$clue/queensland";
}

while (!empty($queue)) {
  $url = array_shift($queue);

  print $url ."\n";

  $html = scraperWiki::scrape($url);

  $dom = new simple_html_dom();
  $dom->load($html);

  foreach ($dom->find('#search-results #search .search-item') as $data) {
    list($latitude, $longitude) = explode(',', $data->getAttribute('data-listing-latlng'));
    $listingid = $$data->getAttribute('data-listing-id');
    
    $data_selector = '.media-content .media .media-content';

    $name = $data->find($name_selector .' .name');
    $address = $data->find($data_selector .' .address');
    $phone = $data->find($data_selector .' .phone .tl-phone-full');

    $record = array(
      'listingid' => $listingid,
      'name' => !empty($name[0]) ? htmlspecialchars_decode($name[0]->plaintext, ENT_QUOTES) : '',
      'address' => !empty($address[0]) ? htmlspecialchars_decode($address[0]->plaintext, ENT_QUOTES) : '',
      'phone' => !empty($phone[0]) ? $phone[0]->plaintext : '',
      'longitutde' => $longitude,
      'latitude' => $latitude,
      'url' => $url,
    );
print_r($record);
//    scraperwiki::save(array('listingid'), $record);
  }

  $next = $dom->find('#search-results #pagination .last a');

print $next[0]->plaintext;

  if (!empty($next[0]) && $next[0]->plaintext == 'next') {
    $full_url = 'http://www.truelocal.com.au/'. $next[0]->getAttribute('href');
    array_unshift($queue, $full_url);
  }

  $dom->__destruct();
}
