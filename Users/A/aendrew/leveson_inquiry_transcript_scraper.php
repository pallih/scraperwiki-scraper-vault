<?php

/*
    Leveson Inquiry Scraper
        by Ændrew Rininsland

    Licensed under the GPLv2

   Yay.

*/

function transcriptToXML_beta( $string, $filename ) { // beta is just to emphasize lack of torough testing
    $lines = explode( "\n", $string ); // split text into an array array of lines

    // these vars will hold the data we need to build our XML
    $date = ''; // the date of the transcript
    $time = ''; // transcript time
    $page = 1; // this will hold the current page number

    $linenr = ''; // this will hold the line nr
    $speaker = ''; // the name of the speaker
    $text = ''; // transcribed text attributed to the speaker
    $new = false; // will be true if a new item has been matched
    $event = ''; // this will hold notes that are in a quote but need to be stored separately (events)

    $xml = ''; // this will be the XML string
    $i = 0; // count the lines to display actual line number for debugging
    foreach( $lines as $line ) { // loop over lines
        $i++;
        if( !preg_match( "/[[:graph:]]/", $line ) ) { // line is empty, does not contain printable characters....
            continue; // ....so we skip to the next one
        }

        if( preg_match( "/^\h*\d+\h+(?P<date>[a-z]+,\h+\d+\h+[a-z]+\h\d{4})\s*$/i", $line, $match ) ) { # it looks like a date
            $date = $match['date']; // set date
            $speaker = ''; // reset vars
            $text = '';
            continue;// no need to handle this line any further
        } elseif( preg_match( "/^\h*\d+\h+([A-Z]+(?:\s+[A-Z]+){0,4}\h+\(.*?\)|(?i:questions\h+by)[A-Z\h]+)\s*$/", $line, $match ) ) { # (qued) event, uppercase text followed by text between parentheses
            $event .= "    <event page=\"{$page}\" line=\"{$linenr}\">{$match[1]}</event>\n"; // add entry to que, to be added after current quote
            continue;// no need to handle this line any further
        } elseif( preg_match( "/^\h*(\d*)\h*\(\h*(?P<time>\d{1,2}[:.]\d{1,2}\h*[ap]m)\)\s*$/i", $line, $match ) ) { # seems we have a time entry
            $time = $match['time']; // set date
            $xml .= "    <time page=\"{$page}\" line=\"{$match[1]}\">" . strtoupper( str_replace( '.', ':', $match['time'] ) ) . "</time>\n"; // add time as entry
            $speaker = ''; // reset vars
            $text = '';
            continue;// no need to handle this line any further
        } elseif( preg_match( "/^\h*(\d+)\s*$/", $line, $match ) && $match[1] >= $page ) { # line has just one or more digits, we assume its a pagenr
            $page = (int) $match[1] + 1; // set pagenr, add one because the nr is at the bottom of the page
            continue;// no need to handle this line any further
        } elseif( preg_match( "/^\h*\d+\s+\(([[:print:]]+)\)\s*$/", $line, $match ) && !$speaker ) { # note, text is between parentheses
            $xml .= "    <event page=\"{$page}\" line=\"{$linenr}\">{$match[1]}</event>\n"; // add entry as note
            continue;// no need to handle this line any further
        } elseif( preg_match( "/^\h*\d+\h+[A-Z\h]+\(.*?\)\s*$/", $line, $match ) && !$speaker ) { # note, uppercase text followed by text between parentheses, only if not in quote
            $xml .= "    <event type=\"note\" speaker=\"\" page=\"{$page}\" line=\"{$linenr}\">{$match[1]}</event>\n"; // add entry as note
            continue;// no need to handle this line any further
        } elseif( preg_match("/^\h*(?P<linenr>\d+)\h+(?P<speaker>(?:\h[A-Z]+(?:\h[A-Z]+){0,4}))[:.]\h*(?P<text>[[:print:]]+?)\s*$/", $line, $match ) ) { # new speaker entry
            if( $new && $speaker ) { // if we have one open we need to add it first
                $xml .= "    <entry type=\"quote\" speaker=\"{$speaker}\" page=\"{$page}\" line=\"{$linenr}\">$text</entry>\n"; // add quote
                $new = false; // reset
                if( $event ) { // if we have a qued note we need to add that too
                    $xml .= $event; // add entry to XML string
                    $event = ''; // clear 'que'
                }
            }
            $speaker = trim( $match['speaker'] ); // assign match to speaker var
            $linenr = (int) $match['linenr']; // assign line number
            $text = trim( $match['text'] ); // assign text
            $new = true; // set new match bool
        } elseif( preg_match( "/^\h*(?P<linenr>\d+)\h+(?P<text>[[:print:]]+?)\s*$/", $line, $match ) ) { # follow up text
            $text .= ' ' . trim( $match['text'] ); // append text
        } else { # unkown line (add check for linenr only lines or remove $match[1] >= $page from the pagenr match conditional)
            // not sure what kind of line this is... add it as a separate 'type'?!
            trigger_error( "Unable to parse line {$filename}, {$i} \"{$line}\"" ); // throw exception / trigger error
            continue; // no need to handle this line any further
        }

        if( !$new && $speaker ) {
            $xml .= "    <entry type=\"quote\" speaker=\"{$speaker}\" page=\"{$page}\" line=\"{$linenr}\">$text</entry>\n";
            $speaker = ''; // reset vars
            $text = '';
            $new = false;
            if( $event ) { // if we have a qued note we need to add that too
                $xml .= $event; // add entry to XML string
                $event = ''; // clear 'que'
            }
        }
    }

    // if we have a match open we need to handle it, this might happen because we do not assign the match in the same iteration as we matched it
    if( $new ) {
        $xml .= "    <entry type=\"quote\" speaker=\"{$speaker}\" page=\"{$page}\" line=\"{$linenr}\">$text</entry>\n";
    }

    $date = new DateTime( $date ); // instantiate datetime with the time from the transcript
    $date = date( 'Y-m-d', $date->getTimestamp() ); // format date
    // now we need to wrap the nodes in a root node
    $xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<hearing date=\"{$date}\">\n{$xml}</hearing>\n";

    return $xml; // return the XML
}


