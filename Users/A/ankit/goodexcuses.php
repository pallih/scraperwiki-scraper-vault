<?php
    require 'scraperwiki/simple_html_dom.php';

$html;
$count = 0;

getExcuse("/Excuses/My-fish-is-sick-and-I-need-to-take-it-to-the-vet/");

function getExcuse($extension)
    {
        global $html;
        global $count;

        $root= "http://www.goodexcuses.co.uk";
        //$extension = "/Excuses/My-fish-is-sick-and-I-need-to-take-it-to-the-vet/" ;
        $html = file_get_html($root.$extension);
        
        //The excuse
        $excuse =$html->find('h2',0)->innertext;
        echo $excuse."\n";

        //save to DB
        $record = array(                          
                          'EXCUSE_ID'    =>   ++$count,
                          'EXCUSE_TEXT'  =>    $excuse,
                          'EXCUSE_URL'   =>    $extension,
                          );
        scraperwiki::save(array('EXCUSE_ID'), $record);       
        
     
        //Get next url
        //echo "\n".goToNextURL()."\n";
        goToNextURL();
    }

    //retrieve next url
    function goToNextURL()
    {
        global $html;
        $next = $html->find('h3 a',1);
        $html->clear(); 
        unset($html);           
        
        getExcuse($next->href);
        //return $next->href;
    }
?><?php
    require 'scraperwiki/simple_html_dom.php';

$html;
$count = 0;

getExcuse("/Excuses/My-fish-is-sick-and-I-need-to-take-it-to-the-vet/");

function getExcuse($extension)
    {
        global $html;
        global $count;

        $root= "http://www.goodexcuses.co.uk";
        //$extension = "/Excuses/My-fish-is-sick-and-I-need-to-take-it-to-the-vet/" ;
        $html = file_get_html($root.$extension);
        
        //The excuse
        $excuse =$html->find('h2',0)->innertext;
        echo $excuse."\n";

        //save to DB
        $record = array(                          
                          'EXCUSE_ID'    =>   ++$count,
                          'EXCUSE_TEXT'  =>    $excuse,
                          'EXCUSE_URL'   =>    $extension,
                          );
        scraperwiki::save(array('EXCUSE_ID'), $record);       
        
     
        //Get next url
        //echo "\n".goToNextURL()."\n";
        goToNextURL();
    }

    //retrieve next url
    function goToNextURL()
    {
        global $html;
        $next = $html->find('h3 a',1);
        $html->clear(); 
        unset($html);           
        
        getExcuse($next->href);
        //return $next->href;
    }
?>