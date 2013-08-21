<?php

// This scraper gets FEC data for MN for 2012 for
// PACs and Parties      
require 'scraperwiki/simple_html_dom.php';

function unformat_money($value) {
    $formatted = floatval(str_replace(',', '', substr($value, 1)));
    return is_float($formatted) ? $formatted : 0;
}

// Get page.  This is apparently not necessary
/*
$url = "http://query.nictusa.com/cgi-bin/cancomsrs/";
$fields = array(
    'dbyear'=>urlencode('12'),
    'cancom'=>urlencode('1'),
    'state'=>urlencode('MN'),
    'submit'=>urlencode('Send Query'),
);

//url-ify the data for the POST
$fields_string = '';
foreach($fields as $key=>$value) {
    $fields_string .= $key . '=' . $value . '&';
}
rtrim($fields_string, '&');

// Make CURL request
$curl = curl_init ($url);
curl_setopt($curl, CURLOPT_URL,$url);
curl_setopt($curl, CURLOPT_POST, count($fields));
curl_setopt($curl, CURLOPT_POSTFIELDS, $fields_string);
$html = curl_exec ($curl);
curl_close ($curl);
*/

$url = "http://query.nictusa.com/cgi-bin/cancomsrs/?_12+COM+MN";
$html = scraperwiki::scrape($url);

// Parse Dom
$dom = new simple_html_dom();
$dom->load($html);
$count = 0;

// There is only one table with no identifiying attributes.
foreach($dom->find("table tbody tr") as $rows) {
    $count++;

    // First row is header
    $data = $rows->find("td");
    if ($count > 1) {
        // Massage
        $link = $data[0]->find('a', 0);
        $href = isset($link->href) ? 'http://query.nictusa.com' . $link->href : '';
        $committee = '';
        if ($href) {
            $ex = explode('+', $href);
            $committee = $ex[1];
        }

        // Create record
        $record = array(
            'id' => md5(trim($data[0]->plaintext)),
            'name' => ucwords(strtolower($data[0]->plaintext)),
            'link' => $href,
            'committee' => $committee,
            'receipts' => unformat_money($data[1]->plaintext),
            'distributed' => unformat_money($data[2]->plaintext),
            'cash' => unformat_money($data[3]->plaintext),
            'debt' => unformat_money($data[4]->plaintext),
            'through' => (trim($data[5]->plaintext)) ? date('Y-m-d', strtotime($data[5]->plaintext)) : '',
            'timestamp' => time(),
        );
        scraperwiki::save(array('id'), $record);
    }
}
?>