if (!file_exists('simpletest/browser.php')){ //first need to download SimpleTest
        $data = file_get_contents("http://aendrew.com/sites/all/libraries/simpletest_1.1alpha3.tar.gz"); 
        file_put_contents("simpletest.tar.gz", $data);
        exec('tar -xzvf simpletest.tar.gz');
}

require_once('simpletest/browser.php'); //for some ridiculous reason, scraperwiki::scrape doesn't work with the evidence listings.
$savedata = array();
$doc = new DOMDocument();
$doc->preserveWhiteSpace = false;
$leveson_evidence_html = scraperwiki::scrape('http://www.levesoninquiry.org.uk/evidence/');
$leveson_evidence_html = preg_replace("#id='fs-year'#", '', $leveson_evidence_html);
$doc->loadHTML($leveson_evidence_html);
$evidence_sidebar = new DOMXPath($doc);
$xpath = "//div[@class='sidebar']/div/ul/li/a"; //arrived at via XPath Helper Chrome plugin. There may be a simpler query than this.
$hearings_links = $evidence_sidebar->query($xpath);
foreach ($hearings_links as $link) { //get URLs of each hearing date...
    $hearing_urls[] = 'http://www.levesoninquiry.org.uk' . $link->getAttribute('href');
}

//print_r($hearing_urls);

foreach ($hearing_urls as $url) { //scrape each hearing day result page for document links...
    $i = 0;
    $browser = new SimpleBrowser();
    $browser->useCookies();
    @$browser->get($url); 
    $html_content = $browser->getContent();
    $hearing_page = new DOMDocument();
    $hearing_page->preserveWhiteSpace = false;
    $hearing_page->loadHTML($html_content);

    $transcript_links_list = new DOMXPath($hearing_page);
    $links_xpath = "//tr/td[2]/div/p/a";
    $evidence_links = $transcript_links_list->query($links_xpath);
    //echo $evidence_links->item(0)->nodeValue;
    $evidence_date_xpath = "/html/body[@class='page page-id-73 page-parent page-template page-template-template-evidence-php section-evidence']/div[@id='main']/div[@id='innermain evidence']/div[@id='content-box']/div[@id='primary']/table[@class='wide golden-one-two']/tr/td[1]/p";
    $evidence_date_results = $transcript_links_list->query($evidence_date_xpath);
    $evidence_date = date('Y-m-d', strtotime($evidence_date_results->item(0)->nodeValue));
    foreach ($evidence_links as $elink) { //scrape each document
    if (preg_match('#Transcript#i', $elink->nodeValue) && (preg_match('#.txt#i', $elink->getAttribute('href')))) { //do only for transcripts
              //  echo $elink->nodeValue . "\n";
            $txt = file_get_contents('http://www.levesoninquiry.org.uk' . $elink->getAttribute('href'));
            $xml = transcriptToXML_beta( $txt, basename($elink->getAttribute('href') ) );           
            $savedata[] = array('id' => $i . '_' . $evidence_date, 'date' => $evidence_date, 'xml' => $xml);
            $i++;
        }
    }
}

scraperwiki::save_sqlite(array('id'), $savedata);

?>
