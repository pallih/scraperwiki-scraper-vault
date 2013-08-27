<?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1239";
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
print "minute";
print $minute[0];
print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);

$question = $cllrbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));


print "question" . $question. "\n";
#print "\n" . "minutesbits" . $minutebits . "\n" ; 
print "cllrbit";
print_r($cllrbit);
$cllrq = $cllrbit[0];
$cllrq = strip_tags($cllrq);
#$cllrq = trim(str_replace('Question:','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));

$cllrq = trim(str_replace(', seconded by ',';',$cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim($cllrq);
$cllrq = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $cllrq );
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace(':','',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
print "cllrq" . $cllrq . "\n";
$following = array("\n\n","\r\n","\n","Following discussion the motion was ","Following discussion the report was ");

$reply = $minutesbit[1];
$reply = trim(strip_tags($reply));
#$question = trim(str_replace('&nbsp;','',$question));

$haystack = $minute[0];
$needle = "Reply:";
$reply = get_phrase_after_string($haystack,$needle);

$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));


$response = $minutesbit[2];
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace($following,'',$response));
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
else if ( substr($cllrq,0,9) == "Question")
{
$qtype = "question";
}

else if ( substr($cllrq,0,8) == "Question")
{
$qtype = "question8";
}
else if ( substr($cllrq,1,18) == "To ask the Manager")
{
$qtype = "question17";
}
else if ( substr($cllrq,1,19) == "To ask the Manager")
{
$qtype = "question19";
}
else {
$qtype = "questionb";
}
print "qtype" . $qtype. "\n";
$questionarray = explode("Question:",$minute[0]);

print "\n" . "$questionarray[1]" . $questionarray[1] ."\n";
$cllrq = trim(str_replace('It was proposed by ','',$cllrq));
if ( $qtype == "question" || $qtype == "question17" || $qtype == "question19"  || $qtype == "question8" )
{
print "\n" . "yes";
$questionarray = explode("To ask the Manager",$minute[0]);
$questionbit = $questionarray[1];
$question = $questionarray[1];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));


$questionarray = explode("Reply",$question);
$question =  $questionarray[0];


print "\n" . "questionarray" . $questionarray[1];
#$needle = "Question:";
#$haystack = $questionbit;

#$question = get_phrase_after_string($haystack,$needle);
#$managerread = array("\n\n","\r\n","\n","The following report by the Manager was READ:-");
print "\n" . "questionfunction" . $question . "\n";
#$question = "questioncheck";
#$question = trim(str_replace($managerread,'',$question));
}
elseif ( $qtype == "motion" || $qtype == "questionb" ) {
$string = $cllrbit[1];
$end = "Following";
$start = "That ";
$question  = get_string($string, $start, $end);
$questionarray = explode("The following",$question);
print "question" . $question . "\n";
$question =  $questionarray[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
/*else {

$question = $cllrbit[1];
$question = trim(strip_tags($question));
#$reply = "replyblaa";
}
*/
if (( $qtype == "motion" ) && ($question == "")) {
$string = $minute;
$end = "Following";
$start = "That ";
$question  = get_string($string, $start, $end);
$questionarray = explode("The following",$question);
print "question" . $question . "\n";
$question =  $questionarray[0];
print "questionarray[1]" . $questionarray[1]. "\n";
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}

if (( $qtype == "motion" ) && ($response == "")) {
$string = $minute;
$end = ".</div>";
$start = "Following discussion the motion was ";
$response  = get_string($string, $start, $end);
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace('&rsquo;','\'',$response));
$response = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$response))));


}
if ( $question == "Reply:" ) {
$haystack = $minute;

$needle = "Reply:";
$question  = get_phrase_after_string($haystack,$needle);
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}


if (( $qtype == "motion" ) && ($reply == "")) {

$haystack = $minute[0];
$needle = "The following report by the Manager was READ:-";
$reply = get_phrase_after_string($haystack,$needle);
print "replytest" . $reply . "\n";
$reply = $cllrbit[2];
$reply = trim(strip_tags($reply));
$reply = trim(str_replace('&nbsp;','',$reply));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
}



if (( $qtype == "motion" ) && ($response == "")) {

$haystack = $minute[0];
$needle = "Following discussion";
$response = get_phrase_after_string($haystack,$needle);
print "responsetest" . $response . "\n";
#$reply = $cllrbit[2];
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace('&rsquo;','\'',$response));
$response = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$response))));
}

