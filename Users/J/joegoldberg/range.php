<?php

require 'scraperwiki/simple_html_dom.php';


for ($i = 1; $i < 100; $i++) {
    $html = scraperWiki::scrape("http://www.osha.gov/pls/imis/industry.search?sic=&sicgroup=&naicsgroup=&naics=23&state=All&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2010&opt=&optt=&scope=&fedagncode=&owner=&emph=&emphtp=&p_start=" . (($i - 1) * 20) . "&p_finish=" . ($i * 20) . "&p_sort=&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);

    $records = array();
    foreach ($dom->find("div tr") as $data) {
        $tds = $data->find("td");
//        print_r($tds);
        if (count($tds) == 12) {
            $record = array(
                'activity' => trim($tds[2]->plaintext),

            );
            scraperwiki::save(array('activity'), $record);
            $records[] = $record;
        }
    }
    $first = true;
    foreach ($records as $recorded) {
        if (!$first) {
            $html = scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.inspection_detail?id=" . $recorded['activity']);
            $dom = new simple_html_dom();
            $dom->load($html);
        }
        $first = false;
    }
}
