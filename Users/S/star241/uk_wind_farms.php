<?php
require  'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load(scraperwiki::scrape("http://www.bwea.com/ukwed/operational.asp"));
foreach ($dom->find("table[@class=outlined]/tr") as $farm) {
    $fields = $farm->find("/td");
    if ($fields[0]->innertext == "<strong>Online</strong>" || $fields[0]->innertext == "<strong> Totals </strong>") {
        continue;
    }
    $insert = array();
    $insert['online'] = trim(utf8_encode($fields[0]->innertext));
    $insert['name'] = trim(utf8_encode($fields[1]->innertext));
    $insert['location'] = trim(utf8_encode($fields[2]->innertext));
    $insert['model'] = trim(str_replace(array("Enercon E-48", "E 48", "E-48"), "Enercon E48", utf8_encode($fields[3]->innertext)));
    $insert['power'] = trim(utf8_encode($fields[4]->innertext));
    $insert['turbines'] = trim(utf8_encode($fields[5]->innertext));
    $insert['power_capacity'] = trim(utf8_encode($fields[6]->innertext));
    $insert['avg_homes'] = trim(utf8_encode($fields[7]->innertext));
    $insert['developer'] = trim(utf8_encode($fields[8]->innertext));
    $insert['operator'] = trim(utf8_encode($fields[9]->innertext));
    $insert['owner'] = trim(utf8_encode($fields[10]->innertext));
    $insert['lat'] = trim(utf8_encode($fields[11]->innertext));
    $insert['lng'] = trim(utf8_encode($fields[12]->innertext));
    scraperwiki::save_sqlite(array("lat", "lng"), $insert);
}
?>
