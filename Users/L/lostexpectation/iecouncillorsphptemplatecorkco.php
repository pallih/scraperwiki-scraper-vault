<?php

require 'scraperwiki/simple_html_dom.php';
$council = "Cork County Council";
$uri = "http://www.corkcoco.ie/co/web/Cork%20County%20Council/About%20Us/Councillors/";



# Example listing address: http://www.corkcoco.ie/co/web/Cork%20County%20Council/About%20Us/Councillors/Balbriggan/
$subpages = array(
    "Bandon%20Electoral%20Area",
    "Bantry%20Electoral%20Area",
    "Carrigaline%20Electoral%20Area",
    "Fermoy%20Electoral%20Area",
    "Kanturk%20Electoral%20Area",
    "Macroom%20Electoral%20Area",
    "Mallow%20Electoral%20Area",
    "Midleton%20Electoral%20Area",
    "Skibbereen%20Electoral%20Area"
    );


$councillors = array();
foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    foreach($dom->find("div[class=rc-smry]") as $cell) {
        # here's the table on detail pages
        $namecell = $cell->find("td strong",0); #strong
        $name =   trim(str_replace("&nbsp;"," ",str_replace("Cllr.","",strip_tags($namecell))));
        $details = $cell->find("td",3);
//print $details;

       
        $detailsparty = explode("</strong>",$details);
        $party = $detailsparty[2];
    //    print $party;

        $party  = utf8_encode($party);
        $party  = trim(str_replace(".","",strip_tags($party)));

//$detailsaddress = $detailsparty[1];
$detailsaddress = explode("<br>",$detailsparty[1]);
$address = $detailsaddress[1] . $detailsaddress[2] . $detailsaddress[3] . $detailsaddress[4];
$address = strip_tags($address);


$phone = $detailsaddress[4];
$mobile = $detailsaddress[5];
$email = $cell->find("a",0);
$email = "broke";
        $imagecell = $cell->find("td",2)->innertext;
print $imagecell;
        $image = "http://www.corkcoco.ie/" . $imagecell->src;
print $image;

$url = $uri . $subpage . "/";



/*

And then the DB stuff

*/




      $councillors["$name"] = array(
            "LEA"     => str_replace("%20"," ",$subpage), 
            "Party"   => $party, #, 
            "Address" => $address,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
           "Url"  => $url,
           "Image"   => $image
       
    );
}
}

#unset($dom);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `address` string, `email` string, `phone` string, `mobile` string, `url` string, `image` string)"); 
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :address, :email, :phone, :mobile, :url, :image)",  
            array(  "auth"    => $council, 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"], #,
                   "email"   => $values["Email"],
                    "url"   => $values["Url"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"], #,
                    "address" => $values["Address"],
                      )
    );
}
scraperwiki::sqlitecommit();
?>