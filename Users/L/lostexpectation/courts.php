<?php

$court = "Foo Bar county Council";
$uri = "http://courts.ie/offices.nsf/WebCOByJurisdiction?OpenView&Start=1&Count=59&Expand=4#4";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
#$e->children(1)
$rows=$dom->find("div[id=ContentsFrame] table tr");
//$rows=$dom->find("div[id=ContentsFrame] table tr")->children[1]->id;
//$rows=$dom->find("div[id=ContentsFrame] table")->children[1]->id;
//$rows=$dom->find("td[class=viewtable] table tbody tr");
//$rows=$dom->find("div[id=ContentsFrame]")->last_child();
//$rows=$dom->find("div[id=ContentsFrame]")->children(1)->children(2)->id;
//print_r($rows);
unset($rows[0]);
//unset($rows[1]);
foreach($rows as $row) {
//print "\n" . "row" . $row;

$rowbs=$row->find("table tr");
unset($rowbs[0]);
unset($rowbs[1]);
unset($rowbs[2]);
foreach($rowbs as $rowb) {

//print "\n" . "rowb" . $rowb;
//$rowcs=$rowb->find("table tr");
//foreach($rowcs as $rowc) {
//print "\n" . "rowc" . $row;
$courtcell = $rowb->find("td",0); #->innertext;
$court = $courtcell;
$court = "district";
//$rowcs=$rowb->find("tbody tr");
//foreach($rowcs as $rowc) {
//$jurisdictioncell = $rowc->find("td",0);
$jurisdictioncell = $rowb->find("td",1)->innertext;
//$jurisdictioncell = $rowb->find("td",0); #->innertext;
$jurisdiction = strip_tags($jurisdictioncell);
//print "\n" . "jurisdictioncell" . $jurisdictioncell;
$urlcell = $rowb->find('td a',0); #->innertext;
//$urlcell = $jurisdictioncell->find('a',1);
//$namecell = $row->find("td a",0);
//print "\n" . "rowb" . $rowb;
//$urlcell = str_replace('<img src="/icons/ecblank.gif" border="0" height="1" width="16" alt="">','',$urlcell);
//print "\n" . "urlcell" . $urlcell;
//$urlcell = $urlcell->find("a",1)->innertext;
//$jurisdiction = "jurisdiction";
//$jurisdiction = $jurisdictioncell;
//$addresscell = $rowc->find("td a",0);
//$address = "address";
// http://courts.ie/offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
///offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
$url = "http://courts.ie" . $urlcell->href;

//print "\n" . "url" . $url;
//unset($dom,$html,$url);
$moredetails = get_extras($url);
print "\n" . "addressb" . $address;
        $courts["$jurisdiction"] = array(
       "Court"   => $court,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
        "Url" =>  $url,
 "Address" => $moredetails["address"],
 "Phone" => $moredetails["phone"]
        );
    }
}
//unset($dom,$html,$url);

//}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`jurisdiction` string, `court` string, `url` string, `address` string, `phone` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $jurisdiction => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:jurisdiction, :court, :url, :address, :phone)",  #, :email, :phone, :mobile, :image, :address)", 
            array(
                    "jurisdiction"    => $jurisdiction,
                    "court"    => $values["Court"],
        #            "court"     => $values["court"],
            #        "jurisdiction"    => $jurisdiction,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                      "url" => $values["Url"],
                    "address" => $values["Address"],
                  "phone" => $values["Phone"]
            
            )
    );
}
scraperwiki::sqlitecommit();



function get_extras($url) {

    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);
//$rows=$localdom->find("div[id=ContentsFrame] table tr");
$rows=$localdom->find("div[id=ContentsFrame] table tr");
//foreach($rows as $row) {
print "\n" . "url" . $url;
//print "\n" . "row" . $row;
//$rows = $row->find("table tr");
foreach($rows as $row) {
$address = $row->find("td",1);
print "\n" . "address" . $address;

$moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["phone"] = $phone;
}
//}
}
?><?php

