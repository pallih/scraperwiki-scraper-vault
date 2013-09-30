<?php
require 'scraperwiki/simple_html_dom.php';   

$link = "http://www.clas.ufl.edu/au/";
echo parsePage( "United States", $link ) ." saved\n";


function parsePage( $country, $link ) 
{
    $html = scraperWiki::scrape( $link );

    $dom = new simple_html_dom();
    $dom->load( $html );
    $counter = 0;
    foreach( $dom->find( "div#mainContainer div#content p" ) as $entry )
    {
        $ancs = $entry->find( "a" );
        if ( empty( $ancs ) )
        {
            continue;
        }
        $name = fixEncoding( $ancs[ 0 ]->plaintext );
        
        if( strlen( $entry->plaintext ) == strlen( $ancs[ 0 ]->plaintext ) && $entry->plaintext != 'top of page' )
        {
            $record = array( 'country' => $country, 'name' => $name, 'link' => $ancs[ 0 ]->href );
            scraperWiki::save( array( 'link' ), $record );
            $counter++;
        }
    }
    return $counter;
}

function fixEncoding( $in_str )
{
    $cur_encoding = mb_detect_encoding( $in_str );
    if( $cur_encoding == "UTF-8" && mb_check_encoding( $in_str, "UTF-8" ) )
    {
        return htmlspecialchars_decode( $in_str );
    }
    else
    {
        return utf8_encode( htmlspecialchars_decode( $in_str ) );
    }
}<?php
require 'scraperwiki/simple_html_dom.php';   

$link = "http://www.clas.ufl.edu/au/";
echo parsePage( "United States", $link ) ." saved\n";


function parsePage( $country, $link ) 
{
    $html = scraperWiki::scrape( $link );

    $dom = new simple_html_dom();
    $dom->load( $html );
    $counter = 0;
    foreach( $dom->find( "div#mainContainer div#content p" ) as $entry )
    {
        $ancs = $entry->find( "a" );
        if ( empty( $ancs ) )
        {
            continue;
        }
        $name = fixEncoding( $ancs[ 0 ]->plaintext );
        
        if( strlen( $entry->plaintext ) == strlen( $ancs[ 0 ]->plaintext ) && $entry->plaintext != 'top of page' )
        {
            $record = array( 'country' => $country, 'name' => $name, 'link' => $ancs[ 0 ]->href );
            scraperWiki::save( array( 'link' ), $record );
            $counter++;
        }
    }
    return $counter;
}

function fixEncoding( $in_str )
{
    $cur_encoding = mb_detect_encoding( $in_str );
    if( $cur_encoding == "UTF-8" && mb_check_encoding( $in_str, "UTF-8" ) )
    {
        return htmlspecialchars_decode( $in_str );
    }
    else
    {
        return utf8_encode( htmlspecialchars_decode( $in_str ) );
    }
}