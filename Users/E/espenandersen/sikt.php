<?php

    require "scraperwiki/simple_html_dom.php";

    $html = file_get_html( 'http://algeinfo.imr.no/index.php' );
    $titTag = $html->find( 'div.special' );
    $imgTag = $html->find( 'table img' );
    $img = imagecreatefromjpeg( 'http://algeinfo.imr.no/' . $imgTag[ 0 ]->src );

    preg_match( "/Dato: ([0-9]+)\.([0-9]+)\.([0-9]+)/", $titTag[ 0 ]->plaintext, $m );
    $date = sprintf( "%s-%s-%s", $m[3], $m[2], $m[1] );

    $areas = array(
        "indre_oslofjord"    => array( 103, 400, 135, 430 ),
        "ytre_oslofjord"     => array( 103, 420, 135, 444 ),
        "gulen"              => array(  17, 373,  41, 397 ),
        "trondheimsfjorden"  => array(  68, 279, 105, 312 ),
        "troms"              => array(  90,  62, 148, 116 ),
        "lofoten_vesterålen" => array(  57, 106, 117, 182 ) );
    
    $data = array( 'date' => $date );

    foreach( $areas as $name => $area ) {

        $good = 0;
        $bad = 0;

        for( $y = $area[ 1 ]; $y <= $area[ 3 ]; $y++ ) {
            for( $x = $area[ 0 ]; $x <= $area[ 2 ]; $x++ ) {
                $rgb = imagecolorat( $img, $x, $y );
                $r = ( $rgb >> 16 ) & 0xFF;
                $g = ( $rgb >>  8 ) & 0xFF;
                $b = ( $rgb       ) & 0xFF;
                if( $r > 250 && $g > 240 && $b > 240 ) {
                    $good++;
                }
                else if( $r > 150 && $r < 175 && $g > 50 && $g < 80 && $b > 70 && $b < 90 ) {
                    $bad++;
                }
            }
        }

        if( $good > 4 || $bad > 4 ) {
            $visibility = round( $good * ( 10 / ( $good + $bad + 1 ) ) );
        }
        else {
            $visibility = 'null';
        }
        $data[ $name ] = $visibility;

    }

    ScraperWiki::save( array( 'date' ), $data );

?>
<?php

    require "scraperwiki/simple_html_dom.php";

    $html = file_get_html( 'http://algeinfo.imr.no/index.php' );
    $titTag = $html->find( 'div.special' );
    $imgTag = $html->find( 'table img' );
    $img = imagecreatefromjpeg( 'http://algeinfo.imr.no/' . $imgTag[ 0 ]->src );

    preg_match( "/Dato: ([0-9]+)\.([0-9]+)\.([0-9]+)/", $titTag[ 0 ]->plaintext, $m );
    $date = sprintf( "%s-%s-%s", $m[3], $m[2], $m[1] );

    $areas = array(
        "indre_oslofjord"    => array( 103, 400, 135, 430 ),
        "ytre_oslofjord"     => array( 103, 420, 135, 444 ),
        "gulen"              => array(  17, 373,  41, 397 ),
        "trondheimsfjorden"  => array(  68, 279, 105, 312 ),
        "troms"              => array(  90,  62, 148, 116 ),
        "lofoten_vesterålen" => array(  57, 106, 117, 182 ) );
    
    $data = array( 'date' => $date );

    foreach( $areas as $name => $area ) {

        $good = 0;
        $bad = 0;

        for( $y = $area[ 1 ]; $y <= $area[ 3 ]; $y++ ) {
            for( $x = $area[ 0 ]; $x <= $area[ 2 ]; $x++ ) {
                $rgb = imagecolorat( $img, $x, $y );
                $r = ( $rgb >> 16 ) & 0xFF;
                $g = ( $rgb >>  8 ) & 0xFF;
                $b = ( $rgb       ) & 0xFF;
                if( $r > 250 && $g > 240 && $b > 240 ) {
                    $good++;
                }
                else if( $r > 150 && $r < 175 && $g > 50 && $g < 80 && $b > 70 && $b < 90 ) {
                    $bad++;
                }
            }
        }

        if( $good > 4 || $bad > 4 ) {
            $visibility = round( $good * ( 10 / ( $good + $bad + 1 ) ) );
        }
        else {
            $visibility = 'null';
        }
        $data[ $name ] = $visibility;

    }

    ScraperWiki::save( array( 'date' ), $data );

?>
