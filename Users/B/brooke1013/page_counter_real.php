<?php

require 'scraperwiki/simple_html_dom.php';$page_counter = 0;
$page_counter = 0;
$next_page = 1;

while ($next_page>0){
    $page_counter++;
    $page_url = "https://rakendused.vm.ee/akta/andmed.php?lk_andmed=".$page_counter;
   // print $page_url."this is the page url \n";
    $html_data = scraperwiki::scrape($page_url);
    if (preg_match('/title="l&otilde;ppu".*lk_andmed=(\d+)/', $html_data, $next_page_url)) {
        //$next_page_url = $next_page_url[0];
        print_r ($next_page_url);
    } else {
        $next_page = 0;
    }
  print $page_url." this is the page url \n";

} 



?>


