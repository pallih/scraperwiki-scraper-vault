<?php

require 'scraperwiki/simple_html_dom.php';           
for ($i=1; $i<=100; $i+=24)
{
    $main_url = "http://www.homeshop18.com/fiction/categoryid:10016/search:/listView:true/start:".$i;
    //print_r($main_url);
    $main_html_content = scraperwiki::scrape($main_url);
    $main_html = str_get_html($main_html_content);
    
    foreach ($main_html->find("<a.productTitle") as $techdiv) {
      
        $url="http://www.homeshop18.com".$techdiv->href;
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
        foreach ($html->find("div#productImageBox img") as $el) {           
             $img_url = $el->src ;
        }
        foreach ($html->find("div#product-info h2.product-name span") as $el) {           
        //    if(el->itemprop=="name")
               $title = $el->innertext ;
        }
        foreach ($html->find("div#product-info span.product-name-by") as $el) {           
              while($el->next_sibling()->tag == "a")        
                {
                $el = $el->next_sibling();
                $authors =  $authors.$el->plaintext.", " ;
                }
        }
        
        foreach ($html->find("div.costs em#mrpPrice") as $el) {           
        //    if(el->itemprop=="name")
                $mrp = str_replace("&#x20B9;&nbsp;","Rs. ",$el->plaintext);
        }
        foreach ($html->find("div.costs h3.cost-now span#hs18Price") as $el) {           
        //    if(el->itemprop=="name")
                $hs18price = str_replace("&#x20B9;&nbsp;","Rs. ",$el->plaintext);
        }
        foreach ($html->find("table.more-detail-tb tr td.col1") as $el) {           
            if($el->plaintext=="Publisher")
                $publisher = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="ISBN-10")
                $isbn_10 = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="ISBN")
                $isbn_13 = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="No of Pages")
                $no_of_pages = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Cover")
                $cover = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Language")
                $language =  str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Date of Publication")
                $date_of_publication = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Year of Publication")
                $year_of_publication = str_replace(": ","",$el->next_sibling()->plaintext);
            
        }
        scraperwiki::save_sqlite(array("isbn_13"),array("title"=>$title, "url"=>$url, "img_url"=>$img_url, "publisher"=>$publisher, "authors"=>$authors, "mrp"=>$mrp, "hs18price"=>$hs18price, "isbn_10"=>$isbn_10, "isbn_13"=>$isbn_13, "no_of_pages"=>$no_of_pages, "cover"=>$cover, "language"=>$language, "date_of_publication"=>$date_of_publication, "year_of_publication"=>$year_of_publication));  
        

    }
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';           
for ($i=1; $i<=100; $i+=24)
{
    $main_url = "http://www.homeshop18.com/fiction/categoryid:10016/search:/listView:true/start:".$i;
    //print_r($main_url);
    $main_html_content = scraperwiki::scrape($main_url);
    $main_html = str_get_html($main_html_content);
    
    foreach ($main_html->find("<a.productTitle") as $techdiv) {
      
        $url="http://www.homeshop18.com".$techdiv->href;
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
        foreach ($html->find("div#productImageBox img") as $el) {           
             $img_url = $el->src ;
        }
        foreach ($html->find("div#product-info h2.product-name span") as $el) {           
        //    if(el->itemprop=="name")
               $title = $el->innertext ;
        }
        foreach ($html->find("div#product-info span.product-name-by") as $el) {           
              while($el->next_sibling()->tag == "a")        
                {
                $el = $el->next_sibling();
                $authors =  $authors.$el->plaintext.", " ;
                }
        }
        
        foreach ($html->find("div.costs em#mrpPrice") as $el) {           
        //    if(el->itemprop=="name")
                $mrp = str_replace("&#x20B9;&nbsp;","Rs. ",$el->plaintext);
        }
        foreach ($html->find("div.costs h3.cost-now span#hs18Price") as $el) {           
        //    if(el->itemprop=="name")
                $hs18price = str_replace("&#x20B9;&nbsp;","Rs. ",$el->plaintext);
        }
        foreach ($html->find("table.more-detail-tb tr td.col1") as $el) {           
            if($el->plaintext=="Publisher")
                $publisher = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="ISBN-10")
                $isbn_10 = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="ISBN")
                $isbn_13 = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="No of Pages")
                $no_of_pages = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Cover")
                $cover = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Language")
                $language =  str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Date of Publication")
                $date_of_publication = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Year of Publication")
                $year_of_publication = str_replace(": ","",$el->next_sibling()->plaintext);
            
        }
        scraperwiki::save_sqlite(array("isbn_13"),array("title"=>$title, "url"=>$url, "img_url"=>$img_url, "publisher"=>$publisher, "authors"=>$authors, "mrp"=>$mrp, "hs18price"=>$hs18price, "isbn_10"=>$isbn_10, "isbn_13"=>$isbn_13, "no_of_pages"=>$no_of_pages, "cover"=>$cover, "language"=>$language, "date_of_publication"=>$date_of_publication, "year_of_publication"=>$year_of_publication));  
        

    }
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';           
for ($i=1; $i<=100; $i+=24)
{
    $main_url = "http://www.homeshop18.com/fiction/categoryid:10016/search:/listView:true/start:".$i;
    //print_r($main_url);
    $main_html_content = scraperwiki::scrape($main_url);
    $main_html = str_get_html($main_html_content);
    
    foreach ($main_html->find("<a.productTitle") as $techdiv) {
      
        $url="http://www.homeshop18.com".$techdiv->href;
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
        foreach ($html->find("div#productImageBox img") as $el) {           
             $img_url = $el->src ;
        }
        foreach ($html->find("div#product-info h2.product-name span") as $el) {           
        //    if(el->itemprop=="name")
               $title = $el->innertext ;
        }
        foreach ($html->find("div#product-info span.product-name-by") as $el) {           
              while($el->next_sibling()->tag == "a")        
                {
                $el = $el->next_sibling();
                $authors =  $authors.$el->plaintext.", " ;
                }
        }
        
        foreach ($html->find("div.costs em#mrpPrice") as $el) {           
        //    if(el->itemprop=="name")
                $mrp = str_replace("&#x20B9;&nbsp;","Rs. ",$el->plaintext);
        }
        foreach ($html->find("div.costs h3.cost-now span#hs18Price") as $el) {           
        //    if(el->itemprop=="name")
                $hs18price = str_replace("&#x20B9;&nbsp;","Rs. ",$el->plaintext);
        }
        foreach ($html->find("table.more-detail-tb tr td.col1") as $el) {           
            if($el->plaintext=="Publisher")
                $publisher = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="ISBN-10")
                $isbn_10 = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="ISBN")
                $isbn_13 = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="No of Pages")
                $no_of_pages = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Cover")
                $cover = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Language")
                $language =  str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Date of Publication")
                $date_of_publication = str_replace(": ","",$el->next_sibling()->plaintext);
            else if($el->plaintext=="Year of Publication")
                $year_of_publication = str_replace(": ","",$el->next_sibling()->plaintext);
            
        }
        scraperwiki::save_sqlite(array("isbn_13"),array("title"=>$title, "url"=>$url, "img_url"=>$img_url, "publisher"=>$publisher, "authors"=>$authors, "mrp"=>$mrp, "hs18price"=>$hs18price, "isbn_10"=>$isbn_10, "isbn_13"=>$isbn_13, "no_of_pages"=>$no_of_pages, "cover"=>$cover, "language"=>$language, "date_of_publication"=>$date_of_publication, "year_of_publication"=>$year_of_publication));  
        

    }
}
?>
