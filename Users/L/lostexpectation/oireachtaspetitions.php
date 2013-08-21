<?php


$uri = "http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

#http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN?openview&start=1&count=15&type=see+all+petitions&lang=EN&r=0.186617837796597


$rows=$dom->find("div[id=viewbody] table tr");
unset($rows[0]);
foreach($rows as $row) {
$refnumbercell = $row->find("td",0);
 $urlcell = $row->find("td a",0);
    $url = "http://petitions.oireachtas.ie/online_petitions.nsf" . $urlcell->href;
    $refnumber = strip_tags($refnumbercell);
    $namecellcontents = $row->find("td",1);
    $namecell = trim(strip_tags($namecellcontents->innertext));
    $name = trim(str_replace(" / ","/",trim($namecell)));
    $titlecell = $row->find("td",2);
    $title = trim($titlecell->plaintext);
    $statuscell = $row->find("td",3);
    $status = trim($statuscell->plaintext);

$councillors["$refnumber"] = array(
              "Name"   => "$name",
                    "Title"   => "$title",
                    "Status"   => "$status",
                 #   "Email"   => "councillor@example.com",
                #    "Phone"   => "01 100 1000",
                #    "Mobile"  => "085 000 0000",
                #    "Image"   => "http://URI",
                #    "Address" => "Postal Address as string"
                    );
}


scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`name` string, `refnumber` string, `title` string, `status` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:name, :refnumber, :title, :status)",  #, :email, :phone, :mobile, :image, :address)", 
            array( 
                    "name"     => $values["Name"],
                    "refnumber"    => $refnumber,
                    "title"   => $values["Title"],
                    "status"   => $values["Status"],
                #    "phone"   => $values["Phone"],
               #     "mobile"  => $values["Mobile"],
               #     "image"   => $values["Image"],
              #      "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?><?php


$uri = "http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

#http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN?openview&start=1&count=15&type=see+all+petitions&lang=EN&r=0.186617837796597


$rows=$dom->find("div[id=viewbody] table tr");
unset($rows[0]);
foreach($rows as $row) {
$refnumbercell = $row->find("td",0);
 $urlcell = $row->find("td a",0);
    $url = "http://petitions.oireachtas.ie/online_petitions.nsf" . $urlcell->href;
    $refnumber = strip_tags($refnumbercell);
    $namecellcontents = $row->find("td",1);
    $namecell = trim(strip_tags($namecellcontents->innertext));
    $name = trim(str_replace(" / ","/",trim($namecell)));
    $titlecell = $row->find("td",2);
    $title = trim($titlecell->plaintext);
    $statuscell = $row->find("td",3);
    $status = trim($statuscell->plaintext);

$councillors["$refnumber"] = array(
              "Name"   => "$name",
                    "Title"   => "$title",
                    "Status"   => "$status",
                 #   "Email"   => "councillor@example.com",
                #    "Phone"   => "01 100 1000",
                #    "Mobile"  => "085 000 0000",
                #    "Image"   => "http://URI",
                #    "Address" => "Postal Address as string"
                    );
}


scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`name` string, `refnumber` string, `title` string, `status` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:name, :refnumber, :title, :status)",  #, :email, :phone, :mobile, :image, :address)", 
            array( 
                    "name"     => $values["Name"],
                    "refnumber"    => $refnumber,
                    "title"   => $values["Title"],
                    "status"   => $values["Status"],
                #    "phone"   => $values["Phone"],
               #     "mobile"  => $values["Mobile"],
               #     "image"   => $values["Image"],
              #      "address" => $values["Address"],
            )
    );
}
scraperwiki::sqlitecommit();
?>