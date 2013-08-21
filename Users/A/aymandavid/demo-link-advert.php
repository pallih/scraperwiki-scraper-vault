<?php
$random_url = array("http://www.tdscripts.com/linkorg.html",
                    "http://www.tdscripts.com/keno.html",
                    "http://www.tdscripts.com/ezibill.shtml",
                    "http://www.tdscripts.com/tdforum.shtml",
                    "http://www.tdscripts.com/picofday.html",
                    "http://www.tdscripts.com/gutsorglory.html");

$url_title = array("Link Organizer",
                   "TD Keno",
                   "eziBill *Free Promotion!",
                   "TD Forum",
                   "TD Pic of Day PHP",
                   "Guts or Glory Poker PHP");
$url_desc = array("- A comprehensive link list organizer",
"- Offer your site visitors an engaging Keno game without the monetary risk",
"- Sell access to and protect your membership area using iBill and our eziBill script",
"- An unthreaded messageboard script to exchange ideas with your site visitors",
"- Run your own picture of the day script from any site anywhere with this handy script",
"- A casino-style card game written entirely in PHP");
srand(time());
$sizeof = count($random_url);
$random = (rand()%$sizeof);
print("<center><a href=\"$random_url[$random]\">$url_title[$random]</a> $url_desc[$random]</center>");
?>
