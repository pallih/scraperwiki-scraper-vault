<?php

$council = "Donegal City Council";
$uri = "http://www.donegalcoco.ie/council/members/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


# Put raw HTML for each Local Electoral Area into array

$content = $dom->find("div[id=PageContent]");
$data = $content[0]->innertext;
//print_r($data);
//$leas = $data;
$leas = explode("<h2>",$data);
unset($leas[0]);
unset($dom);

//$leas=$dom->find("div[id=PageContent] table");
//print_r($leas);
//print_r($this_lea);

foreach($leas as $lea) {
//print "$leas";
//print_r($leas);
//print $lea;
    $leadom = new simple_html_dom();
    $leadom->load($lea);
//break;
//print "leadom";
//print $leadom;
//$leachunk = array();
$leachunk = $leadom;
//print "leachunk";
//print_r($leachunk);
//print $leachunk;
 //   $this_lea = $leadom->find("h2");
    $this_lea = $leachunk->find("a",0);
$this_lea = "leaname";
//print_r($this_lea);
//print "this_lea";
//print $this_lea;

//print_r($this_lea);

//    $leaname = ucwords(strtolower(str_replace('CORK ','Cork City ',str_replace("&nbsp;", " ", str_replace(" LOCAL ELECTORAL AREA", "", $this_lea[0]->plaintext)))));
//print $this_lea;
    $leaname = $this_lea; #[0]; #->plaintext;
#$these_councillors = $leadom->find("div.members");
    $these_councillors = $leachunk->find("tr td");
//print_r($these_councillors);
//break;
    foreach($these_councillors as $this_councillor) {
//print $this_councillor;
        $councillordom = new simple_html_dom();
        $councillordom->load($this_councillor->innertext);
$cllrdata = $councillordom;
//print $cllrdata;
//break;
    //    $nameimg = $councillordom->find("a",0);
$cllrdetails = explode("<br />",$cllrdata);
print_r($cllrdetails);
$name = $cllrdetails[0]->innertext;
print $name;
//break;
    //    $img = "http://www.corkcity.ie" . $nameimg->src; # URL of photo
       // $name = $nameimg->innertext; # Raw name string
        unset($nameimg);

$party = "party";
//break;
  /*      
        # Ugly, but all these things are not valid HTML and/or hand-entered and inconsistently so
        $address = $councillordom->find("p",0)->innertext;
        $therest = explode("<br />",$councillordom->find("p",1)->innertext);
        $partystring = $therest[0];
        $party = str_replace('The ','',str_replace('IND/Neamh Pháirtí','IND',str_replace('Non Party','IND',strip_tags($partystring))));

        $remove = array("tel:","(",")","n/a","home");
        $phone  = trim(
                str_replace("-"," ",
                str_replace($remove,"",strtolower(
                strip_tags($therest[1])
                ))));
        if(substr($phone, 0, 1) == "4") { $phone = "021 " . $phone; } # Add area code for Cork City numbers missing one; they all start with a 4
                                                                      # (This is in fact crap and doesn't apply to non-Eircom numbers,
                                                                      # but there are none of those in this set at present.)

        $mobile = trim(str_replace("Mobile: ","",str_replace("-"," ",strip_tags($therest[2]))));
      $email  = trim(str_replace("email: ","",strip_tags($therest[3])));
*/  
   //     unset($councillordom);

        $councillors["$name"] = array(
            "LEA"     => $leaname,
            "Party"   => $party #,
     #       "Email"   => $email,
    #        "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
     #       "Address" => $address
        );
    }
}

//print_r($councillors);

//scraperwiki::attach("iecouncillorsall");

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Cork City Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"] #,
     #               "email"   => $values["Email"],
     #               "phone"   => $values["Phone"],
     #               "mobile"  => $values["Mobile"],
     #               "image"   => $values["Image"],
     #               "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?>
<?php

$council = "Donegal City Council";
$uri = "http://www.donegalcoco.ie/council/members/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


# Put raw HTML for each Local Electoral Area into array

$content = $dom->find("div[id=PageContent]");
$data = $content[0]->innertext;
//print_r($data);
//$leas = $data;
$leas = explode("<h2>",$data);
unset($leas[0]);
unset($dom);

//$leas=$dom->find("div[id=PageContent] table");
//print_r($leas);
//print_r($this_lea);

