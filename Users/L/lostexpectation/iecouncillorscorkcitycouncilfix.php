<?php

$council = "Cork City Council";
$uri = "http://www.corkcity.ie/yourcouncil/electedmembers/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


# Put raw HTML for each Local Electoral Area into array

$content = $dom->find("div[id=general-body-content]");
$data = $content[0]->innertext;
$leas = explode("<!-- Start General No Title Template -->",$data);
unset($leas[0]);
unset($dom);


# Process LEAs in turn

foreach($leas as $lea) {
    $leadom = new simple_html_dom();
    $leadom->load($lea);
    $this_lea = $leadom->find("h2");
    $leaname = ucwords(strtolower(str_replace('CORK ','Cork City ',str_replace("&nbsp;", " ", str_replace(" LOCAL ELECTORAL AREA", "", $this_lea[0]->plaintext)))));
    
    $these_councillors = $leadom->find("div.members");

    foreach($these_councillors as $this_councillor) {
        $councillordom = new simple_html_dom();
        $councillordom->load($this_councillor->innertext);

        $nameimg = $councillordom->find("img",0);
        $img = "http://www.corkcity.ie" . $nameimg->src; # URL of photo
        $name = str_replace("Cllr. ","",str_replace("Councillor ","",str_replace("Lord Mayor of Cork, ","",$nameimg->title))); # Raw name string
        unset($nameimg);
        $email = trim(str_replace("mailto:","",strip_tags($councillordom->find("a",0)->href)));
    
        # Ugly, but all these things are not valid HTML and/or hand-entered and inconsistently so
        
        $therest = explode("<br />",$councillordom->find("p",1)->innertext);
print $name;
print_r($therest); 
        # ugh the ones where there is no <p> before address means 'mail form' or empty ends up in party var
        $partytest = $therest[0];
        
        if( strlen(strstr($partytest,"Mail Form")) > 0 || strlen($partytest) == 0 ) {
            $therestb = explode("<br />",$councillordom->find("p",0)->innertext);
            
            $partystring = $therestb[0];
            $phone  = $therestb[1];
            $mobile = $therestb[2];
            #get address
            $cllrp = explode("<p>",$councillordom);
            $cllrh2 = $cllrp[0];
            $cllr = explode("</h2>",$cllrh2);

            $address = $cllr[1];
            
            }
        else { #normal
            $partystring = $therest[0];

            $mobile = $therest[2];
            $phone  = $therest[1];

            $address = $councillordom->find("p",0); 
            }
            

            # cleanall         
            $party = str_replace('The ','',str_replace('Non Party/Neamh Pháirtí','Independent',strip_tags($partystring)));
            
            $remove = array("tel:","(",")","n/a","home");
            $phone  = trim(str_replace("-"," ",str_replace($remove,"",strtolower(strip_tags($phone)))));
               if(substr($phone, 0, 1) == "4") { $phone = "021 " . $phone; } # Add area code for Cork City numbers missing one; they all start with a 4
                                                                      # (This is in fact crap and doesn't apply to non-Eircom numbers,
                                                                      # but there are none of those in this set at present.)

            $mobile = trim(str_replace("Mobile: ","",str_replace("-"," ",strip_tags($mobile))));
            
            $address = str_replace("<br />"," ",$address); #because some entries have no space betw , and</br>
            $address = trim(str_replace("&nbsp;"," ",(htmlspecialchars_decode(strip_tags(($address))))));    
        
        

        //$mobile = trim(str_replace("Mobile: ","",str_replace("-"," ",strip_tags($therest[2]))));
        unset($councillordom);

        $councillors["$name"] = array(
            "LEA"     => $leaname,
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Address" => $address,
            "Image"   => $img
            
        );
    }
}

//print_r($councillors);

