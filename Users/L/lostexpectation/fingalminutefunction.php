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
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string, `response` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype, :response)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
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
print "\n" . "url". $url . "\n";
#$rows=$localdom->find("div[id=data1] table tr");

#print "\n" . "urltravelled" . $url . "\n";

#foreach($rows as $row) {
    
#$heading = $localdom->find("span[id=dateheld1]");
#$heading = strip_tags($heading);
print $localdom;
$minute = $localdom->find("span[id=doctext]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");
print "minute0";
print $minute[0];
print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);



#substr

# cllrq

$string = $minute[0];
$start = "Question:";
$end = "</b></div>";
$cllrq = get_string($string, $start, $end);
$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
$cllrq = trim($cllrq);
print "cllrq". $cllrq . "\n";
#replytest

#$haystack = $minute[0];
#$needle = "Question:";
#$cllrq = get_phrase_after_string($haystack,$needle);
if ( ($cllrq == "")) {

$string = $minute[0];
$start = "It was proposed by";
$end = "</div>";

$cllrq = get_string($string, $start, $end);
$startstring = get_string($string, $start, $end);

$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
print "cllrq". $cllrq . "\n";
}

#question
#$startstring = $cllrq . ":";
print "startstring". $startstring . "\n";
$string = $minute[0];
$start = $startstring;
$end = "</";

$question = get_string($string, $start, $end);
print "question". $question . "\n";
#$haystack;
#$needle;
#$question = get_phrase_after_string($haystack,$needle);

/*
if ( ($question == "")) {
$string = $minute;
$end = "Following";
$start = "That ";
$question = get_string($string, $start, $end);
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
*/

#replytest

$haystack = $minute[0];
$needle = "Reply:";
$reply = get_phrase_after_string($haystack,$needle);

/*
# reply
$string = $minute[0];
$start = "Reply:";
$end = ".";
$reply = get_string($string, $start, $end);
*/

$reply = trim(strip_tags($reply));
$reply = trim(str_replace('&nbsp;','',$reply));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "reply". $reply . "\n";

  #  $question = "question";

  #  $cllrq = "cllrq";
     $qtype = "qtype";
  $response = "response";

    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;
  $moredetails["response"] = $response;
   # unset($cllrq,$reply,$question);
  
    return($moredetails);

}

function getInnerSubstring($string,$delim){
    // "foo a foo" becomes: array(""," a ","")
    $string = explode($delim, $string, 3); // also, we only need 2 items at most
    // we check whether the 2nd is set and return it, otherwise we return an empty string
    return isset($string[1]) ? $string[1] : '';
}


function get_string($string, $start, $end){
 $string = " ".$string;
 $pos = strpos($string,$start);
 if ($pos == 0) return "";
 $pos += strlen($start);
 $len = strpos($string,$end,$pos) - $pos;
 return substr($string,$pos,$len);
}




function get_phrase_after_string($haystack,$needle)
        {
                //length of needle
                $len = strlen($needle);
                print "len". $len . "\n";
                //matches $needle until hits a \n or \r
                if(preg_match("#$needle([^\r\n]+)#i", $haystack, $match)) #preg_quote
                {
                        //length of matched text
                        $rsp = strlen($match[0]);
                        print "match[0]". $match[0] . "\n";
                        print "rsp". $rsp . "\n";
                        //determine what to remove
                        $back = $rsp - $len;
                        print "back". $back . "\n";
                        return trim(substr($match[0],- $back));
                }
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
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string, `response` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype, :response)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
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
print "\n" . "url". $url . "\n";
#$rows=$localdom->find("div[id=data1] table tr");

#print "\n" . "urltravelled" . $url . "\n";

#foreach($rows as $row) {
    
#$heading = $localdom->find("span[id=dateheld1]");
#$heading = strip_tags($heading);
print $localdom;
$minute = $localdom->find("span[id=doctext]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");
print "minute0";
print $minute[0];
print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);



#substr

# cllrq

$string = $minute[0];
$start = "Question:";
$end = "</b></div>";
$cllrq = get_string($string, $start, $end);
$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
$cllrq = trim($cllrq);
print "cllrq". $cllrq . "\n";
#replytest

#$haystack = $minute[0];
#$needle = "Question:";
#$cllrq = get_phrase_after_string($haystack,$needle);
if ( ($cllrq == "")) {

$string = $minute[0];
$start = "It was proposed by";
$end = "</div>";

$cllrq = get_string($string, $start, $end);
$startstring = get_string($string, $start, $end);

$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
print "cllrq". $cllrq . "\n";
}

#question
#$startstring = $cllrq . ":";
print "startstring". $startstring . "\n";
$string = $minute[0];
$start = $startstring;
$end = "</";

