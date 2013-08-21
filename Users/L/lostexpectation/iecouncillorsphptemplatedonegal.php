<?php

$council = "Donegal county Council";
$uri = "http://www.donegalcoco.ie/council/members/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$content = $dom->find("div[id=PageContent]");
print_r($content);
break;
$leas = array();
$leas = $content->find("h2");
foreach($leas as $lea) {

//foreach($row->find("div[id=PageContent]") as $cell) { 
//$rows=$dom->find("div[id=PageContent]"); 

//foreach($rows as $row) {
/* Do your stuff here */
$rows=$dom->find("div[id=PageContent] table td"); 

foreach($rows as $row) {

$name = "name";

$party = "party";

        $councillors["$name"] = array(
            "LEA"     => $lea,
            "Party"   => $party #,
   //         "Email"   => $email,
   //         "Phone"   => $phone,
   //         "Mobile"  => $mobile,
  //          "Image"   => $image,
  //          "Address" => $address
        );
}
}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `lea` string, `name` string, `party` string)"); //, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party)",  //, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"] #,
     //               "email"   => $values["Email"],
      //              "phone"   => $values["Phone"],
      //              "mobile"  => $values["Mobile"],
       //             "image"   => $values["Image"],
      //              "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?>