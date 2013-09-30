<?php

//house cleaning
//scraperwiki::save_sqlite(array('id'), array('id'=>1, 'lat'=>1, 'lng'=>1), "users2");
//die;

require 'scraperwiki/simple_html_dom.php';     

function neat_r($arr, $return = false) {
    $out = array();
    $oldtab = "    ";
    $newtab = "-";
    
    $lines = explode("\n", print_r($arr, true));
    
    foreach ($lines as $line) {
 
        //remove numeric indexes like "[0] =>" unless the value is an array
        if (substr($line, -5) != "Array") {    $line = preg_replace("/^(\s*)\[[0-9]+\] => /", "$1", $line, 1); }
        
        //garbage symbols
        foreach (array(
            "Array" => "",
            "["     => "",
            "]"     => "",
            " =>"   => ":",
        ) as $old => $new) {
            $out = str_replace($old, $new, $out);
        }
 
        //garbage lines
        if (in_array(trim($line), array("Array", "(", ")", ""))) continue;
 
        //indents
        $indent = "";
        $indents = floor((substr_count($line, $oldtab) - 1) / 2);
        if ($indents > 0) { for ($i = 0; $i < $indents; $i++) { $indent .= $newtab; } }
 
        $out[] = $indent . trim($line);
    }
 
    $out = implode("\n", $out) . "\n";
    if ($return == true) return $out;
    echo $out;
}

//FIRST go through most voted magento questions and capture question links...
 
//$i<=316 insert this when ready to run there are 316 pages
//make 1==1 below if we want to run this section

if (1==2) for($i=1; $i<=300; $i++) {

    $url = "http://stackoverflow.com/questions/tagged/magento?page=".$i."&sort=votes&pagesize=50";
    
    $html = scraperWiki::scrape($url); 
    $dom = new simple_html_dom();
    $dom->load($html); 
    
    foreach($dom->find('a[class=question-hyperlink]') as $data ){
        $questions['url']=$data->href;
        preg_match("/\/questions\/(?<id>[0-9]*)\//",$questions['url'],$matches);
        $questions['id'] = $matches[1];
        $questions['scraped']=0;
        scraperwiki::save_sqlite(array('id'), $questions, "questions");
    }

}


//Second go to each question and capture all the user links

$questions = scraperwiki::sqliteexecute("select * from questions where scraped=0");  

foreach($questions->keys as $key => $value) $keys[$value]=$key;
$questions = $questions->data;

if (1==2) foreach($questions as $question){

    //echo $question[$keys['scraped']]."\n";

    $url = "http://stackoverflow.com".$question[$keys['url']];

    $html = scraperWiki::scrape($url); 
    $dom = new simple_html_dom();
    $dom->load($html); 
    
    //get all the users boxes from main answerers
    foreach($dom->find('div.user-details a') as $data )
    { 

        if( strpos($data->href,"/users/")!==FALSE) 
        {
        $users['url']=$data->href;
        preg_match("/\/users\/(?<id>[0-9]*)\//",$users['url'],$matches);
        $users['id'] = $matches[1];
        $users['name'] = $data->innertext;
        scraperwiki::save_sqlite(array('id'), $users, "users");
        }
    }

    //get all the comment user links
    foreach($dom->find('a.comment-user') as $data ){ 
        if( strpos($data->href,"/users/")!==FALSE) 
        {
        $users['url']=$data->href;
        preg_match("/\/users\/(?<id>[0-9]*)\//",$users['url'],$matches);
        $users['id'] = $matches[1];
        $users['name'] = $data->innertext;
        scraperwiki::save_sqlite(array('id'), $users, "users");
        }
    }
    
    //now update this question saying it's been scraped. 
    $update_question['id'] = $question[$keys['id']];
    $update_question['url'] = $question[$keys['url']]; 
    $update_question['scraped'] = 1;
    scraperwiki::save_sqlite(array('id'), $update_question, "questions");

}

//Third go through each user page and capture their info!

$users = scraperwiki::sqliteexecute("select * from users2 where scraped IS NULL");  

