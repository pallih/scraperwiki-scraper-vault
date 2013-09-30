<?php
    
$index = 0;
$letters = array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');

#require_once 'simplehtmldom_1_5/simple_html_dom.php';
require 'scraperwiki/simple_html_dom.php';


// dummy savevar() to workaround the bug!
scraperwiki::save_var('dummy', 0);



$letterPlaceholder = scraperwiki::get_var("placeholderLetter");
 // if the letterplaceholder id not null, its a continuation from a previous scrape.
 // So skip over to where the last scrape left off.



if($letterPlaceholder != "")
    $letters = array_splice($letters, array_search($letterPlaceholder, $letters));    


// cycle through the letters of the alphabet, which in turn cycle through 0 - 300 to get all the cottages   
foreach ($letters as $letter) {
    echo($letter);   
    getSiteData($letter);
}




function fourOhFour($dom){
    $isfour_oh_four =$dom->find('H1');
    if(stripos($isfour_oh_four[0],"<h1>No Active 2013 Property details found for")!==false){
        return 1;
    }
    return 0;
}


function getSiteData($letter){
    $MAX_INDEX_SIZE = 300;
    $images = "";
    $description = "";
    $imgrecord = "";
    $agent = "helpfulholidays.com";


    $index = scraperwiki::get_var("placeholderIndex",0);
      if($index == $MAX_INDEX_SIZE)
          $index=0;

    while($index<=$MAX_INDEX_SIZE){
        scraperwiki::save_var("placeholderLetter",$letter);
        scraperwiki::save_var("placeholderIndex",$index);
    
        $url = "http://www.helpfulholidays.com/property.asp?ref=".$letter.$index."&year=2013";
        $dom = new simple_html_dom();
        $html = file_get_html($url);
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
            $description =  utf8_encode (($tds[0]->plaintext));
        }


    // get images
        foreach($dom->find('img[src^=media/'.$letter.$index.']') as $element){
        
            $imgs = $element->find('src');
            $imgsrc = $element->attr['src'];
            $imgrecord .= "http://www.helpfulholidays.com/".$imgsrc;
            }
            

    // get features
     foreach($dom->find('div[id=features]') as $element){        
            $tds = $element->find('td');
            $features =  utf8_encode (($tds[0]->plaintext));
        }


    // get main elements and write to
        foreach($dom->find('td[class=gen11]') as $element){
            
            $tds = $element->find('tr');
        
          if(count($tds)==10){
              // sort out the price by removing dodgy chars and extra text
              $price = str_replace("Prices from "  , "", utf8_encode ($tds[9]->plaintext));    
              $price = substr($price, 2);
              $price = str_replace(")", "",$price);
              $price = str_replace("£", "",$price);
              $price = trim(substr($price,strpos($price, "(")+1));
     
    // Write the records to the database
                  $geoArry = explode(',', $geoData);
                   $record = array(

                  'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

                  'COTTAGE_NAME'         => $letter.$index,

                  'PRICE_LOW'          => utf8_encode(trim(substr($price,strpos($price, "(")+1))),

                  'PRICE_HIGH'         => "NA",

                  "DESCRIPTION"         => utf8_encode(str_replace("’","'",str_replace("”","'",$description))),

                  "FEATURES"            => utf8_encode(str_replace("’","'",str_replace("”","'",$features))),

                  "IMAGES"             => $imgrecord,

                  'CHANGEOVERDAY'     => trim(str_replace("Changeover day: ","", $tds[6]->plaintext)),

                  'LINK'                 => $url,

                  'BEDROOMS'              => trim(str_replace("Bedrooms: ","",$tds[7]->plaintext)),

                  'BATHROOMS'          => trim(substr($tds[8]->plaintext, stripos($tds[8]->plaintext,":")+1)),

                  'LONGTITUDE'         => $geoArry[2],

                  'LATITUDE'             => $geoArry[1],

                  'POSTCODE'             => "NA",

                  'SLEEPS'              => trim(str_replace("\t","", str_replace("Sleeps:","",$tds[4]->plaintext))),

                  'PETS'                 => "NA",

                  "AGENT"             => $agent,

                'Location'              => trim(str_replace("Location: ", "",$tds[1]->plaintext)),
                
                 'Region'              => trim(str_replace("Region: ","",$tds[2]->plaintext)),
                 
                 'County'              => trim(str_replace("County: ","",$tds[3]->plaintext)),
                 );
              }
            }

        scraperwiki::save(array('COTTAGE_ID'), $record);

        $index++;
     }
    }





