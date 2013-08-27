<?php

$council = "Carlow County Council";
$uri = "http://www.carlow.ie/councillors/Pages/carlow-county-councillors.aspx";
$html = scraperwiki::scrape($uri);

$councillors = array();
$moredetails = array();
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
#$rows=$dom->find('div[class="item hline"]');
#print $row; 

# as $cell) {
$content = $dom->find("div[class=content]");
//print_r($content);
//$content = $content[0];
print_r($content);

# item hline details

//foreach($dom->find('div.item.hline') as $cell) {
//$content->find('h1') as $cell) { # [class=councillor]
/*
function get_details($content) {

$rows = $content->find('div.item.hline');
foreach($rows as $row) {

$address = "address";
$phone = "phone";
$mobile = "mobile";
$image = "image";
$email = "email";  
    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
$moredetails["image"] = $image;

return($moredetails);
}
}
*/
# h1 name party
function get_nameparty($content) {
$rows = $content->find('h1',0); 
print_r($rows);
//foreach($dom->find('div[class="item hline"]') as $cell) {
foreach($rows as $row) {
print $row;

$nameparty = $content->find('h1',0);
$nameparty = explode("(",$nameparty);
$partycell = $nameparty[1];
$party = trim(str_replace(")","",$partycell));
$name = trim(str_replace("Cllr. ","",strip_tags($party)));
$namecell = $nameparty[0];
$name = trim(str_replace("Cllr. ","",strip_tags($namecell)));
print $name;

#$party = $row->find("p",0);
//$party = $cell->find("p",0);
print $party;

    
    $moredetails["name"] = $name;
    $moredetails["party"] = $party;
   

return($moredetails);
}
}

//$moredetails = array();  
//$moredetails = get_details($content);
$moredetails = get_nameparty($content);

foreach($moredetails as $moredetail) {

$lea = "lea";
print $lea;



   $councillors["$name"] = array(
     "LEA"     => $lea,
        "Party"   => $moredetails["party"] #,
   //     "Email"   => $moredetails["email"],
  //      "Phone"   => $moredetails["phone"],
   //     "Mobile"  => $moredetails["mobile"],
  //      "Image"   => $moredetails["image"],
   //     "Address" => $moredetails["address"]
  );
       
}
unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)");  #, `email` string, `address` string, `phone` string, `mobile` string, `image` string)"); 
scraperwiki::sqlitecommit();
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => "Carlow County Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
            #        "email"   => $values["Email"],
            #        "address" => $values["Address"], 
            #        "phone"   => $values["Phone"],
            #        "mobile"  => $values["Mobile"],
            #        "image"   => $values["Image"],
               
            )
    );
}
scraperwiki::sqlitecommit();
?><?php

$council = "Carlow County Council";
$uri = "http://www.carlow.ie/councillors/Pages/carlow-county-councillors.aspx";
$html = scraperwiki::scrape($uri);

$councillors = array();
$moredetails = array();
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
#$rows=$dom->find('div[class="item hline"]');
#print $row; 

# as $cell) {
$content = $dom->find("div[class=content]");
//print_r($content);
//$content = $content[0];
print_r($content);

# item hline details

//foreach($dom->find('div.item.hline') as $cell) {
//$content->find('h1') as $cell) { # [class=councillor]
/*
function get_details($content) {

$rows = $content->find('div.item.hline');
foreach($rows as $row) {

$address = "address";
$phone = "phone";
$mobile = "mobile";
$image = "image";
$email = "email";  
    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
$moredetails["image"] = $image;

return($moredetails);
}
}
*/
# h1 name party
function get_nameparty($content) {
$rows = $content->find('h1',0); 
print_r($rows);
//foreach($dom->find('div[class="item hline"]') as $cell) {
foreach($rows as $row) {
print $row;

$nameparty = $content->find('h1',0);
$nameparty = explode("(",$nameparty);
$partycell = $nameparty[1];
$party = trim(str_replace(")","",$partycell));
$name = trim(str_replace("Cllr. ","",strip_tags($party)));
$namecell = $nameparty[0];
$name = trim(str_replace("Cllr. ","",strip_tags($namecell)));
print $name;

#$party = $row->find("p",0);
//$party = $cell->find("p",0);
print $party;

    
    $moredetails["name"] = $name;
    $moredetails["party"] = $party;
   

return($moredetails);
}
}

