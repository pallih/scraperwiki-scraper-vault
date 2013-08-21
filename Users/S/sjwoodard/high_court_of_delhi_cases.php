<?php
function scrape($year, $this_page, $total_pages) {
    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(scraperwiki::scrape('http://delhihighcourt.nic.in/dhc_case_status_list_new.asp?ayear=&pyear='. $year .'&SNo=2&SRecNo='. ($this_page*8) .'&dno=&dyear=&ctype=&cno=&cyear=&party=%&adv='));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//tr[@bgcolor="#ebebeb"]');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results (page ". ($this_page+1) ." of ". $total_pages .") ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = explode("\r\n", preg_replace('/\xC2\xA0/', '', $query->item($i)->nodeValue));
        if ($query->item($i)->getElementsByTagName('button')->item(0)) {
        preg_match("/pno=(.*?)\'/", $query->item($i)->getElementsByTagName('button')->item(0)->getAttribute('onclick'), $path);
        } else {
            $path = array('','');
        }
        preg_match('/(.*?)Advocate :/i', preg_replace('/Vs./i', '', $row[15]), $respondent);
        @$result = array(
            'case_number' => trim(preg_replace('/\d+\/\d+/', ' $0', $row[5])),
            'path' => $path[1],
            'petitioner' =>  trim($row[13]),
            'respondent' =>  trim($respondent[1]),
            'status' => trim(preg_replace('/\[|\]/', '', $row[7]))
        );
        $result['unique_id'] = preg_replace('/\s+/', '', $result['path'] .'-'. $result['case_number']);
        array_push($results, $result);
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
    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$year = date('Y');

$dom = new DOMDocument();
@$dom->loadHTML(scraperwiki::scrape('http://delhihighcourt.nic.in/dhc_case_status_list_new.asp?ayear=&pyear='. $year .'&SNo=2&SRecNo=0&dno=&dyear=&ctype=&cno=&cyear=&party=%&adv='));
$xpath = new DOMXPath($dom);
$dom = null;
unset($dom);
$query = $xpath->query('//tr[@bgcolor="#ebebeb"]');
@$total_pages = intval($xpath->query('//div[@class="archivelink"]')->item(0)->nodeValue);
$xpath = null;
unset($xpath);

for ($this_page = 0; $this_page < $total_pages; $this_page++) {
    scrape($year, $this_page, $total_pages);
}

?>