//scraperwiki::attach("iecouncillorsall");

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `lea` string, `name` string, `party` string, `email` string, `phone` string, `mobile` string, `address` string, `image` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :address, :image)", 
            array(  "auth"    => "Cork City Council", 
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
?>
<?php

$council = "Cork City Council";
$uri = "http://www.corkcity.ie/yourcouncil/electedmembers/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


# Put raw HTML for each Local Electoral Area into array

$content = $dom->find("div[id=general-body-content]");
$data = $content[0]->innertext;
$leas = explode("<!-- Start General No Title Template -->",$data);
unset($leas[0]);
unset($dom);


# Process LEAs in turn

foreach($leas as $lea) {
    $leadom = new simple_html_dom();
    $leadom->load($lea);
    $this_lea = $leadom->find("h2");
    $leaname = ucwords(strtolower(str_replace('CORK ','Cork City ',str_replace("&nbsp;", " ", str_replace(" LOCAL ELECTORAL AREA", "", $this_lea[0]->plaintext)))));
    
    $these_councillors = $leadom->find("div.members");

    foreach($these_councillors as $this_councillor) {
        $councillordom = new simple_html_dom();
        $councillordom->load($this_councillor->innertext);

        $nameimg = $councillordom->find("img",0);
        $img = "http://www.corkcity.ie" . $nameimg->src; # URL of photo
        $name = str_replace("Cllr. ","",str_replace("Councillor ","",str_replace("Lord Mayor of Cork, ","",$nameimg->title))); # Raw name string
        unset($nameimg);
        $email = trim(str_replace("mailto:","",strip_tags($councillordom->find("a",0)->href)));
    
        # Ugly, but all these things are not valid HTML and/or hand-entered and inconsistently so
        
        $therest = explode("<br />",$councillordom->find("p",1)->innertext);
print $name;
print_r($therest); 
        # ugh the ones where there is no <p> before address means 'mail form' or empty ends up in party var
        $partytest = $therest[0];
        
        if( strlen(strstr($partytest,"Mail Form")) > 0 || strlen($partytest) == 0 ) {
            $therestb = explode("<br />",$councillordom->find("p",0)->innertext);
            
            $partystring = $therestb[0];
            $phone  = $therestb[1];
            $mobile = $therestb[2];
            #get address
            $cllrp = explode("<p>",$councillordom);
            $cllrh2 = $cllrp[0];
            $cllr = explode("</h2>",$cllrh2);

            $address = $cllr[1];
            
            }
        else { #normal
            $partystring = $therest[0];

            $mobile = $therest[2];
            $phone  = $therest[1];

            $address = $councillordom->find("p",0); 
            }
            

            # cleanall         
            $party = str_replace('The ','',str_replace('Non Party/Neamh Pháirtí','Independent',strip_tags($partystring)));
            
            $remove = array("tel:","(",")","n/a","home");
            $phone  = trim(str_replace("-"," ",str_replace($remove,"",strtolower(strip_tags($phone)))));
               if(substr($phone, 0, 1) == "4") { $phone = "021 " . $phone; } # Add area code for Cork City numbers missing one; they all start with a 4
                                                                      # (This is in fact crap and doesn't apply to non-Eircom numbers,
                                                                      # but there are none of those in this set at present.)

            $mobile = trim(str_replace("Mobile: ","",str_replace("-"," ",strip_tags($mobile))));
            
            $address = str_replace("<br />"," ",$address); #because some entries have no space betw , and</br>
            $address = trim(str_replace("&nbsp;"," ",(htmlspecialchars_decode(strip_tags(($address))))));    
        
        

        //$mobile = trim(str_replace("Mobile: ","",str_replace("-"," ",strip_tags($therest[2]))));
        unset($councillordom);

        $councillors["$name"] = array(
            "LEA"     => $leaname,
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Address" => $address,
            "Image"   => $img
            
        );
    }
}

//print_r($councillors);

//scraperwiki::attach("iecouncillorsall");

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `lea` string, `name` string, `party` string, `email` string, `phone` string, `mobile` string, `address` string, `image` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :address, :image)", 
            array(  "auth"    => "Cork City Council", 
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
?>