$question = get_string($string, $start, $end);
print "question". $question . "\n";
#$haystack;
#$needle;
#$question = get_phrase_after_string($haystack,$needle);

/*
if ( ($question == "")) {
$string = $minute;
$end = "Following";
$start = "That ";
$question = get_string($string, $start, $end);
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
*/

#replytest

$haystack = $minute[0];
$needle = "Reply:";
$reply = get_phrase_after_string($haystack,$needle);

/*
# reply
$string = $minute[0];
$start = "Reply:";
$end = ".";
$reply = get_string($string, $start, $end);
*/

$reply = trim(strip_tags($reply));
$reply = trim(str_replace('&nbsp;','',$reply));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "reply". $reply . "\n";

  #  $question = "question";

  #  $cllrq = "cllrq";
     $qtype = "qtype";
  $response = "response";

    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;
  $moredetails["response"] = $response;
   # unset($cllrq,$reply,$question);
  
    return($moredetails);

}

function getInnerSubstring($string,$delim){
    // "foo a foo" becomes: array(""," a ","")
    $string = explode($delim, $string, 3); // also, we only need 2 items at most
    // we check whether the 2nd is set and return it, otherwise we return an empty string
    return isset($string[1]) ? $string[1] : '';
}


function get_string($string, $start, $end){
 $string = " ".$string;
 $pos = strpos($string,$start);
 if ($pos == 0) return "";
 $pos += strlen($start);
 $len = strpos($string,$end,$pos) - $pos;
 return substr($string,$pos,$len);
}




function get_phrase_after_string($haystack,$needle)
        {
                //length of needle
                $len = strlen($needle);
                print "len". $len . "\n";
                //matches $needle until hits a \n or \r
                if(preg_match("#$needle([^\r\n]+)#i", $haystack, $match)) #preg_quote
                {
                        //length of matched text
                        $rsp = strlen($match[0]);
                        print "match[0]". $match[0] . "\n";
                        print "rsp". $rsp . "\n";
                        //determine what to remove
                        $back = $rsp - $len;
                        print "back". $back . "\n";
                        return trim(substr($match[0],- $back));
                }
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
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string, `response` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype, :response)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
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
print "\n" . "url". $url . "\n";
#$rows=$localdom->find("div[id=data1] table tr");

#print "\n" . "urltravelled" . $url . "\n";

#foreach($rows as $row) {
    
#$heading = $localdom->find("span[id=dateheld1]");
#$heading = strip_tags($heading);
print $localdom;
$minute = $localdom->find("span[id=doctext]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");
print "minute0";
print $minute[0];
print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);



#substr

# cllrq

$string = $minute[0];
$start = "Question:";
$end = "</b></div>";
$cllrq = get_string($string, $start, $end);
$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
$cllrq = trim($cllrq);
print "cllrq". $cllrq . "\n";
#replytest

#$haystack = $minute[0];
#$needle = "Question:";
#$cllrq = get_phrase_after_string($haystack,$needle);
if ( ($cllrq == "")) {

$string = $minute[0];
$start = "It was proposed by";
$end = "</div>";

$cllrq = get_string($string, $start, $end);
$startstring = get_string($string, $start, $end);

$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
print "cllrq". $cllrq . "\n";
}

#question
#$startstring = $cllrq . ":";
print "startstring". $startstring . "\n";
$string = $minute[0];
$start = $startstring;
$end = "</";

$question = get_string($string, $start, $end);
print "question". $question . "\n";
#$haystack;
#$needle;
#$question = get_phrase_after_string($haystack,$needle);

/*
if ( ($question == "")) {
$string = $minute;
$end = "Following";
$start = "That ";
$question = get_string($string, $start, $end);
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
*/

#replytest

$haystack = $minute[0];
$needle = "Reply:";
$reply = get_phrase_after_string($haystack,$needle);

/*
# reply
$string = $minute[0];
$start = "Reply:";
$end = ".";
$reply = get_string($string, $start, $end);
*/

$reply = trim(strip_tags($reply));
$reply = trim(str_replace('&nbsp;','',$reply));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "reply". $reply . "\n";

  #  $question = "question";

  #  $cllrq = "cllrq";
     $qtype = "qtype";
  $response = "response";

    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;
  $moredetails["response"] = $response;
   # unset($cllrq,$reply,$question);
  
    return($moredetails);

}

function getInnerSubstring($string,$delim){
    // "foo a foo" becomes: array(""," a ","")
    $string = explode($delim, $string, 3); // also, we only need 2 items at most
    // we check whether the 2nd is set and return it, otherwise we return an empty string
    return isset($string[1]) ? $string[1] : '';
}


function get_string($string, $start, $end){
 $string = " ".$string;
 $pos = strpos($string,$start);
 if ($pos == 0) return "";
 $pos += strlen($start);
 $len = strpos($string,$end,$pos) - $pos;
 return substr($string,$pos,$len);
}




