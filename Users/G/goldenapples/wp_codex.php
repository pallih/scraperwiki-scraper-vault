<?php

require( 'scraperwiki/simple_html_dom.php' );

$prefix = 'http://codex.wordpress.org';

$raw = scraperwiki::scrape( 'http://codex.wordpress.org/index.php?title=Special:AllPages' );
$html = str_get_html( $raw );

foreach ( $html->find('td[align="right"] a') as $page ) {
    $page_url = html_entity_decode( $prefix . $page->href );
    print ( "Scraping: " . $page_url . "\r\n" );

    $page_raw = scraperwiki::scrape( $page_url );
    $page_html = str_get_html( $page_raw );

    $table = $page_html->find('table', 2);

    foreach ( $table->find( 'a' ) as $single_page ) {
        $page_elts = array(
            'title' => $single_page->plaintext,
            'href' => $single_page->href
        );
        if ( strpos( $page_elts['href'], 'Special:' ) !== false )
            continue;
        scraperwiki::save_sqlite( array( 'title' ), $page_elts, 'codex_pages' );
    }

}

?>
