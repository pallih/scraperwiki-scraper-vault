<?php

$scrapers = array(
    'iecouncillorsdublincitycouncil',
    /*'iecouncillorscorkcitycouncil',*/
    'iecouncillorsfingalcountycouncil',
    'iecouncillorsphptemplatecavan2',
    );

scraperwiki::sqliteexecute("create table if not exists councillors 
    (`auth` string, 
     `lea` string, 
     `name` string,
     `party` string,
     `email` string,
     `phone` text,
     `mobile` text,
     `image` string,
     `address` string
    )");
scraperwiki::sqliteexecute("delete from councillors");
scraperwiki::sqlitecommit();


foreach($scrapers as $scraper) {
    scraperwiki::attach($scraper);
    $data = scraperwiki::select("* from $scraper.councillors");
    scraperwiki::attach("iecouncillorsall");
    foreach($data as $councillor) {
        scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
                    array(  "auth"    => $councillor["auth"],
                            "lea"     => $councillor["lea"],
                            "name"    => $councillor["name"],
                            "party"   => $councillor["party"],
                            "email"   => $councillor["email"],
                            "phone"   => $councillor["phone"],
                            "mobile"  => $councillor["mobile"],
                            "image"   => $councillor["image"],
                            "address" => $councillor["address"]
                    )
            );        
        }
    }

scraperwiki::sqlitecommit();

?><?php

$scrapers = array(
    'iecouncillorsdublincitycouncil',
    /*'iecouncillorscorkcitycouncil',*/
    'iecouncillorsfingalcountycouncil',
    'iecouncillorsphptemplatecavan2',
    );

scraperwiki::sqliteexecute("create table if not exists councillors 
    (`auth` string, 
     `lea` string, 
     `name` string,
     `party` string,
     `email` string,
     `phone` text,
     `mobile` text,
     `image` string,
     `address` string
    )");
scraperwiki::sqliteexecute("delete from councillors");
scraperwiki::sqlitecommit();


foreach($scrapers as $scraper) {
    scraperwiki::attach($scraper);
    $data = scraperwiki::select("* from $scraper.councillors");
    scraperwiki::attach("iecouncillorsall");
    foreach($data as $councillor) {
        scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
                    array(  "auth"    => $councillor["auth"],
                            "lea"     => $councillor["lea"],
                            "name"    => $councillor["name"],
                            "party"   => $councillor["party"],
                            "email"   => $councillor["email"],
                            "phone"   => $councillor["phone"],
                            "mobile"  => $councillor["mobile"],
                            "image"   => $councillor["image"],
                            "address" => $councillor["address"]
                    )
            );        
        }
    }

scraperwiki::sqlitecommit();

?>