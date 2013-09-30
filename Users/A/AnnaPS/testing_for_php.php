<?php
# Test scraper for PHP language.
# Should contain all our documented PHP functions.
# A fail in this scraper indicates a code failure somewhere.
require  'scraperwiki/simple_html_dom.php';

# Scrape function.
# TODO: Clarify, can we send POST parameters? Does not fail.
$arr = array("foo" => "bar");
$html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html", $arr);
print $html;

# Geo function.
$latlng = scraperwiki::gb_postcode_to_latlng("E1 5AW");
print $latlng[0];

# Save function including date and latlng.
$arr = array('name' => 'Fluffles', 'breed' => 'Alsatian');
scraperwiki::save(array('name'), $arr);
$date = time();
$arr = array("name", "breed", $date, $latlng);

# Metadata functions. 
$latest_message = scraperwiki::get_metadata('keyname', $default='No message yet');
print $latest_message;
$latest_message = 'Scraper input';
scraperwiki::save_metadata('latest_message',$latest_message);
$arr = array("breed","name");

?><?php
# Test scraper for PHP language.
# Should contain all our documented PHP functions.
# A fail in this scraper indicates a code failure somewhere.
require  'scraperwiki/simple_html_dom.php';

# Scrape function.
# TODO: Clarify, can we send POST parameters? Does not fail.
$arr = array("foo" => "bar");
$html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html", $arr);
print $html;

# Geo function.
$latlng = scraperwiki::gb_postcode_to_latlng("E1 5AW");
print $latlng[0];

# Save function including date and latlng.
$arr = array('name' => 'Fluffles', 'breed' => 'Alsatian');
scraperwiki::save(array('name'), $arr);
$date = time();
$arr = array("name", "breed", $date, $latlng);

# Metadata functions. 
$latest_message = scraperwiki::get_metadata('keyname', $default='No message yet');
print $latest_message;
$latest_message = 'Scraper input';
scraperwiki::save_metadata('latest_message',$latest_message);
$arr = array("breed","name");

?>