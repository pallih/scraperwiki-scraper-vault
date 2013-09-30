<?php

$ss1 = 'cz_public_organizations_ufis_ids'; //source scraper 1
$ss2 = 'cz_public_organizations_ufis_retrieval'; //source scraper 2
scraperwiki::attach($ss1); 
scraperwiki::attach($ss2); 

//select all central organizations (and funds)
$ids =  scraperwiki::select( "distinct * from $ss1.organization where chapter>0" );
$id_arr = "";
$i = 0;
$c = count($ids);
for( $i = 0; $i < $c; $i++){
    $id_arr = $id_arr . $ids[$i]['id'];
    if ( $i++ != $c ) 
        $id_arr = $id_arr . ",";
}
print $id_arr;
//$data = scraperwiki::sqliteexecute( "select * from $ss2.swdata where report_id='50' and org_id in ({$id_arr})" );
//if (! empty($data))  
//    $out .= array_to_csv($data);
//  else $out .= $row['id'];


// Requires PHP 5.1.0 at least; I won't do the check pragmatically though.
// http://refactormycode.com/codes/1120-array-to-csv  Chris
function array_to_csv ($data, $delim = ',', $enclosure = '"')
{
    if (empty($data) && !is_array($data)) {
        return false;
    }

    $sock = fopen('php://memory', 'w+');
    
    if ($sock === false) {
        return false;
    }

    // length written
    $length = 0;

    foreach ($data as $row) {
        $tmp = fputcsv($sock, $row, $delim, $enclosure);
        
        if ($tmp === false) {
            return false;
        }
        
        $length += $tmp;
    }

    fseek($sock, 0);

    $csv = fread($sock, $length);
    fclose($sock);

    return $csv;
}
?>
<?php

$ss1 = 'cz_public_organizations_ufis_ids'; //source scraper 1
$ss2 = 'cz_public_organizations_ufis_retrieval'; //source scraper 2
scraperwiki::attach($ss1); 
scraperwiki::attach($ss2); 

//select all central organizations (and funds)
$ids =  scraperwiki::select( "distinct * from $ss1.organization where chapter>0" );
$id_arr = "";
$i = 0;
$c = count($ids);
for( $i = 0; $i < $c; $i++){
    $id_arr = $id_arr . $ids[$i]['id'];
    if ( $i++ != $c ) 
        $id_arr = $id_arr . ",";
}
print $id_arr;
//$data = scraperwiki::sqliteexecute( "select * from $ss2.swdata where report_id='50' and org_id in ({$id_arr})" );
//if (! empty($data))  
//    $out .= array_to_csv($data);
//  else $out .= $row['id'];


// Requires PHP 5.1.0 at least; I won't do the check pragmatically though.
// http://refactormycode.com/codes/1120-array-to-csv  Chris
function array_to_csv ($data, $delim = ',', $enclosure = '"')
{
    if (empty($data) && !is_array($data)) {
        return false;
    }

    $sock = fopen('php://memory', 'w+');
    
    if ($sock === false) {
        return false;
    }

    // length written
    $length = 0;

    foreach ($data as $row) {
        $tmp = fputcsv($sock, $row, $delim, $enclosure);
        
        if ($tmp === false) {
            return false;
        }
        
        $length += $tmp;
    }

    fseek($sock, 0);

    $csv = fread($sock, $length);
    fclose($sock);

    return $csv;
}
?>
<?php

$ss1 = 'cz_public_organizations_ufis_ids'; //source scraper 1
$ss2 = 'cz_public_organizations_ufis_retrieval'; //source scraper 2
scraperwiki::attach($ss1); 
scraperwiki::attach($ss2); 

//select all central organizations (and funds)
$ids =  scraperwiki::select( "distinct * from $ss1.organization where chapter>0" );
$id_arr = "";
$i = 0;
$c = count($ids);
for( $i = 0; $i < $c; $i++){
    $id_arr = $id_arr . $ids[$i]['id'];
    if ( $i++ != $c ) 
        $id_arr = $id_arr . ",";
}
print $id_arr;
//$data = scraperwiki::sqliteexecute( "select * from $ss2.swdata where report_id='50' and org_id in ({$id_arr})" );
//if (! empty($data))  
//    $out .= array_to_csv($data);
//  else $out .= $row['id'];


// Requires PHP 5.1.0 at least; I won't do the check pragmatically though.
// http://refactormycode.com/codes/1120-array-to-csv  Chris
function array_to_csv ($data, $delim = ',', $enclosure = '"')
{
    if (empty($data) && !is_array($data)) {
        return false;
    }

    $sock = fopen('php://memory', 'w+');
    
    if ($sock === false) {
        return false;
    }

    // length written
    $length = 0;

    foreach ($data as $row) {
        $tmp = fputcsv($sock, $row, $delim, $enclosure);
        
        if ($tmp === false) {
            return false;
        }
        
        $length += $tmp;
    }

    fseek($sock, 0);

    $csv = fread($sock, $length);
    fclose($sock);

    return $csv;
}
?>
<?php

$ss1 = 'cz_public_organizations_ufis_ids'; //source scraper 1
$ss2 = 'cz_public_organizations_ufis_retrieval'; //source scraper 2
scraperwiki::attach($ss1); 
scraperwiki::attach($ss2); 

//select all central organizations (and funds)
$ids =  scraperwiki::select( "distinct * from $ss1.organization where chapter>0" );
$id_arr = "";
$i = 0;
$c = count($ids);
for( $i = 0; $i < $c; $i++){
    $id_arr = $id_arr . $ids[$i]['id'];
    if ( $i++ != $c ) 
        $id_arr = $id_arr . ",";
}
print $id_arr;
//$data = scraperwiki::sqliteexecute( "select * from $ss2.swdata where report_id='50' and org_id in ({$id_arr})" );
//if (! empty($data))  
//    $out .= array_to_csv($data);
//  else $out .= $row['id'];


// Requires PHP 5.1.0 at least; I won't do the check pragmatically though.
// http://refactormycode.com/codes/1120-array-to-csv  Chris
function array_to_csv ($data, $delim = ',', $enclosure = '"')
{
    if (empty($data) && !is_array($data)) {
        return false;
    }

    $sock = fopen('php://memory', 'w+');
    
    if ($sock === false) {
        return false;
    }

    // length written
    $length = 0;

    foreach ($data as $row) {
        $tmp = fputcsv($sock, $row, $delim, $enclosure);
        
        if ($tmp === false) {
            return false;
        }
        
        $length += $tmp;
    }

    fseek($sock, 0);

    $csv = fread($sock, $length);
    fclose($sock);

    return $csv;
}
?>
