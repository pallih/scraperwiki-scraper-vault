<?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1229";
$html = scraperwiki::scrape($uri);
$uribase = "http://www.fingalcoco.ie/minutes/";
$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$rows=$dom->find("div[id=data1] table tr");

unset($rows[0]);

foreach($rows as $row) {
    $refurl = $row->find("td a",0);
#print "refurl" . $refurl;
    $titleurl = $row->find("td a",1);
 $title = $row->find("td",1);
print "\n" . "titleurl" . $titleurl;
#$name = str_replace('../../minutes/','',$name);
   # $name = trim(str_replace($namestrip,"",strip_tags($namecell)));

$name = strip_tags($titleurl);
$url = $uribase . $refurl->href;
$url = str_replace('../../minutes/','',$url);
#print "\n" . "url" . $url . "\n";
$moredetails = get_extras($url);
#print "qtypeb" . $qtype. "\n";

$councillors["$name"] = array(
                    "Url"     => $url,
        
                    "Question"   => $title,
          
                    );

}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `question` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :question)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                 
                    "question"   => $values["Question"], #,
#,
                #    "email"   => $values["Email"],
                #    "phone"   => $values["Phone"],
                #    "mobile"  => $values["Mobile"],
                #    "image"   => $values["Image"],
                #    "address" => $values["Address"],
            )
    );

}
#unset($councillors[0]);

scraperwiki::sqlitecommit();



?><?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1229";
$html = scraperwiki::scrape($uri);
$uribase = "http://www.fingalcoco.ie/minutes/";
$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$rows=$dom->find("div[id=data1] table tr");

unset($rows[0]);

foreach($rows as $row) {
    $refurl = $row->find("td a",0);
#print "refurl" . $refurl;
    $titleurl = $row->find("td a",1);
 $title = $row->find("td",1);
print "\n" . "titleurl" . $titleurl;
#$name = str_replace('../../minutes/','',$name);
   # $name = trim(str_replace($namestrip,"",strip_tags($namecell)));

$name = strip_tags($titleurl);
$url = $uribase . $refurl->href;
$url = str_replace('../../minutes/','',$url);
#print "\n" . "url" . $url . "\n";
$moredetails = get_extras($url);
#print "qtypeb" . $qtype. "\n";

$councillors["$name"] = array(
                    "Url"     => $url,
        
                    "Question"   => $title,
          
                    );

}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `question` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :question)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                 
                    "question"   => $values["Question"], #,
#,
                #    "email"   => $values["Email"],
                #    "phone"   => $values["Phone"],
                #    "mobile"  => $values["Mobile"],
                #    "image"   => $values["Image"],
                #    "address" => $values["Address"],
            )
    );

}
#unset($councillors[0]);

scraperwiki::sqlitecommit();



?><?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1229";
$html = scraperwiki::scrape($uri);
$uribase = "http://www.fingalcoco.ie/minutes/";
$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$rows=$dom->find("div[id=data1] table tr");

unset($rows[0]);

foreach($rows as $row) {
    $refurl = $row->find("td a",0);
#print "refurl" . $refurl;
    $titleurl = $row->find("td a",1);
 $title = $row->find("td",1);
print "\n" . "titleurl" . $titleurl;
#$name = str_replace('../../minutes/','',$name);
   # $name = trim(str_replace($namestrip,"",strip_tags($namecell)));

$name = strip_tags($titleurl);
$url = $uribase . $refurl->href;
$url = str_replace('../../minutes/','',$url);
#print "\n" . "url" . $url . "\n";
$moredetails = get_extras($url);
#print "qtypeb" . $qtype. "\n";

$councillors["$name"] = array(
                    "Url"     => $url,
        
                    "Question"   => $title,
          
                    );

}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `question` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :question)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                 
                    "question"   => $values["Question"], #,
#,
                #    "email"   => $values["Email"],
                #    "phone"   => $values["Phone"],
                #    "mobile"  => $values["Mobile"],
                #    "image"   => $values["Image"],
                #    "address" => $values["Address"],
            )
    );

}
#unset($councillors[0]);

scraperwiki::sqlitecommit();



?><?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1229";
$html = scraperwiki::scrape($uri);
$uribase = "http://www.fingalcoco.ie/minutes/";
$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$rows=$dom->find("div[id=data1] table tr");

unset($rows[0]);

foreach($rows as $row) {
    $refurl = $row->find("td a",0);
#print "refurl" . $refurl;
    $titleurl = $row->find("td a",1);
 $title = $row->find("td",1);
print "\n" . "titleurl" . $titleurl;
#$name = str_replace('../../minutes/','',$name);
   # $name = trim(str_replace($namestrip,"",strip_tags($namecell)));

$name = strip_tags($titleurl);
$url = $uribase . $refurl->href;
$url = str_replace('../../minutes/','',$url);
#print "\n" . "url" . $url . "\n";
$moredetails = get_extras($url);
#print "qtypeb" . $qtype. "\n";

$councillors["$name"] = array(
                    "Url"     => $url,
        
                    "Question"   => $title,
          
                    );

}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `question` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :question)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                 
                    "question"   => $values["Question"], #,
#,
                #    "email"   => $values["Email"],
                #    "phone"   => $values["Phone"],
                #    "mobile"  => $values["Mobile"],
                #    "image"   => $values["Image"],
                #    "address" => $values["Address"],
            )
    );

}
#unset($councillors[0]);

scraperwiki::sqlitecommit();



?>