<?php

$council = "Galway County Council";
$uri = "http://www.galway.ie/en/AboutYourCouncil/Councillors/MeettheCouncillors/";
$html = scraperwiki::scrape($uri);

$councillors = array();
$subpages = array(
    "BallinasloeElectoralArea",
    "ConamaraElectoralArea",
    "LoughreaElectoralArea",
    "OranmoreElectoralArea",
    "TuamElectoralArea"
    );

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

/* Do your stuff here */

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage); # . "/"
    $dom->load($html);

# Put raw HTML for each Local Electoral Area into array
foreach($dom->find("div[class=profile]") as $cell) {  

$urlcell = $cell->find("a",1);
    $url = "http://www.galway.ie" . $urlcell->href;

  //    foreach($dom->find("div[class=profiletext]") as $cell) {
    
        $namecell = $cell->find("h4");
        $nameorig = strip_tags($namecell[0]->innertext);
        $namechunk = str_replace("Comh. ","",str_replace("Cllr. ", "",$nameorig));
        $nameparts = explode("-", $namechunk);
        $namec = trim($nameparts[0]);
        $name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $namec ); 
        
        
        
        $contents = $cell->find("div[class=profiletext]");
        
        $parts = explode("<strong>",$contents[0]);

        $partychunk = trim(str_replace("Political Affiliation: ", "",strip_tags($parts[1])));
        $party = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $partychunk );

        $emailchunk = trim(str_replace("&nbsp;","",strip_tags($parts[5])));
        $emailparts = explode(" ", $emailchunk);
        $email = trim($emailparts[1]);


        $phonechunk = str_replace("-","",str_replace("Tel: ","",strip_tags($parts[2])));
        $phoneparts = explode("/", $phonechunk);
        $phone = trim($phoneparts[0]);

        $mobile = trim(str_replace("-","",str_replace("Mobile: ","",strip_tags($parts[3]))));

        $imagecell = $cell->find("img",0);
        $imagechunk = "http://www.galway.ie" .$imagecell->src;
        $image = str_replace(" ","%20",$imagechunk);
  
        $moredetails = get_extras($url);
        unset($namecell,$url);

        $councillors["$name"] = array(

            "LEA"     => str_replace("ElectoralArea", "",$subpage),
            "Party"   => $party,
            "Email"   => $email,
            "Address" => $moredetails["address"],
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image
           );
    }
}
unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `address` string, `phone` string, `mobile` string, `image` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name, 
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "address" => $values["Address"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"]
                    
               
            )
    );
}
scraperwiki::sqlitecommit();
function htmlsan($htmlsanitize){
    return $htmlsanitize = htmlspecialchars($htmlsanitize, ENT_QUOTES, 'UTF-8');
}


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

foreach($localdom->find("div[class=profile]") as $cell) {  

        $addresscontents = $cell->find("div[class=profiletext]");

        $addressparts = explode("<strong>",$addresscontents[0]->innertext);
        $addresschunk = str_replace("Address: ", "",strip_tags($addressparts[7]));
        $address = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $addresschunk );
}
    $moredetails = array();    
    $moredetails["address"] = $address;

    unset($addresscell,$address);
  
    return($moredetails);
}

?><?php

$council = "Galway County Council";
$uri = "http://www.galway.ie/en/AboutYourCouncil/Councillors/MeettheCouncillors/";
$html = scraperwiki::scrape($uri);

$councillors = array();
$subpages = array(
    "BallinasloeElectoralArea",
    "ConamaraElectoralArea",
    "LoughreaElectoralArea",
    "OranmoreElectoralArea",
    "TuamElectoralArea"
    );

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

/* Do your stuff here */

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage); # . "/"
    $dom->load($html);

