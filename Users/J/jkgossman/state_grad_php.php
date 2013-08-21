<?php
require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape("http://dashboard.ed.gov/statecomparison.aspx?i=e&id=0&wt=40");
 

$dom = new simple_html_dom();
$dom->load($html);
$state_grad= $dom->find("table",0);
$tablerows=$state_grad->find("tr");
//print count($tablerows);
for( $i=0; $i<count($tablerows); $i++ )
{
    //print $tablerows[$i];
    print $tablerows[$i]->find("tbody th", 0)->plaintext . "\n";
    print $tablerows[$i]->find("tbody td", 0)->plaintext . "\n";
    $rowdata = array(
        'state' => $tablerows[$i]->find("th", 0)->plaintext,
        'total' => $tablerows[$i]->find("td", 0)->plaintext
    );
    scraperwiki::save(array('state'), $rowdata);
}
?>
