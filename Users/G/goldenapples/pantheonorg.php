<?php

require 'scraperwiki/simple_html_dom.php'; 

$areas = array(
    'Heroes' => "http://pantheon.org/areas/heroes/",
    'Bestiary' => "http://pantheon.org/areas/bestiary/",
    'Folklore' => "http://pantheon.org/areas/folklore/",
    'Arthurian Legend' => "http://pantheon.org/areas/folklore/arthurian/",
     );


// Get all the different areas under "Mythology"
$html = scraperwiki::scrape( "http://pantheon.org/areas/mythology/" );
$dom = new simple_html_dom(); $dom->load($html);
    
foreach ( $dom->find( 'div.content p strong a' ) as $continent ) {
    if (!in_array( $continent->plaintext, array( 'Americas', 'Africa', 'Asia' ) ) ) {
    $html = scraperwiki::scrape( "http://pantheon.org/" . ltrim( $continent->href, '/' ) );
    $dom = new simple_html_dom(); $dom->load($html);

    foreach( $dom->find( 'div.content p strong a' ) as $region )
        if ( !in_array( $region->plaintext, array( 'Basque mythology', 'Celtic mythology', 'Etruscan mythology', 'Greek mythology', 'Greek people' ) ) )
        $areas[ $region->plaintext] = "http://pantheon.org/" . ltrim( $region->href, '/' );
    }
}

// Now loop through the A-Z listing(s) for each area
foreach( $areas as $category => $href ) {
    $html = scraperWiki::scrape( rtrim( $href, '/' ) . '/articles.html' );
    $dom = new simple_html_dom(); $dom->load($html);

    $azlist = $dom->find( 'frame' );
    foreach ( $azlist as $index => $frame ) {
        if ( 0 == $index )
            scrape_azlist( $category, rtrim( $href, '/' ) . '/' . $frame->src );
    }
}

function scrape_azlist( $category, $src ) {

    $html = scraperWiki::scrape( $src );
    $dom = new simple_html_dom(); $dom->load($html);

    $articles_dom = $dom->find( 'ul li a' );

    foreach ( $articles_dom  as $article ) {
        
        if ( strstr( $article->href, 'articles/' ) && strstr( $article->href, '.html' ) ) {

        $record = array(
            'name' => $article->plaintext,
            'category' => $category,
            'link' => $article->href
            );

        $details_source = scraperWiki::scrape( 'http://pantheon.org' . $article->href );
        $details = new simple_html_dom(); $details->load( $details_source );
        
        $source_keys = array( '', '', 'source', 'region', 'nationality' );

        foreach ( $details->find( 'div#trail ol li a' ) as $index => $trail ) {
            if (!in_array( $trail->plaintext, array( 'Home', 'Areas' ) ) )
                $record[ $source_keys[ $index ] ] = $trail->plaintext;
        }
        
        $author = $details->find( 'div#author' );
        if ( !empty( $author[0]->plaintext ) )
            $record['author'] = str_replace(  'by ', '', $author[0]->plaintext );
        
        foreach ( $details->find( 'div#details li' ) as $attr ) {
            $val = $attr->find( 'div.val' );

            if ( $val ) {

                $key = strtolower( str_replace( array( $val[0]->outertext, ' ', ':', ':', "\r", "\n" ), '', $attr->innertext ) );

                if ( $link = $val[0]->find( 'a' ) )
                    $record[ $key ] = $link[0]->href;
                else if ( 'n/a' !== $key )
                    $record[ $key ] = trim( $val[0]->plaintext );
            }
        }

        $body = $details->find( 'div#article' );
        $record['body'] = $body[0]->innertext;
        
        scraperwiki::save_sqlite( array('name'), $record, "characters" );

        }
    }

    foreach ( $dom->find( 'a.grey' ) as $next ) {

    if ( $next->plaintext == 'next' && !strstr( $src, $next->href ) && !strstr( $next->href, 'a-' ) )
        scrape_azlist( $category, implode( '/', explode( '/', $src, -1 ) ) . '/' . $next->href );

    }

    unset( $html, $dom );

}


?>