if (( $qtype == "introduction" ) && ($question == "")) {

$question = $minutesbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
if (( $qtype == "motion" ) && ($question == "")) {

$question = $minutesbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));

}
if (  ( $qtype == "introduction" ) || ( $qtype == "motion" ) && ($reply == "")) {

$reply = $minutesbit[1];
$reply = trim(strip_tags($reply));

$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));

}

#print "reply" . $reply . "\n";

/*
$searchValue = "Reply:";
#$key = array_search($searchValue, $minutesbits);
#$key;

#print "key" . $key . "\n";
#$searchValue = "cherry";

for($i=0; $i< count($minutesbit); $i++) {
   if($minutesbit[$i] == $searchValue) return $i;
}
print "i" . $i . "\n";
$reply = $minutesbit[$i+1];
#$reply = $minutesbits[$key+1];
*/
$reply = strip_tags($reply);
$reply = str_replace('&nbsp;','',$reply);
#print "reply" . $reply . "\n";


$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
#print "\n" . "minuntebit3" . $minutesbit[3] . "\n";


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
                
                //matches $needle until hits a \n or \r
                if(preg_match("#$needle([^\r\n]+)#i", $haystack, $match)) #preg_quote
                {
                        //length of matched text
                        $rsp = strlen($match[0]);
                        
                        //determine what to remove
                        $back = $rsp - $len;
                        
                        return trim(substr($match[0],- $back));
                }
        }
#}
?><?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1239";
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
print "minute";
print $minute[0];
print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);

$question = $cllrbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));


print "question" . $question. "\n";
#print "\n" . "minutesbits" . $minutebits . "\n" ; 
print "cllrbit";
print_r($cllrbit);
$cllrq = $cllrbit[0];
$cllrq = strip_tags($cllrq);
#$cllrq = trim(str_replace('Question:','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));

$cllrq = trim(str_replace(', seconded by ',';',$cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim($cllrq);
$cllrq = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $cllrq );
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace(':','',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
print "cllrq" . $cllrq . "\n";
$following = array("\n\n","\r\n","\n","Following discussion the motion was ","Following discussion the report was ");

$reply = $minutesbit[1];
$reply = trim(strip_tags($reply));
#$question = trim(str_replace('&nbsp;','',$question));

$haystack = $minute[0];
$needle = "Reply:";
$reply = get_phrase_after_string($haystack,$needle);

$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));


$response = $minutesbit[2];
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace($following,'',$response));
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
else if ( substr($cllrq,0,9) == "Question")
{
$qtype = "question";
}

else if ( substr($cllrq,0,8) == "Question")
{
$qtype = "question8";
}
else if ( substr($cllrq,1,18) == "To ask the Manager")
{
$qtype = "question17";
}
else if ( substr($cllrq,1,19) == "To ask the Manager")
{
$qtype = "question19";
}
else {
$qtype = "questionb";
}
print "qtype" . $qtype. "\n";
$questionarray = explode("Question:",$minute[0]);

print "\n" . "$questionarray[1]" . $questionarray[1] ."\n";
$cllrq = trim(str_replace('It was proposed by ','',$cllrq));
if ( $qtype == "question" || $qtype == "question17" || $qtype == "question19"  || $qtype == "question8" )
{
print "\n" . "yes";
$questionarray = explode("To ask the Manager",$minute[0]);
$questionbit = $questionarray[1];
$question = $questionarray[1];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));


$questionarray = explode("Reply",$question);
$question =  $questionarray[0];


print "\n" . "questionarray" . $questionarray[1];
#$needle = "Question:";
#$haystack = $questionbit;

#$question = get_phrase_after_string($haystack,$needle);
#$managerread = array("\n\n","\r\n","\n","The following report by the Manager was READ:-");
print "\n" . "questionfunction" . $question . "\n";
#$question = "questioncheck";
#$question = trim(str_replace($managerread,'',$question));
}
elseif ( $qtype == "motion" || $qtype == "questionb" ) {
$string = $cllrbit[1];
$end = "Following";
$start = "That ";
$question  = get_string($string, $start, $end);
$questionarray = explode("The following",$question);
print "question" . $question . "\n";
$question =  $questionarray[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
/*else {

$question = $cllrbit[1];
$question = trim(strip_tags($question));
#$reply = "replyblaa";
}
*/
if (( $qtype == "motion" ) && ($question == "")) {
$string = $minute;
$end = "Following";
$start = "That ";
$question  = get_string($string, $start, $end);
$questionarray = explode("The following",$question);
print "question" . $question . "\n";
$question =  $questionarray[0];
print "questionarray[1]" . $questionarray[1]. "\n";
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}

if (( $qtype == "motion" ) && ($response == "")) {
$string = $minute;
$end = ".</div>";
$start = "Following discussion the motion was ";
$response  = get_string($string, $start, $end);
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace('&rsquo;','\'',$response));
$response = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$response))));


}
if ( $question == "Reply:" ) {
$haystack = $minute;

$needle = "Reply:";
$question  = get_phrase_after_string($haystack,$needle);
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}


