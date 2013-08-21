<?php
function scrape($bench) {
    $from_date = date('d/m/Y', strtotime('-20 days'));
    $to_date = date('d/m/Y');
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://causelist.kar.nic.in/caseStatus_PartyNameDistrict.asp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17',
        CURLOPT_POSTFIELDS => http_build_query(array(
            'bench_cd' => $bench,
            'txtname' => '%',
            'txtfromdate' => $from_date,
            'txttodate' => $to_date,
            'txttype' => 'D',
            'cbodistrict' => '',
            'cbocasetype' => '',
            'submitval' => 'Y',
            'tempval' => '',
            'firstval' => '',
        )),
    ));

    echo "Loading bench code ". $bench ." using dates ". $from_date ." -> ". $to_date ." ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $ch = null;
    unset($ch);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//form[@name="frmquery1"]/table[2]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->childNodes->item(2)) {
            preg_match_all('/([^\s+]+)/', $row->childNodes->item(2)->nodeValue, $case_number);
            @$result = array(
                'district' =>    trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(0)->nodeValue)),
                'case_number' => $case_number[0][0] .' '. $case_number[0][2] .'/'. $case_number[0][4],
                'filing_date' => trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(4)->nodeValue)),
                'petitioner' =>  trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(5)->nodeValue)),
                'respondent' =>  trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(6)->nodeValue)),
                'sub_type' =>    trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(9)->nodeValue)),
                'sub_sub_type' => trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(10)->nodeValue)),
            );
            if ($i > 0 && $result['case_number']) array_push($results, $result);
        }
        $case_number = null;
        $row = null;
        $result = null;
        unset($case_number);
        unset($row);
        unset($result);
    }
    
    //Clean up and save
    $query = null;
    unset($query);
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}


scrape('B');
scrape('D');
scrape('G');
?>
