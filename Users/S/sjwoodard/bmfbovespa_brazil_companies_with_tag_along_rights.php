<?php
function scrape() {

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(scraperwiki::scrape('http://www.bmfbovespa.com.br/en-us/markets/equities/companies/companies-with-tag-along-rights.aspx?idioma=en-us'));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $rows = $xpath->query('//div[@class="tabela"]/table/tbody/tr');
    $n = $rows->length;
    $xpath = null;
    unset($xpath);
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $rows->item($i)->getElementsByTagName('td');
        array_push($results, array(
            'unique_id' => preg_replace('/\s+/', '', trim(@$row->item(0)->nodeValue) .'-'. trim(@$row->item(2)->nodeValue)),
            'name' => trim(@$row->item(0)->nodeValue),
            'corporate_resolution' => trim(@$row->item(1)->nodeValue),
            'event_date' => trim(@$row->item(2)->nodeValue),
            'tag_voting_pct' => trim(@$row->item(3)->nodeValue),
            'tag_non_voting_pct' => trim(@$row->item(4)->nodeValue),
            'listing_segment' => trim(@$row->item(5)->nodeValue)
        ));
    }

    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
}

scrape();
?><?php
function scrape() {

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(scraperwiki::scrape('http://www.bmfbovespa.com.br/en-us/markets/equities/companies/companies-with-tag-along-rights.aspx?idioma=en-us'));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $rows = $xpath->query('//div[@class="tabela"]/table/tbody/tr');
    $n = $rows->length;
    $xpath = null;
    unset($xpath);
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $rows->item($i)->getElementsByTagName('td');
        array_push($results, array(
            'unique_id' => preg_replace('/\s+/', '', trim(@$row->item(0)->nodeValue) .'-'. trim(@$row->item(2)->nodeValue)),
            'name' => trim(@$row->item(0)->nodeValue),
            'corporate_resolution' => trim(@$row->item(1)->nodeValue),
            'event_date' => trim(@$row->item(2)->nodeValue),
            'tag_voting_pct' => trim(@$row->item(3)->nodeValue),
            'tag_non_voting_pct' => trim(@$row->item(4)->nodeValue),
            'listing_segment' => trim(@$row->item(5)->nodeValue)
        ));
    }

    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
}

scrape();
?><?php
function scrape() {

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(scraperwiki::scrape('http://www.bmfbovespa.com.br/en-us/markets/equities/companies/companies-with-tag-along-rights.aspx?idioma=en-us'));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $rows = $xpath->query('//div[@class="tabela"]/table/tbody/tr');
    $n = $rows->length;
    $xpath = null;
    unset($xpath);
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $rows->item($i)->getElementsByTagName('td');
        array_push($results, array(
            'unique_id' => preg_replace('/\s+/', '', trim(@$row->item(0)->nodeValue) .'-'. trim(@$row->item(2)->nodeValue)),
            'name' => trim(@$row->item(0)->nodeValue),
            'corporate_resolution' => trim(@$row->item(1)->nodeValue),
            'event_date' => trim(@$row->item(2)->nodeValue),
            'tag_voting_pct' => trim(@$row->item(3)->nodeValue),
            'tag_non_voting_pct' => trim(@$row->item(4)->nodeValue),
            'listing_segment' => trim(@$row->item(5)->nodeValue)
        ));
    }

    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
}

scrape();
?>