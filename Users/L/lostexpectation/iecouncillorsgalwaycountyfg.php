<?php

$council = "Galway County Council";
$base = "http://www.finegael.ie";

$uri = "http://www.finegael.ie/our-people/tds/";
$html = scraperwiki::scrape($uri);

$councillors = array();
$page = "http://www.finegael.ie/our-people/tds/?page=";
    

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

/* Do your stuff here */

//$pages = $page . $i;

//for( $i=1; $i<15; $i++ )
//{

//foreach($pages as $page) {



//foreach($dom->find("div[class=politician-photo] a") as $cell) {
//$pagenumb = $cell->find("a");
//for($i = 1; $i <= 15; i++) {
foreach (range(1,16) as $i) {
$page = "?page=" . $i;
//print $page;

    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $page); # . "/"
    $dom->load($html);

$rows=$dom->find("div[class=inner]"); # as $cell) {


foreach($dom->find("div[class=politician-photo]") as $cell) {
//$name = $cell->find("div[class=inner]");
//print $name;
$namecell = $cell->find("a",0);
//print "namecell" . $namecell . "\n";
$url = $base . $namecell->href;  

$url = str_replace("/index.xml","",$url);
//$url = $uri . $namecell->href;  
//print $url;
$name = $namecell->find('img', 0)->getAttribute('alt');
$name = str_replace("Councillor ","",$name);
$name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $name );
//->find('ul.sellerInformation img', 0)
$moredetails = get_extras($url);

        $councillors["$name"] = array(

            "LEA"     => $page, 
            "Url"   => $url, 
            "Address" => $moredetails["address"],
            "Email"   => $moredetails["email"],
            "Phone"   => $moredetails["phone"],
          #  "Mobile"  => $moredetails["$mobile"],
            "Image"   => $moredetails["image"],
  "Localaddress"   => $moredetails["localaddress"],
  "Constituency"   => $moredetails["constituency"]
           );
    }
$i++;
}

unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`lea` string, `name` string, `url` string, `email` string, `address` string, `image` string, `phone` string, `localaddress` string, `constituency` string)"); #, `name` string, `party` string, `email` string, `address` string, `phone` string, `mobile` string, `image` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:lea, :name, :url, :email, :address, :image, :phone, :localaddress, :constituency)", #, :name, :party,, :address, :phone, :mobile, :image)",
            array(  "lea"     => $values["LEA"],
                    "name"    => $name,
                    "url"   => $values["Url"],
                   "email"   => $values["Email"],
                    "address" => $values["Address"],
                    "phone"   => $values["Phone"],
             #       "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
 "localaddress"   => $values["Localaddress"],
 "constituency"   => $values["Constituency"]

               
            )
    );
}
scraperwiki::sqlitecommit();


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);
    $rightcolumn = $localdom->find("div[class=politician-sidebar]");
    $contents = explode("<p>",$rightcolumn[0]->innertext); 
$local = explode("<br />",$contents[4]->innertext);
//$contactarray = explode("<br />",$contents[1]);
//$contact = $contactarray[0]; # 
print $contents[0];
print_r($contents);

$emailchunk = $contents[2]; #->innertext;
$emailarray = explode("<br />",$emailchunk);
//$email = $contact->href;
//print_r($emailarray);
$email = $emailarray[0]; #->find("div[class=image]");
 //$email = $email->innertext;
$email = strip_tags($email); //
//print $emailarray[0];

//$image = $contents[0]->find("div[class=image] img",0);
// $imagecell = $row->find("td img",0);
 //   $image = "http://www.dublincity.ie" .$imagecell->src;
print_r($contents);
$image = $contents[0]->src;
print "\n" . "image" . $image;
print_r($image);
$localaddress = $contents[4];
$localaddress = explode("<br />",$localaddress);
$localaddress = $localaddress[0];
$localaddress = strip_tags($localaddress); 
$constituency = $contents[3];


$constituency = explode("</p>",$constituency);
$constituency = strip_tags($constituency[0]); 
$image = "http://www.finegael.ie" . $contents[0]->src;

$addressarray = explode("<br />",$contents[1]);
print_r($addressarray);
$address = trim($addressarray[0]); 
$address = strip_tags($address); 
$phone = trim(str_replace("Telephone: ","",strip_tags($addressarray[1]))); 

    $moredetails = array();    

    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
  $moredetails["localaddress"] = $localaddress;
 $moredetails["constituency"] = $constituency;
   $moredetails["image"] = $image;
  //  unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);
}
?>
<?php

