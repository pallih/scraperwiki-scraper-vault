<?php

require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape( "http://www.findaschool.org/" );
setlocale(LC_ALL, 'en_GB');
$dom = new simple_html_dom();
$dom->load( $html );
$x = 0;
foreach( $dom->find( "tr" ) as $data )
{
    $ths = $data->find( "th" );
    $tds = $data->find( "td" );
    $country = $ths[ 0 ]->plaintext;
    if( isset( $tds[ 0 ] ) )
    {
        $links = $tds[ 0 ]->find( "a" );
        if( isset( $links[ 0 ] ) )
        {
            $pageNo = 0;
            $link = "http://www.findaschool.org/" . str_replace( ' ', '+', htmlspecialchars_decode( $links[ 0 ]->href ) );
            echo "Parsing $country\n";
            $noRecords = parsePage( $country, $link, $pageNo );
            echo " - " . $noRecords . " records parsed\n";
        }
    }
}

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
        $in_str = iconv("UTF-8","UTF-8//TRANSLIT//IGNORE", htmlspecialchars_decode( $in_str ) );
    }
    else
    {
        $in_str = iconv("UTF-8","UTF-8//TRANSLIT//IGNORE", utf8_encode(  htmlspecialchars_decode( $in_str ) ) );
    }
    $search = explode(",","ç,æ,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø,u,í,“,”,õ,ã");
    $replace = explode(",","c,ae,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o,u,i,\",\",o,a");
    return  str_replace($search, $replace, $in_str);
}
<?php

require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape( "http://www.findaschool.org/" );
setlocale(LC_ALL, 'en_GB');
$dom = new simple_html_dom();
$dom->load( $html );
$x = 0;
foreach( $dom->find( "tr" ) as $data )
{
    $ths = $data->find( "th" );
    $tds = $data->find( "td" );
    $country = $ths[ 0 ]->plaintext;
    if( isset( $tds[ 0 ] ) )
    {
        $links = $tds[ 0 ]->find( "a" );
        if( isset( $links[ 0 ] ) )
        {
            $pageNo = 0;
            $link = "http://www.findaschool.org/" . str_replace( ' ', '+', htmlspecialchars_decode( $links[ 0 ]->href ) );
            echo "Parsing $country\n";
            $noRecords = parsePage( $country, $link, $pageNo );
            echo " - " . $noRecords . " records parsed\n";
        }
    }
}

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
        $in_str = iconv("UTF-8","UTF-8//TRANSLIT//IGNORE", htmlspecialchars_decode( $in_str ) );
    }
    else
    {
        $in_str = iconv("UTF-8","UTF-8//TRANSLIT//IGNORE", utf8_encode(  htmlspecialchars_decode( $in_str ) ) );
    }
    $search = explode(",","ç,æ,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø,u,í,“,”,õ,ã");
    $replace = explode(",","c,ae,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o,u,i,\",\",o,a");
    return  str_replace($search, $replace, $in_str);
}
