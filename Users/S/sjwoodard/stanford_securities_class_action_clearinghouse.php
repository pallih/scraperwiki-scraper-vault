<?php
function scrape($page, $results_per_page) {
    $data = scraperwiki::scrape('http://securities.stanford.edu/fmi/xsl/SCACPUDB/recordlist.xsl?-db=SCACPUDB&-lay=Search&-sortfield.1=FIC_DateFiled&-sortfield.2=LitigationName&-sortorder.1=ascend&-max='.$results_per_page.'&-findall=&-lay.response=ListGral&-encoding=UTF-8&-grammar=fmresultset&-skip='.($results_per_page*($page-1)));

    echo "Loading data (page $page) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML($data);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//form/table/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($a = $row->getElementsByTagName('a')->item(0)) {
            $url = $a->getAttribute('href');
        } else {
            $url = null;
        }
        array_push($results, @$result = array(
            'unique_id' => $row->childNodes->item(0)->nodeValue.'-'.$row->childNodes->item(4)->nodeValue.'-'.substr($row->childNodes->item(1)->nodeValue,0,6),
            'href' => $url,
            'litigation_name'=> $row->childNodes->item(1)->nodeValue,
            'exchange' => $row->childNodes->item(2)->nodeValue,
            'ticker' => $row->childNodes->item(3)->nodeValue,
            'date' => $row->childNodes->item(4)->nodeValue,
            'court' => $row->childNodes->item(5)->nodeValue
        ));
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
    }
    
    //Clean up
    $options = null;
    unset($options);

    //Save to database
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$data = scraperwiki::scrape('http://securities.stanford.edu/fmi/xsl/SCACPUDB/recordlist.xsl?-db=SCACPUDB&-lay=Search&-sortfield.1=FIC_DateFiled&-sortfield.2=LitigationName&-sortorder.1=ascend&-max=1&-findall=&-lay.response=ListGral&-encoding=UTF-8&-grammar=fmresultset&-skip=0');
echo "Loading data ...\n";
$dom = new DOMDocument();
@$dom->loadHTML($data);
$xpath = new DOMXPath($dom);
$dom = null;
unset($dom);
preg_match('/\d+\s+of\s+(.*?)\s+\|/', $xpath->query('//td[@align="right"]')->item(0)->nodeValue, $total_results_match);
$total_results = intval($total_results_match[1]);
$xpath = null;
unset($xpath);

$results_per_page = 1000;
$n = ($total_results / $results_per_page) + 1;
for ($page = 1; $page < $n; $page++) {
    scrape($page, $results_per_page);
}

?>