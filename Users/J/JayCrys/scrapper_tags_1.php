<?php
require 'scraperwiki/simple_html_dom.php';

$table_name = "scrapper_tags";
$unique_keys = "id"; // table primary key

$html_content = scraperwiki::scrape("https://scraperwiki.com/");
$html = str_get_html($html_content);

$id = 0;
foreach ($html->find("ul.tags li a") as $el) {
   // $tags[] = ucwords($el->plaintext) . "\n";
    scraperwiki::save_sqlite(
                    array($unique_keys),
                    array("id"=>++$id, "tags"=>ucwords($el->plaintext)),
                    $table_name);

}

//var_dump($tags);
$html->__destruct();
