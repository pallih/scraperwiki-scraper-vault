<?php

$council = "Dun Laoghaire Rathdown County Council";
$uri = "http://www.dlrcoco.ie/aboutus/councilbusiness/listofcouncillors/"; #http://www.dlrcoco.ie/aboutus/councilbusiness/listofcouncillorsbyelectoralarea/
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


$rows=$dom->find("div[id=content] tr"); 

$i=0;
foreach($rows as $row) {
if ($i > 0)
        {
           
        $cell = $row->find("td",1);
       
        $namepartyadd  = explode("<br />", $cell);
        $namepartyadd = str_replace("&nbsp;"," ",$namepartyadd);
        $namebit = $namepartyadd[0];
        $nameparts  = explode("(", $namebit);
        $flipname = explode(",", $nameparts[0]);

        $name = trim(strip_tags($flipname[1])) . " " . trim(strip_tags($flipname[0]));
        $name = trim(str_replace("&nbsp;","",strip_tags($name)));
        $name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $name );
   //     $name = ucwords(strtolower($name));
        $name = uchiberno($name);
         
        $partyshort = str_replace(")","",$nameparts[1]);
        $party = partyfull($partyshort);

        if (isset($namepartyadd[3])) {
                $address = $namepartyadd[1] . " " . $namepartyadd[2] . " " . $namepartyadd[3];
            }
            else if  (isset($namepartyadd[2])) {
                $address = $namepartyadd[1] . " " . $namepartyadd[2];
            }
            else {
                $address = $namepartyadd[1];
            }

        $address = trim(str_replace("&nbsp;","",strip_tags($address)));
        $address = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $address );


        $mobilephone = $row->find("td",2);
          $mobilephone =  str_replace("Tel","",str_replace("Home","",str_replace("Fax","",str_replace("&nbsp;","",str_replace("Office","",$mobilephone)))));
        $mobilephoneparts  = explode(":", $mobilephone); 
    
        if (!isset($mobilephoneparts[1])) {
                $phone = "";
            }
            else {
                $phone = trim(strip_tags($mobilephoneparts[1]));
                $phone = "0" . substr($phone,0,2) . " " . substr($phone,2,5);
            }
        

        $mobile = trim(str_replace("-"," ",strip_tags($mobilephoneparts[0])));
        $mobile = substr($mobile,0,11);

        $emailcell = $row->find("td",3);
    
        $emailcell = trim(str_replace("Website"," ",str_replace("&nbsp;","",strip_tags($emailcell))));
        $emailparts = explode(" ",$emailcell);
        $email = $emailparts[0];

        $nameimg = $row->find("img",0);
        $image = "http://www.dlrcoco.ie" . $nameimg->src; # URL of photo

        $leacell = $row->find("td",4);
        $leacellparts  = explode("(", $leacell);
        $lea = trim(strip_tags($leacellparts[0]));
        $lea = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $lea );

        

        $councillors["$name"] = array(
            "LEA"     => $lea, 
            "Party"   => $party, 
            "Address" => $address,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image
       
    );

        }
        $i++;
}

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `lea` string, `name` string, `party` string, `address` string, `email` string, `phone` string, `mobile` string, `image` string)"); 

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :address, :email, :phone, :mobile, :image)", 
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

    if($partyshort == "FG")
    {
            $partyshort = "Fine Gael";
    }
    else if($partyshort == "FF") 
    {
            $partyshort = "Fianna Fail";
    }
    else if($partyshort == "Lab") 
    {
            $partyshort = "Labour";
    }
    else if($partyshort == "PBP") 
    {
            $partyshort = "People before Profit";
    }          
    else if($partyshort == "IND" || "ind") 
    {
            $partyshort = "Independent";
    }

return($partyshort);

}


function uchiberno($str)
{
    $strUPPER = strtolower($str);
    $str = ucwords($strUPPER);

    // Not perfect dyer85 http://php.net/manual/en/function.ucwords.php
    return preg_replace(
        '/
            (?: ^ | \\b )         # assertion: beginning of string or a word boundary
            ( O\' | Ma?c | Fitz)  # attempt to match Irish surnames
            ( [^\W\d_] )          # match next char; we exclude digits and _ from \w
        /xe',
        "'\$1' . strtoupper('\$2')",
        $str);
}

?>