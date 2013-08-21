<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.programmableweb.com/apis/directory/1?sort=date&pagesize=100");
$html = str_get_html($html_content);

$apis_rows = $html->find("table#apis > tbody > tr");

foreach($apis_rows as $row) {
    $row_cells = $row->find("td");
    if(count($row_cells) == 4) {
        $api_detail = $row_cells[0]->find("a", 0)->href;
        print $api_detail;
    }
  /*$investors_names = array();
    foreach($investors as $investor) {
        array_push($investors_names, $investor->getAttribute("title"));
    }
    
    $tweet = array('date' => $date, 'name' => $name, 'amount' => $amount, 'investors' => implode(";", $investors_names));
    scraperwiki::save(array("date", "name", "investors"), $tweet);           

}
*/
}
?>
