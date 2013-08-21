<?php

require 'scraperwiki/simple_html_dom.php';
//error_reporting(E_COMPILE_ERROR|E_ERROR|E_CORE_ERROR);
setlocale(LC_ALL, 'en_GB');
$pageNo = 0;
$link = "http://www.findaschool.org/index.php?Country=Germany";
echo "Parsing $country\n";
$noRecords = parsePage( "Germany" , $link, $pageNo );
echo " - " . $noRecords . " records parsed\n";


function parsePage( $country, $link, $pageNo )
{
    $html2 = scraperWiki::scrape( $link );
    $dom2 = new simple_html_dom();
    $dom2->load( $html2 );
    $counter = 0;
    foreach( $dom2->find( "ol li" ) as $entry )
    {
        $ancs = $entry->find( "a" );
        $name = fixEncoding( $ancs[ 0 ]->plaintext );
        $record = array( 'name' => $name, 'link' => fixEncoding( $ancs[ 0 ]->href ), 'country' => fixEncoding( $country ) );
        if( strlen( $entry->plaintext ) > strlen( $ancs[ 0 ]->plaintext ) )
        {
            $state = fixEncoding( substr( $entry->plaintext, strlen( $ancs[ 0 ]->plaintext ) ) );
            $record[ 'state' ] = trim( $state, "( )" );
        }
        scraperWiki::save( array( 'link' ), $record );
        $counter++;
    }
    $pages = $dom2->find( "div.centercontent center a" );
    if( isset( $pages[ ++$pageNo ] ) )
    {
        $counter += parsePage( $country, "http://www.findaschool.org" . str_replace( ' ', '+', htmlspecialchars_decode( $pages[ $pageNo ]->href ) ), $pageNo );
    }
    return $counter;
}

function fixEncoding( $in_str )
{
    $cur_encoding = mb_detect_encoding( $in_str );
    if( $cur_encoding == "UTF-8" && mb_check_encoding( $in_str, "UTF-8" ) )
    {
        return iconv("UTF-8","UTF-8//TRANSLIT", htmlspecialchars_decode( $in_str ) );
    }
    else
    {
        return iconv("UTF-8","UTF-8//TRANSLIT", utf8_encode(  htmlspecialchars_decode( $in_str ) ) );
    }
}
