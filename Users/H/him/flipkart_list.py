<?php

require 'scraperwiki/simple_html_dom.php';           
for ($i=1; $i<=100; $i+=24)
{
    $main_url = "http://www.flipkart.com/books/educational-and-professional/academic-and-professional/school/pr?p%5B%5D=sort%3Dpopularity&sid=bks%2Cenp%2Cq2s%2Czze&start=".$i;
    //print_r($main_url);
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
        foreach ($html->find("span#main-image div div img") as $el) {           
             $img_url = $el->src ;
        }
        foreach ($html->find("div#mprod-summary-title h1") as $el) {           
               $title = $el->innertext ;
        }
        scraperwiki::save_sqlite(array("isbn_13"),array("title"=>$title, "url"=>$url, "img_url"=>$img_url, "publisher"=>$publisher, "authors"=>$authors, "mrp"=>$mrp, "hs18price"=>$hs18price, "isbn_10"=>$isbn_10, "isbn_13"=>$isbn_13, "no_of_pages"=>$no_of_pages, "cover"=>$cover, "language"=>$language, "date_of_publication"=>$date_of_publication, "year_of_publication"=>$year_of_publication));  
        

    }
}
?>
