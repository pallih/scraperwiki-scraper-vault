<?php
require 'scraperwiki/simple_html_dom.php';

/* Mobile pages are of no use bcoz it first Redirects to 
   Desktop page and Takes even more time,
   so its better to not use "mobile.brainyquote.com".
   So set '$mobilePage = false'
*/

 $count=1;              // to count total no of Quotes
 $mobilePage = false;  //to access mobile version  
 $maxPagination = 40;  

    for ($i=1; $i <=$maxPagination ; $i++) { 
        getAllquotes($i, $mobilePage);
    }

    function getAllquotes($i , $mobilePage)
    {
    
        global $count;
        
        //to decide which version to access Mobile/Desktop
        if($mobilePage == true)
            $url = 'http://mobile.brainyquote.com/quotes/topics/topic_funny'.$i. '.html';            
        else
            $url = 'http://www.brainyquote.com/quotes/topics/topic_funny'.$i. '.html';        
        
        $html = file_get_html($url);
        
        echo "<hr><h3>Page no: ".$i ."</h3>" ;
            foreach($html->find('.boxyPaddingBig') as $e)
            {
                echo "<hr>". $count++ . "<br>";
                $quote["text"] = $e->find('a[title="view quote"]',0)->innertext;
                $quote["author"] = $e->find('a[title="view author"]',0)->innertext;
                print_r($quote["text"]. "<br> -".$quote["author"]);
            }

        // you must call $dom->clear() to free memory if call file_get_dom() more then once. 
        $html->clear(); 
           unset($html);
    }

?><?php
require 'scraperwiki/simple_html_dom.php';

/* Mobile pages are of no use bcoz it first Redirects to 
   Desktop page and Takes even more time,
   so its better to not use "mobile.brainyquote.com".
   So set '$mobilePage = false'
*/

 $count=1;              // to count total no of Quotes
 $mobilePage = false;  //to access mobile version  
 $maxPagination = 40;  

    for ($i=1; $i <=$maxPagination ; $i++) { 
        getAllquotes($i, $mobilePage);
    }

    function getAllquotes($i , $mobilePage)
    {
    
        global $count;
        
        //to decide which version to access Mobile/Desktop
        if($mobilePage == true)
            $url = 'http://mobile.brainyquote.com/quotes/topics/topic_funny'.$i. '.html';            
        else
            $url = 'http://www.brainyquote.com/quotes/topics/topic_funny'.$i. '.html';        
        
        $html = file_get_html($url);
        
        echo "<hr><h3>Page no: ".$i ."</h3>" ;
            foreach($html->find('.boxyPaddingBig') as $e)
            {
                echo "<hr>". $count++ . "<br>";
                $quote["text"] = $e->find('a[title="view quote"]',0)->innertext;
                $quote["author"] = $e->find('a[title="view author"]',0)->innertext;
                print_r($quote["text"]. "<br> -".$quote["author"]);
            }

        // you must call $dom->clear() to free memory if call file_get_dom() more then once. 
        $html->clear(); 
           unset($html);
    }

?>