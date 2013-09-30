<?php
require 'scraperwiki/simple_html_dom.php';

print "Hello, Cloud! \n";
$index = 1;    // Initialize the Index of the datastore, so we don't overwrite duplicate donors

#$html_content = scraperwiki::scrape("https://scraperwiki.com/");
#$html = str_get_html($html_content);
#foreach ($html->find("div.featured a") as $el) {
#    print $el . "\n";
#    print $el->href . "\n";
#}


#Array( [Prospects] => CREATE TABLE Prospects (first string, last string, processedFlag integer))

$ShowTables = scraperwiki::show_tables();

scraperwiki::sqliteexecute("drop table Prospects"); #TODO: call show_tables() and check if Prospects exists first
scraperwiki::sqliteexecute("create table Prospects (first string, last string, processedFlag integer)");
scraperwiki::sqliteexecute("insert into Prospects values (?,?,?)", array("Edgar", "Williams", 0));
scraperwiki::sqliteexecute("insert into Prospects values (?,?,?)", array("Mei", "Xiao", 0));
scraperwiki::sqliteexecute("insert into Prospects values (?,?,?)", array("Christopher", "Condon", 0));

scraperwiki::sqlitecommit();

#print_r(scraperwiki::sqliteexecute("select * from Prospects "));
$Prospects = scraperwiki::select("* from Prospects ");

foreach($Prospects as $i) {
    $first = $i['first'];
    $last = $i['last'];


#$last = "Xiao"; $first = "Mei";
#$last = "Bailey"; $first = "James";
#$last = "McGregor"; $first = "John";

#$bystateDetail = scraperWiki::scrape("http://newsmeat.com/fec/bystate_result.php?last=Bailey&first=James");
$bystateResult = scraperWiki::scrape("http://newsmeat.com/fec/bystate_result.php?last=" . $last . "&first=" . $first);
$resultDom = new simple_html_dom();
$resultDom->load($bystateResult);

foreach($resultDom->find("table.content_table table[@cellpadding='3'] tr") as $resultRows){
    $resultCells = $resultRows->find("td");

    // Ignore everything that comes after the table
    if(substr(trim($resultCells[0]->plaintext), 0, 29) == "Today's Most Popular Searches"){
        break;
    }

    // We have to grab the link with a foreach even though there's only one anchor.
    if(isset($resultCells[1])) {
        foreach ($resultCells[1]->find("a") as $cityAnchors) {
            $cityLink = "http://www.newsmeat.com/fec/" . $cityAnchors->href;
#            print $cityLink . "\n";

// }    }    } // uncomment this to test just the link selection.

///*

#$bystateDetail = scraperWiki::scrape("http://newsmeat.com/fec/bystate_detail.php?st=VA&last=Bailey&first=James");
$bystateDetail = scraperWiki::scrape($cityLink);
$detailDom = new simple_html_dom();
$detailDom ->load($bystateDetail);

foreach($detailDom ->find("table.content_table table[@cellpadding='3'] tr") as $detailRows){
    $tds = $detailRows->find("td");

    // Ignore the first row in the table
    if(substr(trim($tds[0]->plaintext), 0, 12) == 'Contributor'){
        continue;
    }

    // Ignore everything that comes after the table
    if(substr($tds[0]->plaintext, 0, 16) == 'Receive an alert'){
        break;
    }

    // If the "Candidate or PAC" column doesn't mention Ron Paul, skip this row (use "===" for strict comparison)
    if(isset($tds[1]) && stripos($tds[1]->plaintext, "Paul, Ron") === false) {
        continue;
    }

    // We have to grab the link with a foreach even though there's only one anchor.
    if(isset($tds[4])) {
        foreach ($tds[4]->find("a") as $el) {
            $link = "http://www.newsmeat.com" . $el->href;
            #print $link . "\n";
        }
    }

    // Grab the name of the Contributor
    if(isset($tds[0])) {
        foreach ($tds[0]->find("b") as $el) {
            $contributor= $el->innertext;
        }
    }

    // Grab the name of the Candidate
    if(isset($tds[1])) {
        foreach ($tds[1]->find("a") as $el) {
            $candidate = $el->innertext;
        }
    }

    $record = array(
        'Index' => $index // This prevents entries from being overwritten
        ,'Contributor Name' => trim($contributor)
        ,'Contributor Full' => $tds[0]->plaintext
        ,'Candidate Name' => $candidate
        ,'Candidate Full' => $tds[1]->plaintext
        ,'Amount' => $tds[2]->plaintext
        ,'Date' => $tds[3]->plaintext
        ,'FEC Filing' => $link
    );
    #print_r($record);
    
    scraperwiki::save(array('Index'), $record);

    $index++;

}

}    }    }    // This closes the ForEach from the Link Selection

}