$council = "Galway County Council";
$base = "http://www.finegael.ie";

$uri = "http://www.finegael.ie/our-people/tds/";
$html = scraperwiki::scrape($uri);

$councillors = array();
$page = "http://www.finegael.ie/our-people/tds/?page=";
    

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

/* Do your stuff here */

//$pages = $page . $i;

//for( $i=1; $i<15; $i++ )
//{

//foreach($pages as $page) {



//foreach($dom->find("div[class=politician-photo] a") as $cell) {
//$pagenumb = $cell->find("a");
//for($i = 1; $i <= 15; i++) {
foreach (range(1,16) as $i) {
$page = "?page=" . $i;
//print $page;

    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $page); # . "/"
    $dom->load($html);

$rows=$dom->find("div[class=inner]"); # as $cell) {


foreach($dom->find("div[class=politician-photo]") as $cell) {
//$name = $cell->find("div[class=inner]");
//print $name;
$namecell = $cell->find("a",0);
//print "namecell" . $namecell . "\n";
$url = $base . $namecell->href;  

$url = str_replace("/index.xml","",$url);
//$url = $uri . $namecell->href;  
//print $url;
$name = $namecell->find('img', 0)->getAttribute('alt');
$name = str_replace("Councillor ","",$name);
$name = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $name );
//->find('ul.sellerInformation img', 0)
$moredetails = get_extras($url);

        $councillors["$name"] = array(

            "LEA"     => $page, 
            "Url"   => $url, 
            "Address" => $moredetails["address"],
            "Email"   => $moredetails["email"],
            "Phone"   => $moredetails["phone"],
          #  "Mobile"  => $moredetails["$mobile"],
            "Image"   => $moredetails["image"],
  "Localaddress"   => $moredetails["localaddress"],
  "Constituency"   => $moredetails["constituency"]
           );
    }
$i++;
}

unset($dom,$html,$uri);

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`lea` string, `name` string, `url` string, `email` string, `address` string, `image` string, `phone` string, `localaddress` string, `constituency` string)"); #, `name` string, `party` string, `email` string, `address` string, `phone` string, `mobile` string, `image` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:lea, :name, :url, :email, :address, :image, :phone, :localaddress, :constituency)", #, :name, :party,, :address, :phone, :mobile, :image)",
            array(  "lea"     => $values["LEA"],
                    "name"    => $name,
                    "url"   => $values["Url"],
                   "email"   => $values["Email"],
                    "address" => $values["Address"],
                    "phone"   => $values["Phone"],
             #       "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
 "localaddress"   => $values["Localaddress"],
 "constituency"   => $values["Constituency"]

               
            )
    );
}
scraperwiki::sqlitecommit();


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);
    $rightcolumn = $localdom->find("div[class=politician-sidebar]");
    $contents = explode("<p>",$rightcolumn[0]->innertext); 
$local = explode("<br />",$contents[4]->innertext);
//$contactarray = explode("<br />",$contents[1]);
//$contact = $contactarray[0]; # 
print $contents[0];
print_r($contents);

$emailchunk = $contents[2]; #->innertext;
$emailarray = explode("<br />",$emailchunk);
//$email = $contact->href;
//print_r($emailarray);
$email = $emailarray[0]; #->find("div[class=image]");
 //$email = $email->innertext;
$email = strip_tags($email); //
//print $emailarray[0];

//$image = $contents[0]->find("div[class=image] img",0);
// $imagecell = $row->find("td img",0);
 //   $image = "http://www.dublincity.ie" .$imagecell->src;
print_r($contents);
$image = $contents[0]->src;
print "\n" . "image" . $image;
print_r($image);
$localaddress = $contents[4];
$localaddress = explode("<br />",$localaddress);
$localaddress = $localaddress[0];
$localaddress = strip_tags($localaddress); 
$constituency = $contents[3];


$constituency = explode("</p>",$constituency);
$constituency = strip_tags($constituency[0]); 
$image = "http://www.finegael.ie" . $contents[0]->src;

$addressarray = explode("<br />",$contents[1]);
print_r($addressarray);
$address = trim($addressarray[0]); 
$address = strip_tags($address); 
$phone = trim(str_replace("Telephone: ","",strip_tags($addressarray[1]))); 

    $moredetails = array();    

    $moredetails["address"] = $address;
    $moredetails["email"] = $email;
    $moredetails["phone"] = $phone;
  $moredetails["localaddress"] = $localaddress;
 $moredetails["constituency"] = $constituency;
   $moredetails["image"] = $image;
  //  unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);
}
?>
