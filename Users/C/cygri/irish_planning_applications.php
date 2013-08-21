<?php

/*
 * Irish Planning Applications
 *
 * This is a scraper for the LGCSB's (old) ePlan system.
 *
 * Contributors:
 * - John Handelaar
 * - Richard Cyganiak
 * - Aftab Iqbal
 * - Gavin Sheridan
 *
 * The LGCSB's ePlan app is an aspx nightmare which forcibly paginates results
 * and refuses GETs on its search form.
 * Once we grab all received applications for the last N days, we loop through
 * only those applications in the state of 'New Application' (and ignore 'Incomplete')
 * because the City adds Irish grid references to the 'Site location' detail page.
 */

require 'scraperwiki/simple_html_dom.php';
require 'geograph/conversionslatlong.class.php';

/*
 * Setting any global vars here in order to
 * make reuse easier
 */
$recent_days = 28;
$sites = array(
    'Donegal' => "http://www.donegal.ie/DCC/iplaninternet/internetenquiry/",
    'Letterkenny' => "http://www.donegal.ie/letterkenny_eplan/internetenquiry/",
    'Bundoran' => "http://www.donegal.ie/bundoran_eplan/internetenquiry/",
    'Buncrana' => "http://www.donegal.ie/buncrana_eplan/internetenquiry/",
    'Kerry' => "http://atomik.kerrycoco.ie/ePlan/InternetEnquiry/",
    'CorkCity' => "http://planning.corkcity.ie/InternetEnquiry/",
    'GalwayCity' => "http://gis.galwaycity.ie/ePlan/InternetEnquiry/",
    'LimerickCo' => "http://www.lcc.ie/ePlan/InternetEnquiry/",
    'Longford' => "http://www.longfordcoco.ie/ePlan/InternetEnquiry/",
    'NTipperary' => "http://www.tipperarynorth.ie/iPlan/InternetEnquiry/",
    'Waterford' => "http://www.waterfordcity.ie/ePlan/InternetEnquiry/",
);

// Loop through all sites
$site_count = 0;
foreach($sites as $county => $site_url) {
    $site_count++;
    echo "Processing site $site_count of " . count($sites) . ": $county\n";
    process_site($site_url, $county, $recent_days);
}

// Process one site
function process_site($site_url, $county, $recent_days) {
    // Do search request
    $thispage = 0;
    $applications = array();
    echo "Fetching search result page for last $recent_days days\n";
    $postvars = array (
        'txtFileNum' => '',
        'txtSurname' => '',
        'ReportType' => 'RECEIVED',
        'txtLocation' => '',
        'NoDays' => $recent_days,
        'limitResults' => '0',
        'Submit5' => 'Search',
        'btnLookupFileNum' => 'Processing...',
        'distanceFrom' => '',     // for 'classic++' version of ePlan
        'selectedTown' => 'any',     // for 'classic++' version of ePlan
    );
    $curl = curl_init();
    $html = http_request($curl, $site_url . "frmSelCritSearch.asp", $postvars);
    // This is the loop for the first and all subsequent search result pages
    while (true) {
        $appsinpage = parse_search_result_page($html);
        echo "Found " . count($appsinpage) . " results in this page\n";
        $applications += $appsinpage;
        if (!has_another_page($html)) break;
        // There is more than one search result page
        $thispage++;
        echo "Fetching search result page " . ($thispage + 1) . "\n";
        $html = http_request($curl, $site_url . "frmSelCritSearch.asp?page_num=$thispage&Op=1", null);
    }
    curl_close($curl);

    // Process all applications by fetching their
    // details page (for description) and location page
    // (for easting/northing which we convert to WGS84 lat/long)
    $count = 0;
    $total = count($applications);
    foreach ($applications as $id => $app) {
        $count++;
        echo "Processing application $count of $total ($app[appref])\n";
        $app['county'] = $county;
        $app['url'] = $site_url . "rpt_ViewApplicDetails.asp?validFileNum=1&app_num_file=$id";
        $detail_html = scraperwiki::scrape($app['url']);
        $app['details'] = parse_detail_page($detail_html);
        echo " ... Got details\n";
        $location_html = scraperwiki::scrape($site_url . "rpt_ViewSiteLocDetails.asp?file_number=$id");
        $latlng = parse_location_page($location_html);
        if ($latlng) {
            $app['lat'] = floatval($latlng[0]);
            $app['lng'] = floatval($latlng[1]);
        }
        echo " ... Got location\n";
        $app = cleanup_application($app);
        echo " ... Performed cleanup\n";
        scraperwiki::save_sqlite(array('county', 'appref'), $app);
        echo " ... Saved\n";
    }
}

