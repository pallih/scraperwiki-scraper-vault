<?php
$tablename = "tod20121103";
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/calls.nsf/professional?OpenView&Start=1&ExpandView");
$dom = new simple_html_dom();
$dom->load($html);

$links = array();
foreach ($dom->find('tr td table tr td a[href*=calls.nsf]') as $a) {
    $pos = strpos($a->plaintext,"View");
    if ($pos !== false) {
        array_push($links,$a->href);
    }
}

//***do paging here

//if the following line is uncommented, the scraper will only try one page. good for testing
//$links = array($links[0]);

foreach ($links as $doc) {
    $html = scraperWiki::scrape($doc);
    $dom = new simple_html_dom();
    $dom->load($html);
    $thisdoc['link'] = $doc;
    foreach ($dom->find('tr td[width=120] font') as $a) {
        if ($a->plaintext == "Call number:") {
            $thisdoc['callnumber'] = $a->parent()->parent()->next_sibling()->plaintext;
        }
    }
    foreach ($dom->find('tr td[width=124] font') as $a) {
        if ($a->plaintext == "Commodity:") { 
            $thisdoc['commodity'] = $a->parent()->parent()->next_sibling()->plaintext;
            //print $a->plaintext." ".$a->parent()->parent()->next_sibling()->plaintext."\n";
        } elseif ($a->plaintext == "Description:") {
            $thisdoc['description'] = $a->parent()->parent()->next_sibling()->plaintext;
            //print $a->plaintext." ".$a->parent()->parent()->next_sibling()->plaintext."\n";
        } elseif ($a->plaintext == "Issue date:") {
            $thisdoc['issuedate'] = $a->parent()->parent()->next_sibling()->plaintext;
            //print $a->plaintext." a".$a->parent()->parent()->next_sibling()->plaintext."\n";
            $a = $a->parent()->parent()->next_sibling()->next_sibling();
            //print $a->src." z".$a->next_sibling()->next_sibling()->plaintext."\n";
            $thisdoc['closingdate'] = $a->next_sibling()->next_sibling()->plaintext;
        }
    }
    foreach ($dom->find('tr td[width=778]') as $a) {
        $pos = strpos($a->plaintext,"Scope of work");
        if ($pos !== false) {
            $thisdoc['scopeofwork'] = $a->plaintext;
        }
    }

    //var_dump($thisdoc);

    //***only add it if it's a new record, or if the data has changed

    scraperwiki::save_sqlite(array('callnumber'), array(
        "doc"=>$thisdoc['link'], 
        "callnumber"=>$thisdoc['callnumber'],
        "commodity"=>$thisdoc['commodity'],
        "description"=>$thisdoc['description'],
        "scopeofwork"=>$thisdoc['scopeofwork'],
        "issuedate"=>$thisdoc['issuedate'],
        "closingdate"=>$thisdoc['closingdate']), $table_name=$tablename, $verbose=2);
}

?>
