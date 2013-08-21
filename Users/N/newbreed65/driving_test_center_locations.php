<?php

    require 'scraperwiki/simple_html_dom.php';

    $html_content= scraperWiki::scrape("www.dsbs.co.uk/local-driving-lessons");
    $html = str_get_html($html_content);
    $line = array();
    $i = 1;    
    
    foreach ($html->find("#cities-list li") as $row) {
    
        $url = preg_match('/<a href=\"([^\"]*)\">(.*)<\/a>/iU', $row->innertext, $match);     
    
        $i = $i +1;
    
        $line[$i]["ID"] = $i;
        $line[$i]["permalink"] = $match[1]; 
        $line[$i]["name"] = $match[2]; 

    }


   // for($i=1;$i<count($line);$i++) {
    for($i=2625;$i<2629($line);$i++) {

        $html_content= scraperWiki::scrape("http://www.dsbs.co.uk" .$line[$i]["permalink"] );
        $html = str_get_html($html_content);

        foreach ($html->find(".stai-block") as $x) { $line[$i]["content"] = $x->innertext; }  
        
        echo $line[$i]["ID"] . ' / ' . $line[$i]["name"] . '/n';
         
        scraperwiki::save(array('ID'),$line[$i]); 
 
    } 
    
?><?php

    require 'scraperwiki/simple_html_dom.php';

    $html_content= scraperWiki::scrape("www.dsbs.co.uk/local-driving-lessons");
    $html = str_get_html($html_content);
    $line = array();
    $i = 1;    
    
    foreach ($html->find("#cities-list li") as $row) {
    
        $url = preg_match('/<a href=\"([^\"]*)\">(.*)<\/a>/iU', $row->innertext, $match);     
    
        $i = $i +1;
    
        $line[$i]["ID"] = $i;
        $line[$i]["permalink"] = $match[1]; 
        $line[$i]["name"] = $match[2]; 

    }


   // for($i=1;$i<count($line);$i++) {
    for($i=2625;$i<2629($line);$i++) {

        $html_content= scraperWiki::scrape("http://www.dsbs.co.uk" .$line[$i]["permalink"] );
        $html = str_get_html($html_content);

        foreach ($html->find(".stai-block") as $x) { $line[$i]["content"] = $x->innertext; }  
        
        echo $line[$i]["ID"] . ' / ' . $line[$i]["name"] . '/n';
         
        scraperwiki::save(array('ID'),$line[$i]); 
 
    } 
    
?>