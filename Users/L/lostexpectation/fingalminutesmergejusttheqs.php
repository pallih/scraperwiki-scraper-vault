<?php
$url = "http://www.fingalcoco.ie/minutes/";
$titleurl = "http://www.fingalcoco.ie/minutes/";

$meetingdetails = array();
$uribase = "http://www.fingalcoco.ie/minutes/";
require 'scraperwiki/simple_html_dom.php';

$depth = 1;
$year = "yearstart";
$committee = "committeestart";
$meetingdate = "meetingdatestart";
$title = "titlestart";
$titleurl = $titleurl;
$name     = "name";
 $url    = "url";
                 
                    $question   = "question";
         
                
  $response   = "response";



$meetings = array(
    'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl, 'name'     => $name, 'url'     => $url,
                 
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
$meetingdate = $row->find("td a",0);
$meetingdate = strip_tags($meetingdate);
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
    #    $meetingdate = $meetings["meetingdate"];
    }

    elseif ( $depth == 4 ){
        $committee = $meetings["committee"];
        #print "3committee" . $meetings["committee"];
        $year = $meetings["year"];
        #print "3year" . $meetings["year"];
     #   $meetingdate = $meetings["meetingdate"];
    }

    else {
        $committee = "committeeelse";
        $year = "yearelse";
        $meetingdate = "meetingdateelse";
    }




    $meetings = array ( 'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl,
        'name'     => $name,
                       
                 
         
             
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



























?><?php
$url = "http://www.fingalcoco.ie/minutes/";
$titleurl = "http://www.fingalcoco.ie/minutes/";

$meetingdetails = array();
$uribase = "http://www.fingalcoco.ie/minutes/";
require 'scraperwiki/simple_html_dom.php';

$depth = 1;
$year = "yearstart";
$committee = "committeestart";
$meetingdate = "meetingdatestart";
$title = "titlestart";
$titleurl = $titleurl;
$name     = "name";
 $url    = "url";
                 
                    $question   = "question";
         
                
  $response   = "response";



$meetings = array(
    'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl, 'name'     => $name, 'url'     => $url,
                 
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
$meetingdate = $row->find("td a",0);
$meetingdate = strip_tags($meetingdate);
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
    #    $meetingdate = $meetings["meetingdate"];
    }

    elseif ( $depth == 4 ){
        $committee = $meetings["committee"];
        #print "3committee" . $meetings["committee"];
        $year = $meetings["year"];
        #print "3year" . $meetings["year"];
     #   $meetingdate = $meetings["meetingdate"];
    }

    else {
        $committee = "committeeelse";
        $year = "yearelse";
        $meetingdate = "meetingdateelse";
    }




    $meetings = array ( 'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl,
        'name'     => $name,
                       
                 
         
             
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



























?><?php
$url = "http://www.fingalcoco.ie/minutes/";
$titleurl = "http://www.fingalcoco.ie/minutes/";

$meetingdetails = array();
$uribase = "http://www.fingalcoco.ie/minutes/";
require 'scraperwiki/simple_html_dom.php';

$depth = 1;
$year = "yearstart";
$committee = "committeestart";
$meetingdate = "meetingdatestart";
$title = "titlestart";
$titleurl = $titleurl;
$name     = "name";
 $url    = "url";
                 
                    $question   = "question";
         
                
  $response   = "response";



$meetings = array(
    'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl, 'name'     => $name, 'url'     => $url,
                 
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
$meetingdate = $row->find("td a",0);
$meetingdate = strip_tags($meetingdate);
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
    #    $meetingdate = $meetings["meetingdate"];
    }

    elseif ( $depth == 4 ){
        $committee = $meetings["committee"];
        #print "3committee" . $meetings["committee"];
        $year = $meetings["year"];
        #print "3year" . $meetings["year"];
     #   $meetingdate = $meetings["meetingdate"];
    }

    else {
        $committee = "committeeelse";
        $year = "yearelse";
        $meetingdate = "meetingdateelse";
    }




    $meetings = array ( 'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl,
        'name'     => $name,
                       
                 
         
             
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



























?><?php
$url = "http://www.fingalcoco.ie/minutes/";
$titleurl = "http://www.fingalcoco.ie/minutes/";

$meetingdetails = array();
$uribase = "http://www.fingalcoco.ie/minutes/";
require 'scraperwiki/simple_html_dom.php';

$depth = 1;
$year = "yearstart";
$committee = "committeestart";
$meetingdate = "meetingdatestart";
$title = "titlestart";
$titleurl = $titleurl;
$name     = "name";
 $url    = "url";
                 
                    $question   = "question";
         
                
  $response   = "response";



$meetings = array(
    'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl, 'name'     => $name, 'url'     => $url,
                 
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
$meetingdate = $row->find("td a",0);
$meetingdate = strip_tags($meetingdate);
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
    #    $meetingdate = $meetings["meetingdate"];
    }

    elseif ( $depth == 4 ){
        $committee = $meetings["committee"];
        #print "3committee" . $meetings["committee"];
        $year = $meetings["year"];
        #print "3year" . $meetings["year"];
     #   $meetingdate = $meetings["meetingdate"];
    }

    else {
        $committee = "committeeelse";
        $year = "yearelse";
        $meetingdate = "meetingdateelse";
    }




    $meetings = array ( 'depth' => $depth, 'year' => $year, 'committee' => $committee, 'meetingdate' => $meetingdate, 'title' => $title, 
                                'titleurl' => $titleurl,
        'name'     => $name,
                       
                 
         
             
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



























?>