function get_phrase_after_string($haystack,$needle)
        {
                //length of needle
                $len = strlen($needle);
                print "len". $len . "\n";
                //matches $needle until hits a \n or \r
                if(preg_match("#$needle([^\r\n]+)#i", $haystack, $match)) #preg_quote
                {
                        //length of matched text
                        $rsp = strlen($match[0]);
                        print "match[0]". $match[0] . "\n";
                        print "rsp". $rsp . "\n";
                        //determine what to remove
                        $back = $rsp - $len;
                        print "back". $back . "\n";
                        return trim(substr($match[0],- $back));
                }
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
scraperwiki::sqliteexecute("create table if not exists councillors (`authority` string, `name` string, `url` string, `reply` string, `question` string, `cllrq` string, `qtype` string, `response` string)"); #, `party` string, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();



foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :name, :url, :reply, :question, :cllrq, :qtype, :response)",  #, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => $council, 
                #    "lea"     => $values["LEA"],
                    "name"    => $name, #, 
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
print "\n" . "url". $url . "\n";
#$rows=$localdom->find("div[id=data1] table tr");

#print "\n" . "urltravelled" . $url . "\n";

#foreach($rows as $row) {
    
#$heading = $localdom->find("span[id=dateheld1]");
#$heading = strip_tags($heading);
print $localdom;
$minute = $localdom->find("span[id=doctext]");   #("span[id=doctext]");
print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");
print "minute0";
print $minute[0];
print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);



#substr

# cllrq

$string = $minute[0];
$start = "Question:";
$end = "</b></div>";
$cllrq = get_string($string, $start, $end);
$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
$cllrq = trim($cllrq);
print "cllrq". $cllrq . "\n";
#replytest

#$haystack = $minute[0];
#$needle = "Question:";
#$cllrq = get_phrase_after_string($haystack,$needle);
if ( ($cllrq == "")) {

$string = $minute[0];
$start = "It was proposed by";
$end = "</div>";

$cllrq = get_string($string, $start, $end);
$startstring = get_string($string, $start, $end);

$cllrq = trim(strip_tags($cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
print "cllrq". $cllrq . "\n";
}

#question
#$startstring = $cllrq . ":";
print "startstring". $startstring . "\n";
$string = $minute[0];
$start = $startstring;
$end = "</";

$question = get_string($string, $start, $end);
print "question". $question . "\n";
#$haystack;
#$needle;
#$question = get_phrase_after_string($haystack,$needle);

/*
if ( ($question == "")) {
$string = $minute;
$end = "Following";
$start = "That ";
$question = get_string($string, $start, $end);
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
*/

#replytest

$haystack = $minute[0];
$needle = "Reply:";
$reply = get_phrase_after_string($haystack,$needle);

/*
# reply
$string = $minute[0];
$start = "Reply:";
$end = ".";
$reply = get_string($string, $start, $end);
*/

$reply = trim(strip_tags($reply));
$reply = trim(str_replace('&nbsp;','',$reply));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
print "reply". $reply . "\n";

  #  $question = "question";

  #  $cllrq = "cllrq";
     $qtype = "qtype";
  $response = "response";

    $moredetails = array();    
    $moredetails["reply"] = $reply;
    $moredetails["question"] = $question;
    $moredetails["cllrq"] = $cllrq;
     $moredetails["qtype"] = $qtype;
  $moredetails["response"] = $response;
   # unset($cllrq,$reply,$question);
  
    return($moredetails);

}

function getInnerSubstring($string,$delim){
    // "foo a foo" becomes: array(""," a ","")
    $string = explode($delim, $string, 3); // also, we only need 2 items at most
    // we check whether the 2nd is set and return it, otherwise we return an empty string
    return isset($string[1]) ? $string[1] : '';
}


function get_string($string, $start, $end){
 $string = " ".$string;
 $pos = strpos($string,$start);
 if ($pos == 0) return "";
 $pos += strlen($start);
 $len = strpos($string,$end,$pos) - $pos;
 return substr($string,$pos,$len);
}




function get_phrase_after_string($haystack,$needle)
        {
                //length of needle
                $len = strlen($needle);
                print "len". $len . "\n";
                //matches $needle until hits a \n or \r
                if(preg_match("#$needle([^\r\n]+)#i", $haystack, $match)) #preg_quote
                {
                        //length of matched text
                        $rsp = strlen($match[0]);
                        print "match[0]". $match[0] . "\n";
                        print "rsp". $rsp . "\n";
                        //determine what to remove
                        $back = $rsp - $len;
                        print "back". $back . "\n";
                        return trim(substr($match[0],- $back));
                }
        }
#}
?>