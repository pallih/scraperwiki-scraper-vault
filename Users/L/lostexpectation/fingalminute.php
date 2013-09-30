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

$councillors["$name"] = array(
                    "Url"     => $url,
                    "Reply"   => $moredetails["reply"],
                    "Question"   => $moredetails["question"],
                      "Cllrq"   => $moredetails["cllrq"],
                    "Qtype"   => $moredetails["qtype"] #, #,
                  #  "Email"   => "councillor@example.com",
                  #  "Phone"   => "01 100 1000",
                  #  "Mobile"  => "085 000 0000",
                  #  "Image"   => "http://URI",
                  #  "Address" => "Postal Address as string"
                    );

}


scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                    "reply"   => $values["Reply"], #,
                    "question"   => $values["Question"], #,
    "cllrq"   => $values["Cllrq"],
     "qtype"   => $values["Qtype"]#,
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
$minute = $localdom->find("div[id=doc]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");

$minutesbit = explode("</div>",$minute[0]);
print "minutesbit";
print_r($minutesbit);
print "\n" . "minutesbits" . $minutebit . "\n" ; 
$minutesq = explode("<div>",$minutesbit[0]);
print "minutesq";
print_r($minutesq);
$cllrq = $minutesq[1];
$cllrq = strip_tags($cllrq);
$cllrq = trim(str_replace('Question:','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));

$cllrq = trim(str_replace(', seconded by ',';',$cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim($cllrq);
$cllrq = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $cllrq );
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace(':','',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));


$question = $minutesbit[1];
$question = trim(strip_tags($question));
$question = (str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));

if ( (substr($cllrq,0,15)) == "It was proposed")
{
$qtype = "motion";
}
else if ( substr($cllrq,0,12) == "It was NOTED")
{
$qtype = "note";
}
else if ( substr($cllrq,0,12) == "")
{
$qtype = "none";
}
else if ( substr($cllrq,0,7) == "Minutes")
{
$qtype = "introduction";
}
else {
$qtype = "question";
}
print "qtype" . $qtype. "\n";

$cllrq = trim(str_replace('It was proposed by ','',$cllrq));

$searchValue = "Reply:";
#$key = array_search($searchValue, $minutesbits);
#$key;

#print "key" . $key . "\n";
#$searchValue = "cherry";

for($i=0; $i< count($minutesbit); $i++) {
   if($minutesbit[$i] == $searchValue) return $i;
}
print "i" . $i . "\n";
$reply = $minutesbit[$i+2];
#$reply = $minutesbits[$key+1];
$reply = strip_tags($reply);
$reply = str_replace('&nbsp;','',$reply);
print "reply" . $reply . "\n";

$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "\n" . "minuntebit3" . $minutesbit[3] . "\n";


    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;

    unset($cllrq,$reply,$question);
  
    return($moredetails);

}

#}
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

$councillors["$name"] = array(
                    "Url"     => $url,
                    "Reply"   => $moredetails["reply"],
                    "Question"   => $moredetails["question"],
                      "Cllrq"   => $moredetails["cllrq"],
                    "Qtype"   => $moredetails["qtype"] #, #,
                  #  "Email"   => "councillor@example.com",
                  #  "Phone"   => "01 100 1000",
                  #  "Mobile"  => "085 000 0000",
                  #  "Image"   => "http://URI",
                  #  "Address" => "Postal Address as string"
                    );

}


scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                    "reply"   => $values["Reply"], #,
                    "question"   => $values["Question"], #,
    "cllrq"   => $values["Cllrq"],
     "qtype"   => $values["Qtype"]#,
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
$minute = $localdom->find("div[id=doc]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");

$minutesbit = explode("</div>",$minute[0]);
print "minutesbit";
print_r($minutesbit);
print "\n" . "minutesbits" . $minutebit . "\n" ; 
$minutesq = explode("<div>",$minutesbit[0]);
print "minutesq";
print_r($minutesq);
$cllrq = $minutesq[1];
$cllrq = strip_tags($cllrq);
$cllrq = trim(str_replace('Question:','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));

$cllrq = trim(str_replace(', seconded by ',';',$cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim($cllrq);
$cllrq = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $cllrq );
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace(':','',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));


$question = $minutesbit[1];
$question = trim(strip_tags($question));
$question = (str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));

if ( (substr($cllrq,0,15)) == "It was proposed")
{
$qtype = "motion";
}
else if ( substr($cllrq,0,12) == "It was NOTED")
{
$qtype = "note";
}
else if ( substr($cllrq,0,12) == "")
{
$qtype = "none";
}
else if ( substr($cllrq,0,7) == "Minutes")
{
$qtype = "introduction";
}
else {
$qtype = "question";
}
print "qtype" . $qtype. "\n";

$cllrq = trim(str_replace('It was proposed by ','',$cllrq));

$searchValue = "Reply:";
#$key = array_search($searchValue, $minutesbits);
#$key;

#print "key" . $key . "\n";
#$searchValue = "cherry";

for($i=0; $i< count($minutesbit); $i++) {
   if($minutesbit[$i] == $searchValue) return $i;
}
print "i" . $i . "\n";
$reply = $minutesbit[$i+2];
#$reply = $minutesbits[$key+1];
$reply = strip_tags($reply);
$reply = str_replace('&nbsp;','',$reply);
print "reply" . $reply . "\n";

$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "\n" . "minuntebit3" . $minutesbit[3] . "\n";


    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;

    unset($cllrq,$reply,$question);
  
    return($moredetails);

}

