<?php

require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `climbing_areas` (`area` text, `region` text)");

for ($id = 1; $id < 724; $id++) {
    echo $id;

    $html_content = scraperwiki::scrape("http://www.rockfax.com/databases/results_crag.html?id=" . $id);
    $html = str_get_html($html_content);

    $area = $region = null;
    
    $nav = array_pop($html->find("div#nav-above"))->find("a");
    $region = $nav[1]->innertext;
    
    $title = array_pop($html->find("h1.entry-title"));
    $area = $title->innertext;

    $data = array();
    $data["area"] = $area;
    $data["region"] = $region;

    scraperwiki::save_sqlite(array("area"), $data, "climbing_areas", 2);

}