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
        }

    // get longtiude / latitude
        $element = $dom->find('body');
        $geoData = $element[0]->attr['onload'];

        

    // get description
        foreach($dom->find('div[id=prop_place_descs]') as $element){        
            $tds = $element->find('tr');
            $description =  utf8_encode($tds[0]->plaintext);
        }

    // get Cottage name
        $element = $dom->find('title');
        $firstTitle =  substr($element[0], strpos($element[0],"|")+1);
        $cottageName = substr( $firstTitle,0,strpos($firstTitle,"sleeps"));
        

    // get images
        $imgrecord ="";
        foreach($dom->find('img[src^=media/'.$letter.$index.']') as $element){ 
            $imgs = $element->find('src');
            $imgsrc = $element->attr['src'];
            $imgrecord .= "http://www.helpfulholidays.com/".$imgsrc.",";
        }
            

    // get features
     foreach($dom->find('div[id=features]') as $element){        
            $tds = $element->find('td');
            $features =  utf8_encode($tds[0]->plaintext);
        }



    // get Price High
     $brecord =  array();
     foreach($dom->find('tr[class=gen9]') as $data){
        $btds = $data->find("td[class=border-std]"); 
        if(count($btds)==11){ 
          array_push($brecord,  $btds[1]->plaintext);
        }
     }
     rsort($brecord); 
     $Pricehigh = $brecord[1];
     $Pricelow = $brecord[count($brecord)-1];




    // get main elements and write to
        foreach($dom->find('td[class=gen11]') as $element){
          $tds = $element->find('tr');
          if(count($tds)==10){
              
              # Bedrooms and bedroom types
              $bedroom_type = trim(str_replace("Bedrooms: ","",$tds[7]->plaintext));
              $bedroom_type  = str_replace("&nbsp;"," ",$bedroom_type);
              $str = preg_replace('/[^0-9.]+/', '-', $bedroom_type);
              $bed_array = explode('-',$str);
              $bedroom_num = "";
              foreach($bed_array as $room){
                $bedroom_num = $bedroom_num  + $room;    
              }

              # Clean the data of special chars
              $areaDesc = substr($description,0,strpos($description,"The property"));
              $areaDesc = str_replace("The place: ","",$areaDesc);
              $areaDesc = html_entity_decode($areaDesc);
              $areaDesc   = strip_tags($areaDesc);
              $areaDesc   = str_replace("Ã©","e",$areaDesc);
              $areaDesc   = str_replace("Â","",$areaDesc);
              
            
              # $cottageDesc  = html_entity_decode($cottageDesc  );
              $cottageDesc = substr($description, strpos($description,"The property"));      
              $cottageDesc  = strip_tags($cottageDesc);        
              $cottageDesc  = str_replace("&nbsp;","",$cottageDesc);
              $cottageDesc  = str_replace("Ã©","e",$cottageDesc  );
              $cottageDesc  = str_replace("Â","",$cottageDesc);
            

             # $features = html_entity_decode($features);
              $features = str_replace("&nbsp;","",$features );
              $features = strip_tags($features ); 
              $features = trim(str_replace("’","'",str_replace("”","'",$features)));
              $features = str_replace("Ã©","e",$features );
              $features = str_replace("Â","",$features );
             // $features = html_entity_decode($features);
 

     
    // Write the records to an array 
              $geoArry = explode(',', $geoData);
              $record = array(

                  'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

                  'COTTAGE_NAME'       => trim($cottageName),

                  'PRICE_LOW'          => trim($Pricelow) ,

                  'PRICE_HIGH'         => trim($Pricehigh) ,

                  'DESCRIPTION'        => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $cottageDesc)),

                  'FEATURES'           => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ',  $features)),    

                  'IMAGES'             => $imgrecord,

                  'CHANGEOVERDAY'      => trim(str_replace("Changeover day: ","", $tds[6]->plaintext)),

                  'LINK'               => $url,

                  'BEDROOMS'            => $bedroom_num,

                  'Bedroom_types'      => $bedroom_type,

                  'BATHROOMS'          => trim(substr($tds[8]->plaintext, stripos($tds[8]->plaintext,":")+1)),

                  'LONGTITUDE'         => trim($geoArry[2]),

                  'LATITUDE'           => trim($geoArry[1]),

                  'POSTCODE'           => "NA",

                  'SLEEPS'             => trim(str_replace("\t","", str_replace("Sleeps:","",$tds[4]->plaintext))),

                  'PETS'               => "NA",

                  'Agent'              => $agent,

                  'Location'           => trim(str_replace("Location: ", "",$tds[1]->plaintext)),
                
                  'Region'             => trim(str_replace("Region: ","",$tds[2]->plaintext)),
                 
                  'County'             => trim(str_replace("County: ","",$tds[3]->plaintext)),

                  'AREA_DESC'          => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $areaDesc)),                 
              );
            }
        }
        # save the data
        scraperwiki::save(array('COTTAGE_ID'), $record);
        
        # Move on to the next page
        $index++;
     }
    }
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
        }

    // get longtiude / latitude
        $element = $dom->find('body');
        $geoData = $element[0]->attr['onload'];

        

    // get description
        foreach($dom->find('div[id=prop_place_descs]') as $element){        
            $tds = $element->find('tr');
            $description =  utf8_encode($tds[0]->plaintext);
        }

    // get Cottage name
        $element = $dom->find('title');
        $firstTitle =  substr($element[0], strpos($element[0],"|")+1);
        $cottageName = substr( $firstTitle,0,strpos($firstTitle,"sleeps"));
        

    // get images
        $imgrecord ="";
        foreach($dom->find('img[src^=media/'.$letter.$index.']') as $element){ 
            $imgs = $element->find('src');
            $imgsrc = $element->attr['src'];
            $imgrecord .= "http://www.helpfulholidays.com/".$imgsrc.",";
        }
            

    // get features
     foreach($dom->find('div[id=features]') as $element){        
            $tds = $element->find('td');
            $features =  utf8_encode($tds[0]->plaintext);
        }



    // get Price High
     $brecord =  array();
     foreach($dom->find('tr[class=gen9]') as $data){
        $btds = $data->find("td[class=border-std]"); 
        if(count($btds)==11){ 
          array_push($brecord,  $btds[1]->plaintext);
        }
     }
     rsort($brecord); 
     $Pricehigh = $brecord[1];
     $Pricelow = $brecord[count($brecord)-1];




    // get main elements and write to
        foreach($dom->find('td[class=gen11]') as $element){
          $tds = $element->find('tr');
          if(count($tds)==10){
              
              # Bedrooms and bedroom types
              $bedroom_type = trim(str_replace("Bedrooms: ","",$tds[7]->plaintext));
              $bedroom_type  = str_replace("&nbsp;"," ",$bedroom_type);
              $str = preg_replace('/[^0-9.]+/', '-', $bedroom_type);
              $bed_array = explode('-',$str);
              $bedroom_num = "";
              foreach($bed_array as $room){
                $bedroom_num = $bedroom_num  + $room;    
              }

              # Clean the data of special chars
              $areaDesc = substr($description,0,strpos($description,"The property"));
              $areaDesc = str_replace("The place: ","",$areaDesc);
              $areaDesc = html_entity_decode($areaDesc);
              $areaDesc   = strip_tags($areaDesc);
              $areaDesc   = str_replace("Ã©","e",$areaDesc);
              $areaDesc   = str_replace("Â","",$areaDesc);
              
            
              # $cottageDesc  = html_entity_decode($cottageDesc  );
              $cottageDesc = substr($description, strpos($description,"The property"));      
              $cottageDesc  = strip_tags($cottageDesc);        
              $cottageDesc  = str_replace("&nbsp;","",$cottageDesc);
              $cottageDesc  = str_replace("Ã©","e",$cottageDesc  );
              $cottageDesc  = str_replace("Â","",$cottageDesc);
            

             # $features = html_entity_decode($features);
              $features = str_replace("&nbsp;","",$features );
              $features = strip_tags($features ); 
              $features = trim(str_replace("’","'",str_replace("”","'",$features)));
              $features = str_replace("Ã©","e",$features );
              $features = str_replace("Â","",$features );
             // $features = html_entity_decode($features);
 

     
    // Write the records to an array 
              $geoArry = explode(',', $geoData);
              $record = array(

                  'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

                  'COTTAGE_NAME'       => trim($cottageName),

                  'PRICE_LOW'          => trim($Pricelow) ,

                  'PRICE_HIGH'         => trim($Pricehigh) ,

                  'DESCRIPTION'        => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $cottageDesc)),

                  'FEATURES'           => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ',  $features)),    

                  'IMAGES'             => $imgrecord,

                  'CHANGEOVERDAY'      => trim(str_replace("Changeover day: ","", $tds[6]->plaintext)),

                  'LINK'               => $url,

                  'BEDROOMS'            => $bedroom_num,

                  'Bedroom_types'      => $bedroom_type,

                  'BATHROOMS'          => trim(substr($tds[8]->plaintext, stripos($tds[8]->plaintext,":")+1)),

                  'LONGTITUDE'         => trim($geoArry[2]),

                  'LATITUDE'           => trim($geoArry[1]),

                  'POSTCODE'           => "NA",

                  'SLEEPS'             => trim(str_replace("\t","", str_replace("Sleeps:","",$tds[4]->plaintext))),

                  'PETS'               => "NA",

                  'Agent'              => $agent,

                  'Location'           => trim(str_replace("Location: ", "",$tds[1]->plaintext)),
                
                  'Region'             => trim(str_replace("Region: ","",$tds[2]->plaintext)),
                 
                  'County'             => trim(str_replace("County: ","",$tds[3]->plaintext)),

                  'AREA_DESC'          => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $areaDesc)),                 
              );
            }
        }
        # save the data
        scraperwiki::save(array('COTTAGE_ID'), $record);
        
        # Move on to the next page
        $index++;
     }
    }
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
        }

    // get longtiude / latitude
        $element = $dom->find('body');
        $geoData = $element[0]->attr['onload'];

        

    // get description
        foreach($dom->find('div[id=prop_place_descs]') as $element){        
            $tds = $element->find('tr');
            $description =  utf8_encode($tds[0]->plaintext);
        }

    // get Cottage name
        $element = $dom->find('title');
        $firstTitle =  substr($element[0], strpos($element[0],"|")+1);
        $cottageName = substr( $firstTitle,0,strpos($firstTitle,"sleeps"));
        

    // get images
        $imgrecord ="";
        foreach($dom->find('img[src^=media/'.$letter.$index.']') as $element){ 
            $imgs = $element->find('src');
            $imgsrc = $element->attr['src'];
            $imgrecord .= "http://www.helpfulholidays.com/".$imgsrc.",";
        }
            

    // get features
     foreach($dom->find('div[id=features]') as $element){        
            $tds = $element->find('td');
            $features =  utf8_encode($tds[0]->plaintext);
        }



    // get Price High
     $brecord =  array();
     foreach($dom->find('tr[class=gen9]') as $data){
        $btds = $data->find("td[class=border-std]"); 
        if(count($btds)==11){ 
          array_push($brecord,  $btds[1]->plaintext);
        }
     }
     rsort($brecord); 
     $Pricehigh = $brecord[1];
     $Pricelow = $brecord[count($brecord)-1];




    // get main elements and write to
        foreach($dom->find('td[class=gen11]') as $element){
          $tds = $element->find('tr');
          if(count($tds)==10){
              
              # Bedrooms and bedroom types
              $bedroom_type = trim(str_replace("Bedrooms: ","",$tds[7]->plaintext));
              $bedroom_type  = str_replace("&nbsp;"," ",$bedroom_type);
              $str = preg_replace('/[^0-9.]+/', '-', $bedroom_type);
              $bed_array = explode('-',$str);
              $bedroom_num = "";
              foreach($bed_array as $room){
                $bedroom_num = $bedroom_num  + $room;    
              }

              # Clean the data of special chars
              $areaDesc = substr($description,0,strpos($description,"The property"));
              $areaDesc = str_replace("The place: ","",$areaDesc);
              $areaDesc = html_entity_decode($areaDesc);
              $areaDesc   = strip_tags($areaDesc);
              $areaDesc   = str_replace("Ã©","e",$areaDesc);
              $areaDesc   = str_replace("Â","",$areaDesc);
              
            
              # $cottageDesc  = html_entity_decode($cottageDesc  );
              $cottageDesc = substr($description, strpos($description,"The property"));      
              $cottageDesc  = strip_tags($cottageDesc);        
              $cottageDesc  = str_replace("&nbsp;","",$cottageDesc);
              $cottageDesc  = str_replace("Ã©","e",$cottageDesc  );
              $cottageDesc  = str_replace("Â","",$cottageDesc);
            

             # $features = html_entity_decode($features);
              $features = str_replace("&nbsp;","",$features );
              $features = strip_tags($features ); 
              $features = trim(str_replace("’","'",str_replace("”","'",$features)));
              $features = str_replace("Ã©","e",$features );
              $features = str_replace("Â","",$features );
             // $features = html_entity_decode($features);
 

     
    // Write the records to an array 
              $geoArry = explode(',', $geoData);
              $record = array(

                  'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

                  'COTTAGE_NAME'       => trim($cottageName),

                  'PRICE_LOW'          => trim($Pricelow) ,

                  'PRICE_HIGH'         => trim($Pricehigh) ,

                  'DESCRIPTION'        => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $cottageDesc)),

                  'FEATURES'           => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ',  $features)),    

                  'IMAGES'             => $imgrecord,

                  'CHANGEOVERDAY'      => trim(str_replace("Changeover day: ","", $tds[6]->plaintext)),

                  'LINK'               => $url,

                  'BEDROOMS'            => $bedroom_num,

                  'Bedroom_types'      => $bedroom_type,

                  'BATHROOMS'          => trim(substr($tds[8]->plaintext, stripos($tds[8]->plaintext,":")+1)),

                  'LONGTITUDE'         => trim($geoArry[2]),

                  'LATITUDE'           => trim($geoArry[1]),

                  'POSTCODE'           => "NA",

                  'SLEEPS'             => trim(str_replace("\t","", str_replace("Sleeps:","",$tds[4]->plaintext))),

                  'PETS'               => "NA",

                  'Agent'              => $agent,

                  'Location'           => trim(str_replace("Location: ", "",$tds[1]->plaintext)),
                
                  'Region'             => trim(str_replace("Region: ","",$tds[2]->plaintext)),
                 
                  'County'             => trim(str_replace("County: ","",$tds[3]->plaintext)),

                  'AREA_DESC'          => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $areaDesc)),                 
              );
            }
        }
        # save the data
        scraperwiki::save(array('COTTAGE_ID'), $record);
        
        # Move on to the next page
        $index++;
     }
    }
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
        }

    // get longtiude / latitude
        $element = $dom->find('body');
        $geoData = $element[0]->attr['onload'];

        

    // get description
        foreach($dom->find('div[id=prop_place_descs]') as $element){        
            $tds = $element->find('tr');
            $description =  utf8_encode($tds[0]->plaintext);
        }

    // get Cottage name
        $element = $dom->find('title');
        $firstTitle =  substr($element[0], strpos($element[0],"|")+1);
        $cottageName = substr( $firstTitle,0,strpos($firstTitle,"sleeps"));
        

    // get images
        $imgrecord ="";
        foreach($dom->find('img[src^=media/'.$letter.$index.']') as $element){ 
            $imgs = $element->find('src');
            $imgsrc = $element->attr['src'];
            $imgrecord .= "http://www.helpfulholidays.com/".$imgsrc.",";
        }
            

    // get features
     foreach($dom->find('div[id=features]') as $element){        
            $tds = $element->find('td');
            $features =  utf8_encode($tds[0]->plaintext);
        }



    // get Price High
     $brecord =  array();
     foreach($dom->find('tr[class=gen9]') as $data){
        $btds = $data->find("td[class=border-std]"); 
        if(count($btds)==11){ 
          array_push($brecord,  $btds[1]->plaintext);
        }
     }
     rsort($brecord); 
     $Pricehigh = $brecord[1];
     $Pricelow = $brecord[count($brecord)-1];




    // get main elements and write to
        foreach($dom->find('td[class=gen11]') as $element){
          $tds = $element->find('tr');
          if(count($tds)==10){
              
              # Bedrooms and bedroom types
              $bedroom_type = trim(str_replace("Bedrooms: ","",$tds[7]->plaintext));
              $bedroom_type  = str_replace("&nbsp;"," ",$bedroom_type);
              $str = preg_replace('/[^0-9.]+/', '-', $bedroom_type);
              $bed_array = explode('-',$str);
              $bedroom_num = "";
              foreach($bed_array as $room){
                $bedroom_num = $bedroom_num  + $room;    
              }

              # Clean the data of special chars
              $areaDesc = substr($description,0,strpos($description,"The property"));
              $areaDesc = str_replace("The place: ","",$areaDesc);
              $areaDesc = html_entity_decode($areaDesc);
              $areaDesc   = strip_tags($areaDesc);
              $areaDesc   = str_replace("Ã©","e",$areaDesc);
              $areaDesc   = str_replace("Â","",$areaDesc);
              
            
              # $cottageDesc  = html_entity_decode($cottageDesc  );
              $cottageDesc = substr($description, strpos($description,"The property"));      
              $cottageDesc  = strip_tags($cottageDesc);        
              $cottageDesc  = str_replace("&nbsp;","",$cottageDesc);
              $cottageDesc  = str_replace("Ã©","e",$cottageDesc  );
              $cottageDesc  = str_replace("Â","",$cottageDesc);
            

             # $features = html_entity_decode($features);
              $features = str_replace("&nbsp;","",$features );
              $features = strip_tags($features ); 
              $features = trim(str_replace("’","'",str_replace("”","'",$features)));
              $features = str_replace("Ã©","e",$features );
              $features = str_replace("Â","",$features );
             // $features = html_entity_decode($features);
 

     
    // Write the records to an array 
              $geoArry = explode(',', $geoData);
              $record = array(

                  'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

                  'COTTAGE_NAME'       => trim($cottageName),

                  'PRICE_LOW'          => trim($Pricelow) ,

                  'PRICE_HIGH'         => trim($Pricehigh) ,

                  'DESCRIPTION'        => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $cottageDesc)),

                  'FEATURES'           => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ',  $features)),    

                  'IMAGES'             => $imgrecord,

                  'CHANGEOVERDAY'      => trim(str_replace("Changeover day: ","", $tds[6]->plaintext)),

                  'LINK'               => $url,

                  'BEDROOMS'            => $bedroom_num,

                  'Bedroom_types'      => $bedroom_type,

                  'BATHROOMS'          => trim(substr($tds[8]->plaintext, stripos($tds[8]->plaintext,":")+1)),

                  'LONGTITUDE'         => trim($geoArry[2]),

                  'LATITUDE'           => trim($geoArry[1]),

                  'POSTCODE'           => "NA",

                  'SLEEPS'             => trim(str_replace("\t","", str_replace("Sleeps:","",$tds[4]->plaintext))),

                  'PETS'               => "NA",

                  'Agent'              => $agent,

                  'Location'           => trim(str_replace("Location: ", "",$tds[1]->plaintext)),
                
                  'Region'             => trim(str_replace("Region: ","",$tds[2]->plaintext)),
                 
                  'County'             => trim(str_replace("County: ","",$tds[3]->plaintext)),

                  'AREA_DESC'          => trim(preg_replace(array('/\s{2,}/', '/[\t\n]/'), ' ', $areaDesc)),                 
              );
            }
        }
        # save the data
        scraperwiki::save(array('COTTAGE_ID'), $record);
        
        # Move on to the next page
        $index++;
     }
    }
