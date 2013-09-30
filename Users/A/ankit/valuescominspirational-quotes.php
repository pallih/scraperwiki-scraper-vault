<?php

require 'scraperwiki/simple_html_dom.php';

$root_url = "http://www.values.com";
$quote_count = 0;

// All other pages upto Last Page ($last_page)
$last_page = 500;

for ($page=1; $page <= $last_page; $page++) 
{ 
             $url = $root_url."/inspirational-quotes?page=".$page;
             $html = file_get_html($url);

        foreach($html->find('.index_card') as $card )
    {
        $quote =  $card->find('.quotation',0)->innertext;       
        $author = $card->find('.quotation_author',0)->plaintext;
                
        $quote = cleanQuotes($quote);
        $author = cleanAuthor($author);
    
        //echo "<br>".$quote."<br>";
        //echo '-'.$author."<hr>";        
try{        
saveIt($quote,$author);
}
catch(Exception $e)
{
saveIt("$e","NOTHING");
}

    }
        
$html->clear(); 
unset($html);   
}

function cleanQuotes($str)
    {
    $str= str_replace("&ldquo;", "", $str);
    $str= str_replace("&rdquo;", "", $str);
    return $str;
    }

function cleanAuthor($a)
    {
    $a = str_replace("&nbsp;&nbsp;&nbsp;Share or Discuss This Quote", "", $a);
    $a = trim($a);
    return $a;
    }

function saveIt($txt,$author){
        global $quote_count;
        $record = array(
                      'QUOTE_ID'    =>   ++$quote_count,
                      'QUOTE_TEXT'  =>    $txt,
                      'QUOTE_AUTHOR' =>   $author 
                        );
        
scraperwiki::save(array('QUOTE_ID'), $record);          
        }

?><?php

require 'scraperwiki/simple_html_dom.php';

$root_url = "http://www.values.com";
$quote_count = 0;

// All other pages upto Last Page ($last_page)
$last_page = 500;

for ($page=1; $page <= $last_page; $page++) 
{ 
             $url = $root_url."/inspirational-quotes?page=".$page;
             $html = file_get_html($url);

        foreach($html->find('.index_card') as $card )
    {
        $quote =  $card->find('.quotation',0)->innertext;       
        $author = $card->find('.quotation_author',0)->plaintext;
                
        $quote = cleanQuotes($quote);
        $author = cleanAuthor($author);
    
        //echo "<br>".$quote."<br>";
        //echo '-'.$author."<hr>";        
try{        
saveIt($quote,$author);
}
catch(Exception $e)
{
saveIt("$e","NOTHING");
}

    }
        
$html->clear(); 
unset($html);   
}

function cleanQuotes($str)
    {
    $str= str_replace("&ldquo;", "", $str);
    $str= str_replace("&rdquo;", "", $str);
    return $str;
    }

function cleanAuthor($a)
    {
    $a = str_replace("&nbsp;&nbsp;&nbsp;Share or Discuss This Quote", "", $a);
    $a = trim($a);
    return $a;
    }

function saveIt($txt,$author){
        global $quote_count;
        $record = array(
                      'QUOTE_ID'    =>   ++$quote_count,
                      'QUOTE_TEXT'  =>    $txt,
                      'QUOTE_AUTHOR' =>   $author 
                        );
        
scraperwiki::save(array('QUOTE_ID'), $record);          
        }

?>