#}
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

$councillors["$name"] = array(
                    "Url"     => $url,
                    "Reply"   => $moredetails["reply"],
                    "Question"   => $moredetails["question"],
                      "Cllrq"   => $moredetails["cllrq"],
                    "Qtype"   => $moredetails["qtype"] #, #,
                  #  "Email"   => "councillor@example.com",
                  #  "Phone"   => "01 100 1000",
                  #  "Mobile"  => "085 000 0000",
                  #  "Image"   => "http://URI",
                  #  "Address" => "Postal Address as string"
                    );

}


scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                    "reply"   => $values["Reply"], #,
                    "question"   => $values["Question"], #,
    "cllrq"   => $values["Cllrq"],
     "qtype"   => $values["Qtype"]#,
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
$minute = $localdom->find("div[id=doc]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");

$minutesbit = explode("</div>",$minute[0]);
print "minutesbit";
print_r($minutesbit);
print "\n" . "minutesbits" . $minutebit . "\n" ; 
$minutesq = explode("<div>",$minutesbit[0]);
print "minutesq";
print_r($minutesq);
$cllrq = $minutesq[1];
$cllrq = strip_tags($cllrq);
$cllrq = trim(str_replace('Question:','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));

$cllrq = trim(str_replace(', seconded by ',';',$cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim($cllrq);
$cllrq = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $cllrq );
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace(':','',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));


$question = $minutesbit[1];
$question = trim(strip_tags($question));
$question = (str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));

if ( (substr($cllrq,0,15)) == "It was proposed")
{
$qtype = "motion";
}
else if ( substr($cllrq,0,12) == "It was NOTED")
{
$qtype = "note";
}
else if ( substr($cllrq,0,12) == "")
{
$qtype = "none";
}
else if ( substr($cllrq,0,7) == "Minutes")
{
$qtype = "introduction";
}
else {
$qtype = "question";
}
print "qtype" . $qtype. "\n";

$cllrq = trim(str_replace('It was proposed by ','',$cllrq));

$searchValue = "Reply:";
#$key = array_search($searchValue, $minutesbits);
#$key;

#print "key" . $key . "\n";
#$searchValue = "cherry";

for($i=0; $i< count($minutesbit); $i++) {
   if($minutesbit[$i] == $searchValue) return $i;
}
print "i" . $i . "\n";
$reply = $minutesbit[$i+2];
#$reply = $minutesbits[$key+1];
$reply = strip_tags($reply);
$reply = str_replace('&nbsp;','',$reply);
print "reply" . $reply . "\n";

$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "\n" . "minuntebit3" . $minutesbit[3] . "\n";


    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;

    unset($cllrq,$reply,$question);
  
    return($moredetails);

}

#}
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

$councillors["$name"] = array(
                    "Url"     => $url,
                    "Reply"   => $moredetails["reply"],
                    "Question"   => $moredetails["question"],
                      "Cllrq"   => $moredetails["cllrq"],
                    "Qtype"   => $moredetails["qtype"] #, #,
                  #  "Email"   => "councillor@example.com",
                  #  "Phone"   => "01 100 1000",
                  #  "Mobile"  => "085 000 0000",
                  #  "Image"   => "http://URI",
                  #  "Address" => "Postal Address as string"
                    );

}


scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
                    "url"   => $values["Url"], #,
                    "reply"   => $values["Reply"], #,
                    "question"   => $values["Question"], #,
    "cllrq"   => $values["Cllrq"],
     "qtype"   => $values["Qtype"]#,
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
$minute = $localdom->find("div[id=doc]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");

$minutesbit = explode("</div>",$minute[0]);
print "minutesbit";
print_r($minutesbit);
print "\n" . "minutesbits" . $minutebit . "\n" ; 
$minutesq = explode("<div>",$minutesbit[0]);
print "minutesq";
print_r($minutesq);
$cllrq = $minutesq[1];
$cllrq = strip_tags($cllrq);
$cllrq = trim(str_replace('Question:','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));

$cllrq = trim(str_replace(', seconded by ',';',$cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim($cllrq);
$cllrq = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $cllrq );
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace(':','',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));


$question = $minutesbit[1];
$question = trim(strip_tags($question));
$question = (str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));

if ( (substr($cllrq,0,15)) == "It was proposed")
{
$qtype = "motion";
}
else if ( substr($cllrq,0,12) == "It was NOTED")
{
$qtype = "note";
}
else if ( substr($cllrq,0,12) == "")
{
$qtype = "none";
}
else if ( substr($cllrq,0,7) == "Minutes")
{
$qtype = "introduction";
}
else {
$qtype = "question";
}
print "qtype" . $qtype. "\n";

$cllrq = trim(str_replace('It was proposed by ','',$cllrq));

$searchValue = "Reply:";
#$key = array_search($searchValue, $minutesbits);
#$key;

#print "key" . $key . "\n";
#$searchValue = "cherry";

for($i=0; $i< count($minutesbit); $i++) {
   if($minutesbit[$i] == $searchValue) return $i;
}
print "i" . $i . "\n";
$reply = $minutesbit[$i+2];
#$reply = $minutesbits[$key+1];
$reply = strip_tags($reply);
$reply = str_replace('&nbsp;','',$reply);
print "reply" . $reply . "\n";

$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "\n" . "minuntebit3" . $minutesbit[3] . "\n";


    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;

    unset($cllrq,$reply,$question);
  
    return($moredetails);

}

#}
?>