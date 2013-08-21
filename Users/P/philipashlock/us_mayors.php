<?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';

// used for debugging
// $states = array("AL", "AK");

// There's a bug of some kind that makes the scraper time out or think its finished after California (CA), so until that is fixed, I just do the scraping in two parts. First is AL - CA and the next is CO - WY. 

//$states = array("AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","GU","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MO","MP","MS","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","PR","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");

$states = array("CO","CT","DC","DE","FL","GA","GU","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MO","MP","MS","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","PR","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");

$url = "http://www.usmayors.org/meetmayors/mayorsatglance.asp";

foreach ($states as $state) {
    //set POST variables
    $fields = array(
                'mode' => 'search_db',
                'State' => $state
            );

    $result = get_post_response($url,$fields);
            

    get_mayors($result);
    sleep(10); // required on scraperwiki.com

// used for debugging
   //if(empty($records)) {
   //    $records = get_mayors($result);                
   //} else {
   //    $records = array_merge($records, get_mayors($result));
   //}
    
}    



// used for debugging
    //header('Content-type: application/json'); print json_encode($records);


function get_post_response($url,$fields) {
    
    //url-ify the data for the POST
    foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
    rtrim($fields_string, '&');

    //open connection
    $ch = curl_init();

    //set the url, number of POST vars, POST data
    curl_setopt($ch,CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);        
    curl_setopt($ch,CURLOPT_POST, count($fields));
    curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

    //execute post
    $result = curl_exec($ch);

    //close connection
    curl_close($ch);
    
    return $result;
        
}





function get_mayors($html) {
    
    $dom = new simple_html_dom();
    $dom->load($html);

    
    foreach ($dom->find("div[@align=center] table") as $data) {
        
    
        //$image = $data->find("table[class=pagesSectionBodyTight] td", 0);
        //$text = $data->find("td", 0);

        //$name = $data->find("strong", 0);
        $raw = $data->innertext;
        $mayor = $data->find("strong", 0);
        $mayor = $mayor->innertext;
        
        $name = substr($mayor, 0, strpos($mayor, '<br>'));
        $location = substr($mayor, strpos($mayor, '<br>') + 4);
        $city = substr($location, 0, strpos($location, ','));
        $state = substr($location, strpos($location, ',') + 2);        

        $bio_url = $data->find("a[class=pagesSectionBodyTight]", 0);
        $bio_url = $bio_url->href;


        $info = null;
        $raw = null;
        
        // These conditions could probably be explicitly associated with each piece of data, but the 
        // variation with "not available" seemed like it could apply to anything, so I figured I'd be 
        // careful and test all condiations against each piece of data
        foreach ($data->find("table[class=pagesSectionBodyTight] td") as $row) {
            
            $raw_info = $row->innertext;
            
            $raw[] = $raw_info;
            
            
            $start = 0;
            $end = strlen($raw_info);
            
            if((strpos($raw_info, '<b>')) && (strpos($raw_info, '</b>'))) {            
                $start = strpos($raw_info, '<b>') + 3;
                $end = strpos($raw_info, '</b>');
            }
            
            // this is to catch the wild card of "not available"
            if(strpos($raw_info, '<i>')) {
                $start = strpos($raw_info, '<i>') + 3;
                $end = strpos($raw_info, '</i>');
            }
            
            if((strpos($raw_info, '<b>')) && (!strpos($raw_info, '</b>'))) {
                $start = strpos($raw_info, '<b>') + 3;
                $end = strpos($raw_info, '</a></B>') - 2;
            }
            
            if(strpos($raw_info, '<a href=') && (!strpos($raw_info, '</a></B>'))) {
                $start = strpos($raw_info, '">') + 2;
                $end = strpos($raw_info, '</a>');
            }    
            
            if(strpos($raw_info, 'height=270 width=216')) {
                $start = strpos($raw_info, '<img src=') + 9;                
                $end = strpos($raw_info, 'height=270') -1;
            }            

            $length = $end - $start;    
        
            $info[] =  substr($raw_info, $start, $length);
        }
        
        $url_photo = ($info[5]) ? 'http://www.usmayors.org' . $info[5] : null;
        $next_election = is_numeric(substr($info[2], 0, 1)) ? date("Y-m-d", strtotime($info[2])) : null;

        if($name) {
            
            //$record[] = array...... - used for debugging
            $record = array('name'=>$name, 
                                   'city' => $city, 
                                'state' => $state, 
                                   'population' => $info[0], 
                                'phone' => $info[1],
                                   'next_election' => $next_election, 
                                'email' => $info[3],
                                'url' => $info[4],
                                'bio_url' => $bio_url,
                                'url_photo' => $url_photo                                                                
                                );
            
            scraperwiki::save(array('city'), $record);
                    
        }

    }
      
//return $record;
    
}




