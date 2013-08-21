<?php

$council = "Cavan County Council";
$uri = "http://www.cavancoco.ie/cavanweb/publish/domain/cavancoco/Default.aspx?StructureID_str=156";
$html = scraperwiki::scrape($uri);

$councillors = array();
$subpages = array(
    "&category=Bailieborough%20Electoral%20Area",
    "&category=Ballyjamesduff%20Electoral%20Area",
    "&category=Belturbet%20Electoral%20Area",
    "&category=Cavan%20Electoral%20Area"
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


      foreach($dom->find("div[class=councillors]") as $cell) {
    
        $personcell = $cell->find("h4");
        $name = trim(strip_tags($personcell[0]->innertext));

        $party = $cell->find("li",0);
        $party = trim(str_replace("<strong>Party:</strong> ", "",$party->innertext));

        $emailcell = $cell->find("a",0);
        $email = trim(str_replace("mailto:","",strip_tags($emailcell)));
        $email = str_replace("<li>", "", str_replace("</li>", "",$email));

        $address = $cell->find("p",0);
        $address = str_replace("<p>", "", str_replace("</p>", "",$address));
        
        $phone = $cell->find("li",1);
        $phone = str_replace("-","",str_replace("Tel:","",strip_tags($phone)));

        $mobile = $cell->find("li",2);
        $mobile = str_replace("-","",str_replace("Mobile:","",strip_tags($mobile)));

        $imagecell = $cell->find("img",0);
        $image = "http://www.cavancoco.ie/cavanweb/publish/domain/cavancoco/" .$imagecell->src;

        $councillors["$name"] = array(
            "LEA"     => str_replace("&category=", "", str_replace("&nbsp;", " ", str_replace("%20Electoral%20Area", "",$subpage))),
            "Party"   => $party,
            "Email"   => $email,
            "Address" => $address,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image
         );
    }
}

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
                    "image"   => $values["Image"],
               
            )
    );
}
scraperwiki::sqlitecommit();
?>