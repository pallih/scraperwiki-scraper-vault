<?php
require 'scraperwiki/simple_html_dom.php'; 
set_time_limit(0);
$lastpage = scraperwiki::get_var('last_page');


//print $lastpage;
// While $i (the loop counter) is less than or equal to 9999 (the number of times you want to navigate)
for ($i = $lastpage; $i <= 11000; $i++) {

     
$html_content = scraperwiki::scrape("https://www.airbnb.co.uk/s?page=".$i."&room_types[]=Entire+home%2Fapt");
$html = str_get_html($html_content);

if (!empty($html)) {
$listingnum = $html->find("li.search_result");
foreach ($listingnum as $el) {           
    //print $el->getAttribute('data-hosting-id') . "\n";
    $roomdeets[]=array(
    'id'=> $el->getAttribute('data-hosting-id'),
    'url'=> 'https://www.airbnb.com/rooms/'.$el->getAttribute('data-hosting-id'),
    );
}
    try {
      scraperwiki::save(array('id'), $roomdeets); 
      scraperwiki::save_var('last_page', $i);
      unset($roomdeets);
    }
    catch (Exception $e) {
      sleep(10);
    }
}
};    // End the loop

if ($i >= 10999) {
scraperwiki::save_var('last_page', 1);
}
?>