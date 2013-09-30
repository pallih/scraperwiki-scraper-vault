<?php

require 'scraperwiki/simple_html_dom.php';

// Singleton Council ePlanning scraper
// (ICON Software Solutions PlanningXchange)
// Sourced from http://portal.singleton.nsw.gov.au/eplanning/pages/xc.track/SearchApplication.aspx?ss=sq
// Formatted for http://www.planningalerts.org.au/

date_default_timezone_set('Australia/Sydney');

$date_format = 'Y-m-d';
$cookie_file = '/tmp/cookies.txt';
$comment_url = 'mailto:ssc@singleton.nsw.gov.au';
$terms_url = 'http://portal.singleton.nsw.gov.au/eplanning/Common/Common/Terms.aspx';
$rss_feed = 'http://portal.singleton.nsw.gov.au/eplanning/pages/XC.Track/SearchApplication.aspx?o=rss&d=last14days&t=8&k=LodgementDate';

print "Scraping portal.singleton.nsw.gov.au...\n";

accept_terms($terms_url, $cookie_file);

// Download and parse RSS feed (last 14 days of applications)
$curl = curl_init($rss_feed);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$rss_response = curl_exec($curl);
curl_close($curl);

$rss = simplexml_load_string($rss_response);

// Iterate through each application
foreach ($rss->channel->item as $item)
{
    // RSS title appears to be the council reference
    $rss_title = explode('-', $item->title);
    $council_reference = trim($rss_title[0]);

    $existingRecords = scraperwiki::select("* from swdata where `council_reference`='" . $council_reference . "'");
    if (sizeof($existingRecords) == 0)
    {
        if (trim($item->category) == "DEVELOPMENT APPLICATION")
        {
            // RSS description appears to be the address followed by the actual description
            $rss_description = preg_split('/\./', $item->description, 2);
            $address = trim($rss_description[0]);
            $description = trim(html_entity_decode($rss_description[1]));
        
            $info_url = trim((string)$item->link);
        
            $date_scraped = date($date_format);
            $date_received = date($date_format, strtotime($item->pubDate));
        
            $curl = curl_init($info_url);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curl, CURLOPT_COOKIEJAR, '/tmp/cookies.txt');
            curl_setopt($curl, CURLOPT_COOKIEFILE, '/tmp/cookies.txt');
            $application_response = curl_exec($curl);
            curl_close($curl);      
        
            $on_notice_from = '';
            $on_notice_to = '';
            $on_notice_matched = preg_match('/^.*<td.*>Notify Adjoining Owners.*<\/td>.*<td.*>(\d\d\/\d\d\/\d\d\d\d)<\/td>.*<td.*>(\d\d\/\d\d\/\d\d\d\d)<\/td>.*$/msU', $application_response, $on_notice_matches);
            if ($on_notice_matched)
            {
                $on_notice_from = date_format(date_create_from_format('d/m/Y', $on_notice_matches[1]), $date_format);
                $on_notice_to = date_format(date_create_from_format('d/m/Y', $on_notice_matches[2]), $date_format);
            }
        
            $application = array(
                'council_reference' => $council_reference,
                'address' => $address,
                'description' => $description,
                'info_url' => $info_url,
                'comment_url' => $comment_url,
                'date_scraped' => $date_scraped,
                'date_received' => $date_received,
                'on_notice_from' => $on_notice_from,
                'on_notice_to' => $on_notice_to
            );
    
            scraperwiki::save(array('council_reference'), $application);
        }
    }
    else
    {
        print ("Skipping already saved record " . $council_reference . "\n");
    }
}

function accept_terms($terms_url, $cookie_file)
{
    $curl = curl_init($terms_url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_COOKIEJAR, $cookie_file);
    curl_setopt($curl, CURLOPT_COOKIEFILE, $cookie_file);
    $terms_response = curl_exec($curl);
    curl_close($curl);
    
    preg_match('/<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*)" \/>/', $terms_response, $viewstate_matches);
    $viewstate = $viewstate_matches[1];
    
    preg_match('/<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*)" \/>/', $terms_response, $eventvalidation_matches);
    $eventvalidation = $eventvalidation_matches[1];
    
    $postfields = array();
    $postfields['__VIEWSTATE'] = $viewstate;
    $postfields['__EVENTVALIDATION'] = $eventvalidation;
    $postfields['ctl00$ctMain1$BtnAgree'] = 'I Agree';
    $postfields['ctl00$ctMain1$chkAgree$ctl02'] = 'on';
    
    $curl = curl_init($terms_url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_POST, 1); 
    curl_setopt($curl, CURLOPT_POSTFIELDS, $postfields); 
    curl_setopt($curl, CURLOPT_COOKIEJAR, $cookie_file);
    curl_setopt($curl, CURLOPT_COOKIEFILE, $cookie_file);
    curl_exec($curl);
    curl_close($curl);
}
?><?php