//$moredetails = array();  
//$moredetails = get_details($content);
$moredetails = get_nameparty($content);

foreach($moredetails as $moredetail) {

$lea = "lea";
print $lea;



   $councillors["$name"] = array(
     "LEA"     => $lea,
        "Party"   => $moredetails["party"] #,
   //     "Email"   => $moredetails["email"],
  //      "Phone"   => $moredetails["phone"],
   //     "Mobile"  => $moredetails["mobile"],
  //      "Image"   => $moredetails["image"],
   //     "Address" => $moredetails["address"]
  );
       
}
unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)");  #, `email` string, `address` string, `phone` string, `mobile` string, `image` string)"); 
scraperwiki::sqlitecommit();
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => "Carlow County Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
            #        "email"   => $values["Email"],
            #        "address" => $values["Address"], 
            #        "phone"   => $values["Phone"],
            #        "mobile"  => $values["Mobile"],
            #        "image"   => $values["Image"],
               
            )
    );
}
scraperwiki::sqlitecommit();
?><?php

$council = "Carlow County Council";
$uri = "http://www.carlow.ie/councillors/Pages/carlow-county-councillors.aspx";
$html = scraperwiki::scrape($uri);

$councillors = array();
$moredetails = array();
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
#$rows=$dom->find('div[class="item hline"]');
#print $row; 

# as $cell) {
$content = $dom->find("div[class=content]");
//print_r($content);
//$content = $content[0];
print_r($content);

# item hline details

//foreach($dom->find('div.item.hline') as $cell) {
//$content->find('h1') as $cell) { # [class=councillor]
/*
function get_details($content) {

$rows = $content->find('div.item.hline');
foreach($rows as $row) {

$address = "address";
$phone = "phone";
$mobile = "mobile";
$image = "image";
$email = "email";  
    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
$moredetails["image"] = $image;

return($moredetails);
}
}
*/
# h1 name party
function get_nameparty($content) {
$rows = $content->find('h1',0); 
print_r($rows);
//foreach($dom->find('div[class="item hline"]') as $cell) {
foreach($rows as $row) {
print $row;

$nameparty = $content->find('h1',0);
$nameparty = explode("(",$nameparty);
$partycell = $nameparty[1];
$party = trim(str_replace(")","",$partycell));
$name = trim(str_replace("Cllr. ","",strip_tags($party)));
$namecell = $nameparty[0];
$name = trim(str_replace("Cllr. ","",strip_tags($namecell)));
print $name;

#$party = $row->find("p",0);
//$party = $cell->find("p",0);
print $party;

    
    $moredetails["name"] = $name;
    $moredetails["party"] = $party;
   

return($moredetails);
}
}

//$moredetails = array();  
//$moredetails = get_details($content);
$moredetails = get_nameparty($content);

foreach($moredetails as $moredetail) {

$lea = "lea";
print $lea;



   $councillors["$name"] = array(
     "LEA"     => $lea,
        "Party"   => $moredetails["party"] #,
   //     "Email"   => $moredetails["email"],
  //      "Phone"   => $moredetails["phone"],
   //     "Mobile"  => $moredetails["mobile"],
  //      "Image"   => $moredetails["image"],
   //     "Address" => $moredetails["address"]
  );
       
}
unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)");  #, `email` string, `address` string, `phone` string, `mobile` string, `image` string)"); 
scraperwiki::sqlitecommit();
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => "Carlow County Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
            #        "email"   => $values["Email"],
            #        "address" => $values["Address"], 
            #        "phone"   => $values["Phone"],
            #        "mobile"  => $values["Mobile"],
            #        "image"   => $values["Image"],
               
            )
    );
}
scraperwiki::sqlitecommit();
?>