/*
 * A function to use instead of scraperwiki::scrape for performing POST
 * requests and for dealing with cookies
 *
 * Arguments:
 * $curl - a curl instance prepared with curl_init()
 * $url - a URL to which we will post form variables
 * $postvars - if not null, an array of keys and values containing form variables for POSTing
 */
function http_request(&$curl, $url, $postvars=NULL) {
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_COOKIEFILE, '/dev/null');   // necessary to enable cookies
    curl_setopt($curl, CURLOPT_POST, !empty($postvars));
    if ($postvars) {
        $fields = array();
        foreach($postvars as $key=>$value) {
            $fields[] = $key.'='.$value;
        }
        curl_setopt($curl, CURLOPT_POSTFIELDS, join($fields, '&'));
    }
    return curl_exec($curl);
}

function parse_search_result_page($html) {
    $dom = new simple_html_dom();
    $dom->load($html);
    $apps = array();
    $rows = $dom->find("table[class='AppDetailsTable'] tr");
    if (!$rows) {     // 'classic++' version of ePlan
        $rows = $dom->find("table[class='AppDetailsTable2'] tr");
    }
    foreach($rows as $row) {
        // Skip header row
        if ($row->find('th')) continue;
        $status = preg_replace("/<BR>/i", " ", strtoupper($row->children[1]->innertext));
        // Skip all states except new applications
        if ($status != 'NEW APPLICATION') continue;
        $id = trim($row->children[0]->plaintext);
        preg_match('!^(\d\d)/(\d\d)/(\d\d\d\d)!', $row->children[4]->plaintext, $match);
        $apps[$id] = array(
            'appref'    => substr($id,0,2) . "/" . substr($id,2),
            'date'      => $match[3] . '-' . $match[2] . '-' . $match[1],
            'applicant' => trim($row->children[5]->plaintext),
            'address'   => trim(preg_replace("/<br>/i", "\n", $row->children[6]->innertext)),
        );
    }
    return $apps;
}

function parse_detail_page($html) {
    $dom = new simple_html_dom();
    $dom->load($html);
    $details = $dom->find("table[class='AppDetailsTable'] tr",15)->children(1)->plaintext;
    return $details;
}

function parse_location_page($html) {
    if (stristr($html,"No Site Location Details Found")) {
        return false;
    }
    $dom = new simple_html_dom();
    $dom->load($html);
    $northing = round(floatval($dom->find("table[class='AppDetailsTable'] tr",1)->children(1)->plaintext));
    $easting  = round(floatval($dom->find("table[class='AppDetailsTable'] tr",1)->children(4)->plaintext));
    // Sometimes, easting and northing are 0 even when a site location page exists
    if ($northing == 0 || $easting == 0) return false;
    $geo = new ConversionsLatLong();
    return $geo->irish_to_wgs84($easting, $northing);
}

function has_another_page($html) {
    if (!preg_match("/Currently viewing page (\d+) of (\d+)/", $html, $match)) return false;
    return intval($match[1]) < intval($match[2]);
}

function cleanup_application($app) {
    // Make application reference all upper-case: fs/12110 => FS/12110
    $app['appref'] = strtoupper($app['appref']);
    // Remove excess punctuation and whitespace from addresses
    $app['address'] = preg_replace('/[., ]+$/', '', preg_replace('/[, ]*\n/m', "\n", $app['address']));
    // Remove excess punctuation and whitespace from end of applicant name
    $app['applicant'] = preg_replace('/[, ]+$/', '', $app['applicant']);
    // First letter of details should be upper-case
    $app['details'] = ucfirst($app['details']);
    return $app;
}