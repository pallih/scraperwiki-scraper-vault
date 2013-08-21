<?php
require 'scraperwiki/simple_html_dom.php';

$awardedtable = "awarded20121215";

for ($i = 1; $i <= 17; $i++) {
    $html = scraperWiki::scrape("https://wx.toronto.ca/inter/pmmd/callawards.nsf/posted+awards?OpenView&Start=1&Count=1000&Expand=3.".$i);
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach ($dom->find('a[href*=OpenDocument]') as $a) {
        $thisrecord = array();
        $thisrecord['link'] = $a->href;
        $thisrecord['category'] = "3.".$i;
        $thisrecord['callnumber'] = $a->plaintext;
        $thisrecord['commodity'] = $a->parent()->parent()->parent()->next_sibling()->plaintext;
        $thisrecord['description'] = iconv("ISO-8859-1", "ASCII//IGNORE", $a->parent()->parent()->parent()->next_sibling()->next_sibling()->plaintext);
        $thisrecord['winner'] = $a->parent()->parent()->parent()->next_sibling()->next_sibling()->next_sibling()->next_sibling()->plaintext;
        $pos = strpos($thisrecord['winner'],"Multiple");
        if ($pos !== false) {
            //we have to follow the link to get winner and amount
        } else {
            $thisrecord['amount'] = $a->parent()->parent()->parent()->next_sibling()->next_sibling()->next_sibling()->next_sibling()->next_sibling()->plaintext;
            $thisrecord['dateawarded'] = $a->parent()->parent()->parent()->next_sibling()->next_sibling()->next_sibling()->next_sibling()->next_sibling()->next_sibling()->plaintext;
        }

        //var_dump($thisrecord['description']);
        //print mb_detect_encoding($thisrecord['description'])."\n";

        scraperwiki::save_sqlite(array('callnumber'), array(
            "link"=>$thisrecord['link'], 
            "category"=>$thisrecord['category'],
            "callnumber"=>$thisrecord['callnumber'],
            "commodity"=>$thisrecord['commodity'],
            "description"=>$thisrecord['description'],
            "winner"=>$thisrecord['winner'],
            "amount"=>$thisrecord['amount'],
            "dateawarded"=>$thisrecord['dateawarded']), $table_name=$awardedtable, $verbose=2);


    }

}


?>
