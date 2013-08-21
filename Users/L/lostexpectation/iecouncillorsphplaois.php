<?php

$council = "Laois county Council";
$uri = "http://www.laois.ie/YourCouncil/AbouttheCouncil/Councillors/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


#http://www.laois.ie/YourCouncil/AbouttheCouncil/Councillors/
$subpages = array(
"Emo",
"Mountmellick",
"Borris-in-Ossory",
"Luggacurren",
"Portlaoise"

    );

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    foreach($dom->find("div[id=textareapadding]") as $cell) {
//$cell = $dom->find("div[id=textareapadding]",0);

//print "cell";
//print $cell;

$cllrs = explode("<hr style=\"border-top:dotted #006699\" />",$cell);
print "\n"."cllrs";
print_r($cllrs);

//    unset($cllr[0]);

foreach($cllrs as $cllr) {
    $tempdom = new simple_html_dom();
    $tempdom->load($cllr);
   $namechunk = $tempdom->find("strong",0);
print "namechunk";
print $namechunk;

$name = trim(strip_tags($namechunk));
//$name = "name";
print "name";
print $name;
   $partychunk = $tempdom->find("strong",1);
//print $partychunk;
$partyshort = trim(strip_tags($partychunk));
$party = partyfull($partyshort);


$lea = $subpage;

#http://www.laois.ie/media/Media,174,en.JPG
$address = $tempdom->find("p",2)->innertext;

//print "\n". "address". $address;

#as james.daly@laoiscoco.ie

$emailname = explode(" ",$name);

//$initial = str_split($emailname[0],1);
$email = $emailname[0] .".". $emailname[1];
$email = str_replace("'","",$email);
$email = strtolower($email) . "@laoiscoco.ie";




$phonemobilecell = $tempdom->find("p",3);
$phonemobilecell = trim(strip_tags($phonemobilecell));
print $phonemobilecell;
$phonearray = explode("(",$phonemobilecell);
print "phonearray";
print_r($phonearray);




$phonearraylength = count($phonearray);

for($i=0; $i <= $phonearraylength; $i++)

{
if ( substr($phonearray[$i],0,2) == "05" ) {
$phonechunk = $phonearray[$i];
}
elseif ( substr($phonearray[$i],0,2) == "08" ) {
$mobilechunk = $phonearray[$i];

}
/*
else 
{
$phonechunk = "";
$mobilechunk = "";
}
*/

}
$phone = trim(preg_replace('/[^0-9]/', ' ', $phonechunk));
$mobile = trim(preg_replace('/[^0-9]/', ' ', $mobilechunk));
print "phone";
print $phone;

    $imagecell = $tempdom->find("img",0);
    $image = "http://www.laois.ie" .$imagecell->src;


unset($mobilechunk,$phonechunk,$phonearray);

        $councillors["$name"] = array(
            "LEA"     => $lea,
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image,
            "Address" => $address
        );
    }
}
unset($tempdom);
}
unset($name,$email,$mobile,$phone,$mobilechunk,$phonechunk,$phonearray,$dom,$html,$uri,$tempdom);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `lea` string, `name` string, `party` string, `email` string, `phone` string, `mobile` string, `image` string, `address` string)"); #);
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
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
scraperwiki::sqlitecommit();



function partyfull($partyshort) {

    if($partyshort == "F.G.")
    {
            $partyshort = "Fine Gael";
    }
    else if($partyshort == "F.F.") 
    {
            $partyshort = "Fianna Fail";
    }

    else if($partyshort == "PBP") 
    {
            $partyshort = "People before Profit";
    }          
    else if($partyshort == "Non Party") 
    {
            $partyshort = "Independent";
    }

return($partyshort);

}
?><?php

$council = "Laois county Council";
$uri = "http://www.laois.ie/YourCouncil/AbouttheCouncil/Councillors/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


#http://www.laois.ie/YourCouncil/AbouttheCouncil/Councillors/
$subpages = array(
"Emo",
"Mountmellick",
"Borris-in-Ossory",
"Luggacurren",
"Portlaoise"

    );

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    foreach($dom->find("div[id=textareapadding]") as $cell) {
//$cell = $dom->find("div[id=textareapadding]",0);

//print "cell";
//print $cell;

$cllrs = explode("<hr style=\"border-top:dotted #006699\" />",$cell);
print "\n"."cllrs";
print_r($cllrs);

//    unset($cllr[0]);

foreach($cllrs as $cllr) {
    $tempdom = new simple_html_dom();
    $tempdom->load($cllr);
   $namechunk = $tempdom->find("strong",0);
print "namechunk";
print $namechunk;

$name = trim(strip_tags($namechunk));
//$name = "name";
print "name";
print $name;
   $partychunk = $tempdom->find("strong",1);
//print $partychunk;
$partyshort = trim(strip_tags($partychunk));
$party = partyfull($partyshort);


$lea = $subpage;

#http://www.laois.ie/media/Media,174,en.JPG
$address = $tempdom->find("p",2)->innertext;

//print "\n". "address". $address;

#as james.daly@laoiscoco.ie

$emailname = explode(" ",$name);

//$initial = str_split($emailname[0],1);
$email = $emailname[0] .".". $emailname[1];
$email = str_replace("'","",$email);
$email = strtolower($email) . "@laoiscoco.ie";




$phonemobilecell = $tempdom->find("p",3);
$phonemobilecell = trim(strip_tags($phonemobilecell));
print $phonemobilecell;
$phonearray = explode("(",$phonemobilecell);
print "phonearray";
print_r($phonearray);




$phonearraylength = count($phonearray);

for($i=0; $i <= $phonearraylength; $i++)

{
if ( substr($phonearray[$i],0,2) == "05" ) {
$phonechunk = $phonearray[$i];
}
elseif ( substr($phonearray[$i],0,2) == "08" ) {
$mobilechunk = $phonearray[$i];

}
/*
else 
{
$phonechunk = "";
$mobilechunk = "";
}
*/

}
$phone = trim(preg_replace('/[^0-9]/', ' ', $phonechunk));
$mobile = trim(preg_replace('/[^0-9]/', ' ', $mobilechunk));
print "phone";
print $phone;

    $imagecell = $tempdom->find("img",0);
    $image = "http://www.laois.ie" .$imagecell->src;


unset($mobilechunk,$phonechunk,$phonearray);

        $councillors["$name"] = array(
            "LEA"     => $lea,
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image,
            "Address" => $address
        );
    }
}
unset($tempdom);
}
unset($name,$email,$mobile,$phone,$mobilechunk,$phonechunk,$phonearray,$dom,$html,$uri,$tempdom);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `lea` string, `name` string, `party` string, `email` string, `phone` string, `mobile` string, `image` string, `address` string)"); #);
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
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
scraperwiki::sqlitecommit();



function partyfull($partyshort) {

    if($partyshort == "F.G.")
    {
            $partyshort = "Fine Gael";
    }
    else if($partyshort == "F.F.") 
    {
            $partyshort = "Fianna Fail";
    }

    else if($partyshort == "PBP") 
    {
            $partyshort = "People before Profit";
    }          
    else if($partyshort == "Non Party") 
    {
            $partyshort = "Independent";
    }

return($partyshort);

}
?>