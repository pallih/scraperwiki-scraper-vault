<?php
require 'scraperwiki/simple_html_dom.php';

$pages = 223;
$users = array();

for ($i = 0; $i <= $pages; $i++) {
  $contents = scraperWiki::scrape("http://drupal.org/profile/country/Finland?page=" . $i);
  $dom = new simple_html_dom();
  $dom->load($contents);
  foreach ($dom->find('#profile .profile .name a') as $user) {
    $uid         = end(explode('/', $user->href));
    $ctr_content = scraperWiki::scrape("http://certifiedtorock.com/u/" . $uid);
    $dom_ctr     = new simple_html_dom();
    $dom_ctr->load($ctr_content);
    foreach ($dom_ctr->find('.content #lcd #lcd-inner') as $score) {
      if (is_numeric(trim(($score->find('div', 0)->plaintext)))) {
        $ctr_value = $score->find('div', 0)->plaintext;

        }
print"test";
    }
    if (empty($ctr_value)) {
      $ctr_value = 'User is not yet certified';
    }
    $users[] = array('uid' => $uid, 'user' => $user->plaintext, 'dolink' => 'http://drupal.org/user/' . $uid, 'ctr' => $ctr_value);

    # Store data in the datastore
    scraperwiki::save(array('uid'), $users);
  }
}
<?php
require 'scraperwiki/simple_html_dom.php';

$pages = 223;
$users = array();

for ($i = 0; $i <= $pages; $i++) {
  $contents = scraperWiki::scrape("http://drupal.org/profile/country/Finland?page=" . $i);
  $dom = new simple_html_dom();
  $dom->load($contents);
  foreach ($dom->find('#profile .profile .name a') as $user) {
    $uid         = end(explode('/', $user->href));
    $ctr_content = scraperWiki::scrape("http://certifiedtorock.com/u/" . $uid);
    $dom_ctr     = new simple_html_dom();
    $dom_ctr->load($ctr_content);
    foreach ($dom_ctr->find('.content #lcd #lcd-inner') as $score) {
      if (is_numeric(trim(($score->find('div', 0)->plaintext)))) {
        $ctr_value = $score->find('div', 0)->plaintext;

        }
print"test";
    }
    if (empty($ctr_value)) {
      $ctr_value = 'User is not yet certified';
    }
    $users[] = array('uid' => $uid, 'user' => $user->plaintext, 'dolink' => 'http://drupal.org/user/' . $uid, 'ctr' => $ctr_value);

    # Store data in the datastore
    scraperwiki::save(array('uid'), $users);
  }
}
