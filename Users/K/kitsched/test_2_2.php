<?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

scraperwiki::attach("test_1_2");
$result = scraperwiki::sqliteexecute("select html from hotel_list_pages");
$hotel_list_pages_contents = $result->data;

foreach($hotel_list_pages_contents as $contents)
{
    $html = $contents[0];

    $dom->load($html);
    
    foreach($dom->find("table.hotellist tr") as $data){
        $tds = $data->find("td h3 a");
        $record = array(
            'hotel' => $tds[0]->plaintext, 
            'url' => $tds[0]->href,
        );
        scraperwiki::save_sqlite(array('hotel'), $record, $table_name = 'hotel_list');
    }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

scraperwiki::attach("test_1_2");
$result = scraperwiki::sqliteexecute("select html from hotel_list_pages");
$hotel_list_pages_contents = $result->data;

foreach($hotel_list_pages_contents as $contents)
{
    $html = $contents[0];

    $dom->load($html);
    
    foreach($dom->find("table.hotellist tr") as $data){
        $tds = $data->find("td h3 a");
        $record = array(
            'hotel' => $tds[0]->plaintext, 
            'url' => $tds[0]->href,
        );
        scraperwiki::save_sqlite(array('hotel'), $record, $table_name = 'hotel_list');
    }
}

?>
