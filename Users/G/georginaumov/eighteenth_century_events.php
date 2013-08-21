<?php
 require 'scraperwiki/simple_html_dom.php'; 

 $strReponse = scraperwiki::scrape("http://en.wikipedia.org/wiki/Eighteenth_century#Events");

 $patternContent = '@<\s*li\s*>\s*<\s*a\s+href="/wiki/[0-9]+"\s+title="[0-9]+"\s*>(?P<start_year>[0-9]+)<\/a>(?::|-|–)(?P<content>(?:(?!<\s*\/\s*li\s*>)(?:.|\s))+)<\s*\/\s*li\s*>@is';
 $patternEndYear = '@^(?P<end_year>[0-9]{4})@';
 
 $maches = array();

 $preparedData = array();

 if (preg_match_all($patternContent, $strReponse, $maches, PREG_SET_ORDER) != false) {

     $size = count($maches);

     for($i = 0 ; $i < $size; $i++) {
        
         // if there is end year provided we must get it 
         $endYearMach = array();

         $dataToStore = array( "start" => $maches[$i]["start_year"] );

         $dom = str_get_html($maches[$i]["content"]);
         $dataToStore['description']  = $dom->plaintext;  
         
         if (preg_match($patternEndYear, $dataToStore['description'] ,  $endYearMach) != 0){
             $dataToStore["end"] = $endYearMach["end_year"];
         }

         // get link and title 
         $linkAndTitleMatch = array();

         preg_replace('@<\s*a\s+href="/wiki/[0-9]+"\s+title="[0-9]+"\s*>[0-9]+<\/a>@', '', $maches[$i]["content"]);

         if (preg_match('@\s*<\s*a\s+href="(?<link>[^"]+)"\s+title="(?P<title>[^0-9][^"]+)"\s*>@', $maches[$i]["content"] ,  $linkAndTitleMatch) != 0){
             $dataToStore['link'] = 'http://en.wikipedia.org' . $linkAndTitleMatch['link'];
             $dataToStore['title'] = $linkAndTitleMatch['title'];
         }  
         
        if (count($dataToStore)) {
           if (isset($dataToStore['end']) == false) {
               $dataToStore['end'] = null;       
           }

             $columns = array_keys($dataToStore);
              
             @scraperwiki::save($columns, $dataToStore);
             
           }
        }

}
?>