?><?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';

// used for debugging
// $states = array("AL", "AK");

// There's a bug of some kind that makes the scraper time out or think its finished after California (CA), so until that is fixed, I just do the scraping in two parts. First is AL - CA and the next is CO - WY. 

//$states = array("AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","GU","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MO","MP","MS","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","PR","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");

$states = array("CO","CT","DC","DE","FL","GA","GU","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MO","MP","MS","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","PR","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");

$url = "http://www.usmayors.org/meetmayors/mayorsatglance.asp";

foreach ($states as $state) {
    //set POST variables
    $fields = array(
                'mode' => 'search_db',
                'State' => $state
            );

    $result = get_post_response($url,$fields);
            

    get_mayors($result);
    sleep(10); // required on scraperwiki.com

// used for debugging
   //if(empty($records)) {
   //    $records = get_mayors($result);                
   //} else {
   //    $records = array_merge($records, get_mayors($result));
   //}
    
}    



// used for debugging
    //header('Content-type: application/json'); print json_encode($records);


function get_post_response($url,$fields) {
    
    //url-ify the data for the POST
    foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
    rtrim($fields_string, '&');

    //open connection
    $ch = curl_init();

    //set the url, number of POST vars, POST data
    curl_setopt($ch,CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);        
    curl_setopt($ch,CURLOPT_POST, count($fields));
    curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

    //execute post
    $result = curl_exec($ch);

    //close connection
    curl_close($ch);
    
    return $result;
        
}





function get_mayors($html) {
    
    $dom = new simple_html_dom();
    $dom->load($html);

    
    foreach ($dom->find("div[@align=center] table") as $data) {
        
    
        //$image = $data->find("table[class=pagesSectionBodyTight] td", 0);
        //$text = $data->find("td", 0);

        //$name = $data->find("strong", 0);
        $raw = $data->innertext;
        $mayor = $data->find("strong", 0);
        $mayor = $mayor->innertext;
        
        $name = substr($mayor, 0, strpos($mayor, '<br>'));
        $location = substr($mayor, strpos($mayor, '<br>') + 4);
        $city = substr($location, 0, strpos($location, ','));
        $state = substr($location, strpos($location, ',') + 2);        

        $bio_url = $data->find("a[class=pagesSectionBodyTight]", 0);
        $bio_url = $bio_url->href;


        $info = null;
        $raw = null;
        
        // These conditions could probably be explicitly associated with each piece of data, but the 
        // variation with "not available" seemed like it could apply to anything, so I figured I'd be 
        // careful and test all condiations against each piece of data
        foreach ($data->find("table[class=pagesSectionBodyTight] td") as $row) {
            
            $raw_info = $row->innertext;
            
            $raw[] = $raw_info;
            
            
            $start = 0;
            $end = strlen($raw_info);
            
            if((strpos($raw_info, '<b>')) && (strpos($raw_info, '</b>'))) {            
                $start = strpos($raw_info, '<b>') + 3;
                $end = strpos($raw_info, '</b>');
            }
            
            // this is to catch the wild card of "not available"
            if(strpos($raw_info, '<i>')) {
                $start = strpos($raw_info, '<i>') + 3;
                $end = strpos($raw_info, '</i>');
            }
            
            if((strpos($raw_info, '<b>')) && (!strpos($raw_info, '</b>'))) {
                $start = strpos($raw_info, '<b>') + 3;
                $end = strpos($raw_info, '</a></B>') - 2;
            }
            
            if(strpos($raw_info, '<a href=') && (!strpos($raw_info, '</a></B>'))) {
                $start = strpos($raw_info, '">') + 2;
                $end = strpos($raw_info, '</a>');
            }    
            
            if(strpos($raw_info, 'height=270 width=216')) {
                $start = strpos($raw_info, '<img src=') + 9;                
                $end = strpos($raw_info, 'height=270') -1;
            }            

            $length = $end - $start;    
        
            $info[] =  substr($raw_info, $start, $length);
        }
        
        $url_photo = ($info[5]) ? 'http://www.usmayors.org' . $info[5] : null;
        $next_election = is_numeric(substr($info[2], 0, 1)) ? date("Y-m-d", strtotime($info[2])) : null;

        if($name) {
            
            //$record[] = array...... - used for debugging
            $record = array('name'=>$name, 
                                   'city' => $city, 
                                'state' => $state, 
                                   'population' => $info[0], 
                                'phone' => $info[1],
                                   'next_election' => $next_election, 
                                'email' => $info[3],
                                'url' => $info[4],
                                'bio_url' => $bio_url,
                                'url_photo' => $url_photo                                                                
                                );
            
            scraperwiki::save(array('city'), $record);
                    
        }

    }
      
//return $record;
    
}




?>