<?php
    
$index = 0;
$letters = array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');

#require_once 'simplehtmldom_1_5/simple_html_dom.php';
require 'scraperwiki/simple_html_dom.php';


// dummy savevar() to workaround the bug!
scraperwiki::save_var('dummy', 0);



$letterPlaceholder = scraperwiki::get_var("placeholderLetter");
 // if the letterplaceholder id not null, its a continuation from a previous scrape.
 // So skip over to where the last scrape left off.



if($letterPlaceholder != "")
    $letters = array_splice($letters, array_search($letterPlaceholder, $letters));    


// cycle through the letters of the alphabet, which in turn cycle through 0 - 300 to get all the cottages   
foreach ($letters as $letter) {
    echo($letter);   
    getSiteData($letter);
}




function fourOhFour($dom){
    $isfour_oh_four =$dom->find('H1');
    if(stripos($isfour_oh_four[0],"<h1>No Active 2013 Property details found for")!==false){
        return 1;
    }
    return 0;
}


function getSiteData($letter){
    $MAX_INDEX_SIZE = 300;
    $images = "";
    $description = "";
    $imgrecord = "";
    $agent = "helpfulholidays.com";


    $index = scraperwiki::get_var("placeholderIndex",0);
      if($index == $MAX_INDEX_SIZE)
          $index=0;

    while($index<=$MAX_INDEX_SIZE){
        scraperwiki::save_var("placeholderLetter",$letter);
        scraperwiki::save_var("placeholderIndex",$index);
    
        $url = "http://www.helpfulholidays.com/property.asp?ref=".$letter.$index."&year=2013";
        $dom = new simple_html_dom();
        $html = file_get_html($url);
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
            $description =  utf8_encode (($tds[0]->plaintext));
        }


    // get images
        foreach($dom->find('img[src^=media/'.$letter.$index.']') as $element){
        
            $imgs = $element->find('src');
            $imgsrc = $element->attr['src'];
            $imgrecord .= "http://www.helpfulholidays.com/".$imgsrc;
            }
            

    // get features
     foreach($dom->find('div[id=features]') as $element){        
            $tds = $element->find('td');
            $features =  utf8_encode (($tds[0]->plaintext));
        }


    // get main elements and write to
        foreach($dom->find('td[class=gen11]') as $element){
            
            $tds = $element->find('tr');
        
          if(count($tds)==10){
              // sort out the price by removing dodgy chars and extra text
              $price = str_replace("Prices from "  , "", utf8_encode ($tds[9]->plaintext));    
              $price = substr($price, 2);
              $price = str_replace(")", "",$price);
              $price = str_replace("£", "",$price);
              $price = trim(substr($price,strpos($price, "(")+1));
     
    // Write the records to the database
                  $geoArry = explode(',', $geoData);
                   $record = array(

                  'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

                  'COTTAGE_NAME'         => $letter.$index,

                  'PRICE_LOW'          => utf8_encode(trim(substr($price,strpos($price, "(")+1))),

                  'PRICE_HIGH'         => "NA",

                  "DESCRIPTION"         => utf8_encode(str_replace("’","'",str_replace("”","'",$description))),

                  "FEATURES"            => utf8_encode(str_replace("’","'",str_replace("”","'",$features))),

                  "IMAGES"             => $imgrecord,

                  'CHANGEOVERDAY'     => trim(str_replace("Changeover day: ","", $tds[6]->plaintext)),

                  'LINK'                 => $url,

                  'BEDROOMS'              => trim(str_replace("Bedrooms: ","",$tds[7]->plaintext)),

                  'BATHROOMS'          => trim(substr($tds[8]->plaintext, stripos($tds[8]->plaintext,":")+1)),

                  'LONGTITUDE'         => $geoArry[2],

                  'LATITUDE'             => $geoArry[1],

                  'POSTCODE'             => "NA",

                  'SLEEPS'              => trim(str_replace("\t","", str_replace("Sleeps:","",$tds[4]->plaintext))),

                  'PETS'                 => "NA",

                  "AGENT"             => $agent,

                'Location'              => trim(str_replace("Location: ", "",$tds[1]->plaintext)),
                
                 'Region'              => trim(str_replace("Region: ","",$tds[2]->plaintext)),
                 
                 'County'              => trim(str_replace("County: ","",$tds[3]->plaintext)),
                 );
              }
            }

        scraperwiki::save(array('COTTAGE_ID'), $record);

        $index++;
     }
    }





