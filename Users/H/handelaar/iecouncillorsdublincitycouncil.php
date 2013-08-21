<?php
require 'scraperwiki/simple_html_dom.php';
$council = "Dublin City Council";
$uri = "http://www.dublincity.ie/YourCouncil/Councillors/Pages/FullCouncillorList.aspx";
$councillors = array();


# Load full Cllr list
$html = scraperwiki::scrape($uri);
$dom = new simple_html_dom();
$dom->load($html);

# Load URIs of Cllr detail pages into $pages
$rows=$dom->find("div[id=ctl00_PlaceHolderMain_ctl02__ControlWrapper_RichHtmlField] table tr");

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");

foreach($rows as $row) {
    $namecell = $row->find("td a",0);
    $url = "http://www.dublincity.ie" . $namecell->href;
    $name = trim(str_replace($namestrip,"",strip_tags($namecell)));
    $leacellcontents = $row->find("td",1);
    $leacell = trim(strip_tags($leacellcontents->innertext));
    $lea = trim(str_replace(" / ","/",trim($leacell)));
    $partycell = $row->find("td",2);
    $party = trim($partycell->plaintext);
    $imagecell = $row->find("td img",0);
    $image = "http://www.dublincity.ie" .$imagecell->src;

    $moredetails = get_extras($url);
    unset($namecell,$url,$leacellcontents,$leacell,$partycell,$imagecell);

    $councillors["$name"] = array(
        "LEA"     => $lea,
        "Party"   => $party,
        "Email"   => $moredetails["email"],
        "Phone"   => $moredetails["phone"],
        "Mobile"  => $moredetails["mobile"],
        "Image"   => $image,
        "Address" => $moredetails["address"]
    );
}
unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `phone` text, `mobile` text, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Dublin City Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
                    "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();




function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);


    $rightcolumn = $localdom->find("div[id=rightSidebar]");
    $contents = explode("</h5>",$rightcolumn[0]);
    
    $addressbits = explode("<h5>",$contents[1]);
    $address = trim(strip_tags($addressbits[0]));
    if (substr($address,-1) == ".") {
        $address = substr($address,0,-1);
    }

    $emailbits = explode("<h5>",$contents[2]);
    $email = trim(str_replace("&nbsp;","",strip_tags($emailbits[0])));

    $phonebits = explode("<h5>",$contents[3]);
    $phone = trim(str_replace("&nbsp;","",strip_tags($phonebits[0])));

    $mobilebits = explode("<h5>",$contents[4]);
    $mobile = trim(str_replace("&nbsp;","",strip_tags($mobilebits[0])));

    $faxbits = explode("<h5>",$contents[5]);
    $fax = trim(str_replace("&nbsp;","",strip_tags($faxbits[0])));


    $moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
    $moredetails["mobile"] = $mobile;
    $moredetails["fax"] = $fax;
    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);

}


?>