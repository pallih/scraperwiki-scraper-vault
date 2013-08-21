<?php

// Basic settings + needles
$paramString = '';
$haystack = 'http://search.twitter.com/search.json?';
$needles = array(
    'topic' => array( 'intouchables' , 'hungergames' ),
);
$mood = array( ':)' , ':(' );

/*  Ze logic separator.
    Theoretically could be almost anything in the
    Search Operators found https://dev.twitter.com/docs/using-search */
$logic = ' AND ';

// Join the needles
foreach ( $needles as $key => $needle ) {

    if ( is_array( $needle ) ) $needles[ $key ] = implode( ' OR ' , $needle );

}

// Basic parameters
$params = array(
  'q'           => implode( $logic , $needles ),
  'result_type' => 'recent',
  'rpp'         => 100,
);

// Language
$languages = array( 'nl' , 'en' , 'de' );

// ASSEMBLE!
$queries = array();
$i = 0;
if ( is_array( $languages ) ) {
    
    foreach ( $languages as $lang ) {

        $q  = 'lang=' . $lang;
        $q .= '&result_type=' . $params[ 'result_type' ];
        $q .= '&rpp=' . $params[ 'rpp' ] . '&';

        if ( is_array( $mood ) ) {
            
            foreach ( $mood as $moo ) {
                
                $q .= 'q=' . urlencode( $params[ 'q' ] . $logic . $moo );
                
                $queries[ $i ][ 'lang' ] = $lang;
                $queries[ $i ][ 'mood' ] = $moo;
                $queries[ $i ][ 'q' ]    = $q;
                
                $i++;
            }
        
        }
        else {

            $q .= 'q=' . urlencode( $params[ 'q' ] );

            $queries[ $i ][ 'lang' ] = $lang;
            $queries[ $i ][ 'mood' ] = '';
            $queries[ $i ][ 'q' ]    = $q;
        
            $i++;
        
        }
    
    }

}
else {

    $q = 'lang=' . $languages;

    foreach ( $params as $param => $value ) {
        
        $q .= '&' . $param . '=' . urlencode( $value );
        
    }
    
    $queries[ $i ][ 'lang' ] = $languages;
    $queries[ $i ][ 'mood' ] = '';
    $queries[ $i ][ 'q' ]    = $q;

}

foreach ( $queries as $lang => $query ) {

    // loop multiple pages
    for ( $page = 1 ; $page <= 15 ; $page ++ ) {
  
      // The scraper call
      print 'Sending API request to: ' . $haystack . $query[ 'q' ] . '&page=' . $page . "\n";
      $twitterData = scraperwiki::scrape( $haystack . $query[ 'q' ] . '&page=' . $page );
      $twitterData = json_decode( $twitterData ); // Decodin'

      //print_r( $twitterData );
  
      // Traverse tweets
    foreach ( $twitterData->results as $tweet ) {
    
        scraperwiki::save_sqlite( array( 'id' ) , array(
          'mood'        => $query[ 'mood' ],
          'lang'        => $query[ 'lang' ],
          'text'        => utf8_encode( $tweet->text ),
          'to_user_id'  => $tweet->to_user_id,
          'from_user_id'=> $tweet->from_user_id,
          'from_user'   => $tweet->from_user,
          'created_at'  => $tweet->created_at,
          'id'          => $tweet->id,
        ) );
    
      }

      sleep( 2 );

    }

}

?>
