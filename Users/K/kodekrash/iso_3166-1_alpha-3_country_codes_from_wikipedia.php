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

    $URL = 'http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3';
    $x = scraperWiki::scrape( $URL );
    if( !empty( $x ) ) {
        $x = partof( $x, 'Officially assigned code elements</span></h3>', '<h3>' );
        $x = partof( $x, '<table', null, true );
        $x = explode( '</table>', $x );
        if( count( $x ) > 0 ) {
            foreach( $x as $y ) {
                $y = explode( '</tr>', $y );
                if( count( $y ) > 0 ) {
                    foreach( $y as $z ) {
                        if( preg_match_all( '/<td(.*?)>(.*?)<\/td>/iu', $z, $m ) ) {
                            if( count( $m[2] ) == 2 ) {
                                $d = array( 'code' => trim( strip_tags( $m[2][0] ) ), 'label' => trim( strip_tags( $m[2][1] ) ) );
                                scraperwiki::save( array( 'code' ), $d );
                            }
                        }
                    }
                }
            }
        }
    }
?>
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

    $URL = 'http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3';
    $x = scraperWiki::scrape( $URL );
    if( !empty( $x ) ) {
        $x = partof( $x, 'Officially assigned code elements</span></h3>', '<h3>' );
        $x = partof( $x, '<table', null, true );
        $x = explode( '</table>', $x );
        if( count( $x ) > 0 ) {
            foreach( $x as $y ) {
                $y = explode( '</tr>', $y );
                if( count( $y ) > 0 ) {
                    foreach( $y as $z ) {
                        if( preg_match_all( '/<td(.*?)>(.*?)<\/td>/iu', $z, $m ) ) {
                            if( count( $m[2] ) == 2 ) {
                                $d = array( 'code' => trim( strip_tags( $m[2][0] ) ), 'label' => trim( strip_tags( $m[2][1] ) ) );
                                scraperwiki::save( array( 'code' ), $d );
                            }
                        }
                    }
                }
            }
        }
    }
?>
