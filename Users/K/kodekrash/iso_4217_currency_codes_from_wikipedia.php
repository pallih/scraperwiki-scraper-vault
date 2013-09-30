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

    $URL = 'http://en.wikipedia.org/wiki/ISO_4217';
    $x = scraperWiki::scrape( $URL );
    if( !empty( $x ) ) {
        $x = partof( $x, 'Active codes</span></h2>', '</table>' );
        $x = explode( '</tr>', $x );
        if( count( $x ) > 0 ) {
            foreach( $x as $y ) {
                if( preg_match_all( '/<td>(.*?)<\/td>/iu', $y, $m ) ) {
                    if( count( $m[1] ) == 5 ) {
                        $d = array();
                        $d['code'] = trim( $m[1][0] );
                        $z = trim( $m[1][1] );
                        $d['number'] = $z == 'Nil' ? null : $z;
                        $z = trim( $m[1][2] );
                        $z = $z == '.' ? null : $z;
                        $d['precision'] = strpos( $z, '<' ) ? substr( $z, 0, strpos( $z, '<' ) ) : $z;
                        $d['name'] = trim( strip_tags( $m[1][3] ) );
                        $d['locations'] = trim( str_replace( '  ', ' ', str_replace( '&#160;', ' ', strip_tags( $m[1][4] ) ) ) );
                        scraperwiki::save( array( 'code' ), $d );
                    }
                }
            }
        }
    }
?><?php

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

    $URL = 'http://en.wikipedia.org/wiki/ISO_4217';
    $x = scraperWiki::scrape( $URL );
    if( !empty( $x ) ) {
        $x = partof( $x, 'Active codes</span></h2>', '</table>' );
        $x = explode( '</tr>', $x );
        if( count( $x ) > 0 ) {
            foreach( $x as $y ) {
                if( preg_match_all( '/<td>(.*?)<\/td>/iu', $y, $m ) ) {
                    if( count( $m[1] ) == 5 ) {
                        $d = array();
                        $d['code'] = trim( $m[1][0] );
                        $z = trim( $m[1][1] );
                        $d['number'] = $z == 'Nil' ? null : $z;
                        $z = trim( $m[1][2] );
                        $z = $z == '.' ? null : $z;
                        $d['precision'] = strpos( $z, '<' ) ? substr( $z, 0, strpos( $z, '<' ) ) : $z;
                        $d['name'] = trim( strip_tags( $m[1][3] ) );
                        $d['locations'] = trim( str_replace( '  ', ' ', str_replace( '&#160;', ' ', strip_tags( $m[1][4] ) ) ) );
                        scraperwiki::save( array( 'code' ), $d );
                    }
                }
            }
        }
    }
?>