<?php

$site_url = 'http://www.galway.ie/PlanningSearch';

function get_search_html($start_date, $end_date, $status = 'received_date') {
    global $site_url;
    $url = "$site_url/PlanningApps.taf?_function=list&_type=adv";
    $postvars = array(
        'datefield' => $status,
        'date1' => '31/12/1990',
        'date2' => '31/12/1990',
    );
    print http_request($url, $postvars);
}

/*
 * A function to use instead of scraperwiki::scrape for performing POST
 * requests and for dealing with cookies
 *
 * Arguments:
 * $url - a URL to which we will post form variables
 * $postvars - if not null, an array of keys and values containing form variables for POSTing
 */
function http_request($url, $postvars=NULL) {
    $curl = curl_init();
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
<?php

$site_url = 'http://www.galway.ie/PlanningSearch';

function get_search_html($start_date, $end_date, $status = 'received_date') {
    global $site_url;
    $url = "$site_url/PlanningApps.taf?_function=list&_type=adv";
    $postvars = array(
        'datefield' => $status,
        'date1' => '31/12/1990',
        'date2' => '31/12/1990',
    );
    print http_request($url, $postvars);
}

/*
 * A function to use instead of scraperwiki::scrape for performing POST
 * requests and for dealing with cookies
 *
 * Arguments:
 * $url - a URL to which we will post form variables
 * $postvars - if not null, an array of keys and values containing form variables for POSTing
 */
function http_request($url, $postvars=NULL) {
    $curl = curl_init();
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
