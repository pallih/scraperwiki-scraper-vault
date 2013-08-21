<?php

require 'scraperwiki/simple_html_dom.php';
//static $counter = 0;
//scraperwiki::save_sqlite( array( 'url' ), array( 'count' => $counter, 'url' => 'http://tunein.com' ), 'pages' );
//scrape_related('http://tunein.com/radio/Music-g1/');

$counter = scraperwiki::get_var('up_to') + 1;

while( $result = scraperwiki::select( "* from pages where count = '$counter'" ) ) {
    scrape_stations( $result[0]['url'] );
    scraperwiki::save_var( 'up_to', $counter );
    $counter++; 
}

function scrape_related( $url ) {
    $exists = scraperwiki::select( "* from pages where url = '$url'" );
    if ( count($exists) ) {
        print_r( $exists );
        return;
    }
    global $counter; $counter++;
    scraperwiki::save_sqlite( array( 'url' ), array( 'count' => $counter, 'url' => $url ), 'pages' );
    $html_content = scraperwiki::scrape( $url );
    $html = str_get_html($html_content);
    foreach ( $html->find( 'div.related a' ) as $related ) {
        scrape_related( 'http://tunein.com' . $related->href );
    }
}

function scrape_stations( $url ) {
    $html_content = scraperwiki::scrape( $url );
    $html = str_get_html($html_content);
    foreach ( $html->find('tr.result') as $result ) {
        $logo = $result->find('img.logo',0)->src;
        if ( preg_match( '/\d{4,6}/', $result->find('a.play',0)->href, $links ) ) {
            $stationID = $links[0];
            $station = $result->find('td.show a',0)->plaintext;
            $tagline = $result->find('td.show span',0)->plaintext;
            $location = $result->find('.location',0)->plaintext;
            scraperwiki::save_sqlite(
                array('stationID'),
                array(
                    'stationID' => $stationID,
                    'station' => $station,
                    'tagline' => trim( $tagline, " -"),
                    'location' => $location,
                    'logo' => $logo
                    ), 'stations' );
            foreach ( $result->find('.genres a') as $genre ) 
                scraperwiki::save_sqlite( array(), array( 'stationID' => $stationID, 'genre' => $genre->plaintext ), 'genres' );
        }
    }
    if ( $next = $html->find('a.next',0) )
        if ( preg_match( "/(?<=location\.href=')[^']*/", $next->outertext, $matches ) )
            scrape_stations( 'http://tunein.com' . $matches[0] );

}

?>
