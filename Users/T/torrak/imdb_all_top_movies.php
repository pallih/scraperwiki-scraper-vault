<?php
# This grabs the IMDB movie ids(in the form tt0123456 from all IMDb "Top" pages.
# ******************* #
# IMDB All Top Movies #
# ******************* #
/** NOTES:
- On all pages but the "Top 250" page, we get 60 movie links per page: 50 top movies + 10 bottom movies. (At the time of creation ofthis scraper.)
**/

# requirements
// print_r ($_SERVER);
require ( @$_SERVER['LOGNAME'] == 'scriptrunner' ? 'scraperwiki/' : '' ) . 'simple_html_dom.php';

# Setting up the variables
$sources = array(
            'http://www.imdb.com/chart/top',
            'http://www.imdb.com/chart/action',
            'http://www.imdb.com/chart/adventure',
            'http://www.imdb.com/chart/animation',
            'http://www.imdb.com/chart/biography',
            'http://www.imdb.com/chart/comedy',
            'http://www.imdb.com/chart/crime',
            //'http://www.imdb.com/chart/documentary',
            'http://www.imdb.com/chart/drama',
            'http://www.imdb.com/chart/family',
            'http://www.imdb.com/chart/fantasy',
            'http://www.imdb.com/chart/filmnoir',
            'http://www.imdb.com/chart/history',
            'http://www.imdb.com/chart/horror',
            'http://www.imdb.com/chart/independent',
            'http://www.imdb.com/chart/music',
            'http://www.imdb.com/chart/musical',
            'http://www.imdb.com/chart/mystery',
            'http://www.imdb.com/chart/romance',
            'http://www.imdb.com/chart/scifi',
            //'http://www.imdb.com/chart/short',
            'http://www.imdb.com/chart/sport',
            'http://www.imdb.com/chart/thriller',
            //'http://www.imdb.com/chart/tvminiseries',
            'http://www.imdb.com/chart/war',
            'http://www.imdb.com/chart/western'
            );
$movie_ids = array(); // will hold our results
print_r ($sources );

# Set up cURL
$ch = curl_init();
curl_setopt($ch, CURLOPT_USERAGENT, "Lynx/2.8.4dev.7 libwww-FM/2.14");    // just in case
curl_setopt($ch, CURLOPT_FAILONERROR, true);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);


# Grab data
foreach ( $sources as $source) {
    $links_page = array();
    curl_setopt($ch, CURLOPT_URL, $source );
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Cache-Control: no-cache'));
    $page = curl_exec($ch);
    if (!$page) {
        echo "<br />cURL error number:" .curl_errno($ch);
        echo "<br />cURL error:" . curl_error($ch);
        exit;
    }
    $html = str_get_html($page);
    foreach( $html->find('a') as $link ) {
        if ( isset($link->href) && ( preg_match( "$/title/tt[0-9]+/$", $link->href ) ) ) {
            preg_match( "/tt[0-9]+/", $link->href, $matches );
            $links_page[] = $matches[0]; // really they're IDs, not links, but given the context the name makes sense (still have to filter them out)
        }
    }
    // Remove the bottom movies -- the Top 250 list is spared by design
    if ( count( $links_page ) == 60 ) {
        array_splice( $links_page, 50 );
    }
    $movie_ids = array_merge( $movie_ids, $links_page );
}
echo "Number of movie IDs collected (including likely duplicates): " . count( $movie_ids ) . "\n";


# Clean up the data: remove duplicates
$movie_ids = array_unique( $movie_ids );
echo "Number of movie IDs collected (unique): " . count( $movie_ids ) . "\n";


# Here are the results!
foreach ($movie_ids as $key => $val) {
    scraperwiki::save_sqlite(array("id", "imdb_id"), array( "id" => $key, "imdb_id" => $val ) );
    //echo "key: " . $key . " / " . "value: " . $val . "\n";
}
//print_r( $movie_ids );


# §

# Figuring out the syntax for the database function on ScraperWiki:
/*
scraperwiki::save_sqlite($unique_keys, $data)
    where:
    $unique_keys is an array
    $data is an array IN WHICH one of the index names is same as oe ofthe unique keys given i the previous argument   
*/

?>