foreach($users->keys as $key => $value) $keys[$value]=$key;
$_users = $users->data;
unset($users);

if (1==2) foreach($_users as $user){

    //get out of here if there's no url or it's a generic user
    if ( $user[$keys['url']] == '' ) {echo "empty url\n"; continue;}
    if ( $user[$keys['name']] == 'Community' ) {echo "generic user\n";continue;}

    $url = "http://stackoverflow.com".$user[$keys['url']];

    $html = scraperWiki::scrape($url);           
    $dom = new simple_html_dom();
    $dom->load($html);

    //problem with the retrieval?  
    if ( ! method_exists($dom,"find") ) continue;
    if ( ! $dom->find('html') ) continue;

    //is the url wrong? account deleted? 
    if ( strpos( $dom->plaintext,'Page Not Found' ) !== FALSE ) { echo "page not found\n"; continue; }
    
    $users['id'] = $user[$keys['id']];
    $users['url'] = $user[$keys['url']];
    $users['scraped'] = 1;
    $users['name'] = $dom->find("h1[id=user-displayname]",0)->innertext;
    $users['location'] = $dom->find("td[class=adr]",0)->innertext;
    
    foreach($dom->find('div[class=data]',0)->find('table',0)->find('td') as $data ) {
        if ( $data->innertext == "age" ) $users['age'] = $data->next_sibling()->innertext;
        if ( $data->innertext == "profile views" ) $users['views'] = $data->next_sibling()->innertext;
    }
    
    $users['website'] = $dom->find('a[class=url]',0)->href;
    $users['member_since'] = $dom->find('td[class=cool]',0)->innertext;
    $users['last_seen'] = $dom->find('span[class=relativetime]',0)->innertext;
    $users['about'] = $dom->find('div[class=user-about-me]',0)->innertext;
    $users['logo'] = $dom->find('img[class=logo]',0)->src;
    $users['reputation'] = $dom->find('div[class=reputation]',0)->find('span',0)->find('a',0)->innertext;
    
    foreach($dom->find('div[class=subheader] h1 a') as $data ) {
        $key = substr( strrchr($data->href,'='), 1); 
        $users[$key] = $data->find('span',0)->innertext;
    }
    
    //this is for tags. it will blow up a table horizontally so we need to link to another vertical table
    foreach($dom->find('div[class=answer-votes]') as $data ) {
        $value = $data->innertext;
        $tag = preg_replace( '/[^a-z]/i', '', $data->next_sibling()->innertext );  
        $tags['tag'] = $tag;
        $tags['value'] = $value;
        $tags['user_id'] = $user[$keys['id']];

        scraperwiki::save_sqlite( '', $tags, "tags");

    }
    
    scraperwiki::save_sqlite(array('id'), $users, "users2");

}

//now lets geocode

$users = scraperwiki::sqliteexecute("SELECT * FROM `users2` WHERE `location` NOT NULL AND `lat` IS NULL GROUP BY `location` ORDER BY `location`");  
foreach($users->keys as $key => $value) $keys[$value]=$key;
$users = $users->data;

