<?php


$uri = "http://www.fixyourstreet.ie/reports?page=1";


$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape($uri);
$dom = new simple_html_dom();
$dom->load($html);
#print $html;
#for ($i = 0; $i < 1; $i++ ) {
$content = $dom->find("div[class=reports-box]");
#print $content;
print_r($content);
#}
#foreach($dom->find("div[class=reports-box]") as $cell) {
#$cell = $dom->find("div[class=reports-box]");
#$rows = $content->find("div[class=r_location]");
$rows = $content->find("div[class=rb_report]");
print "hello";

print_r($rows);
break;
#$title = $dom->find("div[class=r_details]");
#$cell = $dom->find("div[class=r_details]",1);
break;
foreach($rows as $row) {
#print $row;

$cell = $row->find("div[class=r_title]",0);

#print $title;
#print_r($title);
#$link = $title->find("a",1);
#print $link;
#print_r($link);
print "hello";
#$cell = $dom->find("div[class=r_title]");
#print $cell;
#print_r($cell);
#foreach($dom->find("div[class=r_title]") as $cell) {
print "cell" . $cell;
print_r($cell);

$titlelink = $cell->find("a",1);

print "\n". "titlelink" . $titlelink;
print_r($titlelink);
#http://www.fixyourstreet.ie/reports/view/4778
# = str_replace("086 ","086",$phonepieces);
$uid = str_replace("http://www.fixyourstreet.ie/reports/view/","",$titlelink);
$name = "id";
#$uid = "123";
    $councillors["$name"] = array(
           
            "Uid"   => $uid,
            
                    );

}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`name` string, `uid` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:name, :uid)", 
            array( 
                  
                    "name"    => $name,
                    "uid"   => $values["Uid"]
              
            )
    );
}
scraperwiki::sqlitecommit();
?><?php


$uri = "http://www.fixyourstreet.ie/reports?page=1";


$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape($uri);
$dom = new simple_html_dom();
$dom->load($html);
#print $html;
#for ($i = 0; $i < 1; $i++ ) {
$content = $dom->find("div[class=reports-box]");
#print $content;
print_r($content);
#}
#foreach($dom->find("div[class=reports-box]") as $cell) {
#$cell = $dom->find("div[class=reports-box]");
#$rows = $content->find("div[class=r_location]");
$rows = $content->find("div[class=rb_report]");
print "hello";

print_r($rows);
break;
#$title = $dom->find("div[class=r_details]");
#$cell = $dom->find("div[class=r_details]",1);
break;
foreach($rows as $row) {
#print $row;

$cell = $row->find("div[class=r_title]",0);

#print $title;
#print_r($title);
#$link = $title->find("a",1);
#print $link;
#print_r($link);
print "hello";
#$cell = $dom->find("div[class=r_title]");
#print $cell;
#print_r($cell);
#foreach($dom->find("div[class=r_title]") as $cell) {
print "cell" . $cell;
print_r($cell);

$titlelink = $cell->find("a",1);

print "\n". "titlelink" . $titlelink;
print_r($titlelink);
#http://www.fixyourstreet.ie/reports/view/4778
# = str_replace("086 ","086",$phonepieces);
$uid = str_replace("http://www.fixyourstreet.ie/reports/view/","",$titlelink);
$name = "id";
#$uid = "123";
    $councillors["$name"] = array(
           
            "Uid"   => $uid,
            
                    );

}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`name` string, `uid` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:name, :uid)", 
            array( 
                  
                    "name"    => $name,
                    "uid"   => $values["Uid"]
              
            )
    );
}
scraperwiki::sqlitecommit();
?><?php


$uri = "http://www.fixyourstreet.ie/reports?page=1";


$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape($uri);
$dom = new simple_html_dom();
$dom->load($html);
#print $html;
#for ($i = 0; $i < 1; $i++ ) {
$content = $dom->find("div[class=reports-box]");
#print $content;
print_r($content);
#}
#foreach($dom->find("div[class=reports-box]") as $cell) {
#$cell = $dom->find("div[class=reports-box]");
#$rows = $content->find("div[class=r_location]");
$rows = $content->find("div[class=rb_report]");
print "hello";

print_r($rows);
break;
#$title = $dom->find("div[class=r_details]");
#$cell = $dom->find("div[class=r_details]",1);
break;
foreach($rows as $row) {
#print $row;

$cell = $row->find("div[class=r_title]",0);

#print $title;
#print_r($title);
#$link = $title->find("a",1);
#print $link;
#print_r($link);
print "hello";
#$cell = $dom->find("div[class=r_title]");
#print $cell;
#print_r($cell);
#foreach($dom->find("div[class=r_title]") as $cell) {
print "cell" . $cell;
print_r($cell);

$titlelink = $cell->find("a",1);

print "\n". "titlelink" . $titlelink;
print_r($titlelink);
#http://www.fixyourstreet.ie/reports/view/4778
# = str_replace("086 ","086",$phonepieces);
$uid = str_replace("http://www.fixyourstreet.ie/reports/view/","",$titlelink);
$name = "id";
#$uid = "123";
    $councillors["$name"] = array(
           
            "Uid"   => $uid,
            
                    );

}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`name` string, `uid` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:name, :uid)", 
            array( 
                  
                    "name"    => $name,
                    "uid"   => $values["Uid"]
              
            )
    );
}
scraperwiki::sqlitecommit();
?><?php


$uri = "http://www.fixyourstreet.ie/reports?page=1";


$councillors = array();

require 'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape($uri);
$dom = new simple_html_dom();
$dom->load($html);
#print $html;
#for ($i = 0; $i < 1; $i++ ) {
$content = $dom->find("div[class=reports-box]");
#print $content;
print_r($content);
#}
#foreach($dom->find("div[class=reports-box]") as $cell) {
#$cell = $dom->find("div[class=reports-box]");
#$rows = $content->find("div[class=r_location]");
$rows = $content->find("div[class=rb_report]");
print "hello";

print_r($rows);
break;
#$title = $dom->find("div[class=r_details]");
#$cell = $dom->find("div[class=r_details]",1);
break;
foreach($rows as $row) {
#print $row;

$cell = $row->find("div[class=r_title]",0);

#print $title;
#print_r($title);
#$link = $title->find("a",1);
#print $link;
#print_r($link);
print "hello";
#$cell = $dom->find("div[class=r_title]");
#print $cell;
#print_r($cell);
#foreach($dom->find("div[class=r_title]") as $cell) {
print "cell" . $cell;
print_r($cell);

$titlelink = $cell->find("a",1);

print "\n". "titlelink" . $titlelink;
print_r($titlelink);
#http://www.fixyourstreet.ie/reports/view/4778
# = str_replace("086 ","086",$phonepieces);
$uid = str_replace("http://www.fixyourstreet.ie/reports/view/","",$titlelink);
$name = "id";
#$uid = "123";
    $councillors["$name"] = array(
           
            "Uid"   => $uid,
            
                    );

}
scraperwiki::sqliteexecute("drop table councillors");
scraperwiki::sqliteexecute("create table if not exists councillors (`name` string, `uid` string)");
scraperwiki::sqlitecommit();

foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:name, :uid)", 
            array( 
                  
                    "name"    => $name,
                    "uid"   => $values["Uid"]
              
            )
    );
}
scraperwiki::sqlitecommit();
?>