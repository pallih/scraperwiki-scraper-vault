<?php

/*
*   Scrapes posts from a user's tumblr page(s) and spits out their permalink URLs, Quick 'n' Dirty.
*   Warning! This script shouts!
*   Fork it, ... if you can! ;)
*   (C) 2012, realdomdom
*   Licensed under the GNU General Public License (http://www.gnu.org/licenses/gpl-3.0.txt)
*/

require 'scraperwiki/simple_html_dom.php'; // this is just some fucked up script to make HTML tag fondling sexier

$link_number = 0; // link count (honestly, i don't know why i put it)
$allthelinks[] = ""; // All the URLs!
$thevictim = "twitulama"; // replace with some victims username
$victimstrace = $thevictim . ".tumblr.com";
$howmanypages = 2; // replace with the actual number of pages you want it to search for and shoot in your face
$datsearchpattern = "div[class*='post'] a[href*='/post/'], li[class*='post'] a[href*='/post/'], p[class*='post'] a[href*='/post/']"; // see http://simplehtmldom.sourceforge.net/manual.htm for help

print $thevictim . " is \$thevictim.\n";
print "Wait... \$howmanypages did you want me to scrape? Oh right, " . $howmanypages . ".\n";

print "For-loop incoming...\n";
for ($page = 1; $page <= $howmanypages; $page++) {
    print "Scraping dat \$page " . $page . "...\n";
    $dathtml = scraperWiki::scrape("http://" . $thevictim . ".tumblr.com/page/" . $page);
    print "http://" . $thevictim . ".tumblr.com/page/" . $page;
    $dom = new simple_html_dom();
    $dom -> load($dathtml);
    print "Foreach-loop incoming...\n";
    foreach($dom -> find($datsearchpattern) as $element_a){ 
        print "Currently, \$element_a is " . $element_a . "\n";
        $attribute_href = $element_a -> href;
        print "Currently, \$attribute_href is \"" . $attribute_href . "\"\n";
        $allthelinks[$link_number] = $attribute_href;
        //print "scraperwiki::save_var says: ";
        //print_r(scraperwiki::save_var($link_number, $attribute_href)); // like i said, quick 'n' dirty 
        print "And \$link_number is " . $link_number . ".\n\n";
        $link_number += 1;
        print "Brace yourselfs...\n";
    }
    print "Foreach-loop made it through the end. Wow.\n\nBrace yourselfs...\n";
}
print "For-loop made it through the end. Phew.\n";

print "\n";
print "First URL was \"" . $allthelinks[0] ."\"\n";
print "Last URL was \"" . $attribute_href . "\"\n";
print $link_number . " URLs found initially.\n";
$allthelinks = array_unique($allthelinks); // Throwing out those double entries
$allthelinks = array_values($allthelinks); // Making new index
$link_number = count($allthelinks); // Counting what's left
print $link_number . " unique URLs found.\n";
$countdat = 0;
foreach($allthelinks as $datlink){ 
    if (stripos($datlink, $victimstrace) !== FALSE) {
    $alltheuserlinks = array($countdat, $datlink);
    $countdat += 1;
    }
}
print $countdat . " URLs found belong to " . $thevictim . ".\n\n";
print "Here it goes... nggghhh\n";
var_dump($alltheuserlinks); // And now taking a dump in your face

//print "scraperwiki::save says: ";
scraperwiki::save(0,var_dump($allthelinks));

?>
<?php

/*
*   Scrapes posts from a user's tumblr page(s) and spits out their permalink URLs, Quick 'n' Dirty.
*   Warning! This script shouts!
*   Fork it, ... if you can! ;)
*   (C) 2012, realdomdom
*   Licensed under the GNU General Public License (http://www.gnu.org/licenses/gpl-3.0.txt)
*/

require 'scraperwiki/simple_html_dom.php'; // this is just some fucked up script to make HTML tag fondling sexier

$link_number = 0; // link count (honestly, i don't know why i put it)
$allthelinks[] = ""; // All the URLs!
$thevictim = "twitulama"; // replace with some victims username
$victimstrace = $thevictim . ".tumblr.com";
$howmanypages = 2; // replace with the actual number of pages you want it to search for and shoot in your face
$datsearchpattern = "div[class*='post'] a[href*='/post/'], li[class*='post'] a[href*='/post/'], p[class*='post'] a[href*='/post/']"; // see http://simplehtmldom.sourceforge.net/manual.htm for help

print $thevictim . " is \$thevictim.\n";
print "Wait... \$howmanypages did you want me to scrape? Oh right, " . $howmanypages . ".\n";

print "For-loop incoming...\n";
for ($page = 1; $page <= $howmanypages; $page++) {
    print "Scraping dat \$page " . $page . "...\n";
    $dathtml = scraperWiki::scrape("http://" . $thevictim . ".tumblr.com/page/" . $page);
    print "http://" . $thevictim . ".tumblr.com/page/" . $page;
    $dom = new simple_html_dom();
    $dom -> load($dathtml);
    print "Foreach-loop incoming...\n";
    foreach($dom -> find($datsearchpattern) as $element_a){ 
        print "Currently, \$element_a is " . $element_a . "\n";
        $attribute_href = $element_a -> href;
        print "Currently, \$attribute_href is \"" . $attribute_href . "\"\n";
        $allthelinks[$link_number] = $attribute_href;
        //print "scraperwiki::save_var says: ";
        //print_r(scraperwiki::save_var($link_number, $attribute_href)); // like i said, quick 'n' dirty 
        print "And \$link_number is " . $link_number . ".\n\n";
        $link_number += 1;
        print "Brace yourselfs...\n";
    }
    print "Foreach-loop made it through the end. Wow.\n\nBrace yourselfs...\n";
}
print "For-loop made it through the end. Phew.\n";

print "\n";
print "First URL was \"" . $allthelinks[0] ."\"\n";
print "Last URL was \"" . $attribute_href . "\"\n";
print $link_number . " URLs found initially.\n";
$allthelinks = array_unique($allthelinks); // Throwing out those double entries
$allthelinks = array_values($allthelinks); // Making new index
$link_number = count($allthelinks); // Counting what's left
print $link_number . " unique URLs found.\n";
$countdat = 0;
foreach($allthelinks as $datlink){ 
    if (stripos($datlink, $victimstrace) !== FALSE) {
    $alltheuserlinks = array($countdat, $datlink);
    $countdat += 1;
    }
}
print $countdat . " URLs found belong to " . $thevictim . ".\n\n";
print "Here it goes... nggghhh\n";
var_dump($alltheuserlinks); // And now taking a dump in your face

//print "scraperwiki::save says: ";
scraperwiki::save(0,var_dump($allthelinks));

?>
