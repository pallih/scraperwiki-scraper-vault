<?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$page_url = "https://rakendused.vm.ee/akta/andmed.php?lk_andmed=1";
$html = scraperWiki::scrape($page_url); 
$dom = new simple_html_dom(); 
$dom->load($html);
//$innertabledata=$dom->find("div#sisuAla");

//grab all url links in search results page
$regexp = "<a\s[^>]*href=(\"??)(andmed_vaata[^\" >]*?)\\1[^>]*>(.*)<\/a>"; 
if(preg_match_all("/$regexp/siU", $html, $matches)) { 
    // This match creates three arrays within the $matches array.  
    //$matches[2] = array of link addresses --this is the one we want.  
    // $matches[3] = array of link text - including HTML code  
}

//extracts just the $matches[2] array and assigns it to a new array called $links
$link_count=count($matches[2]);
//print_r($matches[2]);
print "This array has ".$link_count." elements in it.";
$counter = 0;
$links = array();
while ($counter < $link_count) {
   $links[$counter] = $matches[2][$counter];
 //  print $links[$counter]."\n";
  $counter++;
}
print_r ($links);
//$unnested_link_count = count($links);
//print "the resulting array has ".$unnested_link_count." in it!";

//as a final step, now we can search through the $links array and find only the links that go to projects
//$project_link_counter = 0;
//$final_links = array();
/*while ($project_link_counter < $link_count) {
    if (preg_match("/^andmed_vaata/",$links[$project_link_counter],$link_matches)) {
         $final_links[]=$links[$counter];
    }
    $project_link_counter++;
}
*/
        $final_link_count = count($final_links);
        print "the resulting array has ".$final_link_count." in it!";



    

?>
<?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$page_url = "https://rakendused.vm.ee/akta/andmed.php?lk_andmed=1";
$html = scraperWiki::scrape($page_url); 
$dom = new simple_html_dom(); 
$dom->load($html);
//$innertabledata=$dom->find("div#sisuAla");

//grab all url links in search results page
$regexp = "<a\s[^>]*href=(\"??)(andmed_vaata[^\" >]*?)\\1[^>]*>(.*)<\/a>"; 
if(preg_match_all("/$regexp/siU", $html, $matches)) { 
    // This match creates three arrays within the $matches array.  
    //$matches[2] = array of link addresses --this is the one we want.  
    // $matches[3] = array of link text - including HTML code  
}

//extracts just the $matches[2] array and assigns it to a new array called $links
$link_count=count($matches[2]);
//print_r($matches[2]);
print "This array has ".$link_count." elements in it.";
$counter = 0;
$links = array();
while ($counter < $link_count) {
   $links[$counter] = $matches[2][$counter];
 //  print $links[$counter]."\n";
  $counter++;
}
print_r ($links);
//$unnested_link_count = count($links);
//print "the resulting array has ".$unnested_link_count." in it!";

//as a final step, now we can search through the $links array and find only the links that go to projects
//$project_link_counter = 0;
//$final_links = array();
/*while ($project_link_counter < $link_count) {
    if (preg_match("/^andmed_vaata/",$links[$project_link_counter],$link_matches)) {
         $final_links[]=$links[$counter];
    }
    $project_link_counter++;
}
*/
        $final_link_count = count($final_links);
        print "the resulting array has ".$final_link_count." in it!";



    

?>
