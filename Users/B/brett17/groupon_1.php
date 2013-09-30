<?php
require 'scraperwiki/simple_html_dom.php';           
set_time_limit( 24 * 3600 );
date_default_timezone_set('America/Toronto');

$base_url = "http://www.groupon.com/browse/dallas?post_subscribe=true";
$dom = new simple_html_dom();
$dom2 = new simple_html_dom();

 $html = scraperWiki::scrape( $base_url );
//usleep(100000);
$dom->load( $html );
$items = $dom->find( 'ul#jCitiesSelectBox li' );
foreach( $items as $item )
{
    //echo $item->onclick. "\n";
    if( !preg_match( "/'(http:[^']+)'/", $item->onclick, $match ) )
        continue;
    $city = $item->plaintext;
    $url = $match[1];
    $url = preg_replace( '/deals/', 'all-deals', $url);

    parseCity( $city, $url );

}


function parseCity( $city, $url )
{

    $html = scraperWiki::scrape( $url );
    if( ! preg_match( '/var itemsLocalDeals = (\[\{.*?\}\]);/', $html, $match ) )
        return;
    //echo  $match[1] . "\n";
    $deals = json_decode( $match[1], true ) ;
    foreach( $deals as $deal )
    {
        parseDeal( $deal, $city );
//exit();
    }

}


function cleanText( $text )
{
    $text = trim( preg_replace( '/\s{2,}/', ' ', $text) );
    return $text;

}

function parseDeal( $deal, $city = null )
{
    global $base_url;
    global $dom2;
    $url = $base_url . $deal['dealPermaLink'];

    $html = scraperWiki::scrape( $url );
    $dom2->load( $html );
    $result['link'] = $url;
    $result['city'] = $deal['cityUrlName'];
    $result['city2'] = $city;
    $result['image'] = $deal['imageUrl'];
    $result['category'] = $deal['category'];

    if( preg_match( '/[\d,]+/', $deal['dealOldPrice'], $match ) )
        $result['value'] = $match[0];

    if( preg_match( '/[\d,]+/', $deal['dealPrice'], $match ) )
        $result['price'] = $match[0];

    if( ( $tmp_data = $dom2->find( 'h1', 0 ) ) )
    {
           $result['title'] = trim( $tmp_data->plaintext );
    }
    else
        continue;
    if( ( $tmp_data = $dom2->find( 'div.contentBoxNormalLeft', 0 ) ) )
    {
           $result['description'] = cleanText( $tmp_data->plaintext );
    }
    else
        continue;

    $secLeft = 0;
    $tmp_data = $dom2->find( 'input[class="jcurrentTimeLeft"]', 0);
    if( $tmp_data && preg_match( '/\d+/', $tmp_data->value, $match ) )
    {

        $secLeft = $match[0] / 1000;
        $result['endDate'] = date('Y-m-d H:i:s', time() + $secLeft );
        $result['time'] = date('Y-m-d H:i:s');
    }

    if( ( $tmp_data = $dom2->find( 'div.merchantContact a', 0 ) ) )
    {
        $result['seller_link'] = cleanText( $tmp_data->href );
    }

    if( ( $tmp_data = $dom2->find( 'div.merchantContact h2', 0 ) ) )
    {
        $result['seller_name'] = cleanText( $tmp_data->plaintext );
    }
        
    if( ( $tmp_data = $dom2->find( 'div.merchantContact', 0 ) ) )
    {
        if( ( $tmp_a = $tmp_data->find( 'a', 0 ) ) )
            $tmp_a->innertext = '';

        if( ( $tmp_a = $tmp_data->find( 'h2', 0 ) ) )
            $tmp_a->innertext = '';

        $result['seller_address'] = cleanText( $tmp_data->plaintext);
    }    
    //print_r( $result ); exit();
    scraperwiki::save(array('link'), $result);
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';           
set_time_limit( 24 * 3600 );
date_default_timezone_set('America/Toronto');

$base_url = "http://www.groupon.com/browse/dallas?post_subscribe=true";
$dom = new simple_html_dom();
$dom2 = new simple_html_dom();

 $html = scraperWiki::scrape( $base_url );
//usleep(100000);
$dom->load( $html );
$items = $dom->find( 'ul#jCitiesSelectBox li' );
foreach( $items as $item )
{
    //echo $item->onclick. "\n";
    if( !preg_match( "/'(http:[^']+)'/", $item->onclick, $match ) )
        continue;
    $city = $item->plaintext;
    $url = $match[1];
    $url = preg_replace( '/deals/', 'all-deals', $url);

    parseCity( $city, $url );

}


function parseCity( $city, $url )
{

    $html = scraperWiki::scrape( $url );
    if( ! preg_match( '/var itemsLocalDeals = (\[\{.*?\}\]);/', $html, $match ) )
        return;
    //echo  $match[1] . "\n";
    $deals = json_decode( $match[1], true ) ;
    foreach( $deals as $deal )
    {
        parseDeal( $deal, $city );
//exit();
    }

}


function cleanText( $text )
{
    $text = trim( preg_replace( '/\s{2,}/', ' ', $text) );
    return $text;

}

function parseDeal( $deal, $city = null )
{
    global $base_url;
    global $dom2;
    $url = $base_url . $deal['dealPermaLink'];

    $html = scraperWiki::scrape( $url );
    $dom2->load( $html );
    $result['link'] = $url;
    $result['city'] = $deal['cityUrlName'];
    $result['city2'] = $city;
    $result['image'] = $deal['imageUrl'];
    $result['category'] = $deal['category'];

    if( preg_match( '/[\d,]+/', $deal['dealOldPrice'], $match ) )
        $result['value'] = $match[0];

    if( preg_match( '/[\d,]+/', $deal['dealPrice'], $match ) )
        $result['price'] = $match[0];

    if( ( $tmp_data = $dom2->find( 'h1', 0 ) ) )
    {
           $result['title'] = trim( $tmp_data->plaintext );
    }
    else
        continue;
    if( ( $tmp_data = $dom2->find( 'div.contentBoxNormalLeft', 0 ) ) )
    {
           $result['description'] = cleanText( $tmp_data->plaintext );
    }
    else
        continue;

    $secLeft = 0;
    $tmp_data = $dom2->find( 'input[class="jcurrentTimeLeft"]', 0);
    if( $tmp_data && preg_match( '/\d+/', $tmp_data->value, $match ) )
    {

        $secLeft = $match[0] / 1000;
        $result['endDate'] = date('Y-m-d H:i:s', time() + $secLeft );
        $result['time'] = date('Y-m-d H:i:s');
    }

    if( ( $tmp_data = $dom2->find( 'div.merchantContact a', 0 ) ) )
    {
        $result['seller_link'] = cleanText( $tmp_data->href );
    }

    if( ( $tmp_data = $dom2->find( 'div.merchantContact h2', 0 ) ) )
    {
        $result['seller_name'] = cleanText( $tmp_data->plaintext );
    }
        
    if( ( $tmp_data = $dom2->find( 'div.merchantContact', 0 ) ) )
    {
        if( ( $tmp_a = $tmp_data->find( 'a', 0 ) ) )
            $tmp_a->innertext = '';

        if( ( $tmp_a = $tmp_data->find( 'h2', 0 ) ) )
            $tmp_a->innertext = '';

        $result['seller_address'] = cleanText( $tmp_data->plaintext);
    }    
    //print_r( $result ); exit();
    scraperwiki::save(array('link'), $result);
}

?>
