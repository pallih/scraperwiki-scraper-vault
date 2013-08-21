<?php

    require 'scraperwiki/simple_html_dom.php';

    $html_content= scraperWiki::scrape("www.dsbs.co.uk/local-driving-lessons");
    $html = str_get_html($html_content);
    $line = array();
    $i = 0;    
    
    foreach ($html->find("#counties-list li") as $row) {
    
        $url = preg_match('/<a href=\"([^\"]*)\">(.*)<\/a>/iU', $row->innertext, $match);     
    
        $i = $i +1;
    
        $line[$i]["ID"] = $i;
        $line[$i]["permalink"] = $match[1]; 
        $line[$i]["name"] = $match[2]; 



    }


     for($i=50;$i<116;$i++) {

        $html_content= scraperWiki::scrape("http://www.dsbs.co.uk" .$line[$i]["permalink"] );
        $html = str_get_html($html_content);

        foreach ($html->find("#county-content") as $x) { $line[$i]["content"] = $x->innertext; }
        
        foreach ($html->find("#county-cities ") as $x) { $line[$i]["cities"] = $x->innertext; }

        echo $line[$i]["ID"] . ' / ' . $line[$i]["name"] . '/n';
         
        scraperwiki::save(array('ID'),$line[$i]); 
 
    }  
?>