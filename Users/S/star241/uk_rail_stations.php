<?php
require  'scraperwiki/simple_html_dom.php';
$domain = "http://en.wikipedia.org";
$start_page = "http://en.wikipedia.org/wiki/UK_railway_stations_%E2%80%93_A";

$dom = new simple_html_dom();
$dom->load(scraperwiki::scrape($start_page));

$scrape_list = array();
foreach($dom->find('//div/div/p/a') as $data) {
    if (strpos($data->href, "/wiki/UK_railway_stations") === 0) {
        $scrape_list[] = $data->href;
    }
}
$c = -1;
while ($dom) {
    $rows = $dom->find("//table[@class=wikitable]/tr");
    var_dump(count($rows));
    foreach ($rows as $row) {
        if ($row->children(0)->tag != "th") {
            echo "Found station...";
            $insert = array();
            $insert['name'] = $row->children(0)->children(0)->innertext;
            $r = $row->children(1)->children(0);
            if (isset($r)) {
                $insert['postcode'] = strip_tags($r->innertext);
            }
            $r = $row->children(2)->children(0);
            if (isset($r)) {
                $insert['code'] = $r->innertext;
            }
            if ($insert['postcode'] != "") {
                echo "..";
                $ll = scraperwiki::gb_postcode_to_latlng($insert['postcode']);
                echo "..";
                $insert['lat'] = $ll[0];
                $insert['lng'] = $ll[1];
            } else {
                $insert['lat'] = 0;
                $insert['lng'] = 0;
            }
            var_dump($insert);
            scraperwiki::save_sqlite(array('name'), $insert);
            echo " Saved\n";
        }
    }
    echo "Page done... Starting next";
    $c++;
    if (isset($scrape_list[$c])) {
        $dom->load(scraperwiki::scrape($domain.$scrape_list[$c]));
    } else {
        $dom = false;    
    }
}
?>
