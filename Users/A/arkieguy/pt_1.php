<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.pulaskitech.edu/_printable.asp?page=%2Fadministration%2Fcalendar_of_events%2Easp&qs=");
$html = str_get_html($html_content);

$key = 1;

//  Read each paragraph from the HTML
foreach ( $html->find("p") as $par )  {

    //  Split the paragraph into lines on BR
    $lines = preg_split(  '~<BR>|</*P>~i', $par, -1, PREG_SPLIT_NO_EMPTY );

    foreach( $lines as $line ) {
        if( ! preg_match( '~^(\S+\s+\d+).*[^[:print:]]\s*(.*)$~i', $line, $fields )  )
            continue;

        $record = array();
        $record['guid'] = $key;

        $fields[1] .= date( ' Y' );

        $start = $fields[1];
        $end = '';
        if( preg_match(  '~,\s*([0-9:]+)\s*([ap].m.)*\s*-*\s*([0-9:]+)*\s*([ap].m.)*~', $fields[2], $match ) ) {
            $start .= ', ' . $match[1];
            if( ! empty( $match[2] ) )
                    $start .= $match[2];
            else
                    $start .= $match[4];

            if( ! empty( $match[3] ) ) {
                $end = $fields[1] . ', '. $match[3] .  $match[4];
            }
        }

        $record['pubDate'] = strtotime( $start );
        $record['title'] = $start;
        if( ! empty( $end ) )
                $record['End'] = strtotime( $end );
        $record['description'] = $fields[2];
        $record['link'] = 'http://www.pulaskitech.edu/administration/calendar_of_events.asp';

        scraperwiki::save(array('guid'), $record);   

        $key ++;
    }
}    
?><?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.pulaskitech.edu/_printable.asp?page=%2Fadministration%2Fcalendar_of_events%2Easp&qs=");
$html = str_get_html($html_content);

$key = 1;

//  Read each paragraph from the HTML
foreach ( $html->find("p") as $par )  {

    //  Split the paragraph into lines on BR
    $lines = preg_split(  '~<BR>|</*P>~i', $par, -1, PREG_SPLIT_NO_EMPTY );

    foreach( $lines as $line ) {
        if( ! preg_match( '~^(\S+\s+\d+).*[^[:print:]]\s*(.*)$~i', $line, $fields )  )
            continue;

        $record = array();
        $record['guid'] = $key;

        $fields[1] .= date( ' Y' );

        $start = $fields[1];
        $end = '';
        if( preg_match(  '~,\s*([0-9:]+)\s*([ap].m.)*\s*-*\s*([0-9:]+)*\s*([ap].m.)*~', $fields[2], $match ) ) {
            $start .= ', ' . $match[1];
            if( ! empty( $match[2] ) )
                    $start .= $match[2];
            else
                    $start .= $match[4];

            if( ! empty( $match[3] ) ) {
                $end = $fields[1] . ', '. $match[3] .  $match[4];
            }
        }

        $record['pubDate'] = strtotime( $start );
        $record['title'] = $start;
        if( ! empty( $end ) )
                $record['End'] = strtotime( $end );
        $record['description'] = $fields[2];
        $record['link'] = 'http://www.pulaskitech.edu/administration/calendar_of_events.asp';

        scraperwiki::save(array('guid'), $record);   

        $key ++;
    }
}    
?>