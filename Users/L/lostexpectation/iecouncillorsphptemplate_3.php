<?php

$council = "Galway City Council";
$uri = "http://www.galwaycity.ie/AllServices/YourCouncil/CouncilMembers/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

# Example listing address: http://www.galwaycity.ie/AllServices/YourCouncil/CouncilMembers/GalwayCityWest/
$subpages = array(
    "GalwayCityEast",
    "GalwayCityWest",
    "GalwayCityCentral",
    
    );

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    $cell = $dom->find("div[id=content]",0);



    $these_councillors = explode("<!-- start Council Member template -->",$cell);


    unset($these_councillors[0]);

foreach($these_councillors as $this_councillor) {
    $tempdom = new simple_html_dom();
    $tempdom->load($this_councillor);
    $cllrs = $tempdom->find("h2",0);


    $name = str_replace("Cllr. ","",strip_tags($cllrs));
    $name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $name );

    $cllrcells = explode("<div",$this_councillor);

    $imagecell = $tempdom->find("img",0);

    if(substr($imagecell,11,5) == "media") {
        $image = "http://www.galwaycity.ie" . $imagecell->src;
            } 
    else{
        $image = "http://www.galwaycity.ie/AllServices/YourCouncil/CouncilMembers/" . $subpage . "/" . $imagecell->src;
}


    $cllrdetails = explode("<br />",$cllrcells[2]);

    $detailslength = count($cllrdetails);

    $email =  $cllrdetails[$detailslength-2];
    $email =  str_replace("Email: ","",strip_tags($email));
    $phone = $cllrdetails[$detailslength-3];
    $phonenumbers = explode(")",$cllrdetails[$detailslength-3]);

    $phone = $phonenumbers[1];




    if ( isset($phonenumbers[2]) ) {
        $mobile = $phonenumbers[2];
    }
    else {
        $mobile = $phonenumbers[1];
    }

    $phone = str_replace("(home/fax","",str_replace("(mobile","",str_replace("(work","",$phone)));
    $mobile = str_replace("(work","",str_replace("(mobile","",str_replace("(fax","",$mobile)));

    trim($phone);
    
    $test = substr($phone,0,4);
    
    if(substr($phone,0,4) != "091") {

        $mobile = $phone;
        $phone = "";
    }

    if(substr($mobile,0,4) == "091") {


    $mobile = "";
    }


  if($detailslength === 8) {
   
        $addresscell = trim($cllrdetails[1]) .", ".  trim($cllrdetails[2]) .", ".  trim($cllrdetails[3]).", ".  trim($cllrdetails[4]);    
    }
    elseif($detailslength === 7) {

        $addresscell = trim($cllrdetails[1]) .", ".  trim($cllrdetails[2]) .", ".  trim($cllrdetails[3]);  
    }
    else 
    {

      $addresscell = trim($cllrdetails[1]) .", ".  trim($cllrdetails[2]);
    }

    $addresscell = trim($addresscell);
    $addresscell = trim(str_replace("Galway,","Galway",$addresscell));
    $addresscell = str_replace(" ,","",str_replace(", ,","",str_replace(",,","",str_replace("<br>","",$addresscell))));

    $address = $addresscell;
    $address = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $address );


    $party =  $cllrdetails[$detailslength-1];
    $party = trim(str_replace("&nbsp;","",str_replace("The ","",str_replace("Party: ","",strip_tags($party)))));

    $party = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $party );

 $councillors["$name"] = array(
            "LEA"     => str_replace("GalwayCity","Galway City ",$subpage),
            "Party"   => $party,
            "Email"   => $email, 
            "Phone"   => $phone, 
            "Mobile"  => $mobile, 
            "Address" => $address,
            "Image"   => $image
        );
    }
}
//}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `phone` text, `mobile` text, `address` string, `image` string)"); #, `image` string,  `address` string)");
//scraperwiki::sqliteexecute("delete from councillors");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :address, :image)", #, :image, :address)", 
            array(  "auth"    => "Galway City Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "address" => $values["Address"],
                    "image"   => $values["Image"] #,
            )
    );
}
scraperwiki::sqlitecommit();
?><?php

