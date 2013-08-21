<?php

$ycode = "ADN.L";

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://uk.finance.yahoo.com/q/pr?s=$ycode");
$html = str_get_html($html_content);

foreach ($html->find("table.yfnc_datamodoutline1 table td") as $el) {           
    if (strstr($el->innertext, "Employees")) {
        $record = array(
            'employees' => $el->next_sibling()->innertext,
            'ycode' => $ycode
        );
        scraperwiki::save(array('ycode'), $record);  
    }
}

$html->__destruct();

?>
