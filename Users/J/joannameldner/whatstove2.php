<?php


require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any/");
$html = str_get_html($html_content);

foreach($html->find("div.jr_tableview a") as $data){
    #print $data . "\n";
    $pos = strpos ( $data->href , '#' );
#    if ( $pos === FALSE ) {
#        print $data->href . "\n";
#        NULL;}

    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record); 
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=2&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=3&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=4&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=5&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}


$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=6&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=7&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=8&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=9&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=10&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}
?>
<?php


require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any/");
$html = str_get_html($html_content);

foreach($html->find("div.jr_tableview a") as $data){
    #print $data . "\n";
    $pos = strpos ( $data->href , '#' );
#    if ( $pos === FALSE ) {
#        print $data->href . "\n";
#        NULL;}

    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record); 
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=2&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=3&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=4&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=5&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}


$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=6&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=7&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=8&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=9&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}

$html_content = scraperwiki::scrape("www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=10&query=any");
$html = str_get_html($html_content);
foreach($html->find("div.jr_tableview a") as $data){
    $pos = strpos ( $data->href , '#' );
    if ( $pos === FALSE ) {
            $record = array( 'link' =>$data->href);
            scraperwiki::save(array('link'), $record);
            #print json_encode($record) . "\n";
        NULL;
        }
}
?>