foreach($leas as $lea) {
//print "$leas";
//print_r($leas);
//print $lea;
    $leadom = new simple_html_dom();
    $leadom->load($lea);
//break;
//print "leadom";
//print $leadom;
//$leachunk = array();
$leachunk = $leadom;
//print "leachunk";
//print_r($leachunk);
//print $leachunk;
 //   $this_lea = $leadom->find("h2");
    $this_lea = $leachunk->find("a",0);
$this_lea = "leaname";
//print_r($this_lea);
//print "this_lea";
//print $this_lea;

//print_r($this_lea);

//    $leaname = ucwords(strtolower(str_replace('CORK ','Cork City ',str_replace("&nbsp;", " ", str_replace(" LOCAL ELECTORAL AREA", "", $this_lea[0]->plaintext)))));
//print $this_lea;
    $leaname = $this_lea; #[0]; #->plaintext;
#$these_councillors = $leadom->find("div.members");
    $these_councillors = $leachunk->find("tr td");
//print_r($these_councillors);
//break;
    foreach($these_councillors as $this_councillor) {
//print $this_councillor;
        $councillordom = new simple_html_dom();
        $councillordom->load($this_councillor->innertext);
$cllrdata = $councillordom;
//print $cllrdata;
//break;
    //    $nameimg = $councillordom->find("a",0);
$cllrdetails = explode("<br />",$cllrdata);
print_r($cllrdetails);
$name = $cllrdetails[0]->innertext;
print $name;
//break;
    //    $img = "http://www.corkcity.ie" . $nameimg->src; # URL of photo
       // $name = $nameimg->innertext; # Raw name string
        unset($nameimg);

$party = "party";
//break;
  /*      
        # Ugly, but all these things are not valid HTML and/or hand-entered and inconsistently so
        $address = $councillordom->find("p",0)->innertext;
        $therest = explode("<br />",$councillordom->find("p",1)->innertext);
        $partystring = $therest[0];
        $party = str_replace('The ','',str_replace('IND/Neamh Pháirtí','IND',str_replace('Non Party','IND',strip_tags($partystring))));

        $remove = array("tel:","(",")","n/a","home");
        $phone  = trim(
                str_replace("-"," ",
                str_replace($remove,"",strtolower(
                strip_tags($therest[1])
                ))));
        if(substr($phone, 0, 1) == "4") { $phone = "021 " . $phone; } # Add area code for Cork City numbers missing one; they all start with a 4
                                                                      # (This is in fact crap and doesn't apply to non-Eircom numbers,
                                                                      # but there are none of those in this set at present.)

        $mobile = trim(str_replace("Mobile: ","",str_replace("-"," ",strip_tags($therest[2]))));
      $email  = trim(str_replace("email: ","",strip_tags($therest[3])));
*/  
   //     unset($councillordom);

        $councillors["$name"] = array(
            "LEA"     => $leaname,
            "Party"   => $party #,
     #       "Email"   => $email,
    #        "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
     #       "Address" => $address
        );
    }
}

//print_r($councillors);

//scraperwiki::attach("iecouncillorsall");

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Cork City Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"] #,
     #               "email"   => $values["Email"],
     #               "phone"   => $values["Phone"],
     #               "mobile"  => $values["Mobile"],
     #               "image"   => $values["Image"],
     #               "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?>
<?php

$council = "Donegal City Council";
$uri = "http://www.donegalcoco.ie/council/members/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


# Put raw HTML for each Local Electoral Area into array

$content = $dom->find("div[id=PageContent]");
$data = $content[0]->innertext;
//print_r($data);
//$leas = $data;
$leas = explode("<h2>",$data);
unset($leas[0]);
unset($dom);

//$leas=$dom->find("div[id=PageContent] table");
//print_r($leas);
//print_r($this_lea);

foreach($leas as $lea) {
//print "$leas";
//print_r($leas);
//print $lea;
    $leadom = new simple_html_dom();
    $leadom->load($lea);
//break;
//print "leadom";
//print $leadom;
//$leachunk = array();
$leachunk = $leadom;
//print "leachunk";
//print_r($leachunk);
//print $leachunk;
 //   $this_lea = $leadom->find("h2");
    $this_lea = $leachunk->find("a",0);
$this_lea = "leaname";
//print_r($this_lea);
//print "this_lea";
//print $this_lea;

//print_r($this_lea);

//    $leaname = ucwords(strtolower(str_replace('CORK ','Cork City ',str_replace("&nbsp;", " ", str_replace(" LOCAL ELECTORAL AREA", "", $this_lea[0]->plaintext)))));
//print $this_lea;
    $leaname = $this_lea; #[0]; #->plaintext;
#$these_councillors = $leadom->find("div.members");
    $these_councillors = $leachunk->find("tr td");
//print_r($these_councillors);
//break;
    foreach($these_councillors as $this_councillor) {
//print $this_councillor;
        $councillordom = new simple_html_dom();
        $councillordom->load($this_councillor->innertext);
$cllrdata = $councillordom;
//print $cllrdata;
//break;
    //    $nameimg = $councillordom->find("a",0);
$cllrdetails = explode("<br />",$cllrdata);
print_r($cllrdetails);
$name = $cllrdetails[0]->innertext;
print $name;
//break;
    //    $img = "http://www.corkcity.ie" . $nameimg->src; # URL of photo
       // $name = $nameimg->innertext; # Raw name string
        unset($nameimg);

$party = "party";
//break;
  /*      
        # Ugly, but all these things are not valid HTML and/or hand-entered and inconsistently so
        $address = $councillordom->find("p",0)->innertext;
        $therest = explode("<br />",$councillordom->find("p",1)->innertext);
        $partystring = $therest[0];
        $party = str_replace('The ','',str_replace('IND/Neamh Pháirtí','IND',str_replace('Non Party','IND',strip_tags($partystring))));

        $remove = array("tel:","(",")","n/a","home");
        $phone  = trim(
                str_replace("-"," ",
                str_replace($remove,"",strtolower(
                strip_tags($therest[1])
                ))));
        if(substr($phone, 0, 1) == "4") { $phone = "021 " . $phone; } # Add area code for Cork City numbers missing one; they all start with a 4
                                                                      # (This is in fact crap and doesn't apply to non-Eircom numbers,
                                                                      # but there are none of those in this set at present.)

        $mobile = trim(str_replace("Mobile: ","",str_replace("-"," ",strip_tags($therest[2]))));
      $email  = trim(str_replace("email: ","",strip_tags($therest[3])));
*/  
   //     unset($councillordom);

        $councillors["$name"] = array(
            "LEA"     => $leaname,
            "Party"   => $party #,
     #       "Email"   => $email,
    #        "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
     #       "Address" => $address
        );
    }
}

//print_r($councillors);

//scraperwiki::attach("iecouncillorsall");

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)", #, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Cork City Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"] #,
     #               "email"   => $values["Email"],
     #               "phone"   => $values["Phone"],
     #               "mobile"  => $values["Mobile"],
     #               "image"   => $values["Image"],
     #               "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?>
