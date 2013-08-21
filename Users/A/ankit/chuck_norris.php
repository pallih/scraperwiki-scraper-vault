<?php
// It reaches 160sec limit on reaching upto 400 pages.
// Run it in parts 350 at a time


require 'scraperwiki/simple_html_dom.php';

$root_url = "http://www.chucknorrisfacts.com";

$joke_count = 0;

//First Page (no trailing page number)

    //To retrieve Last Page
    $html = file_get_html($root_url);

    $last = $html->find('li.pager-last a',0);

    $subject = $last->href; 

    $pattern = '/[0-9]+/';
    preg_match($pattern, $subject, $matches);
    
    $last_page = $matches[0];
    //echo "<h2>last_page</h2>".$last_page;
    // Print all jokes on Home-Page
    //echo "<h2>HomePage </h2>";
    foreach($html->find('.item-list ul li a.createYourOwn') as $joke)
    {
               saveIt($joke->innertext);
    }


// All other pages upto Last Page ($last_page)

for ($page=1; $page <= $last_page; $page++) 
{ 

        $html->clear(); 
        unset($html);        
        
             $url = $root_url."/all-chuck-norris-facts?page=".$page ;
             $html = file_get_html($url);

        //echo "<h2>Page ".($page+1)."</h2>";
        foreach($html->find('.item-list ul li a.createYourOwn') as $joke)
        {
               saveIt($joke->innertext);
        }
        
}

function saveIt($txt){
global $joke_count;
$record = array(
                              'JOKE_ID'    =>   ++$joke_count,
                              'JOKE_TEXT'  =>    $txt,
                                );
scraperwiki::save(array('JOKE_ID'), $record);          

//var_dump($record);
}

?>