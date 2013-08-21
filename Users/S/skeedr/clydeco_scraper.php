<?php

$data = array(array());
$wanted = array(array());
$i = 0;

$search_html = scraperWiki::scrape("http://www.clydeco.com/search/YTo0OntzOjg6ImtleXdvcmRzIjtzOjE4OiJwZXJzb25hbCBpbmp1cnkgdWsiO3M6MTE6InNlYXJjaF9tb2RlIjtzOjM6ImFsbCI7czoxMToicmVzdWx0X3BhZ2UiO3M6Njoic2VhcmNoIjtzOjEwOiJjb2xsZWN0aW9uIjthOjExOntpOjA7czoxOiIxIjtpOjE7czoxOiIyIjtpOjI7czoxOiIzIjtpOjM7czoxOiI0IjtpOjQ7czoxOiI1IjtpOjU7czoxOiI2IjtpOjY7czoxOiI3IjtpOjc7czoxOiI4IjtpOjg7czoxOiI5IjtpOjk7czoyOiIxMCI7aToxMDtzOjI6IjExIjt9fQ");

require 'scraperwiki/simple_html_dom.php';
$search_dom = new simple_html_dom();
$search_dom->load($search_html);
//For each dom object that is a <h4> in an <a class="more">
foreach ($search_dom->find("h4 a.more") as $domobj) {
    //If the text is not [blah]
    if (strstr($domobj->plaintext, "Partner Peter Walmsley wins Defendant Personal Injury Lawyer of the Year")) {
        
    } else {
        //Stick the persons name in 'name' and the address for their about page in 'webaddress'
        $data[$i] = array("name" => $domobj->plaintext, "webaddress" => $domobj->href);
        $i++;
    }
}

$i = 0;
//For each $data index as $person
foreach ($data as &$person) {
print_r("On {$person['name']}\r\n");
    //For each $person as their $key => $value pair
    foreach ($person as $key => &$value) {
print_r("On {$key}\r\n");
        //If the $key is a webaddress
        if ($key == "webaddress") {
            //Scrape their webaddress to see if they are a wanted contact
            $about_html = scraperWiki::scrape($value);
            $about_dom = new simple_html_dom();
            $about_dom->load($about_html);
            //For each dom object that is a <p> in a <div id="content-body">
            foreach ($about_dom->find('div#content-body p') as $aboutdomobj) {
print_r("On {$aboutdomobj->plaintext}\r\n");
                //If the text contains the required strings
                if (strstr($aboutdomobj->plaintext, "personal injury") || strstr($aboutdomobj->plaintext, "clinical negligence") || strstr($aboutdomobj->plaintext, "catastropic")) {
print_r("{$person['name']} is wanted\r\n");
                    //$wanted[] = array($person);
                    $value = $value . "/contact";
                    //Scrape their contact information
                    $contact_html = scraperWiki::scrape($value);
                    $contact_dom = new simple_html_dom();
                    $contact_dom->load($contact_html);
                    //Foreach <p> in a <div #content-body>
                    foreach ($contact_dom->find('div#content-body p') as $contactdomobj) {
                        //If the text contains the telephone no.
                        if (strstr($contactdomobj->plaintext, "Main tel")) {
print_r( substr($contactdomobj->plaintext, 10) . "\r\n" );
                            $newchars=array("+44", " ", "(", ")");
                            $telephoneno =  str_replace($newchars, "", substr($contactdomobj->plaintext, 10));
                            $person['tel'] = $telephoneno;
                        //Elseif it contains their email address
                        } elseif (strstr($contactdomobj->plaintext, "clydeco")) {
print_r($contactdomobj->plaintext . "\r\n");
                            $person['email'] = $contactdomobj->plaintext;
                        }
print_r($contactdomobj->plaintext . "\r\n");
                    }
//Put the person into the wanted array
                    $wanted[$i] = $person;
                    $i++;
                    break 2;
                }else{
print_r("{$person['name']} is not required.\r\n");
                    break 2;
                }
            }
        }
    }
}
print_r($wanted);
foreach($wanted as $person){
     scraperwiki::save_sqlite(array("name"), $person); 
//print_r($person['name'].", ".$person['webaddress'].", ".$person['tel'].", ".$person['email']."\r\n");
}
?>