foreach($users as $user){

    $addr = urlencode($user[$keys['location']]);
    
    $url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='.$addr;
    $get = file_get_contents($url);
    $records = json_decode($get,TRUE);

    echo $addr.":";

    if ( $records['status'] == 'OK' ) { 
    
        //neat_r($records['results'][]); 
        $lat = $records['results'][0]['geometry']['location']['lat'];
        $lng = $records['results'][0]['geometry']['location']['lng'];
        
        echo $lat."-".$lng."\n";

        scraperwiki::sqliteexecute( "update `users2` set `lat`='".$lat."' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqliteexecute( "update `users2` set `lng`='".$lng."' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqlitecommit();  
        
    }else{
        
        echo "N/A\n";
        
        scraperwiki::sqliteexecute( "update `users2` set `lat`='XXX' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqliteexecute( "update `users2` set `lng`='XXX' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqlitecommit();  
    
    }

}

?>
<?php

//house cleaning
//scraperwiki::save_sqlite(array('id'), array('id'=>1, 'lat'=>1, 'lng'=>1), "users2");
//die;

require 'scraperwiki/simple_html_dom.php';     

function neat_r($arr, $return = false) {
    $out = array();
    $oldtab = "    ";
    $newtab = "-";
    
    $lines = explode("\n", print_r($arr, true));
    
    foreach ($lines as $line) {
 
        //remove numeric indexes like "[0] =>" unless the value is an array
        if (substr($line, -5) != "Array") {    $line = preg_replace("/^(\s*)\[[0-9]+\] => /", "$1", $line, 1); }
        
        //garbage symbols
        foreach (array(
            "Array" => "",
            "["     => "",
            "]"     => "",
            " =>"   => ":",
        ) as $old => $new) {
            $out = str_replace($old, $new, $out);
        }
 
        //garbage lines
        if (in_array(trim($line), array("Array", "(", ")", ""))) continue;
 
        //indents
        $indent = "";
        $indents = floor((substr_count($line, $oldtab) - 1) / 2);
        if ($indents > 0) { for ($i = 0; $i < $indents; $i++) { $indent .= $newtab; } }
 
        $out[] = $indent . trim($line);
    }
 
    $out = implode("\n", $out) . "\n";
    if ($return == true) return $out;
    echo $out;
}

//FIRST go through most voted magento questions and capture question links...
 
//$i<=316 insert this when ready to run there are 316 pages
//make 1==1 below if we want to run this section

if (1==2) for($i=1; $i<=300; $i++) {

    $url = "http://stackoverflow.com/questions/tagged/magento?page=".$i."&sort=votes&pagesize=50";
    
    $html = scraperWiki::scrape($url); 
    $dom = new simple_html_dom();
    $dom->load($html); 
    
    foreach($dom->find('a[class=question-hyperlink]') as $data ){
        $questions['url']=$data->href;
        preg_match("/\/questions\/(?<id>[0-9]*)\//",$questions['url'],$matches);
        $questions['id'] = $matches[1];
        $questions['scraped']=0;
        scraperwiki::save_sqlite(array('id'), $questions, "questions");
    }

}


//Second go to each question and capture all the user links

$questions = scraperwiki::sqliteexecute("select * from questions where scraped=0");  

foreach($questions->keys as $key => $value) $keys[$value]=$key;
$questions = $questions->data;

if (1==2) foreach($questions as $question){

    //echo $question[$keys['scraped']]."\n";

    $url = "http://stackoverflow.com".$question[$keys['url']];

    $html = scraperWiki::scrape($url); 
    $dom = new simple_html_dom();
    $dom->load($html); 
    
    //get all the users boxes from main answerers
    foreach($dom->find('div.user-details a') as $data )
    { 

        if( strpos($data->href,"/users/")!==FALSE) 
        {
        $users['url']=$data->href;
        preg_match("/\/users\/(?<id>[0-9]*)\//",$users['url'],$matches);
        $users['id'] = $matches[1];
        $users['name'] = $data->innertext;
        scraperwiki::save_sqlite(array('id'), $users, "users");
        }
    }

    //get all the comment user links
    foreach($dom->find('a.comment-user') as $data ){ 
        if( strpos($data->href,"/users/")!==FALSE) 
        {
        $users['url']=$data->href;
        preg_match("/\/users\/(?<id>[0-9]*)\//",$users['url'],$matches);
        $users['id'] = $matches[1];
        $users['name'] = $data->innertext;
        scraperwiki::save_sqlite(array('id'), $users, "users");
        }
    }
    
    //now update this question saying it's been scraped. 
    $update_question['id'] = $question[$keys['id']];
    $update_question['url'] = $question[$keys['url']]; 
    $update_question['scraped'] = 1;
    scraperwiki::save_sqlite(array('id'), $update_question, "questions");

}

//Third go through each user page and capture their info!

$users = scraperwiki::sqliteexecute("select * from users2 where scraped IS NULL");  

foreach($users->keys as $key => $value) $keys[$value]=$key;
$_users = $users->data;
unset($users);

if (1==2) foreach($_users as $user){

    //get out of here if there's no url or it's a generic user
    if ( $user[$keys['url']] == '' ) {echo "empty url\n"; continue;}
    if ( $user[$keys['name']] == 'Community' ) {echo "generic user\n";continue;}

    $url = "http://stackoverflow.com".$user[$keys['url']];

    $html = scraperWiki::scrape($url);           
    $dom = new simple_html_dom();
    $dom->load($html);

    //problem with the retrieval?  
    if ( ! method_exists($dom,"find") ) continue;
    if ( ! $dom->find('html') ) continue;

    //is the url wrong? account deleted? 
    if ( strpos( $dom->plaintext,'Page Not Found' ) !== FALSE ) { echo "page not found\n"; continue; }
    
    $users['id'] = $user[$keys['id']];
    $users['url'] = $user[$keys['url']];
    $users['scraped'] = 1;
    $users['name'] = $dom->find("h1[id=user-displayname]",0)->innertext;
    $users['location'] = $dom->find("td[class=adr]",0)->innertext;
    
    foreach($dom->find('div[class=data]',0)->find('table',0)->find('td') as $data ) {
        if ( $data->innertext == "age" ) $users['age'] = $data->next_sibling()->innertext;
        if ( $data->innertext == "profile views" ) $users['views'] = $data->next_sibling()->innertext;
    }
    
    $users['website'] = $dom->find('a[class=url]',0)->href;
    $users['member_since'] = $dom->find('td[class=cool]',0)->innertext;
    $users['last_seen'] = $dom->find('span[class=relativetime]',0)->innertext;
    $users['about'] = $dom->find('div[class=user-about-me]',0)->innertext;
    $users['logo'] = $dom->find('img[class=logo]',0)->src;
    $users['reputation'] = $dom->find('div[class=reputation]',0)->find('span',0)->find('a',0)->innertext;
    
    foreach($dom->find('div[class=subheader] h1 a') as $data ) {
        $key = substr( strrchr($data->href,'='), 1); 
        $users[$key] = $data->find('span',0)->innertext;
    }
    
    //this is for tags. it will blow up a table horizontally so we need to link to another vertical table
    foreach($dom->find('div[class=answer-votes]') as $data ) {
        $value = $data->innertext;
        $tag = preg_replace( '/[^a-z]/i', '', $data->next_sibling()->innertext );  
        $tags['tag'] = $tag;
        $tags['value'] = $value;
        $tags['user_id'] = $user[$keys['id']];

        scraperwiki::save_sqlite( '', $tags, "tags");

    }
    
    scraperwiki::save_sqlite(array('id'), $users, "users2");

}

//now lets geocode

$users = scraperwiki::sqliteexecute("SELECT * FROM `users2` WHERE `location` NOT NULL AND `lat` IS NULL GROUP BY `location` ORDER BY `location`");  
foreach($users->keys as $key => $value) $keys[$value]=$key;
$users = $users->data;

foreach($users as $user){

    $addr = urlencode($user[$keys['location']]);
    
    $url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='.$addr;
    $get = file_get_contents($url);
    $records = json_decode($get,TRUE);

    echo $addr.":";

    if ( $records['status'] == 'OK' ) { 
    
        //neat_r($records['results'][]); 
        $lat = $records['results'][0]['geometry']['location']['lat'];
        $lng = $records['results'][0]['geometry']['location']['lng'];
        
        echo $lat."-".$lng."\n";

        scraperwiki::sqliteexecute( "update `users2` set `lat`='".$lat."' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqliteexecute( "update `users2` set `lng`='".$lng."' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqlitecommit();  
        
    }else{
        
        echo "N/A\n";
        
        scraperwiki::sqliteexecute( "update `users2` set `lat`='XXX' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqliteexecute( "update `users2` set `lng`='XXX' where `location`='".$user[$keys['location']]."'" );  
        scraperwiki::sqlitecommit();  
    
    }

}

?>
