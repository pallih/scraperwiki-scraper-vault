<?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1229";
$html = scraperwiki::scrape($uri);
$uribase = "http://www.fingalcoco.ie/minutes/";
$meetings = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

$rows=$dom->find("div[id=data] table tr");

unset($rows[0]);

foreach($rows as $row) {
    $refurl = $row->find("td a",0);
#print "refurl" . $refurl;
    $titleurl = $row->find("td a",1);
print "\n" . "titleurl" . $titleurl;
#$name = str_replace('../../minutes/','',$name);
   # $name = trim(str_replace($namestrip,"",strip_tags($namecell)));
$heading = strip_tags($titleurl);
$name = strip_tags($titleurl);
$url = $uribase . $refurl->href;
$url = str_replace('../../minutes/','',$url);
#print "\n" . "url" . $url . "\n";
$moredetails = get_extras($url);
#print "qtypeb" . $qtype. "\n";

$meetings["$year"] = array(
                    "Url"     => $url,
                    "Reply"   => $moredetails["reply"],
                    "Question"   => $moredetails["question"],
                      "Cllrq"   => $moredetails["cllrq"],
                    "Qtype"   => $moredetails["qtype"], #, #,
  "Response"   => $moredetails["response"] #, #,
                  #  "Email"   => "councillor@example.com",
                  #  "Phone"   => "01 100 1000",
                  #  "Mobile"  => "085 000 0000",
                  #  "Image"   => "http://URI",
                  #  "Address" => "Postal Address as string"
                    );

}


scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `year` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string, `response` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($meetings as $year => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :year, :url, :reply, :question, :cllrq, :qtype, :response)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "year"    => $year, #, 
                    "url"   => $values["Url"], #,
                    "reply"   => $values["Reply"], #,
                    "question"   => $values["Question"], #,
    "cllrq"   => $values["Cllrq"],
     "qtype"   => $values["Qtype"],
     "response"   => $values["Response"]#,
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




function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

$uri = "http://www.fingalcoco.ie/minutes/";

#$rows=$localdom->find("div[id=data1] table tr");

#print "\n" . "urltravelled" . $url . "\n";

#foreach($rows as $row) {
    
#$heading = $localdom->find("span[id=dateheld1]");
#$heading = strip_tags($heading);
print $localdom;
#$minute = $localdom->find("span[id=doctext]");   #("span[id=doctext]");
#print "\n" . "minute". $minute[0] . "\n";



$rows=$localdom->find("div[id=data] table tr");

unset($rows[0]);

foreach($rows as $row) {
    $refurl = $row->find("td a",0);
#print "refurl" . $refurl;
    $titleurl = $row->find("td a",1);
print "\n" . "titleurl" . $titleurl;
#$name = str_replace('../../minutes/','',$name);
   # $name = trim(str_replace($namestrip,"",strip_tags($namecell)));
$heading = strip_tags($titleurl);
$name = strip_tags($titleurl);
$url = $uribase . $refurl->href;
$url = str_replace('../../minutes/','',$url);
#print "\n" . "url" . $url . "\n";
$moredetails = get_extras($url);



    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;
  $moredetails["response"] = $response;
  
    return($moredetails);

}

#}
?>