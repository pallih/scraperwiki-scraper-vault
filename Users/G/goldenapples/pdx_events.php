<?php

require 'scraperwiki/simple_html_dom.php';

$src = scraperwiki::scrape('http://stagbeetlepower.blogspot.com/search/label/events');

$html = new simple_html_dom();
$html->load($src);

$posts = $html->find('div.post');

foreach ( $posts as $post ) {

    // $title = $post->find('h3.entry_title')->plaintext; //...
    // Check if its actually a monthly calendar...

    $events = $post->find('div.MsoNormal');

    foreach ( $events as $event ) {

        $event_name = $event->find('b', 0);

        if ( $event_name ) {

            $tokens = array( 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' );

            $first_date = array_filter( array_map( 'date_pos', $tokens ));
            sort( $first_date, SORT_NUMERIC );

            $d = explode( ',', substr( $event->plaintext, array_shift( $first_date ) ), 3 );

            $event_date = strtotime( $d[0] . ',' . $d[1] );

            $e = array(
                'key' => md5( $event_name->plaintext . $date ),
                'name' => $event_name->plaintext,
                'date' => $event_date,
                'eventinfo' => $event->plaintext
            );
        
            if ( $event_date )
                scraperwiki::save_sqlite( array( 'key' ), $e );

        }
    }
    
}

           
function date_pos( $tok ) {
    global $event;
    return strpos( $event->plaintext, $tok );
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$src = scraperwiki::scrape('http://stagbeetlepower.blogspot.com/search/label/events');

$html = new simple_html_dom();
$html->load($src);

$posts = $html->find('div.post');

foreach ( $posts as $post ) {

    // $title = $post->find('h3.entry_title')->plaintext; //...
    // Check if its actually a monthly calendar...

    $events = $post->find('div.MsoNormal');

    foreach ( $events as $event ) {

        $event_name = $event->find('b', 0);

        if ( $event_name ) {

            $tokens = array( 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' );

            $first_date = array_filter( array_map( 'date_pos', $tokens ));
            sort( $first_date, SORT_NUMERIC );

            $d = explode( ',', substr( $event->plaintext, array_shift( $first_date ) ), 3 );

            $event_date = strtotime( $d[0] . ',' . $d[1] );

            $e = array(
                'key' => md5( $event_name->plaintext . $date ),
                'name' => $event_name->plaintext,
                'date' => $event_date,
                'eventinfo' => $event->plaintext
            );
        
            if ( $event_date )
                scraperwiki::save_sqlite( array( 'key' ), $e );

        }
    }
    
}

           
function date_pos( $tok ) {
    global $event;
    return strpos( $event->plaintext, $tok );
}

?>
