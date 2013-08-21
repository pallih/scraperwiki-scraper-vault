<?php

$council = "Foo Bar county Council";
$uri = "http://path/";
$html = scraperwiki::scrape($uri);

$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

/* Do your stuff here */



/*

Current scrapers construct a 2D array of this type:

$councillors["Joe Bloggs"] = array(
                    "LEA"     => "Name of Local Electoral Area",
                    "Party"   => "Monster Raving Loony Party",
                    "Email"   => "councillor@example.com",
                    "Phone"   => "01 100 1000",
                    "Mobile"  => "085 000 0000",
                    "Image"   => "http://URI",
                    "Address" => "Postal Address as string"
                    );

*No* titles on names, please.

...in order to populate the table whose SQL is constructed below.  
Please keep the table format in tact because a "parent" scraper 
will hoof your data into a combined table.

*/

scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `lea` string, `name` string, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
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
?>