require 'scraperwiki/simple_html_dom.php';

// Singleton Council ePlanning scraper
// (ICON Software Solutions PlanningXchange)
// Sourced from http://portal.singleton.nsw.gov.au/eplanning/pages/xc.track/SearchApplication.aspx?ss=sq
// Formatted for http://www.planningalerts.org.au/

date_default_timezone_set('Australia/Sydney');

$date_format = 'Y-m-d';
$cookie_file = '/tmp/cookies.txt';
$comment_url = 'mailto:ssc@singleton.nsw.gov.au';
$terms_url = 'http://portal.singleton.nsw.gov.au/eplanning/Common/Common/Terms.aspx';
$rss_feed = 'http://portal.singleton.nsw.gov.au/eplanning/pages/XC.Track/SearchApplication.aspx?o=rss&d=last14days&t=8&k=LodgementDate';

print "Scraping portal.singleton.nsw.gov.au...\n";

accept_terms($terms_url, $cookie_file);

// Download and parse RSS feed (last 14 days of applications)
$curl = curl_init($rss_feed);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$rss_response = curl_exec($curl);
curl_close($curl);

$rss = simplexml_load_string($rss_response);

// Iterate through each application
foreach ($rss->channel->item as $item)
{
    // RSS title appears to be the council reference
    $rss_title = explode('-', $item->title);
    $council_reference = trim($rss_title[0]);

    $existingRecords = scraperwiki::select("* from swdata where `council_reference`='" . $council_reference . "'");
    if (sizeof($existingRecords) == 0)
    {
        if (trim($item->category) == "DEVELOPMENT APPLICATION")
        {
            // RSS description appears to be the address followed by the actual description
            $rss_description = preg_split('/\./', $item->description, 2);
            $address = trim($rss_description[0]);
            $description = trim(html_entity_decode($rss_description[1]));
        
            $info_url = trim((string)$item->link);
        
            $date_scraped = date($date_format);
            $date_received = date($date_format, strtotime($item->pubDate));
        
            $curl = curl_init($info_url);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($curl, CURLOPT_COOKIEJAR, '/tmp/cookies.txt');
            curl_setopt($curl, CURLOPT_COOKIEFILE, '/tmp/cookies.txt');
            $application_response = curl_exec($curl);
            curl_close($curl);      
        
            $on_notice_from = '';
            $on_notice_to = '';
            $on_notice_matched = preg_match('/^.*<td.*>Notify Adjoining Owners.*<\/td>.*<td.*>(\d\d\/\d\d\/\d\d\d\d)<\/td>.*<td.*>(\d\d\/\d\d\/\d\d\d\d)<\/td>.*$/msU', $application_response, $on_notice_matches);
            if ($on_notice_matched)
            {
                $on_notice_from = date_format(date_create_from_format('d/m/Y', $on_notice_matches[1]), $date_format);
                $on_notice_to = date_format(date_create_from_format('d/m/Y', $on_notice_matches[2]), $date_format);
            }
        
            $application = array(
                'council_reference' => $council_reference,
                'address' => $address,
                'description' => $description,
                'info_url' => $info_url,
                'comment_url' => $comment_url,
                'date_scraped' => $date_scraped,
                'date_received' => $date_received,
                'on_notice_from' => $on_notice_from,
                'on_notice_to' => $on_notice_to
            );
    
            scraperwiki::save(array('council_reference'), $application);
        }
    }
    else
    {
        print ("Skipping already saved record " . $council_reference . "\n");
    }
}

function accept_terms($terms_url, $cookie_file)
{
    $curl = curl_init($terms_url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_COOKIEJAR, $cookie_file);
    curl_setopt($curl, CURLOPT_COOKIEFILE, $cookie_file);
    $terms_response = curl_exec($curl);
    curl_close($curl);
    
    preg_match('/<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*)" \/>/', $terms_response, $viewstate_matches);
    $viewstate = $viewstate_matches[1];
    
    preg_match('/<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*)" \/>/', $terms_response, $eventvalidation_matches);
    $eventvalidation = $eventvalidation_matches[1];
    
    $postfields = array();
    $postfields['__VIEWSTATE'] = $viewstate;
    $postfields['__EVENTVALIDATION'] = $eventvalidation;
    $postfields['ctl00$ctMain1$BtnAgree'] = 'I Agree';
    $postfields['ctl00$ctMain1$chkAgree$ctl02'] = 'on';
    
    $curl = curl_init($terms_url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_POST, 1); 
    curl_setopt($curl, CURLOPT_POSTFIELDS, $postfields); 
    curl_setopt($curl, CURLOPT_COOKIEJAR, $cookie_file);
    curl_setopt($curl, CURLOPT_COOKIEFILE, $cookie_file);
    curl_exec($curl);
    curl_close($curl);
}
?>