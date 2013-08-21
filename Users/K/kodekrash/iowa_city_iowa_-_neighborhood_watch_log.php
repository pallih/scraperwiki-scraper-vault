<?php

    function partof( $src, $start = null, $stop = null, $inclusive = false ) {
        $b = empty( $start ) ? 0 : strpos( strtolower( $src ), strtolower( $start ), 0 );
        if( $b >= 0 ) {
            $b += $inclusive ? 0 : strlen( $start );
            $e = empty( $stop ) ? strlen( $src ) : strpos( strtolower( $src ), strtolower( $stop ), $b );
            $e += $inclusive ? strlen( $stop ) : 0;
            $e = $e > strlen( $src ) ? strlen( $src ) : $e;
            if( $e > $b ) {
                return trim( substr( $src, $b, $e - $b ) );
            }
        }
    }

    $URL = 'http://www.iowa-city.org/icgov/apps/police/neighborhood.asp';
    $x = scraperWiki::scrape( $URL );
    if( !empty( $x ) ) {
        $x = partof( $x, '<h1>Neighborhood Watch Log</h1>', '<div class="clear"></div>' );
        $x = partof( $x, '<tbody', '</tbody>', true );
        $x = explode( '</tr>', $x );
        if( count( $x ) > 0 ) {
            foreach( $x as $y ) {
                if( preg_match_all( '/<td(.*?)>(.*?)<\/td>/iu', $y, $m ) ) {
                    if( count( $m[2] ) == 6 ) {
                        $d = array();
                        $d['id'] = partof( $m[2][0], '>', '</a>' );
                        $d['link'] = $URL . str_replace( '&amp;', '&', partof( $m[2][0], '"', '"' ) );
                        $z = trim( $m[2][1] );
                        $d['activity'] = empty( $z ) ? null : $z;
                        $d['disposition'] = partof( $m[2][2], '>', '</a>' );
                        $d['location'] = trim( $m[2][3] );
                        $d['datetime'] = date( 'Y-m-d H:i:s', strtotime( trim( $m[2][4] ) ) );
                        $d['notes'] = (bool)( strlen( trim( $m[2][5] ) ) > 1 );
                        scraperwiki::save( array( 'id' ), $d );
                    }
                }
            }
        }
    }

?>