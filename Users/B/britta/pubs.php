<?php

$html = scraperWiki::scrape("http://scholar.google.com/citations?hl=en&user=lxkhmgYAAAAJ&sortby=pubdate&view_op=list_works&pagesize=100");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table.cit-table tr.item") as $data){

    $td_cited = $data->find("td#col-citedby a");
    $td_year = $data->find("td#col-year");
    $td_title = $data->find("td#col-title a");

    if(count($td_cited)==1){
        $record = array(
            'title' => $td_title[0]->plaintext,
            'link' => $td_title[0]->href,
            'citations' => $td_cited[0]->plaintext,
            'year' => $td_year[0]->plaintext
        );
        scraperwiki::save(array('citations'), $record);

    }
}

?>