if (( $qtype == "motion" ) && ($reply == "")) {

$haystack = $minute[0];
$needle = "The following report by the Manager was READ:-";
$reply = get_phrase_after_string($haystack,$needle);
print "replytest" . $reply . "\n";
$reply = $cllrbit[2];
$reply = trim(strip_tags($reply));
$reply = trim(str_replace('&nbsp;','',$reply));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
}



if (( $qtype == "motion" ) && ($response == "")) {

$haystack = $minute[0];
$needle = "Following discussion";
$response = get_phrase_after_string($haystack,$needle);
print "responsetest" . $response . "\n";
#$reply = $cllrbit[2];
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace('&rsquo;','\'',$response));
$response = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$response))));
}

if (( $qtype == "introduction" ) && ($question == "")) {

$question = $minutesbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
if (( $qtype == "motion" ) && ($question == "")) {

$question = $minutesbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));

}
if (  ( $qtype == "introduction" ) || ( $qtype == "motion" ) && ($reply == "")) {

$reply = $minutesbit[1];
$reply = trim(strip_tags($reply));

$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));

}

#print "reply" . $reply . "\n";

/*
$searchValue = "Reply:";
#$key = array_search($searchValue, $minutesbits);
#$key;

#print "key" . $key . "\n";
#$searchValue = "cherry";

for($i=0; $i< count($minutesbit); $i++) {
   if($minutesbit[$i] == $searchValue) return $i;
}
print "i" . $i . "\n";
$reply = $minutesbit[$i+1];
#$reply = $minutesbits[$key+1];
*/
$reply = strip_tags($reply);
$reply = str_replace('&nbsp;','',$reply);
#print "reply" . $reply . "\n";


$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
#print "\n" . "minuntebit3" . $minutesbit[3] . "\n";


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
                
                //matches $needle until hits a \n or \r
                if(preg_match("#$needle([^\r\n]+)#i", $haystack, $match)) #preg_quote
                {
                        //length of matched text
                        $rsp = strlen($match[0]);
                        
                        //determine what to remove
                        $back = $rsp - $len;
                        
                        return trim(substr($match[0],- $back));
                }
        }
#}
?><?php

$council = "Fingal County Council";
$uri = "http://www.fingalcoco.ie/minutes/meeting_items.aspx?id=1239";
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
print "minute";
print $minute[0];
print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);

$question = $cllrbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));


print "question" . $question. "\n";
#print "\n" . "minutesbits" . $minutebits . "\n" ; 
print "cllrbit";
print_r($cllrbit);
$cllrq = $cllrbit[0];
$cllrq = strip_tags($cllrq);
#$cllrq = trim(str_replace('Question:','',$cllrq));
$cllrq = trim(str_replace('&nbsp;','',$cllrq));

$cllrq = trim(str_replace(', seconded by ',';',$cllrq));
$cllrq = trim(str_replace('Councillor ','',$cllrq));
$cllrq = trim($cllrq);
$cllrq = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $cllrq );
$cllrq = trim(str_replace('&rsquo;','\'',$cllrq));
$cllrq = trim(str_replace(':','',$cllrq));
$cllrq = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$cllrq))));
print "cllrq" . $cllrq . "\n";
$following = array("\n\n","\r\n","\n","Following discussion the motion was ","Following discussion the report was ");

$reply = $minutesbit[1];
$reply = trim(strip_tags($reply));
#$question = trim(str_replace('&nbsp;','',$question));

$haystack = $minute[0];
$needle = "Reply:";
$reply = get_phrase_after_string($haystack,$needle);

$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));


$response = $minutesbit[2];
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace($following,'',$response));
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
else if ( substr($cllrq,0,9) == "Question")
{
$qtype = "question";
}

else if ( substr($cllrq,0,8) == "Question")
{
$qtype = "question8";
}
else if ( substr($cllrq,1,18) == "To ask the Manager")
{
$qtype = "question17";
}
else if ( substr($cllrq,1,19) == "To ask the Manager")
{
$qtype = "question19";
}
else {
$qtype = "questionb";
}
print "qtype" . $qtype. "\n";
$questionarray = explode("Question:",$minute[0]);

