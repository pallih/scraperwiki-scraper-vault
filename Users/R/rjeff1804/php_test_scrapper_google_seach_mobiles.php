<?php
 
/* update your path accordingly */
include("lib/simplehtmldom/simple_html_dom.php");

$search_term = "mobiles";
 
$url = "http://www.google.co.in/search?hl=en&q={$search_term}";
 
$html = file_get_html($url);
 
/*
Get all table rows having the id attribute named 'rhsline'.
As the list of sponsored links is in the 'ol' tag; as can be
seen from the DOM tree above; we use the 'children' function
on the $data object to get the sponsored links.
*/
$data =  $html->find('td[id=mbEnd]');
 
/*
  Make sure that sponsors ads are available,
  Some keywords do not have sponsor ads.
*/
if(isset($data[0]))
    echo $data[0]->children(1);
 
?>