$council = "Galway City Council";
$uri = "http://www.galwaycity.ie/AllServices/YourCouncil/CouncilMembers/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

# Example listing address: http://www.galwaycity.ie/AllServices/YourCouncil/CouncilMembers/GalwayCityWest/
$subpages = array(
    "GalwayCityEast",
    "GalwayCityWest",
    "GalwayCityCentral",
    
    );

foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    $cell = $dom->find("div[id=content]",0);



    $these_councillors = explode("<!-- start Council Member template -->",$cell);


    unset($these_councillors[0]);

foreach($these_councillors as $this_councillor) {
    $tempdom = new simple_html_dom();
    $tempdom->load($this_councillor);
    $cllrs = $tempdom->find("h2",0);


    $name = str_replace("Cllr. ","",strip_tags($cllrs));
    $name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $name );

    $cllrcells = explode("<div",$this_councillor);

    $imagecell = $tempdom->find("img",0);

    if(substr($imagecell,11,5) == "media") {
        $image = "http://www.galwaycity.ie" . $imagecell->src;
            } 
    else{
        $image = "http://www.galwaycity.ie/AllServices/YourCouncil/CouncilMembers/" . $subpage . "/" . $imagecell->src;
}


    $cllrdetails = explode("<br />",$cllrcells[2]);

    $detailslength = count($cllrdetails);

    $email =  $cllrdetails[$detailslength-2];
    $email =  str_replace("Email: ","",strip_tags($email));
    $phone = $cllrdetails[$detailslength-3];
    $phonenumbers = explode(")",$cllrdetails[$detailslength-3]);

    $phone = $phonenumbers[1];




    if ( isset($phonenumbers[2]) ) {
        $mobile = $phonenumbers[2];
    }
    else {
        $mobile = $phonenumbers[1];
    }

    $phone = str_replace("(home/fax","",str_replace("(mobile","",str_replace("(work","",$phone)));
    $mobile = str_replace("(work","",str_replace("(mobile","",str_replace("(fax","",$mobile)));

    trim($phone);
    
    $test = substr($phone,0,4);
    
    if(substr($phone,0,4) != "091") {

        $mobile = $phone;
        $phone = "";
    }

    if(substr($mobile,0,4) == "091") {


    $mobile = "";
    }


  if($detailslength === 8) {
   
        $addresscell = trim($cllrdetails[1]) .", ".  trim($cllrdetails[2]) .", ".  trim($cllrdetails[3]).", ".  trim($cllrdetails[4]);    
    }
    elseif($detailslength === 7) {

        $addresscell = trim($cllrdetails[1]) .", ".  trim($cllrdetails[2]) .", ".  trim($cllrdetails[3]);  
    }
    else 
    {

      $addresscell = trim($cllrdetails[1]) .", ".  trim($cllrdetails[2]);
    }

    $addresscell = trim($addresscell);
    $addresscell = trim(str_replace("Galway,","Galway",$addresscell));
    $addresscell = str_replace(" ,","",str_replace(", ,","",str_replace(",,","",str_replace("<br>","",$addresscell))));

    $address = $addresscell;
    $address = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $address );


    $party =  $cllrdetails[$detailslength-1];
    $party = trim(str_replace("&nbsp;","",str_replace("The ","",str_replace("Party: ","",strip_tags($party)))));

    $party = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $party );

 $councillors["$name"] = array(
            "LEA"     => str_replace("GalwayCity","Galway City ",$subpage),
            "Party"   => $party,
            "Email"   => $email, 
            "Phone"   => $phone, 
            "Mobile"  => $mobile, 
            "Address" => $address,
            "Image"   => $image
        );
    }
}
//}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `phone` text, `mobile` text, `address` string, `image` string)"); #, `image` string,  `address` string)");
//scraperwiki::sqliteexecute("delete from councillors");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :address, :image)", #, :image, :address)", 
            array(  "auth"    => "Galway City Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "address" => $values["Address"],
                    "image"   => $values["Image"] #,
            )
    );
}
scraperwiki::sqlitecommit();
?>