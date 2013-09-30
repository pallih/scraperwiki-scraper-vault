
<?php

set_time_limit(0);

require 'scraperwiki/simple_html_dom.php';

//$query_clues = array_merge(range(0, 9), range('a', 'z'));

//http://www.yellowpages.com.au/search/listings?clue=h&locationClue=Queensland&pageNumber=19

$query_clues = array_merge(range('h', 'z'));

$queue = array();
foreach ($query_clues as $clue) {
 $queue[] = "http://www.yellowpages.com.au/search/listings?clue=$clue&locationClue=Queensland";
}

$queue[0] .= '&pageNumber=19';

while (!empty($queue)) {
  $url = array_shift($queue);

  print $url ."\n";

  $html = scraperWiki::scrape($url);

  $dom = new simple_html_dom();
  $dom->load($html);

  foreach ($dom->find('#searchResultListings .listingContainer') as $data) {
    $latitude = $data->getAttribute('latitude');
    $longitude = $data->getAttribute('longitude');

    $compare = $data->find('.compareSelector');
    $listingid = $compare[0]->getAttribute('listingid');
    
    $name_selector = '.listingInfoAndLogo .listingInfoContainer .listingName';
    $data_selector = '.listingInfoAndLogo .listingInfoContainer .listingInfoPanel';

    $name = $data->find($name_selector .' a span');
    $description = $data->find($data_selector .' .textDesc');
    $extended_description = $data->find($data_selector .' .enhancedTextDesc');
    $address = $data->find($data_selector .' .address');
    $preferred_contact = $data->find($data_selector .' .preferredContact span');
    $website = $data->find($data_selector .' .primaryListingLinks a[name="listing_website"]');
    $category = $data->find($data_selector .' .categoryDescription div a span');

    $record = array(
      'listingid' => $listingid,
      'name' => !empty($name[0]) ? htmlspecialchars_decode($name[0]->plaintext, ENT_QUOTES) : '',
      'description' => !empty($description[0]) ? htmlspecialchars_decode($description[0]->plaintext, ENT_QUOTES) : '',
      'extended description' => !empty($extended_description[0]) ? htmlspecialchars_decode($extended_description[0]->plaintext, ENT_QUOTES) : '',
      'address' => !empty($address[0]) ? htmlspecialchars_decode($address[0]->plaintext, ENT_QUOTES) : '',
      'preferred contact' => !empty($preferred_contact[1]) ? $preferred_contact[1]->plaintext : '',
      'website' => !empty($website[0]) ? urldecode(preg_replace('/^.*webSite=([^&]*)&.*$/', '$1', $website[0]->getAttribute('href'))) : '',
      'category' => !empty($category[0]) ? htmlspecialchars_decode($category[0]->plaintext, ENT_QUOTES) : '',
      'longitutde' => $longitude,
      'latitude' => $latitude,
      'url' => $url,
    );

    scraperwiki::save(array('listingid'), $record);
  }

  $next = $dom->find('#pageCountFooter ul li #link-page-next');

  if (!empty($next[0])) {
    $full_url = 'http://www.yellowpages.com.au/'. $next[0]->getAttribute('href');
    preg_match('/&pageNumber=([0-9]+)&/', $full_url, $matches);
    if (!empty($matches[1]) && is_numeric($matches[1])) {
      $pager_url = preg_replace('/&pageNumber=.*$/', '', $url) .'&pageNumber='. $matches[1];
      array_unshift($queue, $pager_url);
    }
  }

  $dom->__destruct();
}

<?php

set_time_limit(0);

require 'scraperwiki/simple_html_dom.php';

//$query_clues = array_merge(range(0, 9), range('a', 'z'));

//http://www.yellowpages.com.au/search/listings?clue=h&locationClue=Queensland&pageNumber=19

$query_clues = array_merge(range('h', 'z'));

$queue = array();
foreach ($query_clues as $clue) {
 $queue[] = "http://www.yellowpages.com.au/search/listings?clue=$clue&locationClue=Queensland";
}

$queue[0] .= '&pageNumber=19';

while (!empty($queue)) {
  $url = array_shift($queue);

  print $url ."\n";

  $html = scraperWiki::scrape($url);

  $dom = new simple_html_dom();
  $dom->load($html);

  foreach ($dom->find('#searchResultListings .listingContainer') as $data) {
    $latitude = $data->getAttribute('latitude');
    $longitude = $data->getAttribute('longitude');

    $compare = $data->find('.compareSelector');
    $listingid = $compare[0]->getAttribute('listingid');
    
    $name_selector = '.listingInfoAndLogo .listingInfoContainer .listingName';
    $data_selector = '.listingInfoAndLogo .listingInfoContainer .listingInfoPanel';

    $name = $data->find($name_selector .' a span');
    $description = $data->find($data_selector .' .textDesc');
    $extended_description = $data->find($data_selector .' .enhancedTextDesc');
    $address = $data->find($data_selector .' .address');
    $preferred_contact = $data->find($data_selector .' .preferredContact span');
    $website = $data->find($data_selector .' .primaryListingLinks a[name="listing_website"]');
    $category = $data->find($data_selector .' .categoryDescription div a span');

    $record = array(
      'listingid' => $listingid,
      'name' => !empty($name[0]) ? htmlspecialchars_decode($name[0]->plaintext, ENT_QUOTES) : '',
      'description' => !empty($description[0]) ? htmlspecialchars_decode($description[0]->plaintext, ENT_QUOTES) : '',
      'extended description' => !empty($extended_description[0]) ? htmlspecialchars_decode($extended_description[0]->plaintext, ENT_QUOTES) : '',
      'address' => !empty($address[0]) ? htmlspecialchars_decode($address[0]->plaintext, ENT_QUOTES) : '',
      'preferred contact' => !empty($preferred_contact[1]) ? $preferred_contact[1]->plaintext : '',
      'website' => !empty($website[0]) ? urldecode(preg_replace('/^.*webSite=([^&]*)&.*$/', '$1', $website[0]->getAttribute('href'))) : '',
      'category' => !empty($category[0]) ? htmlspecialchars_decode($category[0]->plaintext, ENT_QUOTES) : '',
      'longitutde' => $longitude,
      'latitude' => $latitude,
      'url' => $url,
    );

    scraperwiki::save(array('listingid'), $record);
  }

  $next = $dom->find('#pageCountFooter ul li #link-page-next');

  if (!empty($next[0])) {
    $full_url = 'http://www.yellowpages.com.au/'. $next[0]->getAttribute('href');
    preg_match('/&pageNumber=([0-9]+)&/', $full_url, $matches);
    if (!empty($matches[1]) && is_numeric($matches[1])) {
      $pager_url = preg_replace('/&pageNumber=.*$/', '', $url) .'&pageNumber='. $matches[1];
      array_unshift($queue, $pager_url);
    }
  }

  $dom->__destruct();
}
