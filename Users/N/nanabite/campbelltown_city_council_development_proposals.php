<?php

date_default_timezone_set('Australia/Sydney');
require 'scraperwiki/simple_html_dom.php';

$indexUrl = "http://www.campbelltown.nsw.gov.au/default.asp?iNavCatId=2970&iSubCatId=2971";
print("Scraping index at " . $indexUrl . "\n");
$mainUrl = scraperWiki::scrape($indexUrl);

$dom = new simple_html_dom();
$dom->load($mainUrl);
$container = $dom->find("td.copyBlock", 0);
$records = array();

foreach($container->find("a") as $link)
{
    if($link->plaintext != "")
    {
        preg_match('/^(.+)iDocID=(.+)&iNavCatID/', $link->href, $councilReferenceMatches);
        $record = array(
            'info_url' => 'http://www.campbelltown.nsw.gov.au/' . $link->href, 
            'council_reference' => $councilReferenceMatches[2],
            'address' => $link->plaintext . ", NSW"
        );

        array_push($records, $record);
    }
}

print (count($records) . " items to scrape\n");

foreach($records as $record)
{
    print("Scraping " . $record['info_url'] . "\n");

    $subUrl = scraperWiki::scrape($record['info_url']);
    $dom = new simple_html_dom();
    $dom->load($subUrl);

    $description = $dom->find("div#content", 2);
    $description = strip_tags($description);

    // Fix up random stuff
    $description = str_replace('&rsquo;', '’', $description);
    $description = str_replace('&sect;', '', $description);

    $description = html_entity_decode($description);

    // Strip excess whitespace
    $description = trim(preg_replace('/\s\s+/', ' ', $description));

    $record['description'] = substr($description, 0 , 225) . "...";
    $record['comment_url'] = 'mailto:council@campbelltown.nsw.gov.au';
    $record['date_scraped'] = date('Y-m-d');

    $searchText = array(
        '/close of business on(.+)\.(.+)Your submission should include:/i',
        '/write to council before(.+), quoting/i'
    );

    foreach($searchText as $regex)
    {
        preg_match($regex, $description, $onNoticeToMatches);
        if(sizeof($onNoticeToMatches) > 0)
        {
            $dateString = trim($onNoticeToMatches[1]);
            $record['on_notice_to'] = date('Y-m-d', strtotime($dateString));
            if($record['on_notice_to'] == '1970-01-01')
            {
                throw new Exception('On notice to date could not be determined.');
            }

            break;
        }
    }

    #$existingRecords = scraperwiki::sqliteexecute("select * from swdata where `council_reference`='" . $record['council_reference'] . "'");
    #if (sizeof($existingRecords) == 0)
    #{
        scraperwiki::save(array('council_reference'), $record);
    #}
    #else
    #{
    #    print ("Skipping already saved record " . $record['council_reference'] . "\n");
    #}
}

?>