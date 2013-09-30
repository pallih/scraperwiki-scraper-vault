<?php

//print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://scholar.google.com/citations?hl=en&user=lxkhmgYAAAAJ&pagesize=100&sortby=pubdate&view_op=list_works&cstart=0");
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
            'citations' => $td_cited[0]->plaintext
        );
        scraperwiki::save(array('publication'), $record);

    }
}

?>
<?php

//print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://scholar.google.com/citations?hl=en&user=lxkhmgYAAAAJ&pagesize=100&sortby=pubdate&view_op=list_works&cstart=0");
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
            'citations' => $td_cited[0]->plaintext
        );
        scraperwiki::save(array('publication'), $record);

    }
}

?>