# Put raw HTML for each Local Electoral Area into array
foreach($dom->find("div[class=profile]") as $cell) {  

$urlcell = $cell->find("a",1);
    $url = "http://www.galway.ie" . $urlcell->href;

  //    foreach($dom->find("div[class=profiletext]") as $cell) {
    
        $namecell = $cell->find("h4");
        $nameorig = strip_tags($namecell[0]->innertext);
        $namechunk = str_replace("Comh. ","",str_replace("Cllr. ", "",$nameorig));
        $nameparts = explode("-", $namechunk);
        $namec = trim($nameparts[0]);
        $name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $namec ); 
        
        
        
        $contents = $cell->find("div[class=profiletext]");
        
        $parts = explode("<strong>",$contents[0]);

        $partychunk = trim(str_replace("Political Affiliation: ", "",strip_tags($parts[1])));
        $party = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $partychunk );

        $emailchunk = trim(str_replace("&nbsp;","",strip_tags($parts[5])));
        $emailparts = explode(" ", $emailchunk);
        $email = trim($emailparts[1]);


        $phonechunk = str_replace("-","",str_replace("Tel: ","",strip_tags($parts[2])));
        $phoneparts = explode("/", $phonechunk);
        $phone = trim($phoneparts[0]);

        $mobile = trim(str_replace("-","",str_replace("Mobile: ","",strip_tags($parts[3]))));

        $imagecell = $cell->find("img",0);
        $imagechunk = "http://www.galway.ie" .$imagecell->src;
        $image = str_replace(" ","%20",$imagechunk);
  
        $moredetails = get_extras($url);
        unset($namecell,$url);

        $councillors["$name"] = array(

            "LEA"     => str_replace("ElectoralArea", "",$subpage),
            "Party"   => $party,
            "Email"   => $email,
            "Address" => $moredetails["address"],
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image
           );
    }
}
unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `address` string, `phone` string, `mobile` string, `image` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name, 
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "address" => $values["Address"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"]
                    
               
            )
    );
}
scraperwiki::sqlitecommit();
function htmlsan($htmlsanitize){
    return $htmlsanitize = htmlspecialchars($htmlsanitize, ENT_QUOTES, 'UTF-8');
}


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

foreach($localdom->find("div[class=profile]") as $cell) {  

        $addresscontents = $cell->find("div[class=profiletext]");

        $addressparts = explode("<strong>",$addresscontents[0]->innertext);
        $addresschunk = str_replace("Address: ", "",strip_tags($addressparts[7]));
        $address = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $addresschunk );
}
    $moredetails = array();    
    $moredetails["address"] = $address;

    unset($addresscell,$address);
  
    return($moredetails);
}

?><?php

$council = "Galway County Council";
$uri = "http://www.galway.ie/en/AboutYourCouncil/Councillors/MeettheCouncillors/";
$html = scraperwiki::scrape($uri);

$councillors = array();
$subpages = array(
    "BallinasloeElectoralArea",
    "ConamaraElectoralArea",
    "LoughreaElectoralArea",
    "OranmoreElectoralArea",
    "TuamElectoralArea"
    );

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

/* Do your stuff here */

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage); # . "/"
    $dom->load($html);

# Put raw HTML for each Local Electoral Area into array
foreach($dom->find("div[class=profile]") as $cell) {  

$urlcell = $cell->find("a",1);
    $url = "http://www.galway.ie" . $urlcell->href;

  //    foreach($dom->find("div[class=profiletext]") as $cell) {
    
        $namecell = $cell->find("h4");
        $nameorig = strip_tags($namecell[0]->innertext);
        $namechunk = str_replace("Comh. ","",str_replace("Cllr. ", "",$nameorig));
        $nameparts = explode("-", $namechunk);
        $namec = trim($nameparts[0]);
        $name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $namec ); 
        
        
        
        $contents = $cell->find("div[class=profiletext]");
        
        $parts = explode("<strong>",$contents[0]);

        $partychunk = trim(str_replace("Political Affiliation: ", "",strip_tags($parts[1])));
        $party = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $partychunk );

        $emailchunk = trim(str_replace("&nbsp;","",strip_tags($parts[5])));
        $emailparts = explode(" ", $emailchunk);
        $email = trim($emailparts[1]);


        $phonechunk = str_replace("-","",str_replace("Tel: ","",strip_tags($parts[2])));
        $phoneparts = explode("/", $phonechunk);
        $phone = trim($phoneparts[0]);

        $mobile = trim(str_replace("-","",str_replace("Mobile: ","",strip_tags($parts[3]))));

        $imagecell = $cell->find("img",0);
        $imagechunk = "http://www.galway.ie" .$imagecell->src;
        $image = str_replace(" ","%20",$imagechunk);
  
        $moredetails = get_extras($url);
        unset($namecell,$url);

        $councillors["$name"] = array(

            "LEA"     => str_replace("ElectoralArea", "",$subpage),
            "Party"   => $party,
            "Email"   => $email,
            "Address" => $moredetails["address"],
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image
           );
    }
}
unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `address` string, `phone` string, `mobile` string, `image` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name, 
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "address" => $values["Address"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"]
                    
               
            )
    );
}
scraperwiki::sqlitecommit();
function htmlsan($htmlsanitize){
    return $htmlsanitize = htmlspecialchars($htmlsanitize, ENT_QUOTES, 'UTF-8');
}


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

foreach($localdom->find("div[class=profile]") as $cell) {  

        $addresscontents = $cell->find("div[class=profiletext]");

        $addressparts = explode("<strong>",$addresscontents[0]->innertext);
        $addresschunk = str_replace("Address: ", "",strip_tags($addressparts[7]));
        $address = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $addresschunk );
}
    $moredetails = array();    
    $moredetails["address"] = $address;

    unset($addresscell,$address);
  
    return($moredetails);
}

?>