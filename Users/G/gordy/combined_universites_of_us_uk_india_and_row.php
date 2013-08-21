<?php
/**
 * Attach the 4 scrapers that are used to compile 
 * each list of academic institutions
 */
error_reporting(E_COMPILE_ERROR|E_ERROR|E_CORE_ERROR);
const WORLD = "universities_of_the_world";
const INDIA = "universities_of_india";
const USA = "universities_of_the_usa";
const UK = "universities_in_the_uk_from_ucas";
scraperwiki::attach( WORLD ); 
scraperwiki::attach( INDIA );
scraperwiki::attach( USA );
scraperwiki::attach( UK ); 

/**
 * Build a combhined list of these universities
 */
$sets = array();
$sets[ WORLD ]  = getRowCount( WORLD );
$sets[ INDIA ] = getRowCount( INDIA );
$sets[ USA ] = getRowCount( USA );
$sets[ UK ] = getRowCount( UK );

$limit = 100;
foreach( $sets as $set => $count ) 
{
    echo "Loading $set \n ";
    $offset = 0;
    while ( $offset < $count ) 
    {
        echo "Offset $offset / $count \n ";
        $where = "";
        if ( $set == WORLD )
        {
            $where = "WHERE country NOT IN ('United States','United Kingdom', 'India')";
        }
        saveData( $set, $where, $offset, $limit );
        $offset+= $limit;
    }
}


function saveData ( $set, $where, $offset, $limit )
{
    $rs = scraperwiki::select( "* FROM " . $set . ".swdata " . $where . " LIMIT ".$limit." OFFSET " . $offset  );
    foreach( $rs as $row ) 
    {
        $record = array();
        $record[ 'name' ] = $row[ 'name' ];
        $record[ 'link' ] = $row[ 'link' ];
        $record[ 'country' ] = $row[ 'country' ];
        if ( isset( $row[ 'state' ] ) )
        {
            $record[ 'state' ] = $row[ 'state' ];
        }
        scraperwiki::save( array ("name","link"), $record );
    }
}

function getRowCount( $set ) 
{
    $rs = scraperwiki::select( "COUNT(*) as c FROM " . $set . ".swdata"  );
    return $rs[0]['c'];
}