$court = "Foo Bar county Council";
$uri = "http://courts.ie/offices.nsf/WebCOByJurisdiction?OpenView&Start=1&Count=59&Expand=4#4";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
#$e->children(1)
$rows=$dom->find("div[id=ContentsFrame] table tr");
//$rows=$dom->find("div[id=ContentsFrame] table tr")->children[1]->id;
//$rows=$dom->find("div[id=ContentsFrame] table")->children[1]->id;
//$rows=$dom->find("td[class=viewtable] table tbody tr");
//$rows=$dom->find("div[id=ContentsFrame]")->last_child();
//$rows=$dom->find("div[id=ContentsFrame]")->children(1)->children(2)->id;
//print_r($rows);
unset($rows[0]);
//unset($rows[1]);
foreach($rows as $row) {
//print "\n" . "row" . $row;

$rowbs=$row->find("table tr");
unset($rowbs[0]);
unset($rowbs[1]);
unset($rowbs[2]);
foreach($rowbs as $rowb) {

//print "\n" . "rowb" . $rowb;
//$rowcs=$rowb->find("table tr");
//foreach($rowcs as $rowc) {
//print "\n" . "rowc" . $row;
$courtcell = $rowb->find("td",0); #->innertext;
$court = $courtcell;
$court = "district";
//$rowcs=$rowb->find("tbody tr");
//foreach($rowcs as $rowc) {
//$jurisdictioncell = $rowc->find("td",0);
$jurisdictioncell = $rowb->find("td",1)->innertext;
//$jurisdictioncell = $rowb->find("td",0); #->innertext;
$jurisdiction = strip_tags($jurisdictioncell);
//print "\n" . "jurisdictioncell" . $jurisdictioncell;
$urlcell = $rowb->find('td a',0); #->innertext;
//$urlcell = $jurisdictioncell->find('a',1);
//$namecell = $row->find("td a",0);
//print "\n" . "rowb" . $rowb;
//$urlcell = str_replace('<img src="/icons/ecblank.gif" border="0" height="1" width="16" alt="">','',$urlcell);
//print "\n" . "urlcell" . $urlcell;
//$urlcell = $urlcell->find("a",1)->innertext;
//$jurisdiction = "jurisdiction";
//$jurisdiction = $jurisdictioncell;
//$addresscell = $rowc->find("td a",0);
//$address = "address";
// http://courts.ie/offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
///offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
$url = "http://courts.ie" . $urlcell->href;

//print "\n" . "url" . $url;
//unset($dom,$html,$url);
$moredetails = get_extras($url);
print "\n" . "addressb" . $address;
        $courts["$jurisdiction"] = array(
       "Court"   => $court,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
        "Url" =>  $url,
 "Address" => $moredetails["address"],
 "Phone" => $moredetails["phone"]
        );
    }
}
//unset($dom,$html,$url);

//}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`jurisdiction` string, `court` string, `url` string, `address` string, `phone` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $jurisdiction => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:jurisdiction, :court, :url, :address, :phone)",  #, :email, :phone, :mobile, :image, :address)", 
            array(
                    "jurisdiction"    => $jurisdiction,
                    "court"    => $values["Court"],
        #            "court"     => $values["court"],
            #        "jurisdiction"    => $jurisdiction,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                      "url" => $values["Url"],
                    "address" => $values["Address"],
                  "phone" => $values["Phone"]
            
            )
    );
}
scraperwiki::sqlitecommit();



function get_extras($url) {

    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);
//$rows=$localdom->find("div[id=ContentsFrame] table tr");
$rows=$localdom->find("div[id=ContentsFrame] table tr");
//foreach($rows as $row) {
print "\n" . "url" . $url;
//print "\n" . "row" . $row;
//$rows = $row->find("table tr");
foreach($rows as $row) {
$address = $row->find("td",1);
print "\n" . "address" . $address;

$moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["phone"] = $phone;
}
//}
}
?><?php

