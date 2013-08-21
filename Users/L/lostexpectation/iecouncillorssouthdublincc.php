<?php
require 'scraperwiki/simple_html_dom.php';

$council = "South Dublin County Council"; #going to do it based on email being like cjones@sdublincoco.ie
$baseuri = "http://corporateservices.southdublin.ie/index.php?option=com_contact";
$pageuri = "http://corporateservices.southdublin.ie/index.php?option=com_content&task=view&id=127&Itemid=109"; # http://corporateservices.southdublin.ie/index.php?option=com_content&task=view&id=127&Itemid=109";


$councillors = array();


$subpages = array(
    "&catid=151&Itemid=115",
    "&catid=152&Itemid=115",
    "&catid=153&Itemid=115",
    "&catid=154&Itemid=115",
    "&catid=174&Itemid=115"
    );


# get the subpages the proper way
/*
$pagehtml = scraperwiki::scrape($pageuri);
$pagedom = new simple_html_dom();
$pagedom->load($pagehtml);


foreach($dom->find("div[class=contentpaneopen]") as $cell) {

$subpages = $cell->find('a');

$subpages = str_replace("../../../index.php?","",$subpages);
}

#<a href="../../../index.php?option=com_contact&amp;catid=151&amp;Itemid=115">Lucan (5 Councillors)</a>
#../../../index.php?option=com_contact
#$rows = $pagedom->find("div[class=content_outline] a");
$rows = array();
$rows = $pagedom->find("div[class=contentpaneopen] a");


foreach($rows as $row) {

$subpages = $row->find('a',0); #,0->innertext

$subpagename = $row->innertext;
#$subpages = $cell->find("a");
$subpages = str_replace("../../../index.php?option=com_contact","",$subpages);

}

*/
foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($baseuri . $subpage);
    $dom->load($html);


foreach($dom->find("div[class=componentheading]") as $cell) {
$lea = trim(strip_tags(str_replace("Councillors","",$cell)));
};

$rows = $dom->find("div[class=contentpane] table tr"); # http://corporateservices.southdublin.ie/index.php?option=com_contact&catid=151&Itemid=115
$i=0; 

foreach($rows as $row) {

if ($i > 0) #skip header
       {
$namecell = $row->find("td a",0);

$name = strip_tags(str_replace("Cllr.","",$namecell)); #->innertext
$name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $name);
$name = trim($name);
//utf8_decode($name);
# <a href="index.php?option=com_contact&amp;task=view&amp;contact_id=21&amp;Itemid=115" class="category">

$url = "http://corporateservices.southdublin.ie/" . $namecell->href;

#http://corporateservices.southdublin.ie/index.php?option=com_contact&task=view&contact_id=32&Itemid=115
$url = str_replace("&amp;","&",$url);
print $url;

$moredetails = get_extras($url);

 $councillors["$name"] = array(
        "LEA"     => $lea,
        "Url"     => $url,
        "Party"   => $moredetails["party"],
        "Email"   => $moredetails["email"],
        "Phone"   => $moredetails["phone"],
        "Mobile"  => $moredetails["mobile"],
        "Image"   => $moredetails["image"],
        "Address" => $moredetails["address"]
    );
}$i++;  
}
     
}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `url` string, `name` string,`party` string, `email` string, `phone` string, `mobile` string, `image` string, `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :url,  :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "url"     => $values["Url"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
                    "address" => $values["Address"]
              )
    );
}

function get_extras($url) {
$localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);


print $url;

    $contents = $localdom->find("div[class=contentpane]",0);
print "contents";
print $contents;
//print_r($contents);
    $details = explode("<div>",$contents); #[0]);
//print "details"."\n";
//print $details[0];
# getting a error eveytime i try  $imagecell->find("img",0); or ("img")

$imagecell = $details[0];

$image = "image";

$party = trim(strip_tags($details[1]));
$party = str_replace("Mayor, "," ",str_replace("Deputy"," ",str_replace("The"," ",$party)));
$party  = trim($party);

$address = str_replace("<br />"," ",($details[3]));
$address = trim(strip_tags(str_replace("c/o"," ",$address)));

$namecell = $details[0];
$namecell = str_replace("Cllr.","",$namecell);
$namecell = trim(strip_tags($namecell));
$namecell = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $namecell);

#create email like cjones@sdublincoco.ie

$emailname = explode(" ",$namecell);

$initial = str_split($emailname[0],1);
$email = $initial[0] . $emailname[1];
$email = str_replace("'","",$email);
$email = strtolower($email) . "@sdublincoco.ie";


# phone and mobile first and second
$phonemobile = trim(strip_tags($details[4]));
$phonemobile = explode("/",$phonemobile);

$mobile = $phonemobile[1];
$phone = $phonemobile[0];


    if(substr($phone, 0, 3) == "085" || substr($phone, 0, 3) == "086" || substr($phone, 0, 3) == "087"  ) 
    { 
    $mobile = $phonemobile[0];
    $phone = $phonemobile[1];
    }
    else { 
    $mobile = $phonemobile[1]; 
    $phone = $phonemobile[0]; 
    }

    if (empty($phone)){ $phone = "";}
    else if (substr($phone, 0, 2) == "01") 
    { 
        $phone = trim($phone); }
    else { 
        $phone = "01" . " ". $phone; 
    }

    $phone = trim(strip_tags(str_replace("www.trevorgilligan.com","",$phone)));
    $mobile = trim(strip_tags(str_replace("www.trevorgilligan.com","",$mobile)));

    $moredetails = array();    
    $moredetails["party"] = $party;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
    $moredetails["address"] = $address;
    $moredetails["image"] = $image;
 //   unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);
}


scraperwiki::sqlitecommit();
?>