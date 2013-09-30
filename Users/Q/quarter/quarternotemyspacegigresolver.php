<?php
#######################################################
#
# Quarter Note
# Scrape MySpace and return :
# Large HTML Table of Events and Gigs
#
#######################################################

require  'scraperwiki/simple_html_dom.php';

# These are the elements we are interested in receiving!
$artistName      = "devo";
$myspaceURL      = "http://www.myspace.com/" . $artistName;
$html            = scraperwiki::scrape( $myspaceURL );

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$myspaceDOM = new simple_html_dom();
$myspaceDOM->load($html);

$artistEvents = $myspaceDOM->find('div[id=profile_bandschedule]',0)->plaintext;


scraperwiki::save(
    array('myspaceID'), 
    array('events' => $artistEvents, 'myspaceID' => $artistName )
);
   //
    
?><?php
#######################################################
#
# Quarter Note
# Scrape MySpace and return :
# Large HTML Table of Events and Gigs
#
#######################################################

require  'scraperwiki/simple_html_dom.php';

# These are the elements we are interested in receiving!
$artistName      = "devo";
$myspaceURL      = "http://www.myspace.com/" . $artistName;
$html            = scraperwiki::scrape( $myspaceURL );

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$myspaceDOM = new simple_html_dom();
$myspaceDOM->load($html);

$artistEvents = $myspaceDOM->find('div[id=profile_bandschedule]',0)->plaintext;


scraperwiki::save(
    array('myspaceID'), 
    array('events' => $artistEvents, 'myspaceID' => $artistName )
);
   //
    
?>