$court = "Foo Bar county Council";
$uri = "http://courts.ie/offices.nsf/WebCOByJurisdiction?OpenView&Start=1&Count=59&Expand=4#4";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
#$e->children(1)
$rows=$dom->find("div[id=ContentsFrame] table tr");
//$rows=$dom->find("div[id=ContentsFrame] table tr")->children[1]->id;
//$rows=$dom->find("div[id=ContentsFrame] table")->children[1]->id;
//$rows=$dom->find("td[class=viewtable] table tbody tr");
//$rows=$dom->find("div[id=ContentsFrame]")->last_child();
//$rows=$dom->find("div[id=ContentsFrame]")->children(1)->children(2)->id;
//print_r($rows);
unset($rows[0]);
//unset($rows[1]);
foreach($rows as $row) {
//print "\n" . "row" . $row;

$rowbs=$row->find("table tr");
unset($rowbs[0]);
unset($rowbs[1]);
unset($rowbs[2]);
foreach($rowbs as $rowb) {

//print "\n" . "rowb" . $rowb;
//$rowcs=$rowb->find("table tr");
//foreach($rowcs as $rowc) {
//print "\n" . "rowc" . $row;
$courtcell = $rowb->find("td",0); #->innertext;
$court = $courtcell;
$court = "district";
//$rowcs=$rowb->find("tbody tr");
//foreach($rowcs as $rowc) {
//$jurisdictioncell = $rowc->find("td",0);
$jurisdictioncell = $rowb->find("td",1)->innertext;
//$jurisdictioncell = $rowb->find("td",0); #->innertext;
$jurisdiction = strip_tags($jurisdictioncell);
//print "\n" . "jurisdictioncell" . $jurisdictioncell;
$urlcell = $rowb->find('td a',0); #->innertext;
//$urlcell = $jurisdictioncell->find('a',1);
//$namecell = $row->find("td a",0);
//print "\n" . "rowb" . $rowb;
//$urlcell = str_replace('<img src="/icons/ecblank.gif" border="0" height="1" width="16" alt="">','',$urlcell);
//print "\n" . "urlcell" . $urlcell;
//$urlcell = $urlcell->find("a",1)->innertext;
//$jurisdiction = "jurisdiction";
//$jurisdiction = $jurisdictioncell;
//$addresscell = $rowc->find("td a",0);
//$address = "address";
// http://courts.ie/offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
///offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
$url = "http://courts.ie" . $urlcell->href;

//print "\n" . "url" . $url;
//unset($dom,$html,$url);
$moredetails = get_extras($url);
print "\n" . "addressb" . $address;
        $courts["$jurisdiction"] = array(
       "Court"   => $court,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
        "Url" =>  $url,
 "Address" => $moredetails["address"],
 "Phone" => $moredetails["phone"]
        );
    }
}
//unset($dom,$html,$url);

//}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`jurisdiction` string, `court` string, `url` string, `address` string, `phone` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $jurisdiction => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:jurisdiction, :court, :url, :address, :phone)",  #, :email, :phone, :mobile, :image, :address)", 
            array(
                    "jurisdiction"    => $jurisdiction,
                    "court"    => $values["Court"],
        #            "court"     => $values["court"],
            #        "jurisdiction"    => $jurisdiction,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                      "url" => $values["Url"],
                    "address" => $values["Address"],
                  "phone" => $values["Phone"]
            
            )
    );
}
scraperwiki::sqlitecommit();



function get_extras($url) {

    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);
//$rows=$localdom->find("div[id=ContentsFrame] table tr");
$rows=$localdom->find("div[id=ContentsFrame] table tr");
//foreach($rows as $row) {
print "\n" . "url" . $url;
//print "\n" . "row" . $row;
//$rows = $row->find("table tr");
foreach($rows as $row) {
$address = $row->find("td",1);
print "\n" . "address" . $address;

$moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["phone"] = $phone;
}
//}
}
?><?php

$court = "Foo Bar county Council";
$uri = "http://courts.ie/offices.nsf/WebCOByJurisdiction?OpenView&Start=1&Count=59&Expand=4#4";
$html = scraperwiki::scrape($uri);

