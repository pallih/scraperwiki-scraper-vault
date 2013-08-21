<?php
$url = "http://www.fingalcoco.ie/minutes/";
$titleurl = "http://www.fingalcoco.ie/minutes/";

$meetingdetails = array();
$uribase = "http://www.fingalcoco.ie/minutes/";
require 'scraperwiki/simple_html_dom.php';
#$meetings = array('titleurl');
$depth = 1;
$year = "yearstart";
$committee = "committeestart";
$meetingdate = "meetingdatestart";
$title = "titlestart";
$titleurl = $titleurl;
$name     = "name";
 $url    = "url";
                   $reply   = "reply";
                    $question   = "question";
                      $cllrq   = "cllrq";
                    $qtype   = "qtype";
  $response   = "response";



$meetings = array(
    'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl, 'name'     => $name, 'url'     => $url,
                    'reply'   => $reply,
                    'question'   => $question,
                      'cllrq'   => $cllrq,
                    'qtype'   => $qtype,
  'response'   => $response
);




#$dom = new simple_html_dom();
#$html = scraperwiki::scrape($titleurl);
#$dom->load($html);

/*
function findLinks($url, $depth, $maxDepth) {
  // fetch $url and parse it
  // ...
  if ($depth <= $maxDepth)
    foreach($html->find('a') as $element)
      findLinks($element->href, $depth + 1, $maxDepth);
}
*/
    $maxDepth = 4;
    $depth = 1;

    #$moredetails = 


findLinks($titleurl, $depth, $maxDepth, $meetings);



function findLinks($titleurl, $depth, $maxDepth, $meetings) {
    #static $maxDepth = 4;
    print "titleurl" . $titleurl . "\n";
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($titleurl);
    $dom->load($html);

    print "depth" . $depth ."\n";
    print "maxdepth" . $maxDepth ."\n";
    

    if ( $depth > 1 ) {
        $rows = $dom->find("div[id=data1] table tbody tr");
    }
    else {
        $rows = $dom->find("div[id=data] table tbody tr");
    }
    unset($rows[0]);

    if ($depth <= $maxDepth) {
        $count = 0;

  #      $i=0;
    
        foreach($rows as $row) {
print "row" .  "\n";

/*
            $check0 = $row->find("td a",0);
print "check0" . $check0 . "\n";
            $check1 = $row->find("td a",1);
print "check1" . $check1 . "\n";
            if ( (!empty($check0)) && (!empty($check1)) ) {
                print "both not empty" . "\n";
}
 if ( (empty($check0)) && (empty($check1)) ) {
                print "both empty" . "\n";
}
            if ( (!empty($check0)) && (!empty($check1)) ) { 
            
*/

            $uribase = "http://www.fingalcoco.ie/minutes/";
        #print "row1" . $row ."\n";
        #print "row2" . $rows[1] ."\n";

            if ( $depth > 2 ) {
                $titleurl = $row->find("td a",1);
            }
            else {
                $titleurl = $row->find("td a",0);
            }


    #$titleurl = $row->find("td a",0);
    #print "titleurl1" . $titleurl . "\n";
    #$titleurl = $row->href;
    $title = strip_tags($titleurl);
    #print "title" . $title . "\n";
    #print "titleurl2" . $titleurl . "\n";
    $titleurl = $uribase . $titleurl->href;
    $titleurl = str_replace('../../minutes/','',$titleurl);
    #$titleurl = $uribase . $titleurl;
    print "titleurl3" . $titleurl . "\n";

    #year,comittee,meetingdate,minuteref,url


    if ( $depth == 1 ) {
        $committee = "";
        $year = $title;
        $meetingdate = "";
    }
    elseif ( $depth == 2 ){
        $committee = $title;
        $year = $meetings["year"];
        #print "year" . $meetings["year"];
        $meetingdate = "";
    }

    elseif ( $depth == 3 ){
        $committee = $meetings["committee"];
        #print "3committee" . $meetings["committee"];
        $year = $meetings["year"];
        #print "3year" . $meetings["year"];
        $meetingdate = $title;
    }

    elseif ( $depth == 4 ){
        $committee = $meetings["committee"];
        #print "4committee" . $meetings["committee"];
        $year = $meetings["year"];
        #print "4year" . $meetings["year"];
        $meetingdate = $meetings["meetingdate"];
        #print "4meetingdate" . $meetings["meetingdate"];
    }

    else {
        $committee = "committeeelse";
        $year = "yearelse";
        $meetingdate = "meetingdateelse";
    }

if ( $depth == 4) {
print "yes";

#$meetingdetails = get_meetingdetails($titleurl);

$meetingdetails = get_extras($titleurl);
print "meetingdetails" . print_r($meetingdetails) . "\n";
/*
$councillors["$name"] = array(
                    "name"     => $meetingdetails["name"],
                    "Url"     => $meetingdetails["url"],
                    "Reply"   => $meetingdetails["reply"],
                    "Question"   => $meetingdetails["question"],
                      "Cllrq"   => $meetingdetails["cllrq"],
                    "Qtype"   => $meetingdetails["qtype"], #, #,
  "Response"   => $meetingdetails["response"] #, #,
                      );

#}

$name  = $councillors["name"];
                               $url     = $councillors["url"];
                    $reply   = $councillors["reply"];
                    $question   = $councillors["question"];
                      $cllrq   = $councillors["cllrq"];
                    $qtype   = $councillors["qtype"]; 
 $response   = $councillors["response"];

*/

                    $reply   = $meetingdetails["reply"];
                    $question   = $meetingdetails["question"];
                      $cllrq   = $meetingdetails["cllrq"];
                    $qtype   = $meetingdetails["qtype"]; 
 $response   = $meetingdetails["response"];

}
else 
{

 $url    = "urlelse";
                   $reply   = "replyelse";
                    $question   = "questionelse";
                      $cllrq   = "cllrqelse";
                    $qtype   = "qtypeelse";
  $response   = "responseelse";
}


    $meetings = array ( 'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl,
        'name'     => $name,
                       
                    'reply'   => $reply,
                    'question'   => $question,
                      'cllrq'   => $cllrq,
                    'qtype'   => $qtype, 
  'response'   => $response
                                 );
      scraperwiki::save(array( 'titleurl','title'), $meetings);

#}

      findLinks($titleurl, $depth + 1, $maxDepth, $meetings);

  #   }  

  #      $i++;
  #      if($i==3) break;
     }   
    }

}

