<?php

$ss1 = 'cz_public_organizations_ufis_ids'; //source scraper 1
$ss2 = 'cz_public_organization_ufis_retrieval_central_50'; //source scraper 2
scraperwiki::attach($ss1); 
scraperwiki::attach($ss2); 

//select all central organizations (and funds)
$ids =  scraperwiki::select( "distinct id from $ss1.organization where chapter>0" );

//get rid of leading 0s in org_id (ICO)
foreach ($ids as $id) {
  $id_arr[] = ltrim($id['id'],'0');
}

$id_str = implode(",",$id_arr);
$out = '';
//we have to limit the query to about 20000, because otherwise we get errors
$c_ar = scraperwiki::sqliteexecute( "select count(*) as c from $ss2.swdata where report_id='50' and org_id in ({$id_str})");
$count = $c_ar->data[0][0];
for ($i = 0; (20000*$i)<= $count; $i++) {
  $offset = 20000 * $i;
  $data = scraperwiki::sqliteexecute( "select org_id,year,paragraph_id,entry_id,column_code,report_id,_value from $ss2.swdata where report_id='50' and org_id in ({$id_str}) order by org_id, year, paragraph_id, entry_id, column_code limit 20000 offset {$offset}" );

  $keys = array($data->keys);
  if ($i == 0) {
    $out = array_to_csv($keys);
    $out .= array_to_csv($data->data);
  } else 
    $out = array_to_csv($data->data);
  
print str_replace("\n","<br/>\n",$out);

}


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
