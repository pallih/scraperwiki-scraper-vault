<?php
require 'scraperwiki/simple_html_dom.php';

$url = "http://www.hobbyking.com/hobbyking/store/brushless_motor_rc_data.asp";

print "Retrieving motor list\n";
   
$html = scraperWiki::scrape($url);
//print $html . "\n";

// Get table of motors:
// Each row contains the following (amongst other stuff too):
// <td...>
//  [<a href="#" onclick="ajax2('motorcompare.asp?idproduct=14397','batt2')">2</a>]
//  [<a href="#" onclick="ajax2('motorcompare.asp?idproduct=14397','batt3')">3</a>]
//  [<a href="#" onclick="ajax2('motorcompare.asp?idproduct=14397','batt4')">4</a>]
// ...</td>
// Use regex to look for 'motorcompare.asp?idproduct=14397', specifically extract the number.
$regex_pattern = "/\'motorcompare.asp\?idproduct=(.*?)\'/";

preg_match_all($regex_pattern, $html, $matches);

$ids = $matches[1];

foreach ($ids as $id)
{
    $id = intval($id);
    //print $id . "\n";
    scraperwiki::save(array("id"), array( "id" => $id));
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';

$url = "http://www.hobbyking.com/hobbyking/store/brushless_motor_rc_data.asp";

print "Retrieving motor list\n";
   
$html = scraperWiki::scrape($url);
//print $html . "\n";

// Get table of motors:
// Each row contains the following (amongst other stuff too):
// <td...>
//  [<a href="#" onclick="ajax2('motorcompare.asp?idproduct=14397','batt2')">2</a>]
//  [<a href="#" onclick="ajax2('motorcompare.asp?idproduct=14397','batt3')">3</a>]
//  [<a href="#" onclick="ajax2('motorcompare.asp?idproduct=14397','batt4')">4</a>]
// ...</td>
// Use regex to look for 'motorcompare.asp?idproduct=14397', specifically extract the number.
$regex_pattern = "/\'motorcompare.asp\?idproduct=(.*?)\'/";

preg_match_all($regex_pattern, $html, $matches);

$ids = $matches[1];

foreach ($ids as $id)
{
    $id = intval($id);
    //print $id . "\n";
    scraperwiki::save(array("id"), array( "id" => $id));
}

?>
