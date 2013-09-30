<?php
require 'scraperwiki/simple_html_dom.php';           
$last_id = scraperwiki::get_var('last_id', 1);
for ($i = $last_id; $i<$last_id+1000; $i++) {
    $html = scraperWiki::scrape("http://drupal.org/user/" . $i);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("#page-title") as $name) {
      $username = $name->plaintext;
    }
    foreach($dom->find(".user-member dd") as $data) {
      $registration = $data->plaintext;
    }
    $record = array(
        'uid' => $i,
        'name' => $username,
        'registration_date' => $registration,
    );
    scraperwiki::save(array('uid'), $record);
    scraperwiki::save_var('last_id', $i);
}

?><?php
require 'scraperwiki/simple_html_dom.php';           
$last_id = scraperwiki::get_var('last_id', 1);
for ($i = $last_id; $i<$last_id+1000; $i++) {
    $html = scraperWiki::scrape("http://drupal.org/user/" . $i);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("#page-title") as $name) {
      $username = $name->plaintext;
    }
    foreach($dom->find(".user-member dd") as $data) {
      $registration = $data->plaintext;
    }
    $record = array(
        'uid' => $i,
        'name' => $username,
        'registration_date' => $registration,
    );
    scraperwiki::save(array('uid'), $record);
    scraperwiki::save_var('last_id', $i);
}

?>