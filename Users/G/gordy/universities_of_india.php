<?php
require 'scraperwiki/simple_html_dom.php';   

$link = "http://www.indiastudycenter.com/Univ/Statewise-Universities.asp";
run( "India", $link );

function run( $country, $link) 
{
    $dom = getHtmlDom( $link );
    $counter = 0;
    foreach( $dom->find( "div.r div.c p" ) as $entry )
    {
        $ancs = $entry->find( "a" );
        if ( empty( $ancs ) )
        {
            continue;
        }

        if( strlen( $entry->plaintext ) == strlen( $ancs[ 0 ]->plaintext ) )
        {
            $link = "http://www.indiastudycenter.com" . str_replace( ' ', '+', htmlspecialchars_decode( $ancs[ 0 ]->href ) );
            $state = fixEncoding( $ancs[ 0 ]->plaintext );
            echo "Parsing $state \n";
            parseState( $country, $state, $link );
        }
    }
    return $counter;
}


function parseState( $country, $state, $link ) 
{
    $dom = getHtmlDom( $link );
    $counter = 0;
    foreach( $dom->find( "div.r div.c p" ) as $entry )
    {
        $ancs = $entry->find( "a" );
        if ( empty( $ancs ) )
        {
            continue;
        }
        
        if( strlen( $entry->plaintext ) == strlen( $ancs[ 0 ]->plaintext ) )
        {
            $counter++;            
            $name = fixEncoding( $ancs[ 0 ]->plaintext );
            $record = getDetails( $country, $state, $name, "http://www.indiastudycenter.com" . str_replace( ' ', '+', htmlspecialchars_decode( $ancs[ 0 ]->href ) ) );
            scraperwiki::save( array( 'name' ), $record );
        }
    }
    return $counter;
}

function getDetails( $country, $state, $name, $link ) 
{
    $dom = getHtmlDom( $link );
    $details= array();
    $ename = explode( ",", $name);
    $details[ 'name' ] = trim( $ename [ 0 ] );
    $details[ 'country' ] = trim( $country );
    $details[ 'state' ] = trim( $state );
    $divrs = $dom->find( "div.r");
    if ( !empty ( $divrs ) ) 
    {
        $divcs = $divrs[ 0 ]->find( "div.c");
        if ( !empty ( $divcs ) ) 
        {
            foreach( $divcs[ 0 ]->find( "p" ) as $entry )
            {
                $contact = fixEncoding( $entry->plaintext );
                $telephone = getTelephone( $contact );
                if ( null != $telephone ) 
                {
                    $details[ 'telephone' ] = fixEncoding( $telephone );
                    continue;
                }
                $fax = getFax( $contact );
                if ( null != $fax ) 
                {
                    $details[ 'fax' ] = fixEncoding( $fax );
                    continue;
                }
                $email = getEmail( $contact );
                if ( null != $email ) 
                {
                    $details[ 'email' ] = fixEncoding( $email );
                    continue;
                }
                $website = getWebsite( $contact ); 
                if ( null != $website ) 
                {
                    $details[ 'website' ] = fixEncoding( $website );
                    continue;
                }
                if ( null == getPincode( $contact ) ) 
                {
                    $address = getAddress( $contact );
                    $addressCount = count( $address );
                    foreach( $address as $id => $line )
                    {
                        $details[ 'address ' . ($id + 1) ] = fixEncoding( $line );
                    }
                }
            }
        }
    }
    return $details;
}

function getAddress( $contact )
{
    $addressString = substr( $contact, 0 );
    return mb_split( '[/\n]', $addressString );
}

