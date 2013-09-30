<?php
#name
#screen_name
#description
#profile_image_url
#profile_image_url_https
#url
#protected
#followers_count
#friends_count


// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$baseurl = "https://api.twitter.com/1/lists/members.xml?slug=MPs-on-Twitter&owner_screen_name=FinancialTimes&skip_status=true&include_entities=true";
$cursor = -1;
#print $baseurl."&cursor=".$cursor;

$html = scraperwiki::scrape($baseurl."&cursor=".$cursor);
$dom = new simple_html_dom();
$dom->load($html);


$arr = array();
foreach ($dom->find('users_list users user id') as $id )
    array_push($arr, $id->plaintext);

print_r($arr);

$nextcursor = $dom->find('next_cursor', 0);
#print $nextcursor;

#$arr = array(); 
#foreach ($dom->find('id') as $id)
#    array_push($arr, $id->plaintext);
#
#print_r($arr);


#end loop by setting cursor for next loop
#$cursor = $nextcursor
?><?php
#name
#screen_name
#description
#profile_image_url
#profile_image_url_https
#url
#protected
#followers_count
#friends_count


// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$baseurl = "https://api.twitter.com/1/lists/members.xml?slug=MPs-on-Twitter&owner_screen_name=FinancialTimes&skip_status=true&include_entities=true";
$cursor = -1;
#print $baseurl."&cursor=".$cursor;

$html = scraperwiki::scrape($baseurl."&cursor=".$cursor);
$dom = new simple_html_dom();
$dom->load($html);


$arr = array();
foreach ($dom->find('users_list users user id') as $id )
    array_push($arr, $id->plaintext);

print_r($arr);

$nextcursor = $dom->find('next_cursor', 0);
#print $nextcursor;

#$arr = array(); 
#foreach ($dom->find('id') as $id)
#    array_push($arr, $id->plaintext);
#
#print_r($arr);


#end loop by setting cursor for next loop
#$cursor = $nextcursor
?>