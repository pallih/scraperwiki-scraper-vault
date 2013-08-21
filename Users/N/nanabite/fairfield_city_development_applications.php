<?php 

date_default_timezone_set('Australia/Sydney');
require 'scraperwiki/simple_html_dom.php';

$mainUrl = scraperWiki::scrape("http://www.fairfieldcity.nsw.gov.au/default.asp?iNavCatId=7&iSubCatId=86");

$dom = new simple_html_dom();
$dom->load($mainUrl);
$container = $dom->find("#main table #content", 0);

foreach($container->find("table") as $table)
{
    $record = array();
    $record['council_reference'] = '';
    $record['description'] = '';

    foreach($table->find("td") as $cell)
    {
        if(stristr($cell->innertext, "Council DA No</strong>") > -1
            || stristr($cell->innertext, "File Number</strong>") > -1
            || stristr($cell->innertext, "Application Number</strong>") > -1
            || stristr($cell->innertext, "Council DA No:</strong>") > -1
            || stristr($cell->innertext, "File Number:</strong>") > -1
            || stristr($cell->innertext, "Application Number:</strong>") > -1
            || stristr($cell->innertext, "Council DA No.</strong>") > -1
            || stristr($cell->innertext, "File No.</strong>") > -1
            || stristr($cell->innertext, "Application No.</strong>") > -1
            || stristr($cell->innertext, "Council DA No</strong>") > -1
            || stristr($cell->innertext, "File Number</span>") > -1
            || stristr($cell->innertext, "Application Number</span>") > -1
            || stristr($cell->innertext, "Council DA No:</span>") > -1
            || stristr($cell->innertext, "File Number:</span>") > -1
            || stristr($cell->innertext, "Application Number:</span>") > -1
            || stristr($cell->innertext, "Council DA No.</span>") > -1
            || stristr($cell->innertext, "File No.</span>") > -1
            || stristr($cell->innertext, "Application No.</span>") > -1
            || stristr($cell->innertext, "<strong>Application") > -1)
        {
            $record['council_reference'] = html_entity_decode($cell->next_sibling()->plaintext);
            $record['council_reference'] = preg_replace('/[ ]/', '', $record['council_reference']);
        }

        if((stristr($cell->innertext, "Property Address</strong>") > -1
            || stristr($cell->innertext, "Location</strong>") > -1
            || stristr($cell->innertext, "Property Address</span>") > -1
            || stristr($cell->innertext, "Location</span>") > -1
            || stristr($cell->innertext, "Property Address:</strong>") > -1
            || stristr($cell->innertext, "Location:</strong>") > -1
            || stristr($cell->innertext, "Property Address:</span>") > -1
            || stristr($cell->innertext, "Location:</span>") > -1))
        {
            $record['address'] = trim(preg_replace('/[^a-zA-Z0-9 \.,]/', '', html_entity_decode($cell->next_sibling()->plaintext))) . ", NSW";
        }

        if($record['description'] == '' &&
            (stristr($cell->innertext, "Project Title</strong>") > -1
            || stristr($cell->innertext, "Development</strong>") > -1
            || stristr($cell->innertext, "Details</strong>") > -1
            || stristr($cell->innertext, "Project Title:</strong>") > -1
            || stristr($cell->innertext, "Development:</strong>") > -1
            || stristr($cell->innertext, "Exhibition:</strong>") > -1
            || stristr($cell->innertext, "Project Title</span>") > -1
            || stristr($cell->innertext, "Development</span>") > -1
            || stristr($cell->innertext, "Details</span>") > -1
            || stristr($cell->innertext, "Project Title:</span>") > -1
            || stristr($cell->innertext, "Development:</span>") > -1
            || stristr($cell->innertext, "Exhibition:</span>") > -1))
        {
            $description = trim(html_entity_decode($cell->next_sibling()->plaintext));
            $description = preg_replace('/[^a-zA-Z0-9 \.,]/', '', $description);
            if(strlen($description) > 228)
            {
                $description = substr($description, 0, 225) . "...";
            }
            
            $record['description'] = $description;
        }

        if((strstr($cell->innertext, "<strong>Date DA Lodged</strong>") > -1
            || strstr($cell->innertext, "Date DA Lodged</span>") > -1))
        {
            $record['date_received'] = date('Y-m-d', strtotime(trim(html_entity_decode($cell->next_sibling()->plaintext))));
        }

        if((strstr($cell->innertext, "<strong>Exhibition dates</strong>") > -1
            || strstr($cell->innertext, "Exhibition dates</span>") > -1
            || strstr($cell->innertext, "<strong>Exhbition dates</strong>") > -1
            || strstr($cell->innertext, "Exhbition dates</span>") > -1))
        {
            $dateString = trim(html_entity_decode($cell->next_sibling()->plaintext));
            $dateArray = preg_split('/ to /i', $dateString);
            $date = date('Y-m-d', strtotime(trim($dateArray[1])));
            if($date != '1970-01-01')
            {
                $record['on_notice_to'] = $date;
            }
            else
            {
                $dateArray = preg_split('/ - /i', $dateString);
                $date = date('Y-m-d', strtotime(trim($dateArray[1])));
                if($date != '1970-01-01')
                {
                    $record['on_notice_to'] = $date;
                }
            }
        }

        if((strstr($cell->innertext, "<strong>Exhibition Period") > -1))
        {
            $dateString = trim(html_entity_decode($cell->next_sibling()->plaintext));
            preg_match('/ from (.+) to (.+)\. Copies/i', $dateString, $dateArray);
            $date = date('Y-m-d', strtotime(trim($dateArray[2])));
            if($date != '1970-01-01')
            {
                $record['on_notice_to'] = $date;
            }
        }
    }

    $record['info_url'] = 'http://www.fairfieldcity.nsw.gov.au/default.asp?iNavCatId=7&iSubCatId=86';
    $record['comment_url'] = 'http://www.fairfieldcity.nsw.gov.au/default.asp?iDocID=6779&iNavCatID=54&iSubCatID=2249';
    $record['date_scraped'] = date('Y-m-d');

    if($record['council_reference'] != '' && $record['description'] != '')
    {
        $existingRecords = scraperwiki::select("* from swdata where `council_reference`='" . $record['council_reference'] . "'");
        if (count($existingRecords) == 0)
        {
            print ("Saving record " . $record['council_reference'] . "\n");
            //print_r ($record);
            scraperwiki::save(array('council_reference'), $record);
        }
        else
        {
            print ("Skipping already saved record " . $record['council_reference'] . "\n");
        }
    }
    else
    {
        print ("Unable to save the following record:\n");
        print_r ($record);
    }
}

?>