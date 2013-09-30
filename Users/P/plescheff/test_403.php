<?php

require 'scraperwiki/simple_html_dom.php';     

define('RESULTS_PER_PAGE', 200);

$requestParams = array(
    'ae' => 2,//sort by price
    'af' => RESULTS_PER_PAGE,//no of results per page
    'f1' => 2007,//start year
    'f2' => 2010,//end uera
    'g1' => 3000,//price from
    'g2' => 30000,//price to
    'ad' => 1,//ads from last X days
    'by' => 2,//non-auction ads
    'q' => 2,//non-crashed ads
    'd' => range(4,7),//no of seats
);


$a24ksi = read_listing($requestParams);

$data = array(
    'a24ksi_val' => $a24ksi['val'],
    'a24ksi_n' => $a24ksi['n'],
    'date' => date('Y-m-d'),
    'ts' => time(),
);

scraperwiki::save(array('date'), $data);


function read_listing($params, $url='http://www.auto24.ee/kasutatud/nimekiri.php') {
    $endpoint = build_query($url, $params);

    $html = scraperWiki::scrape($endpoint);   

    $dom = new simple_html_dom();
    
    $dom->load($html);

    $totalResultsEl = $dom->find('.paginator .current-range strong');
    $totalResults = $totalResultsEl[0]->plaintext;
    $medianItem = ($totalResults+1)/2;

    if ($medianItem > RESULTS_PER_PAGE) {
        $listingOffset = floor($medianItem/RESULTS_PER_PAGE)*RESULTS_PER_PAGE;
        
        $params['ak'] = $listingOffset;
        $medianItem -= $listingOffset;

        $endpoint = build_query($url, $params);

        $html = scraperWiki::scrape($endpoint);   
    
        $dom = new simple_html_dom();
        
        $dom->load($html);
    }

    $rows = $dom->find("[@id=usedVehiclesSearchResult] .result-row");

    $lPoint = floor($medianItem)-1;
    $hPoint = ceil($medianItem)-1;

    $a24ksi = 0;

    if ($lPoint == $hPoint) {
        $rowData = get_row_data($rows[$lPoint]);
        $a24ksi = $rowData['price'];
    } else {
        $lRowData = get_row_data($rows[$lPoint]);
        $hRowData = get_row_data($rows[$hPoint]);

        $a24ksi = round(($lRowData['price']+$hRowData['price'])/2);
    }

    return array(
        'n' => $totalResults,
        'val' => $a24ksi
    );
}

function build_query($url, $params) {
    return $url . '?' . http_build_query($params);
}

function get_row_data($row) {
    $titleData = $row->find('.make_and_model > a');
    $priceData = $row->find('.price');
    
    $title = $titleData[0]->plaintext;
    $price = (int) str_replace('&nbsp;', '', $priceData[0]->plaintext);
    $link = $titleData[0]->href;
    $id = str_replace('/used/','',$link);

    if (strpos($priceData[0]->plaintext, '20%')!==false) {
        $price *= 1.2;
    }

    return array(
        'id' => $id,
        'title' => $title,
        'price' => $price,
        'url' => $link,
        'ts' => date('Y-m-d H:i:s')
    );
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';     

define('RESULTS_PER_PAGE', 200);

$requestParams = array(
    'ae' => 2,//sort by price
    'af' => RESULTS_PER_PAGE,//no of results per page
    'f1' => 2007,//start year
    'f2' => 2010,//end uera
    'g1' => 3000,//price from
    'g2' => 30000,//price to
    'ad' => 1,//ads from last X days
    'by' => 2,//non-auction ads
    'q' => 2,//non-crashed ads
    'd' => range(4,7),//no of seats
);


$a24ksi = read_listing($requestParams);

$data = array(
    'a24ksi_val' => $a24ksi['val'],
    'a24ksi_n' => $a24ksi['n'],
    'date' => date('Y-m-d'),
    'ts' => time(),
);

scraperwiki::save(array('date'), $data);


function read_listing($params, $url='http://www.auto24.ee/kasutatud/nimekiri.php') {
    $endpoint = build_query($url, $params);

    $html = scraperWiki::scrape($endpoint);   

    $dom = new simple_html_dom();
    
    $dom->load($html);

    $totalResultsEl = $dom->find('.paginator .current-range strong');
    $totalResults = $totalResultsEl[0]->plaintext;
    $medianItem = ($totalResults+1)/2;

    if ($medianItem > RESULTS_PER_PAGE) {
        $listingOffset = floor($medianItem/RESULTS_PER_PAGE)*RESULTS_PER_PAGE;
        
        $params['ak'] = $listingOffset;
        $medianItem -= $listingOffset;

        $endpoint = build_query($url, $params);

        $html = scraperWiki::scrape($endpoint);   
    
        $dom = new simple_html_dom();
        
        $dom->load($html);
    }

    $rows = $dom->find("[@id=usedVehiclesSearchResult] .result-row");

    $lPoint = floor($medianItem)-1;
    $hPoint = ceil($medianItem)-1;

    $a24ksi = 0;

    if ($lPoint == $hPoint) {
        $rowData = get_row_data($rows[$lPoint]);
        $a24ksi = $rowData['price'];
    } else {
        $lRowData = get_row_data($rows[$lPoint]);
        $hRowData = get_row_data($rows[$hPoint]);

        $a24ksi = round(($lRowData['price']+$hRowData['price'])/2);
    }

    return array(
        'n' => $totalResults,
        'val' => $a24ksi
    );
}

function build_query($url, $params) {
    return $url . '?' . http_build_query($params);
}

function get_row_data($row) {
    $titleData = $row->find('.make_and_model > a');
    $priceData = $row->find('.price');
    
    $title = $titleData[0]->plaintext;
    $price = (int) str_replace('&nbsp;', '', $priceData[0]->plaintext);
    $link = $titleData[0]->href;
    $id = str_replace('/used/','',$link);

    if (strpos($priceData[0]->plaintext, '20%')!==false) {
        $price *= 1.2;
    }

    return array(
        'id' => $id,
        'title' => $title,
        'price' => $price,
        'url' => $link,
        'ts' => date('Y-m-d H:i:s')
    );
}

?>
