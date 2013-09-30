<?php
require 'scraperwiki/simple_html_dom.php';

$purchaserstable = "purchasers20121215";
scraperwiki::sqliteexecute("create table IF NOT EXISTS ".$purchaserstable." (callnumber text, company text, phone text, fax text, added text, UNIQUE (callnumber,company,phone))");

$html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/calls.nsf/pvendors?OpenView&ExpandView");
$dom = new simple_html_dom();
$dom->load($html);

$maintable = $dom->find('body table table',3);

foreach($maintable->find('tr') as $thisrow) {
    if ($thisrow->find('table')) {
        //skip it
    } elseif ($thisrow->find('a')) {
        $callnumber = $thisrow->find('td',1)->plaintext;
        //print "CALL: ".$callnumber."\n";
    } else {
        $thisrec = array();
        $thisrec['company'] = $thisrow->find('td',2)->plaintext;
        $thisrec['phone'] = $thisrow->find('td',3)->plaintext;
        $thisrec['fax'] = $thisrow->find('td',4)->plaintext;
        //print "COMPANY: ".$thisrec['company']."\n";

        $foundit = array();
        $foundit = 
            scraperwiki::select(sprintf("* FROM ".$purchaserstable." WHERE callnumber = '%s' AND company = '%s' AND phone = '%s'",
            sqlite_escape_string($callnumber),
            sqlite_escape_string($thisrec['company']),
            sqlite_escape_string($thisrec['phone'])));
        if ( isset($foundit[0]['callnumber']) ) {
            //it's already in there
        } else {
            scraperwiki::sqliteexecute(sprintf("insert into ".$purchaserstable." (callnumber,company,phone,fax,added) values('%s','%s','%s','%s',datetime('now'))",
                sqlite_escape_string($callnumber),
                sqlite_escape_string($thisrec['company']),
                sqlite_escape_string($thisrec['phone']),
                sqlite_escape_string($thisrec['fax'])));
            scraperwiki::sqlitecommit(); 
        }

    }
}

function sqlite_escape_string($a) {
    $a = preg_replace("/'/","''",$a);
    return $a;
}


?>
<?php
require 'scraperwiki/simple_html_dom.php';

$purchaserstable = "purchasers20121215";
scraperwiki::sqliteexecute("create table IF NOT EXISTS ".$purchaserstable." (callnumber text, company text, phone text, fax text, added text, UNIQUE (callnumber,company,phone))");

$html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/calls.nsf/pvendors?OpenView&ExpandView");
$dom = new simple_html_dom();
$dom->load($html);

$maintable = $dom->find('body table table',3);

foreach($maintable->find('tr') as $thisrow) {
    if ($thisrow->find('table')) {
        //skip it
    } elseif ($thisrow->find('a')) {
        $callnumber = $thisrow->find('td',1)->plaintext;
        //print "CALL: ".$callnumber."\n";
    } else {
        $thisrec = array();
        $thisrec['company'] = $thisrow->find('td',2)->plaintext;
        $thisrec['phone'] = $thisrow->find('td',3)->plaintext;
        $thisrec['fax'] = $thisrow->find('td',4)->plaintext;
        //print "COMPANY: ".$thisrec['company']."\n";

        $foundit = array();
        $foundit = 
            scraperwiki::select(sprintf("* FROM ".$purchaserstable." WHERE callnumber = '%s' AND company = '%s' AND phone = '%s'",
            sqlite_escape_string($callnumber),
            sqlite_escape_string($thisrec['company']),
            sqlite_escape_string($thisrec['phone'])));
        if ( isset($foundit[0]['callnumber']) ) {
            //it's already in there
        } else {
            scraperwiki::sqliteexecute(sprintf("insert into ".$purchaserstable." (callnumber,company,phone,fax,added) values('%s','%s','%s','%s',datetime('now'))",
                sqlite_escape_string($callnumber),
                sqlite_escape_string($thisrec['company']),
                sqlite_escape_string($thisrec['phone']),
                sqlite_escape_string($thisrec['fax'])));
            scraperwiki::sqlitecommit(); 
        }

    }
}

function sqlite_escape_string($a) {
    $a = preg_replace("/'/","''",$a);
    return $a;
}


?>