#}

#scraperwiki::sqlitecommit();


function get_extras($titleurl) {
    $localhtml = scraperwiki::scrape($titleurl);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

$uri = "http://www.fingalcoco.ie/minutes/";

#$rows=$localdom->find("div[id=data1] table tr");

#print "\n" . "urltravelled" . $url . "\n";

#foreach($rows as $row) {
    
#$heading = $localdom->find("span[id=dateheld1]");
#$heading = strip_tags($heading);
#print $localdom;
$minute = $localdom->find("span[id=doctext]");   #("span[id=doctext]");
#print "\n" . "minute". $minute[0] . "\n";
#print_r($minute);

#$minutes = strip_tags($heading);
#    $nameurl2 = $row->find("td a",0);
#$name2 = strip_tags($nameurl2);
#$url2 = $uri . $nameurl2->href;
#$url2 = str_replace('../../minutes/','',$url2);

$namestrip = array("\n\n","\r\n","\n","Councillor ","Dr. ","Lord Mayor, ","Lord Mayor","Deputy ");
#print "minutes";
#print_r($minutes);
#print "\n";
$minutesbit = explode("<div>&nbsp;</div>",$minute[0]);
$cllrbit = explode("<div><b>&nbsp;</b></div>",$minute[0]);
#$questionarray = explode("<div><b>&nbsp;</b></div>",$minute[1]);
#print "minutesbit";
#print_r($minutesbit);
#print "\n";
$question = $minutesbit[0];
$question = trim(strip_tags($question));
$question = trim(str_replace('&nbsp;','',$question));
$question = trim(str_replace('&rsquo;','\'',$question));
$question = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$question))));


#print "question" . $question. "\n";
#print "\n" . "minutesbits" . $minutebits . "\n" ; 
#print "cllrbit";
#print_r($cllrbit);
$cllrq = $cllrbit[0];
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

$following = array("\n\n","\r\n","\n","Following discussion the motion was ","Following discussion the report was ");



$reply = $minutesbit[1];
$reply = trim(strip_tags($reply));
#$question = trim(str_replace('&nbsp;','',$question));
$reply = trim(str_replace('&rsquo;','\'',$reply));
$reply = trim(str_replace('&rdquo;','',(str_replace('&ldquo;','',$reply))));


$cllrq = trim(str_replace('It was proposed by ','',$cllrq));

if (substr($reply,0,6) == "Reply:" ) {
$cllrqb = $cllrbit[1];
$reply = $cllrqb;
}




$response = $minutesbit[2];
$response = strip_tags($response);
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
else {
$qtype = "question";
}
#print "qtype" . $qtype. "\n";


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
    unset($cllrq,$reply,$question);
  
    return($moredetails);

}
#}

?>