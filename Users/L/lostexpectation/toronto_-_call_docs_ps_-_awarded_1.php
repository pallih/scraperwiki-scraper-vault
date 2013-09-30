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
   "Status4" => $moredetails["status4"],
"Status5" => $moredetails["status5"],
"Status6" => $moredetails["status6"],
     "Date4" => $moredetails["date4"],
     "Date5" => $moredetails["date5"],


"Status7" => $moredetails["status7"],
"Status8" => $moredetails["status8"],
     "Date6" => $moredetails["date6"],
     "Date7" => $moredetails["date7"],

 "Date8" => $moredetails["date8"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `status4` string, `status5` string, `status6` string, `status7` string, `status8` string, `date1` string, `date2` string, `date3` string, `date4` string, `date5` string, `date6` string, `date7` string, `date8` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :status4, :status5, :status6, :status7, :status8, :date1, :date2, :date3, :date4, :date5, :date6, :date7, :date8, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
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
   "status4"  => $values["Status4"],
 "status5"  => $values["Status5"],
   "status6"  => $values["Status6"],
 "status7"  => $values["Status7"],
   "status8"  => $values["Status8"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
     "date4"  => $values["Date4"],
 "date5"  => $values["Date5"],                
     "date6"  => $values["Date6"],
 "date7"  => $values["Date7"],                 
     "date8"  => $values["Date8"],
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



$date = array();
$status = array();

$x = 0;
$b = $howmanyupdates - 1;
for ($x = 0; $x < $howmanyupdates; $x++) {
print "howmanyupdates" . $howmanyupdates . "\n";
#for ($d = $howmanyupdates; $d >= 1; $d--) {
print "start";
$c = $x * 2;
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
print "\n" . "b" . $b . "c" . $c . "d" . $d . "x" . $x . "\n";

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


if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
}
#}
#}
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status3" . $status3 . "\n";


$status4 = $status[3];
$status4 = substr($status4,9);
print "\n" . "status4" . $status4 . "\n";


$status5 = $status[4];
$status5 = substr($status5,9);
print "\n" . "status5" . $status5 . "\n";


$status6 = $status[5];
$status6 = substr($status6,9);
print "\n" . "status6" . $status6 . "\n";

$status7 = $status[6];
$status7 = substr($status7,9);
print "\n" . "status7" . $status7 . "\n";

$status8 = $status[7];
$status8 = substr($status8,9);
print "\n" . "status8" . $status8 . "\n";

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

   $date4 = $date[3];
$date4 = strip_tags($date4);
$date4 = trim(str_replace("&nbsp;Date:","",$date4));


   $date5 = $date[4];
$date5 = strip_tags($date5);
$date5 = trim(str_replace("&nbsp;Date:","",$date5));

   $date6 = $date[5];
$date6 = strip_tags($date6);
$date6 = trim(str_replace("&nbsp;Date:","",$date6));

   $date7 = $date[6];
$date7 = strip_tags($date7);
$date7 = trim(str_replace("&nbsp;Date:","",$date7));


   $date8 = $date[7];
$date8 = strip_tags($date8);
$date8 = trim(str_replace("&nbsp;Date:","",$date8));



#unset($date);
#unset($status);

#}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
   $moredetails["status2"] = $status2;
 $moredetails["status3"] = $status3;
 $moredetails["status4"] = $status4;
 $moredetails["status5"] = $status5;
 $moredetails["status6"] = $status6;
 $moredetails["status7"] = $status7;
 $moredetails["status8"] = $status8;
    $moredetails["published"] = $published;
    $moredetails["date1"] = $date1;
 $moredetails["date2"] = $date2;
 $moredetails["date3"] = $date3;
 $moredetails["date4"] = $date4;
 $moredetails["date5"] = $date5;
 $moredetails["date6"] = $date6;
 $moredetails["date7"] = $date7;
 $moredetails["date8"] = $date8;
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
   "Status4" => $moredetails["status4"],
"Status5" => $moredetails["status5"],
"Status6" => $moredetails["status6"],
     "Date4" => $moredetails["date4"],
     "Date5" => $moredetails["date5"],


"Status7" => $moredetails["status7"],
"Status8" => $moredetails["status8"],
     "Date6" => $moredetails["date6"],
     "Date7" => $moredetails["date7"],

 "Date8" => $moredetails["date8"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `status4` string, `status5` string, `status6` string, `status7` string, `status8` string, `date1` string, `date2` string, `date3` string, `date4` string, `date5` string, `date6` string, `date7` string, `date8` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :status4, :status5, :status6, :status7, :status8, :date1, :date2, :date3, :date4, :date5, :date6, :date7, :date8, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
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
   "status4"  => $values["Status4"],
 "status5"  => $values["Status5"],
   "status6"  => $values["Status6"],
 "status7"  => $values["Status7"],
   "status8"  => $values["Status8"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
     "date4"  => $values["Date4"],
 "date5"  => $values["Date5"],                
     "date6"  => $values["Date6"],
 "date7"  => $values["Date7"],                 
     "date8"  => $values["Date8"],
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



$date = array();
$status = array();

$x = 0;
$b = $howmanyupdates - 1;
for ($x = 0; $x < $howmanyupdates; $x++) {
print "howmanyupdates" . $howmanyupdates . "\n";
#for ($d = $howmanyupdates; $d >= 1; $d--) {
print "start";
$c = $x * 2;
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
print "\n" . "b" . $b . "c" . $c . "d" . $d . "x" . $x . "\n";

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


if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
}
#}
#}
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status3" . $status3 . "\n";


$status4 = $status[3];
$status4 = substr($status4,9);
print "\n" . "status4" . $status4 . "\n";


$status5 = $status[4];
$status5 = substr($status5,9);
print "\n" . "status5" . $status5 . "\n";


$status6 = $status[5];
$status6 = substr($status6,9);
print "\n" . "status6" . $status6 . "\n";

$status7 = $status[6];
$status7 = substr($status7,9);
print "\n" . "status7" . $status7 . "\n";

$status8 = $status[7];
$status8 = substr($status8,9);
print "\n" . "status8" . $status8 . "\n";

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

   $date4 = $date[3];
$date4 = strip_tags($date4);
$date4 = trim(str_replace("&nbsp;Date:","",$date4));


   $date5 = $date[4];
$date5 = strip_tags($date5);
$date5 = trim(str_replace("&nbsp;Date:","",$date5));

   $date6 = $date[5];
$date6 = strip_tags($date6);
$date6 = trim(str_replace("&nbsp;Date:","",$date6));

   $date7 = $date[6];
$date7 = strip_tags($date7);
$date7 = trim(str_replace("&nbsp;Date:","",$date7));


   $date8 = $date[7];
$date8 = strip_tags($date8);
$date8 = trim(str_replace("&nbsp;Date:","",$date8));



#unset($date);
#unset($status);

#}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
   $moredetails["status2"] = $status2;
 $moredetails["status3"] = $status3;
 $moredetails["status4"] = $status4;
 $moredetails["status5"] = $status5;
 $moredetails["status6"] = $status6;
 $moredetails["status7"] = $status7;
 $moredetails["status8"] = $status8;
    $moredetails["published"] = $published;
    $moredetails["date1"] = $date1;
 $moredetails["date2"] = $date2;
 $moredetails["date3"] = $date3;
 $moredetails["date4"] = $date4;
 $moredetails["date5"] = $date5;
 $moredetails["date6"] = $date6;
 $moredetails["date7"] = $date7;
 $moredetails["date8"] = $date8;
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
   "Status4" => $moredetails["status4"],
"Status5" => $moredetails["status5"],
"Status6" => $moredetails["status6"],
     "Date4" => $moredetails["date4"],
     "Date5" => $moredetails["date5"],


"Status7" => $moredetails["status7"],
"Status8" => $moredetails["status8"],
     "Date6" => $moredetails["date6"],
     "Date7" => $moredetails["date7"],

 "Date8" => $moredetails["date8"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `status4` string, `status5` string, `status6` string, `status7` string, `status8` string, `date1` string, `date2` string, `date3` string, `date4` string, `date5` string, `date6` string, `date7` string, `date8` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :status4, :status5, :status6, :status7, :status8, :date1, :date2, :date3, :date4, :date5, :date6, :date7, :date8, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
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
   "status4"  => $values["Status4"],
 "status5"  => $values["Status5"],
   "status6"  => $values["Status6"],
 "status7"  => $values["Status7"],
   "status8"  => $values["Status8"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
     "date4"  => $values["Date4"],
 "date5"  => $values["Date5"],                
     "date6"  => $values["Date6"],
 "date7"  => $values["Date7"],                 
     "date8"  => $values["Date8"],
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



$date = array();
$status = array();

$x = 0;
$b = $howmanyupdates - 1;
for ($x = 0; $x < $howmanyupdates; $x++) {
print "howmanyupdates" . $howmanyupdates . "\n";
#for ($d = $howmanyupdates; $d >= 1; $d--) {
print "start";
$c = $x * 2;
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
print "\n" . "b" . $b . "c" . $c . "d" . $d . "x" . $x . "\n";

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


if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
}
#}
#}
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status3" . $status3 . "\n";


$status4 = $status[3];
$status4 = substr($status4,9);
print "\n" . "status4" . $status4 . "\n";


$status5 = $status[4];
$status5 = substr($status5,9);
print "\n" . "status5" . $status5 . "\n";


$status6 = $status[5];
$status6 = substr($status6,9);
print "\n" . "status6" . $status6 . "\n";

$status7 = $status[6];
$status7 = substr($status7,9);
print "\n" . "status7" . $status7 . "\n";

$status8 = $status[7];
$status8 = substr($status8,9);
print "\n" . "status8" . $status8 . "\n";

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

   $date4 = $date[3];
$date4 = strip_tags($date4);
$date4 = trim(str_replace("&nbsp;Date:","",$date4));


   $date5 = $date[4];
$date5 = strip_tags($date5);
$date5 = trim(str_replace("&nbsp;Date:","",$date5));

   $date6 = $date[5];
$date6 = strip_tags($date6);
$date6 = trim(str_replace("&nbsp;Date:","",$date6));

   $date7 = $date[6];
$date7 = strip_tags($date7);
$date7 = trim(str_replace("&nbsp;Date:","",$date7));


   $date8 = $date[7];
$date8 = strip_tags($date8);
$date8 = trim(str_replace("&nbsp;Date:","",$date8));



#unset($date);
#unset($status);

#}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
   $moredetails["status2"] = $status2;
 $moredetails["status3"] = $status3;
 $moredetails["status4"] = $status4;
 $moredetails["status5"] = $status5;
 $moredetails["status6"] = $status6;
 $moredetails["status7"] = $status7;
 $moredetails["status8"] = $status8;
    $moredetails["published"] = $published;
    $moredetails["date1"] = $date1;
 $moredetails["date2"] = $date2;
 $moredetails["date3"] = $date3;
 $moredetails["date4"] = $date4;
 $moredetails["date5"] = $date5;
 $moredetails["date6"] = $date6;
 $moredetails["date7"] = $date7;
 $moredetails["date8"] = $date8;
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
   "Status4" => $moredetails["status4"],
"Status5" => $moredetails["status5"],
"Status6" => $moredetails["status6"],
     "Date4" => $moredetails["date4"],
     "Date5" => $moredetails["date5"],


"Status7" => $moredetails["status7"],
"Status8" => $moredetails["status8"],
"Status9" => $moredetails["status9"],
"Status10" => $moredetails["status10"],
     "Date6" => $moredetails["date6"],
     "Date7" => $moredetails["date7"],

 "Date8" => $moredetails["date8"],

    "Date9" => $moredetails["date9"],
 "Date10" => $moredetails["date10"],
     "Corpname" => $moredetails["corpname"],
"Published" => $moredetails["published"]
                    );
}
#}

#scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`url` string,`name` string, `refnumber` string, `title` string, `status` string, `submittedby` string, `petitiontext` string, `status1` string, `status2` string, `status3` string, `status4` string, `status5` string, `status6` string, `status7` string, `status8` string, `status9` string, `status10` string, `date1` string, `date2` string, `date3` string, `date4` string, `date5` string, `date6` string, `date7` string, `date8` string, `date9` string, `date10` string, `corpname` string, `published` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $refnumber => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:url, :name, :refnumber, :title, :status, :submittedby, :petitiontext, :status1, :status2, :status3, :status4, :status5, :status6, :status7, :status8, :status9, :status10,  :date1, :date2, :date3, :date4, :date5, :date6, :date7, :date8, :date9, :date10, :corpname, :published)",  #, :email, :phone, :mobile, :image, :address)", 
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
   "status4"  => $values["Status4"],
 "status5"  => $values["Status5"],
   "status6"  => $values["Status6"],
 "status7"  => $values["Status7"],
   "status8"  => $values["Status8"],
 "status9"  => $values["Status9"],
   "status10"  => $values["Status10"],
                     "date1"  => $values["Date1"],
     "date2"  => $values["Date2"],
 "date3"  => $values["Date3"],
     "date4"  => $values["Date4"],
 "date5"  => $values["Date5"],                
     "date6"  => $values["Date6"],
 "date7"  => $values["Date7"],                 
     "date8"  => $values["Date8"],
 "date9"  => $values["Date9"],                 
     "date10"  => $values["Date10"],
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



$date = array();
$status = array();

$x = 0;
$b = $howmanyupdates - 1;
for ($x = 0; $x < $howmanyupdates; $x++) {
print "howmanyupdates" . $howmanyupdates . "\n";
#for ($d = $howmanyupdates; $d >= 1; $d--) {
print "start";
$c = $x * 2;
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
print "\n" . "b" . $b . "c" . $c . "d" . $d . "x" . $x . "\n";

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


if (is_numeric($status[$b]) || ($status[$b] == 0 )) {
$status[$b] = "";
}
if (is_numeric($date[$b]) || ($status[$b] == 0 )) {
$date[$b] = "";
}

$b--;
}
#}
#}
$status1 = $status[0];
$status1 = substr($status1,9);
print "\n" . "status1" . $status1 . "\n";

$status2 = $status[1];
$status2 = substr($status2,9);
print "\n" . "status2" . $status2 . "\n";

$status3 = $status[2];
$status3 = substr($status3,9);
print "\n" . "status3" . $status3 . "\n";


$status4 = $status[3];
$status4 = substr($status4,9);
print "\n" . "status4" . $status4 . "\n";


$status5 = $status[4];
$status5 = substr($status5,9);
print "\n" . "status5" . $status5 . "\n";


$status6 = $status[5];
$status6 = substr($status6,9);
print "\n" . "status6" . $status6 . "\n";

$status7 = $status[6];
$status7 = substr($status7,9);
print "\n" . "status7" . $status7 . "\n";

$status8 = $status[7];
$status8 = substr($status8,9);
print "\n" . "status8" . $status8 . "\n";

$status9 = $status[8];
$status9 = substr($status9,9);
print "\n" . "status9" . $status9 . "\n";

$status10 = $status[9];
$status10 = substr($status10,9);
print "\n" . "status10" . $status10 . "\n";
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

   $date4 = $date[3];
$date4 = strip_tags($date4);
$date4 = trim(str_replace("&nbsp;Date:","",$date4));


   $date5 = $date[4];
$date5 = strip_tags($date5);
$date5 = trim(str_replace("&nbsp;Date:","",$date5));

   $date6 = $date[5];
$date6 = strip_tags($date6);
$date6 = trim(str_replace("&nbsp;Date:","",$date6));

   $date7 = $date[6];
$date7 = strip_tags($date7);
$date7 = trim(str_replace("&nbsp;Date:","",$date7));


   $date8 = $date[7];
$date8 = strip_tags($date8);
$date8 = trim(str_replace("&nbsp;Date:","",$date8));


   $date9 = $date[8];
$date9 = strip_tags($date9);
$date9 = trim(str_replace("&nbsp;Date:","",$date9));


   $date10 = $date[9];
$date10 = strip_tags($date10);
$date10 = trim(str_replace("&nbsp;Date:","",$date10));




#unset($date);
#unset($status);

#}




#$detailslength = count($cllrdetails);

$moredetails = array();    
    $moredetails["submittedby"] = $submittedby;
    $moredetails["petitiontext"] = $petitiontext;
    $moredetails["corpname"] = $corpname;
   $moredetails["status1"] = $status1;
   $moredetails["status2"] = $status2;
 $moredetails["status3"] = $status3;
 $moredetails["status4"] = $status4;
 $moredetails["status5"] = $status5;
 $moredetails["status6"] = $status6;
 $moredetails["status7"] = $status7;
 $moredetails["status8"] = $status8;
 $moredetails["status9"] = $status9;
 $moredetails["status10"] = $status10;
    $moredetails["published"] = $published;
    $moredetails["date1"] = $date1;
 $moredetails["date2"] = $date2;
 $moredetails["date3"] = $date3;
 $moredetails["date4"] = $date4;
 $moredetails["date5"] = $date5;
 $moredetails["date6"] = $date6;
 $moredetails["date7"] = $date7;
 $moredetails["date8"] = $date8;
 $moredetails["date9"] = $date9;
 $moredetails["date10"] = $date10;
#    unset($addressbits,$address,$emailbits,$email,$phonebits,$phone,$mobilebits,$mobile,$faxbits,$fax);
  
    return($moredetails);

}




?>
