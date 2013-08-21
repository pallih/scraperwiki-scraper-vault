<?php

// *********
// This scraper has been replace by https://scraperwiki.com/scrapers/rockdale_city_council_development_applications_-_r/
// *********

require 'scraperwiki/simple_html_dom.php';

// Rockdale City Council ePlanning scraper
// (ICON Software Solutions PlanningXchange)
// Sourced from http://rccweb.rockdale.nsw.gov.au/EPlanning/pages/xc.track/default.aspx
// Formatted for http://www.planningalerts.org.au/

date_default_timezone_set('Australia/Sydney');

$date_format = 'Y-m-d';
$cookie_file = '/tmp/cookies.txt';
$comment_url = 'mailto:rcc@rockdale.nsw.gov.au';
$terms_url = 'http://rccweb.rockdale.nsw.gov.au/EPlanning/Common/Common/Terms.aspx';
$rss_feed = 'http://rccweb.rockdale.nsw.gov.au/EPlanning/Pages/XC.Track/SearchApplication.aspx?o=xml&d=last14days&t=217&k=LodgementDate';

print "Scraping rccweb.rockdale.nsw.gov.au...\n";

//accept_terms($terms_url, $cookie_file);

// Download and parse RSS feed (last 14 days of applications)
$curl = curl_init($rss_feed);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$rss_response = curl_exec($curl);
curl_close($curl);

print_r($rss_response);
//preg_match('/<NewDataSet>(.*)<\/NewDataSet>/', $rss_response, $match);
//print_r($match);

$rss = simplexml_load_string($rss_response);

// Iterate through each application
foreach ($rss->channel->item as $item)
{
    // RSS title appears to be the council reference
    $rss_title = explode(' ', $item->title);
    $council_reference = $rss_title[0];

    /*
        DA = Development Application
        CA = Complying Development
        CC = Construction Certificate
    */

    if (substr($council_reference, 0, 2) == "DA")
    {
        // RSS description appears to be the address followed by the actual description
        $rss_description = preg_split('/\./', $item->description, 2);
        $address = trim($rss_description[0]);
        $description = trim($rss_description[1]);
    
        $info_url = (string)$item->link;
    
        $date_scraped = date($date_format);
        $date_received = date($date_format, strtotime($item->pubDate));
    
        $curl = curl_init($info_url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_COOKIEJAR, '/tmp/cookies.txt');
        curl_setopt($curl, CURLOPT_COOKIEFILE, '/tmp/cookies.txt');
        $application_response = curl_exec($curl);
        curl_close($curl);
    
        $on_notice_matched = preg_match('/^.*<td.*>Application on Exhibition for (.*) Days.*<\/td>.*<td.*>(\d\d\/\d\d\/\d\d\d\d)<\/td>.*$/msU', $application_response, $on_notice_matches);
        if ($on_notice_matched)
        {
            $on_notice_from = date_format(date_create_from_format('d/m/Y', $on_notice_matches[2]), $date_format);
            $on_notice_to = date($date_format, strtotime($on_notice_from . " +" . $on_notice_matches[1] . " days"));
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
        print_r($application);

        //if (scraperwiki::select("* from swdata where `council_reference`='$council_reference'"))
        //{
        //    print "Skipping already saved record $council_reference";
        //}else{
        //    print "Saving $council_reference...\n";
        //    scraperwiki::save(array('council_reference'), $application);
        //}  
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