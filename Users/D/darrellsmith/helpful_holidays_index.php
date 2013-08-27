<?php
    
$index = 0;
$letters = array('A','B','C','D','E','F','G','H','J','K','L','M','P','Q','R','S','T','Z');

#require_once 'simplehtmldom_1_5/simple_html_dom.php';
require 'scraperwiki/simple_html_dom.php';


// dummy savevar() to workaround the bug!
scraperwiki::save_var('dummy', 0);

// resume from the last 'bookmark', in case it times out
$letterPlaceholder = scraperwiki::get_var("placeholderLetter");

 // if the letterplaceholder id not null, its a continuation from a previous scrape.
 // So skip over to where the last scrape left off.
if($letterPlaceholder != "")
    $letters = array_splice($letters, array_search($letterPlaceholder, $letters));    


// cycle through the letters of the alphabet, which in turn cycle through 0 - 300 to get all the cottages   
foreach ($letters as $letter) {
    scraperwiki::save_var("placeholderLetter",$letter);
   # echo($letter);   
    getSiteData($letter);
  
}

# Check for pages with no usable data
function fourOhFour($html){
    if(strpos($html,"<h1>No Active 2013 Property details found for",20000)!==false){
        return true;
    }
    return false;
}





# scrape the page
function getSiteData($letter){
    $dom = new simple_html_dom(); 
    # MAX_INDEX_SIZE, the maximum index for each Letter (A0-A600) increase this to search more pages
    $MAX_INDEX_SIZE = 300;
    $images = "";
    $description = "";
    $imgrecord = "";
    $agent = "helpfulholidays.com";


    $index = scraperwiki::get_var("placeholderIndex",0);
    if($index >= $MAX_INDEX_SIZE)
      $index=0;

    while($index<=$MAX_INDEX_SIZE){
       
        scraperwiki::save_var("placeholderIndex",$index);
    
        $url = "http://www.helpfulholidays.com/property.asp?ref=".$letter.$index."&year=2013";

        $html = scraperWiki::scrape($url); 
        // convert the character encoding to UTF-8
        $html = iconv("iso-8859-1", "UTF-8", $html);
       
        $dom->load($html);

        if(fourOhfour($dom)){
            $index++;
            continue;
        }else{
    // Write the records to an array 
          $record = array(
            'Helpful_Holiday_Index'         => $letter.$index
          );
       }
            
        
        # save the data
        scraperwiki::save(array('Helpful_Holiday_Index'), $record);
        
        # Move on to the next page
        $index++;
    }
}<?php
    
$index = 0;
$letters = array('A','B','C','D','E','F','G','H','J','K','L','M','P','Q','R','S','T','Z');

#require_once 'simplehtmldom_1_5/simple_html_dom.php';
require 'scraperwiki/simple_html_dom.php';


// dummy savevar() to workaround the bug!
scraperwiki::save_var('dummy', 0);

// resume from the last 'bookmark', in case it times out
$letterPlaceholder = scraperwiki::get_var("placeholderLetter");

 // if the letterplaceholder id not null, its a continuation from a previous scrape.
 // So skip over to where the last scrape left off.
if($letterPlaceholder != "")
    $letters = array_splice($letters, array_search($letterPlaceholder, $letters));    


// cycle through the letters of the alphabet, which in turn cycle through 0 - 300 to get all the cottages   
foreach ($letters as $letter) {
    scraperwiki::save_var("placeholderLetter",$letter);
   # echo($letter);   
    getSiteData($letter);
  
}

# Check for pages with no usable data
function fourOhFour($html){
    if(strpos($html,"<h1>No Active 2013 Property details found for",20000)!==false){
        return true;
    }
    return false;
}





# scrape the page
function getSiteData($letter){
    $dom = new simple_html_dom(); 
    # MAX_INDEX_SIZE, the maximum index for each Letter (A0-A600) increase this to search more pages
    $MAX_INDEX_SIZE = 300;
    $images = "";
    $description = "";
    $imgrecord = "";
    $agent = "helpfulholidays.com";


    $index = scraperwiki::get_var("placeholderIndex",0);
    if($index >= $MAX_INDEX_SIZE)
      $index=0;

    while($index<=$MAX_INDEX_SIZE){
       
        scraperwiki::save_var("placeholderIndex",$index);
    
        $url = "http://www.helpfulholidays.com/property.asp?ref=".$letter.$index."&year=2013";

        $html = scraperWiki::scrape($url); 
        // convert the character encoding to UTF-8
        $html = iconv("iso-8859-1", "UTF-8", $html);
       
        $dom->load($html);

        if(fourOhfour($dom)){
            $index++;
            continue;
        }else{
    // Write the records to an array 
          $record = array(
            'Helpful_Holiday_Index'         => $letter.$index
          );
       }
            
        
        # save the data
        scraperwiki::save(array('Helpful_Holiday_Index'), $record);
        
        # Move on to the next page
        $index++;
    }
}<?php
    
$index = 0;
$letters = array('A','B','C','D','E','F','G','H','J','K','L','M','P','Q','R','S','T','Z');

#require_once 'simplehtmldom_1_5/simple_html_dom.php';
require 'scraperwiki/simple_html_dom.php';


// dummy savevar() to workaround the bug!
scraperwiki::save_var('dummy', 0);

// resume from the last 'bookmark', in case it times out
$letterPlaceholder = scraperwiki::get_var("placeholderLetter");

 // if the letterplaceholder id not null, its a continuation from a previous scrape.
 // So skip over to where the last scrape left off.
if($letterPlaceholder != "")
    $letters = array_splice($letters, array_search($letterPlaceholder, $letters));    


// cycle through the letters of the alphabet, which in turn cycle through 0 - 300 to get all the cottages   
foreach ($letters as $letter) {
    scraperwiki::save_var("placeholderLetter",$letter);
   # echo($letter);   
    getSiteData($letter);
  
}

# Check for pages with no usable data
function fourOhFour($html){
    if(strpos($html,"<h1>No Active 2013 Property details found for",20000)!==false){
        return true;
    }
    return false;
}





# scrape the page
function getSiteData($letter){
    $dom = new simple_html_dom(); 
    # MAX_INDEX_SIZE, the maximum index for each Letter (A0-A600) increase this to search more pages
    $MAX_INDEX_SIZE = 300;
    $images = "";
    $description = "";
    $imgrecord = "";
    $agent = "helpfulholidays.com";


    $index = scraperwiki::get_var("placeholderIndex",0);
    if($index >= $MAX_INDEX_SIZE)
      $index=0;

    while($index<=$MAX_INDEX_SIZE){
       
        scraperwiki::save_var("placeholderIndex",$index);
    
        $url = "http://www.helpfulholidays.com/property.asp?ref=".$letter.$index."&year=2013";

        $html = scraperWiki::scrape($url); 
        // convert the character encoding to UTF-8
        $html = iconv("iso-8859-1", "UTF-8", $html);
       
        $dom->load($html);

        if(fourOhfour($dom)){
            $index++;
            continue;
        }else{
    // Write the records to an array 
          $record = array(
            'Helpful_Holiday_Index'         => $letter.$index
          );
       }
            
        
        # save the data
        scraperwiki::save(array('Helpful_Holiday_Index'), $record);
        
        # Move on to the next page
        $index++;
    }
}