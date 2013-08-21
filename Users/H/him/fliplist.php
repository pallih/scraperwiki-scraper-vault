<?php

require 'scraperwiki/simple_html_dom.php';           
for ($i=1; $i<=100; $i+=20)
{
    $main_url = "http://www.flipkart.com/books/educational-and-professional/academic-and-professional/school/pr?p%5B%5D=sort%3Dpopularity&sid=bks%2Cenp%2Cq2s%2Czze&start=".$i;
    print($main_url);
    $main_html_content = scraperwiki::scrape($main_url);
    $main_html = str_get_html($main_html_content);
    
    foreach ($main_html->find("<a.lu-title") as $techdiv) {
      
        $url="http://www.flipkart.com".$techdiv->href;
        $title="";
        $img_url="";
        $publisher="";
        $authors="";
        $mrp="";
        $hs18price="";
        $isbn_10="";
        $isbn_13="";
        $no_of_pages="";
        $cover="";
        $language="";
        $date_of_publication="";
        $year_of_publication="";
        $html_content = scraperwiki::scrape($url);
        $html = str_get_html($html_content);
        
        scraperwiki::save_sqlite(array("url"),array("url"=>$url));
    }
}
?>
