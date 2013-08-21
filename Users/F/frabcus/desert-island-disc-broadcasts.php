<?php
######################################
# Basic PHP scraper
######################################

require 'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.bbc.co.uk/radio4/factual/desertislanddiscs_archive.shtml");

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('a') as $data)
{
    # Store data in the datastore
    $url = $data->href;
    if (!strstr($url, '.shtml')) {
        $url = str_replace(".shtm", ".shtml", $url);
    }

    $tidied_url = str_replace("discs2", "discs_2", $url); # cope with desertislanddiscs20060212.shtml
    $tidied_url = str_replace("_200040104.shtml", "_20040104.shtml", $tidied_url); # cope with desertislanddiscs_200040104.shtml

    if (preg_match("#^/radio4/factual/desert#", $tidied_url, $matches)) {
        preg_match("#^/radio4/factual/desertislanddiscs_(\d\d\d\d)(\d\d)(\d\d).shtml#", $tidied_url, $matches);

        $url = "http://www.bbc.co.uk" . $url;
        $guest = $data->plaintext;
        if (count($matches) != 4) {
            print "didn't get match on " . $tidied_url . "\n";
            exit;
        } else {
            $date = $matches[1] . "-" . $matches[2] . "-" . $matches[3];
            print $guest . " " . $date . " " . $url . "\n";
            scraperwiki::save(array('date', 'guest'), array('guest' => $guest, 'url' => $url, 'date' => $date), $date);
        }
    }

}

?>