$courts = array();

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
#$e->children(1)
$rows=$dom->find("div[id=ContentsFrame] table tr");
//$rows=$dom->find("div[id=ContentsFrame] table tr")->children[1]->id;
//$rows=$dom->find("div[id=ContentsFrame] table")->children[1]->id;
//$rows=$dom->find("td[class=viewtable] table tbody tr");
//$rows=$dom->find("div[id=ContentsFrame]")->last_child();
//$rows=$dom->find("div[id=ContentsFrame]")->children(1)->children(2)->id;
//print_r($rows);
unset($rows[0]);
//unset($rows[1]);
foreach($rows as $row) {
//print "\n" . "row" . $row;

$rowbs=$row->find("table tr");
unset($rowbs[0]);
unset($rowbs[1]);
unset($rowbs[2]);
foreach($rowbs as $rowb) {

//print "\n" . "rowb" . $rowb;
//$rowcs=$rowb->find("table tr");
//foreach($rowcs as $rowc) {
//print "\n" . "rowc" . $row;
$courtcell = $rowb->find("td",0); #->innertext;
$court = $courtcell;
$court = "district";
//$rowcs=$rowb->find("tbody tr");
//foreach($rowcs as $rowc) {
//$jurisdictioncell = $rowc->find("td",0);
$jurisdictioncell = $rowb->find("td",1)->innertext;
//$jurisdictioncell = $rowb->find("td",0); #->innertext;
$jurisdiction = strip_tags($jurisdictioncell);
//print "\n" . "jurisdictioncell" . $jurisdictioncell;
$urlcell = $rowb->find('td a',0); #->innertext;
//$urlcell = $jurisdictioncell->find('a',1);
//$namecell = $row->find("td a",0);
//print "\n" . "rowb" . $rowb;
//$urlcell = str_replace('<img src="/icons/ecblank.gif" border="0" height="1" width="16" alt="">','',$urlcell);
//print "\n" . "urlcell" . $urlcell;
//$urlcell = $urlcell->find("a",1)->innertext;
//$jurisdiction = "jurisdiction";
//$jurisdiction = $jurisdictioncell;
//$addresscell = $rowc->find("td a",0);
//$address = "address";
// http://courts.ie/offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
///offices.nsf/bae2125da4ef043080256e45004d04f3/5cb75e327208271f80256e450050b9a0?OpenDocument
$url = "http://courts.ie" . $urlcell->href;

//print "\n" . "url" . $url;
//unset($dom,$html,$url);
$moredetails = get_extras($url);
print "\n" . "addressb" . $address;
        $courts["$jurisdiction"] = array(
       "Court"   => $court,
     #       "Party"   => $party,
      #      "Email"   => $email,
     #       "Phone"   => $phone,
     #       "Mobile"  => $mobile,
     #       "Image"   => $img,
        "Url" =>  $url,
 "Address" => $moredetails["address"],
 "Phone" => $moredetails["phone"]
        );
    }
}
//unset($dom,$html,$url);

//}
scraperwiki::sqliteexecute("drop table courts");
scraperwiki::sqliteexecute("create table if not exists courts (`jurisdiction` string, `court` string, `url` string, `address` string, `phone` string)"); #, `email` string, `phone` string, `mobile` string, `image` string,  `address` string)");
scraperwiki::sqlitecommit();

foreach ($courts as $jurisdiction => $values) {
    scraperwiki::sqliteexecute("insert or replace into courts values (:jurisdiction, :court, :url, :address, :phone)",  #, :email, :phone, :mobile, :image, :address)", 
            array(
                    "jurisdiction"    => $jurisdiction,
                    "court"    => $values["Court"],
        #            "court"     => $values["court"],
            #        "jurisdiction"    => $jurisdiction,
          #          "party"   => $values["Party"],
         #           "email"   => $values["Email"],
         #           "phone"   => $values["Phone"],
         #           "mobile"  => $values["Mobile"],
         #           "image"   => $values["Image"],
                      "url" => $values["Url"],
                    "address" => $values["Address"],
                  "phone" => $values["Phone"]
            
            )
    );
}
scraperwiki::sqlitecommit();



function get_extras($url) {

    $localhtml = scraperwiki::scrape($url);
    $localdom = new simple_html_dom();
    $localdom->load($localhtml);
//$rows=$localdom->find("div[id=ContentsFrame] table tr");
$rows=$localdom->find("div[id=ContentsFrame] table tr");
//foreach($rows as $row) {
print "\n" . "url" . $url;
//print "\n" . "row" . $row;
//$rows = $row->find("table tr");
foreach($rows as $row) {
$address = $row->find("td",1);
print "\n" . "address" . $address;

$moredetails = array();    
    $moredetails["address"] = $address;
    $moredetails["phone"] = $phone;
}
//}
}
?>