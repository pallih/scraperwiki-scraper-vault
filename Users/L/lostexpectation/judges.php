<?php


$uri = "http://courts.ie/courts.ie/library3.nsf/WebPageCurrentWeb/646E98A7939A4C65802576D9005652F8?OpenDocument&l=en";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


//$rows=$dom->find("div[id=ContentsFrame] p");

foreach($dom->find("div[id=ContentsFrame] p") as $cell) {
//foreach($rows as $row) {
print "\n" . "cell" . $cell;
//print "\n" . "row" . $row;

$assignmentcell = explode("<h2>",$cell);
foreach($cells as $cell) {
$assignment = $cell;
print "\n" . "assignment" . $assignment;
$judgecells = explode("<br />",$cell);

foreach($judgecells as $judgecell) {

$judge = $judgecell;
//print "\n" . "judge" . $judge;
}
        $courts["$judge"] = array(
  #     "Courttype"   => $courttype,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
            "Assignment" => $assignment
        );
  //  }
}
}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`judge` string, `assignment` string)"); #, `courttype` string, `phone` string, `mobile` string, `image` string,  `assignment` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $judge => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:judge, :assignment)",  #, :courttype, :phone, :mobile, :image, :assignment)", 
            array(  "judge"    => $judge,
        #            "courttype"    => $values["Courttype"],
        #            "court"     => $values["court"],
            #        "judge"    => $judge,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                    "assignment" => $values["Assignment"]
            )
    );
}
scraperwiki::sqlitecommit();
?><?php


$uri = "http://courts.ie/courts.ie/library3.nsf/WebPageCurrentWeb/646E98A7939A4C65802576D9005652F8?OpenDocument&l=en";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


//$rows=$dom->find("div[id=ContentsFrame] p");

foreach($dom->find("div[id=ContentsFrame] p") as $cell) {
//foreach($rows as $row) {
print "\n" . "cell" . $cell;
//print "\n" . "row" . $row;

$assignmentcell = explode("<h2>",$cell);
foreach($cells as $cell) {
$assignment = $cell;
print "\n" . "assignment" . $assignment;
$judgecells = explode("<br />",$cell);

foreach($judgecells as $judgecell) {

$judge = $judgecell;
//print "\n" . "judge" . $judge;
}
        $courts["$judge"] = array(
  #     "Courttype"   => $courttype,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
            "Assignment" => $assignment
        );
  //  }
}
}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`judge` string, `assignment` string)"); #, `courttype` string, `phone` string, `mobile` string, `image` string,  `assignment` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $judge => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:judge, :assignment)",  #, :courttype, :phone, :mobile, :image, :assignment)", 
            array(  "judge"    => $judge,
        #            "courttype"    => $values["Courttype"],
        #            "court"     => $values["court"],
            #        "judge"    => $judge,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                    "assignment" => $values["Assignment"]
            )
    );
}
scraperwiki::sqlitecommit();
?><?php


$uri = "http://courts.ie/courts.ie/library3.nsf/WebPageCurrentWeb/646E98A7939A4C65802576D9005652F8?OpenDocument&l=en";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


//$rows=$dom->find("div[id=ContentsFrame] p");

foreach($dom->find("div[id=ContentsFrame] p") as $cell) {
//foreach($rows as $row) {
print "\n" . "cell" . $cell;
//print "\n" . "row" . $row;

$assignmentcell = explode("<h2>",$cell);
foreach($cells as $cell) {
$assignment = $cell;
print "\n" . "assignment" . $assignment;
$judgecells = explode("<br />",$cell);

foreach($judgecells as $judgecell) {

$judge = $judgecell;
//print "\n" . "judge" . $judge;
}
        $courts["$judge"] = array(
  #     "Courttype"   => $courttype,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
            "Assignment" => $assignment
        );
  //  }
}
}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`judge` string, `assignment` string)"); #, `courttype` string, `phone` string, `mobile` string, `image` string,  `assignment` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $judge => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:judge, :assignment)",  #, :courttype, :phone, :mobile, :image, :assignment)", 
            array(  "judge"    => $judge,
        #            "courttype"    => $values["Courttype"],
        #            "court"     => $values["court"],
            #        "judge"    => $judge,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                    "assignment" => $values["Assignment"]
            )
    );
}
scraperwiki::sqlitecommit();
?><?php


$uri = "http://courts.ie/courts.ie/library3.nsf/WebPageCurrentWeb/646E98A7939A4C65802576D9005652F8?OpenDocument&l=en";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


//$rows=$dom->find("div[id=ContentsFrame] p");

foreach($dom->find("div[id=ContentsFrame] p") as $cell) {
//foreach($rows as $row) {
print "\n" . "cell" . $cell;
//print "\n" . "row" . $row;

$assignmentcell = explode("<h2>",$cell);
foreach($cells as $cell) {
$assignment = $cell;
print "\n" . "assignment" . $assignment;
$judgecells = explode("<br />",$cell);

foreach($judgecells as $judgecell) {

$judge = $judgecell;
//print "\n" . "judge" . $judge;
}
        $courts["$judge"] = array(
  #     "Courttype"   => $courttype,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
            "Assignment" => $assignment
        );
  //  }
}
}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`judge` string, `assignment` string)"); #, `courttype` string, `phone` string, `mobile` string, `image` string,  `assignment` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $judge => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:judge, :assignment)",  #, :courttype, :phone, :mobile, :image, :assignment)", 
            array(  "judge"    => $judge,
        #            "courttype"    => $values["Courttype"],
        #            "court"     => $values["court"],
            #        "judge"    => $judge,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                    "assignment" => $values["Assignment"]
            )
    );
}
scraperwiki::sqlitecommit();
?>