print "\n" . "$questionarray[1]" . $questionarray[1] ."\n";
$cllrq = trim(str_replace('It was proposed by ','',$cllrq));
if ( $qtype == "question" || $qtype == "question17" || $qtype == "question19"  || $qtype == "question8" )
{
print "\n" . "yes";
$questionarray = explode("To ask the Manager",$minute[0]);
$questionbit = $questionarray[1];
$question = $questionarray[1];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));


$questionarray = explode("Reply",$question);
$question =  $questionarray[0];


print "\n" . "questionarray" . $questionarray[1];
#$needle = "Question:";
#$haystack = $questionbit;

#$question = get_phrase_after_string($haystack,$needle);
#$managerread = array("\n\n","\r\n","\n","The following report by the Manager was READ:-");
print "\n" . "questionfunction" . $question . "\n";
#$question = "questioncheck";
#$question = trim(str_replace($managerread,'',$question));
}
elseif ( $qtype == "motion" || $qtype == "questionb" ) {
$string = $cllrbit[1];
$end = "Following";
$start = "That ";
$question  = get_string($string, $start, $end);
$questionarray = explode("The following",$question);
print "question" . $question . "\n";
$question =  $questionarray[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
/*else {

$question = $cllrbit[1];
$question = trim(strip_tags($question));
#$reply = "replyblaa";
}
*/
if (( $qtype == "motion" ) && ($question == "")) {
$string = $minute;
$end = "Following";
$start = "That ";
$question  = get_string($string, $start, $end);
$questionarray = explode("The following",$question);
print "question" . $question . "\n";
$question =  $questionarray[0];
print "questionarray[1]" . $questionarray[1]. "\n";
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}

if (( $qtype == "motion" ) && ($response == "")) {
$string = $minute;
$end = ".</div>";
$start = "Following discussion the motion was ";
$response  = get_string($string, $start, $end);
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace('&rsquo;','\'',$response));
$response = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$response))));


}
if ( $question == "Reply:" ) {
$haystack = $minute;

$needle = "Reply:";
$question  = get_phrase_after_string($haystack,$needle);
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}


if (( $qtype == "motion" ) && ($reply == "")) {

$haystack = $minute[0];
$needle = "The following report by the Manager was READ:-";
$reply = get_phrase_after_string($haystack,$needle);
print "replytest" . $reply . "\n";
$reply = $cllrbit[2];
$reply = trim(strip_tags($reply));
$reply = trim(str_replace('&nbsp;','',$reply));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
}



if (( $qtype == "motion" ) && ($response == "")) {

$haystack = $minute[0];
$needle = "Following discussion";
$response = get_phrase_after_string($haystack,$needle);
print "responsetest" . $response . "\n";
#$reply = $cllrbit[2];
$response = trim(strip_tags($response));
$response = trim(str_replace('&nbsp;','',$response));
$response = trim(str_replace('&rsquo;','\'',$response));
$response = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$response))));
}

if (( $qtype == "introduction" ) && ($question == "")) {

$question = $minutesbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));
}
if (( $qtype == "motion" ) && ($question == "")) {

$question = $minutesbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));

}
if (  ( $qtype == "introduction" ) || ( $qtype == "motion" ) && ($reply == "")) {

$reply = $minutesbit[1];
$reply = trim(strip_tags($reply));

$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));

}

#print "reply" . $reply . "\n";

/*
$searchValue = "Reply:";
#$key = array_search($searchValue, $minutesbits);
#$key;

#print "key" . $key . "\n";
#$searchValue = "cherry";

for($i=0; $i< count($minutesbit); $i++) {
   if($minutesbit[$i] == $searchValue) return $i;
}
print "i" . $i . "\n";
$reply = $minutesbit[$i+1];
#$reply = $minutesbits[$key+1];
*/
$reply = strip_tags($reply);
$reply = str_replace('&nbsp;','',$reply);
#print "reply" . $reply . "\n";


$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));
#print "\n" . "minuntebit3" . $minutesbit[3] . "\n";


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
                
                //matches $needle until hits a \n or \r
                if(preg_match("#$needle([^\r\n]+)#i", $haystack, $match)) #preg_quote
                {
                        //length of matched text
                        $rsp = strlen($match[0]);
                        
                        //determine what to remove
                        $back = $rsp - $len;
                        
                        return trim(substr($match[0],- $back));
                }
        }
#}
?>