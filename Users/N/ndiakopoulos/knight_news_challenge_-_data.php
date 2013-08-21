<?php
require 'scraperwiki/simple_html_dom.php'; 

$url = "http://newschallenge.tumblr.com/archive";
$html_entries = scraperWiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html_entries);
$dom2 = new simple_html_dom();

foreach($dom->find("a.brick") as $data)
{
    $href_entry = $data->href;
    $html_entry = scraperWiki::scrape($href_entry);
    $dom2->load($html_entry);
    // parse out the answers to each question
    $answers = $dom2->find("div.single p");
    $details = $dom2->find("h5");
    $details_array = explode("\n", $details[0]->plaintext);
        $record = array(
            'href_entry' => $href_entry,
            'short_proposal' => $answers[0]->plaintext,
            'how_different' => $answers[1]->plaintext,
            'how_useful' => $answers[2]->plaintext,
            'why_will_it_work' => $answers[3]->plaintext,
            'who' => $answers[4]->plaintext,
            'already_built' => $answers[5]->plaintext,
            'how_use_funds' => $answers[6]->plaintext,
            'how_sustain' => $answers[7]->plaintext,
            'months_to_complete' => str_replace("Expected number of months to complete project: ", "", $details_array[0]),
            'total_cost' => str_replace("Total Project Cost: ", "", $details_array[1])
        );
    scraperwiki::save_sqlite(array('href_entry'), $record); 
    //print_r($record);
}
?>
