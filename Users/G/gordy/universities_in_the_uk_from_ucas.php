<?php
require 'scraperwiki/simple_html_dom.php';

$letters = 'abcdefghijklmnopqrstuvwxyz';
$numLetters = strlen( $letters );
for( $i = 0; $i < $numLetters; $i++ )
{
    $html = scraperWiki::scrape( "http://www.ucas.com/students/choosingcourses/choosinguni/instguide/" . $letters[ $i ] . "/" );

    $dom = new simple_html_dom();
    $dom->load( $html );
    foreach( $dom->find( "tr" ) as $data )
    {
        $tds = $data->find( "td" );
        $h3 = $tds[ 0 ]->find( "h3" );
        $university = $h3[ 0 ]->plaintext;
        $contactString = str_replace( $university, "", $tds[ 0 ]->plaintext );
        $uniObject = getDetails( $university, $contactString );
        if( isset( $tds[ 1 ] ) )
        {
            $img = $tds[ 1 ]->find( "img" );
            $uniObject[ 'image' ] = "http://www.ucas.com/" . $img[ 0 ]->src . "\n";
        }
        scraperwiki::save( array( 'code' ), $uniObject );
    }
}

function getDetails( $university, $contact )
{
    $details = array( );
    $codeName = mb_split( '[-]', $university );
    $details[ 'code' ] = trim( $codeName[ 0 ] );
    $details[ 'name' ] = trim( $codeName[ 1 ] );
    $address = getAddress( $contact );
    $addressCount = count( $address );
    foreach( $address as $id => $line )
    {
        if( $addressCount == $id + 1 )
        {
            $details[ 'postcode' ] = $line;
        }
        else
        {
            $details[ 'address ' . ($id + 1) ] = $line;
        }
    }
    $details[ 'telephone' ] = getTelephone( $contact );
    $details[ 'fax' ] = getFax( $contact );
    $details[ 'email' ] = getEmail( $contact );
    $details[ 'link' ] = getWebsite( $contact );
    $details[ 'country' ] = "United Kingdom";
    return $details;
}

function getAddress( $contact )
{
    $tstart = strpos( $contact, "t:" );
    $addressString = substr( $contact, 0, strrpos( substr( $contact, 0, $tstart ), "\n" ) );
    return mb_split( '[/\n]', $addressString );
}

function getEmail( $contact )
{
    $matches = array( );
    preg_match( '/(?s)e:(.*?)\n/', $contact, $matches );
    if( is_array( $matches ) && !empty( $matches ) )
    {
        return substr( $matches[ 0 ], 3 );
    }
    return null;
}

function getWebsite( $contact )
{
    $matches = array( );
    preg_match( '/(?s)w:.*?\n/', $contact, $matches );
    if( is_array( $matches ) && !empty( $matches ) )
    {
        return "http://" . substr( $matches[ 0 ], 3 );
    }
    return null;
}

function getTelephone( $contact )
{
    $matches = array( );
    preg_match( '/(?s)t:.*?\n/', $contact, $matches );
    if( is_array( $matches ) && !empty( $matches ) )
    {
        return substr( $matches[ 0 ], 3 );
    }
    return null;
}

function getFax( $contact )
{
    $matches = array( );
    preg_match( '/(?s)f:.*?\n/', $contact, $matches );
    if( is_array( $matches ) && !empty( $matches ) )
    {
        return substr( $matches[ 0 ], 3 );
    }
    return null;
}