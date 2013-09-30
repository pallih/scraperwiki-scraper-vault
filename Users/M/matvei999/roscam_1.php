<?php

// Table name: swdata

//scraperwiki::sqliteexecute("drop table swdata"); 
//scraperwiki::sqliteexecute("create table swdata"); 
//print_r(scraperwiki::sqliteexecute("select * from swdata")); 

require 'scraperwiki/simple_html_dom.php';

for($i=1; $i<=85; $i++) {

    $html = file_get_html('http://www.romancescam.com/blog/index.php?&p='.$i); 
    
    foreach($html->find('div[class=post]') as $element) {
        
        // Nullify all values first
        $ip = '';
        $first_name = '';
        $last_name = '';
        $age = '';
        $gender = '';
        $email_provider = '';
        $email = '';


        // Get rid of HTML entities that confuse Regex
        $text = $element->innertext;
        $text = str_replace(array('&nbsp;'), array(' '), $text);

    
        // Parse name
        preg_match('/\bname\s+(.*?)<br \/>/i', $text, $name);
        $name = explode(" ", $name[1]);
        $first_name = $name[0];
        $last_name = $name[1];

    
        // Parse birthdate
        preg_match('/birthday\s+(.*?)<br \/>/i', $text, $birthday);
        $birthday = str_replace('/', '.', $birthday[1]);
        $birthday = explode('.', $birthday);

        
        // If a birthday was given, find age from that
        if($birthday[2] > 0) {
            $age = date('Y') - (int)$birthday[2];
        }


        // Otherwise, age was given, so we grab that directly
        else {
            preg_match('/(\d{2}) years old/i', $text, $age);
            $age = $age[1];
        }


        // Parse IP address
        preg_match("/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/", $text, $ip); 

        
        // Parse gender
        preg_match('/(fe)*male/i', $text, $gender);

    
        // Parse email provider
        preg_match('/[a-zA-Z0-9_\.+]+@(.*?)(\.[a-z]{2,3}){1,2}/i', $text, $email);
        $email_provider = explode('@', $email[0]);


        // Save to the database if we have at least an IP    
        if($ip[0]) {
            scraperwiki::save_sqlite(array("email_address"), array("ip"=>$ip[0], "age"=>$age, "first_name"=>$first_name, "last_name"=>$last_name, "gender"=>$gender[0], "email_address" => $email[0], "email_provider"=>$email_provider[1]));
        }
    
        echo "\n";
        echo $ip[0];
        echo "\n";
        echo $age;
        echo "\n";
        echo $gender[0];
        echo "\n";
        echo $email[0];
        echo "\n";
        echo $email_provider[1];
        echo "\n";
    
    }

}

?>
<?php

// Table name: swdata

//scraperwiki::sqliteexecute("drop table swdata"); 
//scraperwiki::sqliteexecute("create table swdata"); 
//print_r(scraperwiki::sqliteexecute("select * from swdata")); 

require 'scraperwiki/simple_html_dom.php';

for($i=1; $i<=85; $i++) {

    $html = file_get_html('http://www.romancescam.com/blog/index.php?&p='.$i); 
    
    foreach($html->find('div[class=post]') as $element) {
        
        // Nullify all values first
        $ip = '';
        $first_name = '';
        $last_name = '';
        $age = '';
        $gender = '';
        $email_provider = '';
        $email = '';


        // Get rid of HTML entities that confuse Regex
        $text = $element->innertext;
        $text = str_replace(array('&nbsp;'), array(' '), $text);

    
        // Parse name
        preg_match('/\bname\s+(.*?)<br \/>/i', $text, $name);
        $name = explode(" ", $name[1]);
        $first_name = $name[0];
        $last_name = $name[1];

    
        // Parse birthdate
        preg_match('/birthday\s+(.*?)<br \/>/i', $text, $birthday);
        $birthday = str_replace('/', '.', $birthday[1]);
        $birthday = explode('.', $birthday);

        
        // If a birthday was given, find age from that
        if($birthday[2] > 0) {
            $age = date('Y') - (int)$birthday[2];
        }


        // Otherwise, age was given, so we grab that directly
        else {
            preg_match('/(\d{2}) years old/i', $text, $age);
            $age = $age[1];
        }


        // Parse IP address
        preg_match("/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/", $text, $ip); 

        
        // Parse gender
        preg_match('/(fe)*male/i', $text, $gender);

    
        // Parse email provider
        preg_match('/[a-zA-Z0-9_\.+]+@(.*?)(\.[a-z]{2,3}){1,2}/i', $text, $email);
        $email_provider = explode('@', $email[0]);


        // Save to the database if we have at least an IP    
        if($ip[0]) {
            scraperwiki::save_sqlite(array("email_address"), array("ip"=>$ip[0], "age"=>$age, "first_name"=>$first_name, "last_name"=>$last_name, "gender"=>$gender[0], "email_address" => $email[0], "email_provider"=>$email_provider[1]));
        }
    
        echo "\n";
        echo $ip[0];
        echo "\n";
        echo $age;
        echo "\n";
        echo $gender[0];
        echo "\n";
        echo $email[0];
        echo "\n";
        echo $email_provider[1];
        echo "\n";
    
    }

}

?>
