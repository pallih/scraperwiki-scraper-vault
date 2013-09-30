<?php
#download the webpage
$html = scraperwiki::scrape("http://www.npia.police.uk/en/5999.htm");



#step through the page line by line       
foreach(preg_split("/(\r?\n)/", $html) as $line){
#empty varibles 
    unset($url);
    unset($date);
    unset($title);
    unset($data);
    unset($record);



#match the lines containing the information wanted, extracting elements
#limiting it to a specific line in case there was dodgy data somewhere stopping it saving

 

   if (preg_match('/<h2><a href=\"(.*?)\">(\d.*?) -(.*?)<\/a>/', $line, $content)){

    #make urls absolute
    $url = "http://www.npia.police.uk".$content[1];
    $date = $content[2];
    $title = $content[3];

    #set url and title as unique keys
    $unique_keys = array('url', 'title');

    #We want the date in the form 2009-11-02
    #it is in the form  01 February 2011

    date_default_timezone_set('UTC'); 
    $timestamp = strtotime($date);
    $date= date('Y-m-d', $timestamp);


#save the data
#way that no longer works:
    $data['url']=$url;
   $data['title']=$title;
   $data['date']=$date;

##print_r($data); 
    scraperwiki::save(array('url'), $data);


#another way which also doesn't work!

#$record = array("url"=>$url, "title"=>$title, "date"=>$date);   

#print_r($record); 

#   scraperwiki::save(array('url'), $record);           
    }
}



?><?php
#download the webpage
$html = scraperwiki::scrape("http://www.npia.police.uk/en/5999.htm");



#step through the page line by line       
foreach(preg_split("/(\r?\n)/", $html) as $line){
#empty varibles 
    unset($url);
    unset($date);
    unset($title);
    unset($data);
    unset($record);



#match the lines containing the information wanted, extracting elements
#limiting it to a specific line in case there was dodgy data somewhere stopping it saving

 

   if (preg_match('/<h2><a href=\"(.*?)\">(\d.*?) -(.*?)<\/a>/', $line, $content)){

    #make urls absolute
    $url = "http://www.npia.police.uk".$content[1];
    $date = $content[2];
    $title = $content[3];

    #set url and title as unique keys
    $unique_keys = array('url', 'title');

    #We want the date in the form 2009-11-02
    #it is in the form  01 February 2011

    date_default_timezone_set('UTC'); 
    $timestamp = strtotime($date);
    $date= date('Y-m-d', $timestamp);


#save the data
#way that no longer works:
    $data['url']=$url;
   $data['title']=$title;
   $data['date']=$date;

##print_r($data); 
    scraperwiki::save(array('url'), $data);


#another way which also doesn't work!

#$record = array("url"=>$url, "title"=>$title, "date"=>$date);   

#print_r($record); 

#   scraperwiki::save(array('url'), $record);           
    }
}



?>