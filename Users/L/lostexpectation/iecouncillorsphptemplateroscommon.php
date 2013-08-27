<?php

$council = "Roscommon county Council";
$uri = "http://www.roscommoncoco.ie/en/Services/Corporateservices/Local_Representatives/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$subpages = array(
    "Boyle_Electoral_Area",
    "Athlone_Electoral_Area",
    "Castlerea_Electoral_Area",
    "Roscommon_Electoral_Area",
    "Strokestown_Electoral_Area",

    );


foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage  . "/");

 $rows=$dom->find("ul[class=mainDoclist] li"); 
 foreach($rows as $row) {
print $row;
#foreach($dom->find("div[class=main-copy-section] li") as $cell) {  
$namecell = $row->find("h2",0);
$name = strip_tags($namecell);
    $url = "http://www.roscommoncoco.ie" . $namecell->href;
print $url;
$party = "party";

  #  $moredetails = get_extras($url);
 #   unset($namecell,$url,$leacellcontents,$leacell,$partycell,$imagecell);



 $councillors["$name"] = array(
        "LEA"     => str_replace("_Electoral_Area","",$subpage),
        "Party"   => $party #,
  #      "Email"   => $moredetails["email"],
  #      "Phone"   => $moredetails["phone"],
  #      "Mobile"  => $moredetails["mobile"],
 #       "Image"   => $moredetails["image"],
 #       "Address" => $moredetails["address"]
  );
       
}
}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)"); #, `email` string, `address` string, `phone` string, `mobile` string, `image` string)"); 
scraperwiki::sqlitecommit();
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values[$party] # $values["Party"],
         #           "email"   => $values["Email"],
         #           "address" => $values["Address"], 
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
               
            )
    );
}
scraperwiki::sqlitecommit();

function get_extras($url) {
$localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

//foreach($localdom->find("div[class=main-copy-section]") as $cell) {  
$cell = $localdom->find("div[class=main-copy-section]");

$rows=$cell->find("div[class=reduced] tr"); 
$i=0;
foreach($rows as $row) {
if ($i > 0)
        {



$name = $row->find("td",0);
$address = $row->find("td",0);
$party = $row->find("td",3);
$email = $row->find("td",2);
$phone = $row->find("td",1);
//$mobile = 
$imagecell = $localdom->find("p",0);
    $image = "http://www.roscommoncoco.ie" .$imagecell->src;

    $moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
    $moredetails["image"] = $image;
    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile);
  
    return($moredetails);

        }
        $i++;
}
}

?><?php

$council = "Roscommon county Council";
$uri = "http://www.roscommoncoco.ie/en/Services/Corporateservices/Local_Representatives/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$subpages = array(
    "Boyle_Electoral_Area",
    "Athlone_Electoral_Area",
    "Castlerea_Electoral_Area",
    "Roscommon_Electoral_Area",
    "Strokestown_Electoral_Area",

    );


foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage  . "/");

 $rows=$dom->find("ul[class=mainDoclist] li"); 
 foreach($rows as $row) {
print $row;
#foreach($dom->find("div[class=main-copy-section] li") as $cell) {  
$namecell = $row->find("h2",0);
$name = strip_tags($namecell);
    $url = "http://www.roscommoncoco.ie" . $namecell->href;
print $url;
$party = "party";

  #  $moredetails = get_extras($url);
 #   unset($namecell,$url,$leacellcontents,$leacell,$partycell,$imagecell);



 $councillors["$name"] = array(
        "LEA"     => str_replace("_Electoral_Area","",$subpage),
        "Party"   => $party #,
  #      "Email"   => $moredetails["email"],
  #      "Phone"   => $moredetails["phone"],
  #      "Mobile"  => $moredetails["mobile"],
 #       "Image"   => $moredetails["image"],
 #       "Address" => $moredetails["address"]
  );
       
}
}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)"); #, `email` string, `address` string, `phone` string, `mobile` string, `image` string)"); 
scraperwiki::sqlitecommit();
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values[$party] # $values["Party"],
         #           "email"   => $values["Email"],
         #           "address" => $values["Address"], 
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
               
            )
    );
}
scraperwiki::sqlitecommit();

function get_extras($url) {
$localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

//foreach($localdom->find("div[class=main-copy-section]") as $cell) {  
$cell = $localdom->find("div[class=main-copy-section]");

$rows=$cell->find("div[class=reduced] tr"); 
$i=0;
foreach($rows as $row) {
if ($i > 0)
        {



$name = $row->find("td",0);
$address = $row->find("td",0);
$party = $row->find("td",3);
$email = $row->find("td",2);
$phone = $row->find("td",1);
//$mobile = 
$imagecell = $localdom->find("p",0);
    $image = "http://www.roscommoncoco.ie" .$imagecell->src;

    $moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
    $moredetails["image"] = $image;
    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile);
  
    return($moredetails);

        }
        $i++;
}
}

?><?php

$council = "Roscommon county Council";
$uri = "http://www.roscommoncoco.ie/en/Services/Corporateservices/Local_Representatives/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$subpages = array(
    "Boyle_Electoral_Area",
    "Athlone_Electoral_Area",
    "Castlerea_Electoral_Area",
    "Roscommon_Electoral_Area",
    "Strokestown_Electoral_Area",

    );


foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage  . "/");

 $rows=$dom->find("ul[class=mainDoclist] li"); 
 foreach($rows as $row) {
print $row;
#foreach($dom->find("div[class=main-copy-section] li") as $cell) {  
$namecell = $row->find("h2",0);
$name = strip_tags($namecell);
    $url = "http://www.roscommoncoco.ie" . $namecell->href;
print $url;
$party = "party";

  #  $moredetails = get_extras($url);
 #   unset($namecell,$url,$leacellcontents,$leacell,$partycell,$imagecell);



 $councillors["$name"] = array(
        "LEA"     => str_replace("_Electoral_Area","",$subpage),
        "Party"   => $party #,
  #      "Email"   => $moredetails["email"],
  #      "Phone"   => $moredetails["phone"],
  #      "Mobile"  => $moredetails["mobile"],
 #       "Image"   => $moredetails["image"],
 #       "Address" => $moredetails["address"]
  );
       
}
}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)"); #, `email` string, `address` string, `phone` string, `mobile` string, `image` string)"); 
scraperwiki::sqlitecommit();
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :address, :phone, :mobile, :image)",
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values[$party] # $values["Party"],
         #           "email"   => $values["Email"],
         #           "address" => $values["Address"], 
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
               
            )
    );
}
scraperwiki::sqlitecommit();

function get_extras($url) {
$localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

//foreach($localdom->find("div[class=main-copy-section]") as $cell) {  
$cell = $localdom->find("div[class=main-copy-section]");

$rows=$cell->find("div[class=reduced] tr"); 
$i=0;
foreach($rows as $row) {
if ($i > 0)
        {



$name = $row->find("td",0);
$address = $row->find("td",0);
$party = $row->find("td",3);
$email = $row->find("td",2);
$phone = $row->find("td",1);
//$mobile = 
$imagecell = $localdom->find("p",0);
    $image = "http://www.roscommoncoco.ie" .$imagecell->src;

    $moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
    $moredetails["image"] = $image;
    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile);
  
    return($moredetails);

        }
        $i++;
}
}

?>