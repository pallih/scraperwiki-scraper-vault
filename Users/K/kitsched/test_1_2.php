<?php

$destination_id = -1746443; // Berlin

$current_timestamp = date('Y-m-d');

$checkin_year = date('Y');
$checkin_month = date('m');
$checkin_day = date('d');

$tomorrow = strtotime(date('Y-m-d')." +1 day");

$checkout_year = date('Y', $tomorrow);
$checkout_month = date('m', $tomorrow);
$checkout_day = date('d', $tomorrow);

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$base = 'http://www.booking.com';
$url = $base.'/searchresults.html?src=index&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-us.html%3Fsid%3De4599c2cc1b5fe9c85dcc7190040859f%3B&sid=e4599c2cc1b5fe9c85dcc7190040859f&si=ai%2Cco%2Cci%2Cre%2Cdi&checkin_monthday='.$checkin_day.'&checkin_year_month='.$checkin_year.'-'.$checkin_month.'&checkout_monthday='.$checkout_day.'&checkout_year_month='.$checkout_year.'-'.$checkout_month.'&group_adults=2&group_children=0&clear_group=0&dest_type=city&dest_id='.$destination_id;

$i = 1;
while($url != '')
{
    $html = scraperWiki::scrape($url);

    $record = array(
        'url' => $url,
        'html' => $html,
    );
    scraperwiki::save_sqlite(array('url'), $record, $table_name = 'hotel_list_pages');

    $dom->load($html);

    $tds = $dom->find("td.next a");
    
    if(sizeof($tds))
    {
        $url = $base.$tds[0]->href;
    }
    else
    {
        $url = '';
    }
    echo($i++."\n");
}
?>
<?php

$destination_id = -1746443; // Berlin

$current_timestamp = date('Y-m-d');

$checkin_year = date('Y');
$checkin_month = date('m');
$checkin_day = date('d');

$tomorrow = strtotime(date('Y-m-d')." +1 day");

$checkout_year = date('Y', $tomorrow);
$checkout_month = date('m', $tomorrow);
$checkout_day = date('d', $tomorrow);

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$base = 'http://www.booking.com';
$url = $base.'/searchresults.html?src=index&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-us.html%3Fsid%3De4599c2cc1b5fe9c85dcc7190040859f%3B&sid=e4599c2cc1b5fe9c85dcc7190040859f&si=ai%2Cco%2Cci%2Cre%2Cdi&checkin_monthday='.$checkin_day.'&checkin_year_month='.$checkin_year.'-'.$checkin_month.'&checkout_monthday='.$checkout_day.'&checkout_year_month='.$checkout_year.'-'.$checkout_month.'&group_adults=2&group_children=0&clear_group=0&dest_type=city&dest_id='.$destination_id;

$i = 1;
while($url != '')
{
    $html = scraperWiki::scrape($url);

    $record = array(
        'url' => $url,
        'html' => $html,
    );
    scraperwiki::save_sqlite(array('url'), $record, $table_name = 'hotel_list_pages');

    $dom->load($html);

    $tds = $dom->find("td.next a");
    
    if(sizeof($tds))
    {
        $url = $base.$tds[0]->href;
    }
    else
    {
        $url = '';
    }
    echo($i++."\n");
}
?>
