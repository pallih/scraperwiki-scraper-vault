<?php

    require 'scraperwiki/simple_html_dom.php';
    require 'geograph/conversionslatlong.class.php';

    /*
    $fmtSampleFixed = array( "25p"     =>  array( "offset" => 109, "length" =>  5 ),
                             "median"  =>  array( "offset" =>  89, "length" =>  5 ),
                             "75p"     =>  array( "offset" =>  69, "length" =>  5 ),
                             "level"   =>  array( "offset" =>  48, "length" =>  6 ),
                             "time"    =>  array( "offset" =>   0, "length" => 13 ) );
    */

    $fmtSampleFixed = array( "level"   =>  array( "offset" =>  48, "length" =>  6 ),
                             "time"    =>  array( "offset" =>   0, "length" => 13 ) );

    $urlBase = 'http://www2.nve.no/h/hd/plotreal/H/';
    $urlDamList = $urlBase . 'list.html';
    $htmDamList = scraperWiki::scrape( $urlDamList );
    $domDamList = new simple_html_dom( $htmDamList );
    foreach( $domDamList->find( 'a' ) as $dam ) {
        if( preg_match( "/[0-9]+\\.[0-9]+\\.[0-9]+/", $dam->href, $m ) ) {

            $uidDam = $m[0];
            $titDam = utf8_encode( $dam->plaintext );

            $urlInf = $urlBase . $dam->href;
            $txtInf = utf8_encode( scraperWiki::scrape( $urlInf ) );
            preg_match_all( "/((?:Sone :)|(?:.st  :)|(?:Nord :)) <B>([^<]+)</u", $txtInf, $m, PREG_SET_ORDER );
            foreach( $m as $kv ) $pos[ $kv[ 1 ] ] = $kv[ 2 ];
            $utmDam = sprintf( "%sN %s %s", $pos[ "Sone :" ], $pos[ "Nord :" ], $pos[ "Øst  :" ] );
            $urlDam = $urlBase . str_replace( 'index.html', 'basis.txt', $dam->href );
            $txtDam = scraperWiki::scrape( $urlDam );
            $arrDam = explode( "\n", $txtDam );
            $lenArr = count( $arrDam );

            for( $i = 2; $i < $lenArr; $i++ ) {
                $row = array();
                $ln = $arrDam[ $i ];
                foreach( $fmtSampleFixed as $col => $pos ) {
                    $row[ $col ] = trim( substr( $ln, $pos[ "offset" ], $pos[ "length" ] ) );
                }
    
                if( !is_numeric( $row[ "level" ] ) ) continue;

                $row[ "time" ] = sprintf( "%s-%s-%s %s:%s:00", 
                                          substr( $row[ "time" ],  0, 2 ),
                                          substr( $row[ "time" ],  2, 2 ),
                                          substr( $row[ "time" ],  4, 4 ),
                                          substr( $row[ "time" ],  9, 2 ),
                                          substr( $row[ "time" ], 11, 2 ));
    
                $row[ "id_dam" ]  = $uidDam;
                $row[ "dam" ]     = $titDam;
                $row[ "utm_pos" ] = empty( $utmDam ) ? "NULL" : $utmDam;
    
                scraperWiki::save( array( 'id_dam', 'time' ), $row );
            }
        }
    }

?>
<?php

    require 'scraperwiki/simple_html_dom.php';
    require 'geograph/conversionslatlong.class.php';

    /*
    $fmtSampleFixed = array( "25p"     =>  array( "offset" => 109, "length" =>  5 ),
                             "median"  =>  array( "offset" =>  89, "length" =>  5 ),
                             "75p"     =>  array( "offset" =>  69, "length" =>  5 ),
                             "level"   =>  array( "offset" =>  48, "length" =>  6 ),
                             "time"    =>  array( "offset" =>   0, "length" => 13 ) );
    */

    $fmtSampleFixed = array( "level"   =>  array( "offset" =>  48, "length" =>  6 ),
                             "time"    =>  array( "offset" =>   0, "length" => 13 ) );

    $urlBase = 'http://www2.nve.no/h/hd/plotreal/H/';
    $urlDamList = $urlBase . 'list.html';
    $htmDamList = scraperWiki::scrape( $urlDamList );
    $domDamList = new simple_html_dom( $htmDamList );
    foreach( $domDamList->find( 'a' ) as $dam ) {
        if( preg_match( "/[0-9]+\\.[0-9]+\\.[0-9]+/", $dam->href, $m ) ) {

            $uidDam = $m[0];
            $titDam = utf8_encode( $dam->plaintext );

            $urlInf = $urlBase . $dam->href;
            $txtInf = utf8_encode( scraperWiki::scrape( $urlInf ) );
            preg_match_all( "/((?:Sone :)|(?:.st  :)|(?:Nord :)) <B>([^<]+)</u", $txtInf, $m, PREG_SET_ORDER );
            foreach( $m as $kv ) $pos[ $kv[ 1 ] ] = $kv[ 2 ];
            $utmDam = sprintf( "%sN %s %s", $pos[ "Sone :" ], $pos[ "Nord :" ], $pos[ "Øst  :" ] );
            $urlDam = $urlBase . str_replace( 'index.html', 'basis.txt', $dam->href );
            $txtDam = scraperWiki::scrape( $urlDam );
            $arrDam = explode( "\n", $txtDam );
            $lenArr = count( $arrDam );

            for( $i = 2; $i < $lenArr; $i++ ) {
                $row = array();
                $ln = $arrDam[ $i ];
                foreach( $fmtSampleFixed as $col => $pos ) {
                    $row[ $col ] = trim( substr( $ln, $pos[ "offset" ], $pos[ "length" ] ) );
                }
    
                if( !is_numeric( $row[ "level" ] ) ) continue;

                $row[ "time" ] = sprintf( "%s-%s-%s %s:%s:00", 
                                          substr( $row[ "time" ],  0, 2 ),
                                          substr( $row[ "time" ],  2, 2 ),
                                          substr( $row[ "time" ],  4, 4 ),
                                          substr( $row[ "time" ],  9, 2 ),
                                          substr( $row[ "time" ], 11, 2 ));
    
                $row[ "id_dam" ]  = $uidDam;
                $row[ "dam" ]     = $titDam;
                $row[ "utm_pos" ] = empty( $utmDam ) ? "NULL" : $utmDam;
    
                scraperWiki::save( array( 'id_dam', 'time' ), $row );
            }
        }
    }

?>
