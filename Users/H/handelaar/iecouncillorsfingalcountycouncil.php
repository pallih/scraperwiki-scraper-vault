<?php
require 'scraperwiki/simple_html_dom.php';

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/YourLocalCouncil/LocalDemocracy/Councillors/";


# Example listing address: http://www.fingalcoco.ie/YourLocalCouncil/LocalDemocracy/Councillors/Balbriggan/
$subpages = array(
    "Balbriggan",
    "Castleknock",
    "HowthMalahide",
    "Mulhuddart",
    "Swords"
    );

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    foreach($dom->find("div[class=councillors_main_container]") as $cell) {
        $personstring = $cell->find("div[class=councillor_title]");
        $parts = explode(" &nbsp ",$personstring[0]->plaintext);
        $remove = array("","(",")","The "," Party");
        $name = trim($parts[0]);
        $party = trim(str_replace($remove,"",$parts[1]));

        $imagestring = $cell->find("div[class=councillor_image] img");
        $image = trim(str_replace(" ","%20",$imagestring[0]->src));

        $addressstring = $cell->find("div[class=councillor_name]");
        $address = trim(str_replace("Address:&nbsp;","",$addressstring[0]->plaintext));

        $emailstring = $cell->find("div[class=councillor_email]");
        $email = trim(str_replace("Email:&nbsp","",$emailstring[0]->plaintext));

        $faxstring = $cell->find("div[class=councillor_fax]");
        $fax = trim(str_replace("Fax:&nbsp;","",$faxstring[0]->plaintext));

        $phonestring = $cell->find("div[class=councillor_telephone]");
        $phonepieces =  preg_replace('/[^0-9 ]/', '', $phonestring[0]->plaintext);
        $phonepieces = str_replace("085 ","085",$phonepieces);
        $phonepieces = str_replace("086 ","086",$phonepieces);
        $phonepieces = trim(str_replace("087 ","087",$phonepieces));
        
        $phonebits = array();
        //echo $phonepieces . "\n";
        if(substr($phonepieces,0,2) == "08") {
                $mobile = str_replace(" ","",$phonepieces);
                $phone = "";
            } 
        elseif(stristr($phonepieces," ")) {
                $parts = explode(" ",str_replace("  "," ",str_replace("  "," ",$phonepieces)));
                $phone  = $parts[0];
                $mobile = $parts[1];
                if($mobile == $phone) {
                    $mobile = "";
                }
                if((substr($phone,0,2) != "01") && $phone != "") {
                    $phone = "01" . $phone;
                }
            }
        $councillors["$name"] = array(
            "LEA"     => str_replace("HowthMalahide","Howth-Malahide",$subpage),
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image,
            "Address" => $address
        );
    }
}
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `phone` text, `mobile` text, `image` string,  `address` string)");
scraperwiki::sqliteexecute("delete from councillors");

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Fingal County Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
                    "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?><?php
require 'scraperwiki/simple_html_dom.php';

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/YourLocalCouncil/LocalDemocracy/Councillors/";


# Example listing address: http://www.fingalcoco.ie/YourLocalCouncil/LocalDemocracy/Councillors/Balbriggan/
$subpages = array(
    "Balbriggan",
    "Castleknock",
    "HowthMalahide",
    "Mulhuddart",
    "Swords"
    );

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    foreach($dom->find("div[class=councillors_main_container]") as $cell) {
        $personstring = $cell->find("div[class=councillor_title]");
        $parts = explode(" &nbsp ",$personstring[0]->plaintext);
        $remove = array("","(",")","The "," Party");
        $name = trim($parts[0]);
        $party = trim(str_replace($remove,"",$parts[1]));

        $imagestring = $cell->find("div[class=councillor_image] img");
        $image = trim(str_replace(" ","%20",$imagestring[0]->src));

        $addressstring = $cell->find("div[class=councillor_name]");
        $address = trim(str_replace("Address:&nbsp;","",$addressstring[0]->plaintext));

        $emailstring = $cell->find("div[class=councillor_email]");
        $email = trim(str_replace("Email:&nbsp","",$emailstring[0]->plaintext));

        $faxstring = $cell->find("div[class=councillor_fax]");
        $fax = trim(str_replace("Fax:&nbsp;","",$faxstring[0]->plaintext));

        $phonestring = $cell->find("div[class=councillor_telephone]");
        $phonepieces =  preg_replace('/[^0-9 ]/', '', $phonestring[0]->plaintext);
        $phonepieces = str_replace("085 ","085",$phonepieces);
        $phonepieces = str_replace("086 ","086",$phonepieces);
        $phonepieces = trim(str_replace("087 ","087",$phonepieces));
        
        $phonebits = array();
        //echo $phonepieces . "\n";
        if(substr($phonepieces,0,2) == "08") {
                $mobile = str_replace(" ","",$phonepieces);
                $phone = "";
            } 
        elseif(stristr($phonepieces," ")) {
                $parts = explode(" ",str_replace("  "," ",str_replace("  "," ",$phonepieces)));
                $phone  = $parts[0];
                $mobile = $parts[1];
                if($mobile == $phone) {
                    $mobile = "";
                }
                if((substr($phone,0,2) != "01") && $phone != "") {
                    $phone = "01" . $phone;
                }
            }
        $councillors["$name"] = array(
            "LEA"     => str_replace("HowthMalahide","Howth-Malahide",$subpage),
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image,
            "Address" => $address
        );
    }
}
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `phone` text, `mobile` text, `image` string,  `address` string)");
scraperwiki::sqliteexecute("delete from councillors");

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Fingal County Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
                    "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?>