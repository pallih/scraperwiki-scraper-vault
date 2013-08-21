<?php
// Gets basic data and links for invasive species from the MN DNR

         
require 'scraperwiki/simple_html_dom.php';

// Get basic data from a given page
function data_from_overview_page($url, $type) {
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    $count = 0;
    $base_url = 'http://www.dnr.state.mn.us';

    foreach($dom->find(".paddingbig table tr table tr") as $rows) {
        $count++;

        $data = $rows->find("td");
        $link_image = $data[0]->find("a");
        $image = $data[0]->find("img");
        $link_text = $data[1]->find("a");
        $name = $link_text[0]->plaintext;

        if (!empty($data[0]->plaintext)) {
            $record = array(
                'id' => $type . '--' . strtolower(str_replace(' ', '-', $name)),
                'type' => $type,
                'name' => $name,
                'link' => (!empty($link_image[0]->href)) ? $base_url . $link_image[0]->href : '',
                'thumb_url' => (!empty($image[0]->src)) ? $image[0]->src : '',
                'timestamp' => time(),
            );
    
            scraperwiki::save(array('id'), $record);
        }
    }
}

// Pages
$pages = array(
    'aquaticanimals' => 'http://www.dnr.state.mn.us/invasives/aquaticanimals/index.html',
    'aquaticplants' => 'http://www.dnr.state.mn.us/invasives/aquaticplants/index.html',
    'terrestrialanimals' => 'http://www.dnr.state.mn.us/invasives/terrestrialanimals/index.html',
    'terrestrialplants' => 'http://www.dnr.state.mn.us/invasives/terrestrialplants/index.html' 
);

// Go through pages
foreach ($pages as $k => $p) {
    data_from_overview_page($p, $k);
}

?>
