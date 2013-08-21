<?php

// This scraper gets Minnesota bill data for the Senate, as
// the Open States API does not have this information   
require 'scraperwiki/simple_html_dom.php';

// Remove htlm spaces.
function html_trim($value = '') {
    return trim(str_replace('&nbsp;', ' ', $value));
}

// Function to get basic bill data from givernsite
function get_bills_from_governer() {
    $base_url = 'http://mn.gov/governor/policy/legislation/';
    $pages = 20;
    $start_page = 1;
    $bills = array();

    for ($i = $start_page; $i <= $pages; $i++) {
        $html = scraperwiki::scrape(trim($base_url . '?page=' . $i));
        
        // Parse Dom
        $dom = new simple_html_dom();
        $dom->load($html);
        $count = 0;
        
        // Legislation table
        foreach($dom->find('table.table_legislation tbody tr') as $rows) {
            $count++;
        
            // First row is header
            $data = $rows->find('td');
            if ($count > 1) {
                // Is this house or senate
                $bill = html_trim($data[1]->plaintext);
                if (!empty($bill)) {
                    $bill = 'HF' . $bill;
                    $body = 'house';
                }
                else {
                    $bill = 'SF' . html_trim($data[2]->plaintext);
                    $body = 'senate';
                }
    
                // Check veto
                $status = '';
                if (html_trim($data[6]->plaintext) != '-') {
                    $status = 'vetoed';
                }
        
                // Create record
                $bill = array(
                    'id' => $bill . '-2012',
                    'year' => '2012',
                    'body' => strtolower($body),
                    'bill' => $bill,
                    'description' => html_trim($data[3]->plaintext),
                    'status' => $status,
                    'timestamp' => time(),
                );
                $bills[] = $bill;
        
                // Save if not already in DB
                scraperwiki::save_sqlite(array('id'), $bill);
            }
        }
    }

    return $bills;
}

// Function to get bill details.
function get_bill_details($r = array()) {
    if (empty($r['bill'])) { return; }
    $html = scraperwiki::scrape('https://www.revisor.mn.gov/revisor/pages/search_status/status_detail.php?b=House&ssn=0&y=2012&f=' . $r['bill']);
    
    // Parse Dom
    $dom = new simple_html_dom();
    $dom->load($html);
    $count = 0;

    // Table based layout without real identifiers.  Get Senate votes if avialable.
    $senate = $dom->find('table[summary=Actions]', 1);
    if (!empty($senate)) {
        foreach($senate->find('tr') as $rows) {
            $count++;
        
            // First row is header
            if ($count > 1) {
                $data = $rows->find('td');
                $roll_call = html_trim($data[5]->plaintext);
                if (!empty($roll_call)) {
                    $votes = explode('-', $roll_call);

                    // Update record
                    $r['senate_vote_yes'] = $votes[0];
                    $r['senate_vote_no'] = $votes[1];
                    $r['senate_last_vote'] = html_trim($data[0]->plaintext);
                    $r['timestamp'] = time();
        
                    // Save.
                    scraperwiki::save_sqlite(array('id'), $r);
                }
            }
        }
    }
}

function fill_in_blanks() {
    $bills = array('SF149', 'SF2112', 'SF2354', 'SF2316', 'SF2464', 'SF1921', 'HF1467', 'SF2098', 'SF2392', 'HF247', 'HF2958', 'HF1752', 'HF322', 'HF2967', 'HF2690', 'SF1755', 'SF1808', 'HF2685', 'HF1721', 'SF1983', 'SF1143', 'SF1653', 'SF1420');
    foreach ($bills as $b) {

        // Update record
        $r = array(
            'id' => $b . '-2012',
            'year' => '2012',
            'bill' => $b,
            'bosy' => 'senate',
            'timestamp' => time(),
        );

        // Save.
        scraperwiki::save_sqlite(array('id'), $r);
    }
}

// Make the magic happen
get_bills_from_governer();

// Fill in some blanks
fill_in_blanks();

$rows = scraperwiki::select('* FROM swdata ORDER BY bill DESC');
foreach ($rows as $r) {
    get_bill_details($r);
}
?>