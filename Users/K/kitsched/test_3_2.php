<?php

$base = 'http://www.booking.com';

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

scraperwiki::attach("test_2_2");
$result = scraperwiki::sqliteexecute("select url, hotel from hotel_list");
$hotel_list_contents = $result->data;

$total_records = sizeof($hotel_list_contents);

$i = 1;
foreach($hotel_list_contents as $contents)
{
    echo($i++." of $total_records...\n");

    $url = $base.$contents[0];

    $html = scraperWiki::scrape($url);
    $dom->load($html);

    $record = array(
        'url' => $contents[0],
        'hotel' => $contents[1],
        'html' => $html,
    );
    scraperwiki::save_sqlite(array('hotel'), $record, $table_name = 'hotels');

    echo($i."\n");
    if($i == 30) break;
}

?>
<?php

$base = 'http://www.booking.com';

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

scraperwiki::attach("test_2_2");
$result = scraperwiki::sqliteexecute("select url, hotel from hotel_list");
$hotel_list_contents = $result->data;

$total_records = sizeof($hotel_list_contents);

$i = 1;
foreach($hotel_list_contents as $contents)
{
    echo($i++." of $total_records...\n");

    $url = $base.$contents[0];

    $html = scraperWiki::scrape($url);
    $dom->load($html);

    $record = array(
        'url' => $contents[0],
        'hotel' => $contents[1],
        'html' => $html,
    );
    scraperwiki::save_sqlite(array('hotel'), $record, $table_name = 'hotels');

    echo($i."\n");
    if($i == 30) break;
}

?>
