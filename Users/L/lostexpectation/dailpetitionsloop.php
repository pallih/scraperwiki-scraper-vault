<?php
require 'scraperwiki/simple_html_dom.php';
$councillors = array();


for ($i = 1; $i <= 81; $i++) {
 #   $html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/callawards.nsf/posted+awards?OpenView&Start=1&Count=1000&Expand=3.".$i);
$html = scraperWiki::scrape("http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN?openview&start=" . $i . "&count=1"); #&start=30&count=15
    $dom = new simple_html_dom();
    $dom->load($html);

   # foreach ($dom->find('a[href*=OpenDocument]') as $a) {
      $rows=$dom->find("div[id=viewbody] table tr");
unset($rows[0]);
foreach($rows as $row) {
$refnumbercell = $row->find("td",0);
$urlcell = $row->find("td a",0)->href;
#print $urlcell;
$urlcell = strip_tags($urlcell);
$urlcell = ltrim($urlcell,'.');

#print "\n" . "urlcell" . $urlcell;
    $url = "http://petitions.oireachtas.ie/online_petitions.nsf" . $urlcell; # ->href;
#print "\n" . "url" . $url;

#http://petitions.oireachtas.ie/online_petitions.nsf./Published_Petitions_EN/4B1C5516D35CB1A880257AE9005FC246?OpenDocument&type=published+petition&lang=EN&r=0.651346608682383
#http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN/70244C3CADEE670880257ABE00553093?OpenDocument&type=published+petition&lang=EN&r=0.221820401312276
    $refnumber = strip_tags($refnumbercell);
    $namecellcontents = $row->find("td",1);
    $namecell = trim(strip_tags($namecellcontents->innertext));
    $name = trim(str_replace(" / ","/",trim($namecell)));
    $titlecell = $row->find("td",2);
    $title = trim($titlecell->plaintext);
    $title = str_replace("&amp;","&",$title);
    $statuscell = $row->find("td",3);
    $status = trim($statuscell->plaintext);
        //var_dump($thisrecord['description']);
        //print mb_detect_encoding($thisrecord['description'])."\n";


    $moredetails = get_extras($url);
}
$councillors["$refnumber"] = array(
              "Url"   => "$url",
              "Name"   => "$name",
                    "Title"   => "$title",
                    "Status"   => "$status",
                 #   "Email"   => "councillor@example.com",
                #    "Phone"   => "01 100 1000",
                #    "Mobile"  => "085 000 0000",
                #    "Image"   => "http://URI",
                "Submittedby" => $moredetails["submittedby"],
     "Petitiontext" => $moredetails["petitiontext"],
     "Status1" => $moredetails["status1"],
"Status2" => $moredetails["status2"],
"Status3" => $moredetails["status3"],
     "Date1" => $moredetails["date1"],
     "Date2" => $moredetails["date2"],
 "Date3" => $moredetails["date3"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `date1` string, `date2` string, `date3` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :date1, :date2, :date3, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
            array( 
 "url"     => $values["Url"],
                    "name"     => $values["Name"],
                    "refnumber"    => $refnumber,
                    "title"   => $values["Title"],
                    "status"   => $values["Status"],
                    "submittedby"   => $values["Submittedby"],
                    "petitiontext"  => $values["Petitiontext"],
                     "status1"  => $values["Status1"],
      "status2"  => $values["Status2"],
 "status3"  => $values["Status3"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
                    "corpname"   => $values["Corpname"],
                    "published" => $values["Published"]
            )
    );
#}
}
scraperwiki::sqlitecommit();


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

    $column = $localdom->find("div[class=column-center2]");
print $url;
 #   $trows=$column->find("div[class=column-center-inner] table tr");
#print_r($column[2]);
 #  $contents = explode("</tr>",$column[0]); 
$contents = explode("</h2>",$column[0]); 
print "\n" . "contents";
print_r($contents);
 $contentbs = explode("</h2>",$contents[2]); 
print "contentbs";
print_r($contentbs);
$publishedcell = explode("<br />",$contentbs[0]); 
print "publishedcell";
print_r($publishedcell);
if (
$published = $publishedcell[1] > 0) {
$published = $publishedcell[1];
}
else {
$published = $publishedcell[1];
}
$published = trim(strip_tags($published));

$published = substr($published, 10); 
print "\n" . "published" . $published;
 $historical = explode("</tr>",$contentbs[0]); 
# $contentbs = explode("</h2>",$contents[2]); 
print "historical";
print_r($historical);
 #  $details = explode("</h2>",$contents); 
 $subtext = explode("</tr>",$contents[1]); 
#print "subtext";
#print_r($subtext);

   # foreach($rows as $row) {
#    $submittedby = $column->find("td",1);

 #   $petitiontext = $column->find("td",1); 
$namestrip = array("Corporate Name:","Unincorporated Name:","Unincorporated Association Name:");





$subtextname5 = $subtext[5];
$subtextname5 = trim(strip_tags($subtextname5));
#print "\n" . "subtextname5" . $subtextname5;

$subtextname6 = $subtext[6];
$subtextname6 = trim(strip_tags($subtextname6));
#print "\n" . "subtextname6" . $subtextname6;

$subtextname7 = $subtext[7];
$subtextname7 = trim(strip_tags($subtextname7));
#print "\n" . "subtextname7" . $subtextname7;





 if(substr($subtextname5,0,9) == "Corporate" || substr($subtextname5,0,13) == "Unincorporated" )  {
            $corpname  = $subtext[5];
print "\n" . "corpname" . $corpname;
$corpname = trim(strip_tags($corpname));
$corpname = str_replace($namestrip,"",$corpname);
}  

else  {
$corpname  = "n/a";
 }


 if(substr($subtextname5,0,8) == "Petition") {
       $petitiontext  = $subtext[5];
 $petitiontext  = "petitiontext5";
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext5cut" . $petitiontext . "\n";

}
 else if(substr($subtextname6,0,8) == "Petition") {
       $petitiontext = $subtext[6];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext6cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext6";
 $corpname  = "n/a";
}

 else if(substr($subtextname7,0,8) == "Petition") {
       $petitiontext  = $subtext[7];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext7cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext7";

}

 else {
 $submittedby  = $subtext[4];
    $submittedby = strip_tags($submittedby);
$submittedby = substr($submittedby, 13); #Submitted By:
$submittedby = "blaa";
 $corpname  = "n/a";

 $petitiontext   = "notavailableyet";
}



#print "\n" . "corpname" . $corpname;
$subtextname4 = $subtext[4];
$subtextname4 = strip_tags($subtextname4);
$submittedby = $subtextname4;
#print "\n" . "subtextname4" . $subtextname4 . "\n";
#$submittedby = substr($submittedby, 13);
$submittedby = substr($submittedby, 13);
$submittedby = trim(str_replace("Submitted By:","",$submittedby));
#print "\n" . "submittedby" . $submittedby . "\n";
#$str = substr($str, 1);
  #  2)Status:


$howmanyupdates = strip_tags(trim($historical[0]));
$howmanyupdates = substr($howmanyupdates,0,1);
print "howmanyupdates" . $howmanyupdates . "\n";


$date = array();
$status = array();

$i = 0;
$b = $howmanyupdates - 1;
for ($i = 0; $i < $howmanyupdates; $i++) {
#for ($d = $howmanyupdates; $d >= 1; $d--) {

$c = $i * 2;
#print "\n" . "b" . $b . "c" . $c . "\n";
$temphiststat = $historical[$c];
print $temphiststat;
$d = $c+1;
$temphistdate = $historical[$d];
print $temphistdate;
#}
#for ($b = $howmanyupdates; $b >= 0; $b--) {
#for ($b = 0; $b <= $howmanyupdates; $b++) {
#$b--;
#$b = $howmanyupdates;
#$d $b +1;
#$b = $d - 1;
print "\n" . "b" . $b . "c" . $c . "d" . $d . "\n";

$status[$b] = $temphiststat;
$date[$b] = $temphistdate;
#$status[$b] = $historical[$c];
#$date[$b] = $historical[$c+1];
#$b =  $i/2; 

$status[$b] = strip_tags($status[$b]);
$status[$b] = trim(str_replace("&nbsp;Status","",$status[$b]));
print "statusnumb" . $c . $status[$b] . "\n";

print "date" . $d . $date[$b] . "\n";
$date[$b] = strip_tags($date[$b]);
$date[$b] = trim(str_replace("&nbsp;Date:","",$date[$b]));




#}

#}
#}

/*
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status2" . $status2 . "\n";
#print "\n" . "status2b" . $status2 . "\n";
#$status1 = $historical[0];
#$status1 = strip_tags($status1);

#$status1 = substr($status1, 10);

   $date1 = $date[0];
$date1 = strip_tags($date1);
$date1 = trim(str_replace("&nbsp;Date:","",$date1));
#$contents = explode("</tr>",$column[0]); 
   $date2 = $date[1];
$date2 = strip_tags($date2);
$date2 = trim(str_replace("&nbsp;Date:","",$date2));


   $date3 = $date[2];
$date3 = strip_tags($date3);
$date3 = trim(str_replace("&nbsp;Date:","",$date3));


*/

if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
#unset($date[]);
#unset($status[]);
}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
    $moredetails["date1"] = $date1;
   $moredetails["status2"] = $status2;
    $moredetails["published"] = $published;
    $moredetails["date2"] = $date2;
    $moredetails["status3"] = $status3;
    $moredetails["date3"] = $date3;
 #   $moredetails["status4"] = $status43;
 #   $moredetails["date4"] = $date4;

#    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);

}




?>
<?php
require 'scraperwiki/simple_html_dom.php';
$councillors = array();


for ($i = 1; $i <= 81; $i++) {
 #   $html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/callawards.nsf/posted+awards?OpenView&Start=1&Count=1000&Expand=3.".$i);
$html = scraperWiki::scrape("http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN?openview&start=" . $i . "&count=1"); #&start=30&count=15
    $dom = new simple_html_dom();
    $dom->load($html);

   # foreach ($dom->find('a[href*=OpenDocument]') as $a) {
      $rows=$dom->find("div[id=viewbody] table tr");
unset($rows[0]);
foreach($rows as $row) {
$refnumbercell = $row->find("td",0);
$urlcell = $row->find("td a",0)->href;
#print $urlcell;
$urlcell = strip_tags($urlcell);
$urlcell = ltrim($urlcell,'.');

#print "\n" . "urlcell" . $urlcell;
    $url = "http://petitions.oireachtas.ie/online_petitions.nsf" . $urlcell; # ->href;
#print "\n" . "url" . $url;

#http://petitions.oireachtas.ie/online_petitions.nsf./Published_Petitions_EN/4B1C5516D35CB1A880257AE9005FC246?OpenDocument&type=published+petition&lang=EN&r=0.651346608682383
#http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN/70244C3CADEE670880257ABE00553093?OpenDocument&type=published+petition&lang=EN&r=0.221820401312276
    $refnumber = strip_tags($refnumbercell);
    $namecellcontents = $row->find("td",1);
    $namecell = trim(strip_tags($namecellcontents->innertext));
    $name = trim(str_replace(" / ","/",trim($namecell)));
    $titlecell = $row->find("td",2);
    $title = trim($titlecell->plaintext);
    $title = str_replace("&amp;","&",$title);
    $statuscell = $row->find("td",3);
    $status = trim($statuscell->plaintext);
        //var_dump($thisrecord['description']);
        //print mb_detect_encoding($thisrecord['description'])."\n";


    $moredetails = get_extras($url);
}
$councillors["$refnumber"] = array(
              "Url"   => "$url",
              "Name"   => "$name",
                    "Title"   => "$title",
                    "Status"   => "$status",
                 #   "Email"   => "councillor@example.com",
                #    "Phone"   => "01 100 1000",
                #    "Mobile"  => "085 000 0000",
                #    "Image"   => "http://URI",
                "Submittedby" => $moredetails["submittedby"],
     "Petitiontext" => $moredetails["petitiontext"],
     "Status1" => $moredetails["status1"],
"Status2" => $moredetails["status2"],
"Status3" => $moredetails["status3"],
     "Date1" => $moredetails["date1"],
     "Date2" => $moredetails["date2"],
 "Date3" => $moredetails["date3"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `date1` string, `date2` string, `date3` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :date1, :date2, :date3, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
            array( 
 "url"     => $values["Url"],
                    "name"     => $values["Name"],
                    "refnumber"    => $refnumber,
                    "title"   => $values["Title"],
                    "status"   => $values["Status"],
                    "submittedby"   => $values["Submittedby"],
                    "petitiontext"  => $values["Petitiontext"],
                     "status1"  => $values["Status1"],
      "status2"  => $values["Status2"],
 "status3"  => $values["Status3"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
                    "corpname"   => $values["Corpname"],
                    "published" => $values["Published"]
            )
    );
#}
}
scraperwiki::sqlitecommit();


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

    $column = $localdom->find("div[class=column-center2]");
print $url;
 #   $trows=$column->find("div[class=column-center-inner] table tr");
#print_r($column[2]);
 #  $contents = explode("</tr>",$column[0]); 
$contents = explode("</h2>",$column[0]); 
print "\n" . "contents";
print_r($contents);
 $contentbs = explode("</h2>",$contents[2]); 
print "contentbs";
print_r($contentbs);
$publishedcell = explode("<br />",$contentbs[0]); 
print "publishedcell";
print_r($publishedcell);
if (
$published = $publishedcell[1] > 0) {
$published = $publishedcell[1];
}
else {
$published = $publishedcell[1];
}
$published = trim(strip_tags($published));

$published = substr($published, 10); 
print "\n" . "published" . $published;
 $historical = explode("</tr>",$contentbs[0]); 
# $contentbs = explode("</h2>",$contents[2]); 
print "historical";
print_r($historical);
 #  $details = explode("</h2>",$contents); 
 $subtext = explode("</tr>",$contents[1]); 
#print "subtext";
#print_r($subtext);

   # foreach($rows as $row) {
#    $submittedby = $column->find("td",1);

 #   $petitiontext = $column->find("td",1); 
$namestrip = array("Corporate Name:","Unincorporated Name:","Unincorporated Association Name:");





$subtextname5 = $subtext[5];
$subtextname5 = trim(strip_tags($subtextname5));
#print "\n" . "subtextname5" . $subtextname5;

$subtextname6 = $subtext[6];
$subtextname6 = trim(strip_tags($subtextname6));
#print "\n" . "subtextname6" . $subtextname6;

$subtextname7 = $subtext[7];
$subtextname7 = trim(strip_tags($subtextname7));
#print "\n" . "subtextname7" . $subtextname7;





 if(substr($subtextname5,0,9) == "Corporate" || substr($subtextname5,0,13) == "Unincorporated" )  {
            $corpname  = $subtext[5];
print "\n" . "corpname" . $corpname;
$corpname = trim(strip_tags($corpname));
$corpname = str_replace($namestrip,"",$corpname);
}  

else  {
$corpname  = "n/a";
 }


 if(substr($subtextname5,0,8) == "Petition") {
       $petitiontext  = $subtext[5];
 $petitiontext  = "petitiontext5";
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext5cut" . $petitiontext . "\n";

}
 else if(substr($subtextname6,0,8) == "Petition") {
       $petitiontext = $subtext[6];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext6cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext6";
 $corpname  = "n/a";
}

 else if(substr($subtextname7,0,8) == "Petition") {
       $petitiontext  = $subtext[7];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext7cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext7";

}

 else {
 $submittedby  = $subtext[4];
    $submittedby = strip_tags($submittedby);
$submittedby = substr($submittedby, 13); #Submitted By:
$submittedby = "blaa";
 $corpname  = "n/a";

 $petitiontext   = "notavailableyet";
}



#print "\n" . "corpname" . $corpname;
$subtextname4 = $subtext[4];
$subtextname4 = strip_tags($subtextname4);
$submittedby = $subtextname4;
#print "\n" . "subtextname4" . $subtextname4 . "\n";
#$submittedby = substr($submittedby, 13);
$submittedby = substr($submittedby, 13);
$submittedby = trim(str_replace("Submitted By:","",$submittedby));
#print "\n" . "submittedby" . $submittedby . "\n";
#$str = substr($str, 1);
  #  2)Status:


$howmanyupdates = strip_tags(trim($historical[0]));
$howmanyupdates = substr($howmanyupdates,0,1);
print "howmanyupdates" . $howmanyupdates . "\n";


$date = array();
$status = array();

$i = 0;
$b = $howmanyupdates - 1;
for ($i = 0; $i < $howmanyupdates; $i++) {
#for ($d = $howmanyupdates; $d >= 1; $d--) {

$c = $i * 2;
#print "\n" . "b" . $b . "c" . $c . "\n";
$temphiststat = $historical[$c];
print $temphiststat;
$d = $c+1;
$temphistdate = $historical[$d];
print $temphistdate;
#}
#for ($b = $howmanyupdates; $b >= 0; $b--) {
#for ($b = 0; $b <= $howmanyupdates; $b++) {
#$b--;
#$b = $howmanyupdates;
#$d $b +1;
#$b = $d - 1;
print "\n" . "b" . $b . "c" . $c . "d" . $d . "\n";

$status[$b] = $temphiststat;
$date[$b] = $temphistdate;
#$status[$b] = $historical[$c];
#$date[$b] = $historical[$c+1];
#$b =  $i/2; 

$status[$b] = strip_tags($status[$b]);
$status[$b] = trim(str_replace("&nbsp;Status","",$status[$b]));
print "statusnumb" . $c . $status[$b] . "\n";

print "date" . $d . $date[$b] . "\n";
$date[$b] = strip_tags($date[$b]);
$date[$b] = trim(str_replace("&nbsp;Date:","",$date[$b]));




#}

#}
#}

/*
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status2" . $status2 . "\n";
#print "\n" . "status2b" . $status2 . "\n";
#$status1 = $historical[0];
#$status1 = strip_tags($status1);

#$status1 = substr($status1, 10);

   $date1 = $date[0];
$date1 = strip_tags($date1);
$date1 = trim(str_replace("&nbsp;Date:","",$date1));
#$contents = explode("</tr>",$column[0]); 
   $date2 = $date[1];
$date2 = strip_tags($date2);
$date2 = trim(str_replace("&nbsp;Date:","",$date2));


   $date3 = $date[2];
$date3 = strip_tags($date3);
$date3 = trim(str_replace("&nbsp;Date:","",$date3));


*/

if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
#unset($date[]);
#unset($status[]);
}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
    $moredetails["date1"] = $date1;
   $moredetails["status2"] = $status2;
    $moredetails["published"] = $published;
    $moredetails["date2"] = $date2;
    $moredetails["status3"] = $status3;
    $moredetails["date3"] = $date3;
 #   $moredetails["status4"] = $status43;
 #   $moredetails["date4"] = $date4;

#    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);

}




?>
<?php
require 'scraperwiki/simple_html_dom.php';
$councillors = array();


for ($i = 1; $i <= 81; $i++) {
 #   $html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/callawards.nsf/posted+awards?OpenView&Start=1&Count=1000&Expand=3.".$i);
$html = scraperWiki::scrape("http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN?openview&start=" . $i . "&count=1"); #&start=30&count=15
    $dom = new simple_html_dom();
    $dom->load($html);

   # foreach ($dom->find('a[href*=OpenDocument]') as $a) {
      $rows=$dom->find("div[id=viewbody] table tr");
unset($rows[0]);
foreach($rows as $row) {
$refnumbercell = $row->find("td",0);
$urlcell = $row->find("td a",0)->href;
#print $urlcell;
$urlcell = strip_tags($urlcell);
$urlcell = ltrim($urlcell,'.');

#print "\n" . "urlcell" . $urlcell;
    $url = "http://petitions.oireachtas.ie/online_petitions.nsf" . $urlcell; # ->href;
#print "\n" . "url" . $url;

#http://petitions.oireachtas.ie/online_petitions.nsf./Published_Petitions_EN/4B1C5516D35CB1A880257AE9005FC246?OpenDocument&type=published+petition&lang=EN&r=0.651346608682383
#http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN/70244C3CADEE670880257ABE00553093?OpenDocument&type=published+petition&lang=EN&r=0.221820401312276
    $refnumber = strip_tags($refnumbercell);
    $namecellcontents = $row->find("td",1);
    $namecell = trim(strip_tags($namecellcontents->innertext));
    $name = trim(str_replace(" / ","/",trim($namecell)));
    $titlecell = $row->find("td",2);
    $title = trim($titlecell->plaintext);
    $title = str_replace("&amp;","&",$title);
    $statuscell = $row->find("td",3);
    $status = trim($statuscell->plaintext);
        //var_dump($thisrecord['description']);
        //print mb_detect_encoding($thisrecord['description'])."\n";


    $moredetails = get_extras($url);
}
$councillors["$refnumber"] = array(
              "Url"   => "$url",
              "Name"   => "$name",
                    "Title"   => "$title",
                    "Status"   => "$status",
                 #   "Email"   => "councillor@example.com",
                #    "Phone"   => "01 100 1000",
                #    "Mobile"  => "085 000 0000",
                #    "Image"   => "http://URI",
                "Submittedby" => $moredetails["submittedby"],
     "Petitiontext" => $moredetails["petitiontext"],
     "Status1" => $moredetails["status1"],
"Status2" => $moredetails["status2"],
"Status3" => $moredetails["status3"],
     "Date1" => $moredetails["date1"],
     "Date2" => $moredetails["date2"],
 "Date3" => $moredetails["date3"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `date1` string, `date2` string, `date3` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :date1, :date2, :date3, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
            array( 
 "url"     => $values["Url"],
                    "name"     => $values["Name"],
                    "refnumber"    => $refnumber,
                    "title"   => $values["Title"],
                    "status"   => $values["Status"],
                    "submittedby"   => $values["Submittedby"],
                    "petitiontext"  => $values["Petitiontext"],
                     "status1"  => $values["Status1"],
      "status2"  => $values["Status2"],
 "status3"  => $values["Status3"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
                    "corpname"   => $values["Corpname"],
                    "published" => $values["Published"]
            )
    );
#}
}
scraperwiki::sqlitecommit();


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

    $column = $localdom->find("div[class=column-center2]");
print $url;
 #   $trows=$column->find("div[class=column-center-inner] table tr");
#print_r($column[2]);
 #  $contents = explode("</tr>",$column[0]); 
$contents = explode("</h2>",$column[0]); 
print "\n" . "contents";
print_r($contents);
 $contentbs = explode("</h2>",$contents[2]); 
print "contentbs";
print_r($contentbs);
$publishedcell = explode("<br />",$contentbs[0]); 
print "publishedcell";
print_r($publishedcell);
if (
$published = $publishedcell[1] > 0) {
$published = $publishedcell[1];
}
else {
$published = $publishedcell[1];
}
$published = trim(strip_tags($published));

$published = substr($published, 10); 
print "\n" . "published" . $published;
 $historical = explode("</tr>",$contentbs[0]); 
# $contentbs = explode("</h2>",$contents[2]); 
print "historical";
print_r($historical);
 #  $details = explode("</h2>",$contents); 
 $subtext = explode("</tr>",$contents[1]); 
#print "subtext";
#print_r($subtext);

   # foreach($rows as $row) {
#    $submittedby = $column->find("td",1);

 #   $petitiontext = $column->find("td",1); 
$namestrip = array("Corporate Name:","Unincorporated Name:","Unincorporated Association Name:");





$subtextname5 = $subtext[5];
$subtextname5 = trim(strip_tags($subtextname5));
#print "\n" . "subtextname5" . $subtextname5;

$subtextname6 = $subtext[6];
$subtextname6 = trim(strip_tags($subtextname6));
#print "\n" . "subtextname6" . $subtextname6;

$subtextname7 = $subtext[7];
$subtextname7 = trim(strip_tags($subtextname7));
#print "\n" . "subtextname7" . $subtextname7;





 if(substr($subtextname5,0,9) == "Corporate" || substr($subtextname5,0,13) == "Unincorporated" )  {
            $corpname  = $subtext[5];
print "\n" . "corpname" . $corpname;
$corpname = trim(strip_tags($corpname));
$corpname = str_replace($namestrip,"",$corpname);
}  

else  {
$corpname  = "n/a";
 }


 if(substr($subtextname5,0,8) == "Petition") {
       $petitiontext  = $subtext[5];
 $petitiontext  = "petitiontext5";
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext5cut" . $petitiontext . "\n";

}
 else if(substr($subtextname6,0,8) == "Petition") {
       $petitiontext = $subtext[6];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext6cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext6";
 $corpname  = "n/a";
}

 else if(substr($subtextname7,0,8) == "Petition") {
       $petitiontext  = $subtext[7];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext7cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext7";

}

 else {
 $submittedby  = $subtext[4];
    $submittedby = strip_tags($submittedby);
$submittedby = substr($submittedby, 13); #Submitted By:
$submittedby = "blaa";
 $corpname  = "n/a";

 $petitiontext   = "notavailableyet";
}



#print "\n" . "corpname" . $corpname;
$subtextname4 = $subtext[4];
$subtextname4 = strip_tags($subtextname4);
$submittedby = $subtextname4;
#print "\n" . "subtextname4" . $subtextname4 . "\n";
#$submittedby = substr($submittedby, 13);
$submittedby = substr($submittedby, 13);
$submittedby = trim(str_replace("Submitted By:","",$submittedby));
#print "\n" . "submittedby" . $submittedby . "\n";
#$str = substr($str, 1);
  #  2)Status:


$howmanyupdates = strip_tags(trim($historical[0]));
$howmanyupdates = substr($howmanyupdates,0,1);
print "howmanyupdates" . $howmanyupdates . "\n";


$date = array();
$status = array();

$i = 0;
$b = $howmanyupdates - 1;
for ($i = 0; $i < $howmanyupdates; $i++) {
#for ($d = $howmanyupdates; $d >= 1; $d--) {

$c = $i * 2;
#print "\n" . "b" . $b . "c" . $c . "\n";
$temphiststat = $historical[$c];
print $temphiststat;
$d = $c+1;
$temphistdate = $historical[$d];
print $temphistdate;
#}
#for ($b = $howmanyupdates; $b >= 0; $b--) {
#for ($b = 0; $b <= $howmanyupdates; $b++) {
#$b--;
#$b = $howmanyupdates;
#$d $b +1;
#$b = $d - 1;
print "\n" . "b" . $b . "c" . $c . "d" . $d . "\n";

$status[$b] = $temphiststat;
$date[$b] = $temphistdate;
#$status[$b] = $historical[$c];
#$date[$b] = $historical[$c+1];
#$b =  $i/2; 

$status[$b] = strip_tags($status[$b]);
$status[$b] = trim(str_replace("&nbsp;Status","",$status[$b]));
print "statusnumb" . $c . $status[$b] . "\n";

print "date" . $d . $date[$b] . "\n";
$date[$b] = strip_tags($date[$b]);
$date[$b] = trim(str_replace("&nbsp;Date:","",$date[$b]));




#}

#}
#}

/*
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status2" . $status2 . "\n";
#print "\n" . "status2b" . $status2 . "\n";
#$status1 = $historical[0];
#$status1 = strip_tags($status1);

#$status1 = substr($status1, 10);

   $date1 = $date[0];
$date1 = strip_tags($date1);
$date1 = trim(str_replace("&nbsp;Date:","",$date1));
#$contents = explode("</tr>",$column[0]); 
   $date2 = $date[1];
$date2 = strip_tags($date2);
$date2 = trim(str_replace("&nbsp;Date:","",$date2));


   $date3 = $date[2];
$date3 = strip_tags($date3);
$date3 = trim(str_replace("&nbsp;Date:","",$date3));


*/

if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
#unset($date[]);
#unset($status[]);
}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
    $moredetails["date1"] = $date1;
   $moredetails["status2"] = $status2;
    $moredetails["published"] = $published;
    $moredetails["date2"] = $date2;
    $moredetails["status3"] = $status3;
    $moredetails["date3"] = $date3;
 #   $moredetails["status4"] = $status43;
 #   $moredetails["date4"] = $date4;

#    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);

}




?>
<?php
require 'scraperwiki/simple_html_dom.php';
$councillors = array();


for ($i = 1; $i <= 81; $i++) {
 #   $html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/callawards.nsf/posted+awards?OpenView&Start=1&Count=1000&Expand=3.".$i);
$html = scraperWiki::scrape("http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN?openview&start=" . $i . "&count=1"); #&start=30&count=15
    $dom = new simple_html_dom();
    $dom->load($html);

   # foreach ($dom->find('a[href*=OpenDocument]') as $a) {
      $rows=$dom->find("div[id=viewbody] table tr");
unset($rows[0]);
foreach($rows as $row) {
$refnumbercell = $row->find("td",0);
$urlcell = $row->find("td a",0)->href;
#print $urlcell;
$urlcell = strip_tags($urlcell);
$urlcell = ltrim($urlcell,'.');

#print "\n" . "urlcell" . $urlcell;
    $url = "http://petitions.oireachtas.ie/online_petitions.nsf" . $urlcell; # ->href;
#print "\n" . "url" . $url;

#http://petitions.oireachtas.ie/online_petitions.nsf./Published_Petitions_EN/4B1C5516D35CB1A880257AE9005FC246?OpenDocument&type=published+petition&lang=EN&r=0.651346608682383
#http://petitions.oireachtas.ie/online_petitions.nsf/Published_Petitions_EN/70244C3CADEE670880257ABE00553093?OpenDocument&type=published+petition&lang=EN&r=0.221820401312276
    $refnumber = strip_tags($refnumbercell);
    $namecellcontents = $row->find("td",1);
    $namecell = trim(strip_tags($namecellcontents->innertext));
    $name = trim(str_replace(" / ","/",trim($namecell)));
    $titlecell = $row->find("td",2);
    $title = trim($titlecell->plaintext);
    $title = str_replace("&amp;","&",$title);
    $statuscell = $row->find("td",3);
    $status = trim($statuscell->plaintext);
        //var_dump($thisrecord['description']);
        //print mb_detect_encoding($thisrecord['description'])."\n";


    $moredetails = get_extras($url);
}
$councillors["$refnumber"] = array(
              "Url"   => "$url",
              "Name"   => "$name",
                    "Title"   => "$title",
                    "Status"   => "$status",
                 #   "Email"   => "councillor@example.com",
                #    "Phone"   => "01 100 1000",
                #    "Mobile"  => "085 000 0000",
                #    "Image"   => "http://URI",
                "Submittedby" => $moredetails["submittedby"],
     "Petitiontext" => $moredetails["petitiontext"],
     "Status1" => $moredetails["status1"],
"Status2" => $moredetails["status2"],
"Status3" => $moredetails["status3"],
     "Date1" => $moredetails["date1"],
     "Date2" => $moredetails["date2"],
 "Date3" => $moredetails["date3"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `date1` string, `date2` string, `date3` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :date1, :date2, :date3, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
            array( 
 "url"     => $values["Url"],
                    "name"     => $values["Name"],
                    "refnumber"    => $refnumber,
                    "title"   => $values["Title"],
                    "status"   => $values["Status"],
                    "submittedby"   => $values["Submittedby"],
                    "petitiontext"  => $values["Petitiontext"],
                     "status1"  => $values["Status1"],
      "status2"  => $values["Status2"],
 "status3"  => $values["Status3"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
                    "corpname"   => $values["Corpname"],
                    "published" => $values["Published"]
            )
    );
#}
}
scraperwiki::sqlitecommit();


function get_extras($url) {
    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);

    $column = $localdom->find("div[class=column-center2]");
print $url;
 #   $trows=$column->find("div[class=column-center-inner] table tr");
#print_r($column[2]);
 #  $contents = explode("</tr>",$column[0]); 
$contents = explode("</h2>",$column[0]); 
print "\n" . "contents";
print_r($contents);
 $contentbs = explode("</h2>",$contents[2]); 
print "contentbs";
print_r($contentbs);
$publishedcell = explode("<br />",$contentbs[0]); 
print "publishedcell";
print_r($publishedcell);
if (
$published = $publishedcell[1] > 0) {
$published = $publishedcell[1];
}
else {
$published = $publishedcell[1];
}
$published = trim(strip_tags($published));

$published = substr($published, 10); 
print "\n" . "published" . $published;
 $historical = explode("</tr>",$contentbs[0]); 
# $contentbs = explode("</h2>",$contents[2]); 
print "historical";
print_r($historical);
 #  $details = explode("</h2>",$contents); 
 $subtext = explode("</tr>",$contents[1]); 
#print "subtext";
#print_r($subtext);

   # foreach($rows as $row) {
#    $submittedby = $column->find("td",1);

 #   $petitiontext = $column->find("td",1); 
$namestrip = array("Corporate Name:","Unincorporated Name:","Unincorporated Association Name:");





$subtextname5 = $subtext[5];
$subtextname5 = trim(strip_tags($subtextname5));
#print "\n" . "subtextname5" . $subtextname5;

$subtextname6 = $subtext[6];
$subtextname6 = trim(strip_tags($subtextname6));
#print "\n" . "subtextname6" . $subtextname6;

$subtextname7 = $subtext[7];
$subtextname7 = trim(strip_tags($subtextname7));
#print "\n" . "subtextname7" . $subtextname7;





 if(substr($subtextname5,0,9) == "Corporate" || substr($subtextname5,0,13) == "Unincorporated" )  {
            $corpname  = $subtext[5];
print "\n" . "corpname" . $corpname;
$corpname = trim(strip_tags($corpname));
$corpname = str_replace($namestrip,"",$corpname);
}  

else  {
$corpname  = "n/a";
 }


 if(substr($subtextname5,0,8) == "Petition") {
       $petitiontext  = $subtext[5];
 $petitiontext  = "petitiontext5";
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext5cut" . $petitiontext . "\n";

}
 else if(substr($subtextname6,0,8) == "Petition") {
       $petitiontext = $subtext[6];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext6cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext6";
 $corpname  = "n/a";
}

 else if(substr($subtextname7,0,8) == "Petition") {
       $petitiontext  = $subtext[7];
$petitiontext = trim(strip_tags($petitiontext));
print "\n" . "petitiontext" . $petitiontext . "\n";
$petitiontext = substr($petitiontext, 14); 
print "\n" . "petitiontext7cut" . $petitiontext . "\n";
# $petitiontext   = "petitiontext7";

}

 else {
 $submittedby  = $subtext[4];
    $submittedby = strip_tags($submittedby);
$submittedby = substr($submittedby, 13); #Submitted By:
$submittedby = "blaa";
 $corpname  = "n/a";

 $petitiontext   = "notavailableyet";
}



#print "\n" . "corpname" . $corpname;
$subtextname4 = $subtext[4];
$subtextname4 = strip_tags($subtextname4);
$submittedby = $subtextname4;
#print "\n" . "subtextname4" . $subtextname4 . "\n";
#$submittedby = substr($submittedby, 13);
$submittedby = substr($submittedby, 13);
$submittedby = trim(str_replace("Submitted By:","",$submittedby));
#print "\n" . "submittedby" . $submittedby . "\n";
#$str = substr($str, 1);
  #  2)Status:


$howmanyupdates = strip_tags(trim($historical[0]));
$howmanyupdates = substr($howmanyupdates,0,1);
print "howmanyupdates" . $howmanyupdates . "\n";


$date = array();
$status = array();

$i = 0;
$b = $howmanyupdates - 1;
for ($i = 0; $i < $howmanyupdates; $i++) {
#for ($d = $howmanyupdates; $d >= 1; $d--) {

$c = $i * 2;
#print "\n" . "b" . $b . "c" . $c . "\n";
$temphiststat = $historical[$c];
print $temphiststat;
$d = $c+1;
$temphistdate = $historical[$d];
print $temphistdate;
#}
#for ($b = $howmanyupdates; $b >= 0; $b--) {
#for ($b = 0; $b <= $howmanyupdates; $b++) {
#$b--;
#$b = $howmanyupdates;
#$d $b +1;
#$b = $d - 1;
print "\n" . "b" . $b . "c" . $c . "d" . $d . "\n";

$status[$b] = $temphiststat;
$date[$b] = $temphistdate;
#$status[$b] = $historical[$c];
#$date[$b] = $historical[$c+1];
#$b =  $i/2; 

$status[$b] = strip_tags($status[$b]);
$status[$b] = trim(str_replace("&nbsp;Status","",$status[$b]));
print "statusnumb" . $c . $status[$b] . "\n";

print "date" . $d . $date[$b] . "\n";
$date[$b] = strip_tags($date[$b]);
$date[$b] = trim(str_replace("&nbsp;Date:","",$date[$b]));




#}

#}
#}

/*
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status2" . $status2 . "\n";
#print "\n" . "status2b" . $status2 . "\n";
#$status1 = $historical[0];
#$status1 = strip_tags($status1);

#$status1 = substr($status1, 10);

   $date1 = $date[0];
$date1 = strip_tags($date1);
$date1 = trim(str_replace("&nbsp;Date:","",$date1));
#$contents = explode("</tr>",$column[0]); 
   $date2 = $date[1];
$date2 = strip_tags($date2);
$date2 = trim(str_replace("&nbsp;Date:","",$date2));


   $date3 = $date[2];
$date3 = strip_tags($date3);
$date3 = trim(str_replace("&nbsp;Date:","",$date3));


*/

if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
#unset($date[]);
#unset($status[]);
}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
    $moredetails["date1"] = $date1;
   $moredetails["status2"] = $status2;
    $moredetails["published"] = $published;
    $moredetails["date2"] = $date2;
    $moredetails["status3"] = $status3;
    $moredetails["date3"] = $date3;
 #   $moredetails["status4"] = $status43;
 #   $moredetails["date4"] = $date4;

#    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);

}




?>