function getPincode( $contact )
{
    $matches = explode( 'Pin Code:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function getEmail( $contact )
{
    $matches = explode( 'Email:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function getWebsite( $contact )
{
    $matches = explode( 'page:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return "http://".trim( $matches[ 1 ] );
    }
    return null;
}

function getTelephone( $contact )
{
    $matches = explode( 'Telephone:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function getFax( $contact )
{
    $matches = explode( 'Fax:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function fixEncoding( $in_str ) 
{ 
    $cur_encoding = mb_detect_encoding( $in_str ) ; 
    if( $cur_encoding == "UTF-8" && mb_check_encoding( $in_str,"UTF-8" ) ) {
        return addslashes( $in_str ); 
    } else { 
        return addslashes( utf8_encode($in_str) ); 
    }
} 

function getHtmlDom( $link ) 
{
    $html = scraperWiki::scrape( $link );
    $dom = new simple_html_dom();
    $dom->load( $html );
    return $dom;
}<?php
require 'scraperwiki/simple_html_dom.php';   

$link = "http://www.indiastudycenter.com/Univ/Statewise-Universities.asp";
run( "India", $link );

function run( $country, $link) 
{
    $dom = getHtmlDom( $link );
    $counter = 0;
    foreach( $dom->find( "div.r div.c p" ) as $entry )
    {
        $ancs = $entry->find( "a" );
        if ( empty( $ancs ) )
        {
            continue;
        }

        if( strlen( $entry->plaintext ) == strlen( $ancs[ 0 ]->plaintext ) )
        {
            $link = "http://www.indiastudycenter.com" . str_replace( ' ', '+', htmlspecialchars_decode( $ancs[ 0 ]->href ) );
            $state = fixEncoding( $ancs[ 0 ]->plaintext );
            echo "Parsing $state \n";
            parseState( $country, $state, $link );
        }
    }
    return $counter;
}


function parseState( $country, $state, $link ) 
{
    $dom = getHtmlDom( $link );
    $counter = 0;
    foreach( $dom->find( "div.r div.c p" ) as $entry )
    {
        $ancs = $entry->find( "a" );
        if ( empty( $ancs ) )
        {
            continue;
        }
        
        if( strlen( $entry->plaintext ) == strlen( $ancs[ 0 ]->plaintext ) )
        {
            $counter++;            
            $name = fixEncoding( $ancs[ 0 ]->plaintext );
            $record = getDetails( $country, $state, $name, "http://www.indiastudycenter.com" . str_replace( ' ', '+', htmlspecialchars_decode( $ancs[ 0 ]->href ) ) );
            scraperwiki::save( array( 'name' ), $record );
        }
    }
    return $counter;
}

function getDetails( $country, $state, $name, $link ) 
{
    $dom = getHtmlDom( $link );
    $details= array();
    $ename = explode( ",", $name);
    $details[ 'name' ] = trim( $ename [ 0 ] );
    $details[ 'country' ] = trim( $country );
    $details[ 'state' ] = trim( $state );
    $divrs = $dom->find( "div.r");
    if ( !empty ( $divrs ) ) 
    {
        $divcs = $divrs[ 0 ]->find( "div.c");
        if ( !empty ( $divcs ) ) 
        {
            foreach( $divcs[ 0 ]->find( "p" ) as $entry )
            {
                $contact = fixEncoding( $entry->plaintext );
                $telephone = getTelephone( $contact );
                if ( null != $telephone ) 
                {
                    $details[ 'telephone' ] = fixEncoding( $telephone );
                    continue;
                }
                $fax = getFax( $contact );
                if ( null != $fax ) 
                {
                    $details[ 'fax' ] = fixEncoding( $fax );
                    continue;
                }
                $email = getEmail( $contact );
                if ( null != $email ) 
                {
                    $details[ 'email' ] = fixEncoding( $email );
                    continue;
                }
                $website = getWebsite( $contact ); 
                if ( null != $website ) 
                {
                    $details[ 'website' ] = fixEncoding( $website );
                    continue;
                }
                if ( null == getPincode( $contact ) ) 
                {
                    $address = getAddress( $contact );
                    $addressCount = count( $address );
                    foreach( $address as $id => $line )
                    {
                        $details[ 'address ' . ($id + 1) ] = fixEncoding( $line );
                    }
                }
            }
        }
    }
    return $details;
}

function getAddress( $contact )
{
    $addressString = substr( $contact, 0 );
    return mb_split( '[/\n]', $addressString );
}

function getPincode( $contact )
{
    $matches = explode( 'Pin Code:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function getEmail( $contact )
{
    $matches = explode( 'Email:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function getWebsite( $contact )
{
    $matches = explode( 'page:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return "http://".trim( $matches[ 1 ] );
    }
    return null;
}

function getTelephone( $contact )
{
    $matches = explode( 'Telephone:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function getFax( $contact )
{
    $matches = explode( 'Fax:', $contact );
    if( is_array( $matches ) && count( $matches ) == 2 )
    {
        return trim( $matches[ 1 ] );
    }
    return null;
}

function fixEncoding( $in_str ) 
{ 
    $cur_encoding = mb_detect_encoding( $in_str ) ; 
    if( $cur_encoding == "UTF-8" && mb_check_encoding( $in_str,"UTF-8" ) ) {
        return addslashes( $in_str ); 
    } else { 
        return addslashes( utf8_encode($in_str) ); 
    }
} 

function getHtmlDom( $link ) 
{
    $html = scraperWiki::scrape( $link );
    $dom = new simple_html_dom();
    $dom->load( $html );
    return $dom;
}