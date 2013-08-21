<?php

# Blank PHP
print "Testing getting 1 year CMT from Bankrate.\n";

$html_content = scraperWiki::scrape("http://www.bankrate.com/rates/interest-rates/1-year-cmt.aspx");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           


$html = str_get_html($html_content);

$data[0] = "";


foreach ($html->find("div.interactivetopaction ") as $el) {           
    //print $el . "\n";
    //print "1 year CMT ". $el->innertext . "\n";
    $data[0] = $el->innertext;
}

$i = 1;

foreach ($html->find("div.boxcontent") as $box) {           
    foreach ($box->find("td") as $el) {           
        //print $el->innertext . "\n";
        $data[$i] = $el->innertext;
        $i++;
    }
}

//print_r($data);

scraperwiki::save_var("date", $data[0]);
scraperwiki::save_var("1yearcmt", $data[6]);

$html->__destruct();
?>