//*/
?><?php
require 'scraperwiki/simple_html_dom.php';

print "Hello, Cloud! \n";
$index = 1;    // Initialize the Index of the datastore, so we don't overwrite duplicate donors

#$html_content = scraperwiki::scrape("https://scraperwiki.com/");
#$html = str_get_html($html_content);
#foreach ($html->find("div.featured a") as $el) {
#    print $el . "\n";
#    print $el->href . "\n";
#}


#Array( [Prospects] => CREATE TABLE Prospects (first string, last string, processedFlag integer))

$ShowTables = scraperwiki::show_tables();

scraperwiki::sqliteexecute("drop table Prospects"); #TODO: call show_tables() and check if Prospects exists first
scraperwiki::sqliteexecute("create table Prospects (first string, last string, processedFlag integer)");
scraperwiki::sqliteexecute("insert into Prospects values (?,?,?)", array("Edgar", "Williams", 0));
scraperwiki::sqliteexecute("insert into Prospects values (?,?,?)", array("Mei", "Xiao", 0));
scraperwiki::sqliteexecute("insert into Prospects values (?,?,?)", array("Christopher", "Condon", 0));

scraperwiki::sqlitecommit();

#print_r(scraperwiki::sqliteexecute("select * from Prospects "));
$Prospects = scraperwiki::select("* from Prospects ");

foreach($Prospects as $i) {
    $first = $i['first'];
    $last = $i['last'];


#$last = "Xiao"; $first = "Mei";
#$last = "Bailey"; $first = "James";
#$last = "McGregor"; $first = "John";

#$bystateDetail = scraperWiki::scrape("http://newsmeat.com/fec/bystate_result.php?last=Bailey&first=James");
$bystateResult = scraperWiki::scrape("http://newsmeat.com/fec/bystate_result.php?last=" . $last . "&first=" . $first);
$resultDom = new simple_html_dom();
$resultDom->load($bystateResult);

foreach($resultDom->find("table.content_table table[@cellpadding='3'] tr") as $resultRows){
    $resultCells = $resultRows->find("td");

    // Ignore everything that comes after the table
    if(substr(trim($resultCells[0]->plaintext), 0, 29) == "Today's Most Popular Searches"){
        break;
    }

    // We have to grab the link with a foreach even though there's only one anchor.
    if(isset($resultCells[1])) {
        foreach ($resultCells[1]->find("a") as $cityAnchors) {
            $cityLink = "http://www.newsmeat.com/fec/" . $cityAnchors->href;
#            print $cityLink . "\n";

// }    }    } // uncomment this to test just the link selection.

///*

#$bystateDetail = scraperWiki::scrape("http://newsmeat.com/fec/bystate_detail.php?st=VA&last=Bailey&first=James");
$bystateDetail = scraperWiki::scrape($cityLink);
$detailDom = new simple_html_dom();
$detailDom ->load($bystateDetail);

foreach($detailDom ->find("table.content_table table[@cellpadding='3'] tr") as $detailRows){
    $tds = $detailRows->find("td");

    // Ignore the first row in the table
    if(substr(trim($tds[0]->plaintext), 0, 12) == 'Contributor'){
        continue;
    }

    // Ignore everything that comes after the table
    if(substr($tds[0]->plaintext, 0, 16) == 'Receive an alert'){
        break;
    }

    // If the "Candidate or PAC" column doesn't mention Ron Paul, skip this row (use "===" for strict comparison)
    if(isset($tds[1]) && stripos($tds[1]->plaintext, "Paul, Ron") === false) {
        continue;
    }

    // We have to grab the link with a foreach even though there's only one anchor.
    if(isset($tds[4])) {
        foreach ($tds[4]->find("a") as $el) {
            $link = "http://www.newsmeat.com" . $el->href;
            #print $link . "\n";
        }
    }

    // Grab the name of the Contributor
    if(isset($tds[0])) {
        foreach ($tds[0]->find("b") as $el) {
            $contributor= $el->innertext;
        }
    }

    // Grab the name of the Candidate
    if(isset($tds[1])) {
        foreach ($tds[1]->find("a") as $el) {
            $candidate = $el->innertext;
        }
    }

    $record = array(
        'Index' => $index // This prevents entries from being overwritten
        ,'Contributor Name' => trim($contributor)
        ,'Contributor Full' => $tds[0]->plaintext
        ,'Candidate Name' => $candidate
        ,'Candidate Full' => $tds[1]->plaintext
        ,'Amount' => $tds[2]->plaintext
        ,'Date' => $tds[3]->plaintext
        ,'FEC Filing' => $link
    );
    #print_r($record);
    
    scraperwiki::save(array('Index'), $record);

    $index++;

}

}    }    }    // This closes the ForEach from the Link Selection

}

//*/
?>