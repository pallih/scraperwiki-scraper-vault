<?php
# Blank PHP
$sourcescraper = 'nwis_schedule_2';
scraperwiki::attach($sourcescraper);
$data = scraperwiki::select(
    "* from nwis_schedule_2.swdata
    where team1 = 'NWIS HO HEIN'
    or team2 = 'NWIS HO HEIGN' 
    order by timestamp desc limit 10"
);
#print_r($data);


?>
<table>
<?php
foreach($data as $d){
?>
<tr>
<td><?= date(DATE_RFC822, $d['timestamp']) ?></td>
</tr>
<?php
}
?>
</table>

<br /><br />
<pre>
<?php
#print_r( geoip_db_get_all_info() );
#echo geoip_database_info(GEOIP_COUNTRY_EDITION);
#print_r($_SERVER);
#echo geoip_country_code3_by_name($_SERVER['REMOTE_ADDR']);
$ip; 
if (getenv("HTTP_CLIENT_IP")) 
$ip = getenv("HTTP_CLIENT_IP"); 
else if(getenv("HTTP_X_FORWARDED_FOR")) 
$ip = getenv("HTTP_X_FORWARDED_FOR"); 
else if(getenv("REMOTE_ADDR")) 
$ip = getenv("REMOTE_ADDR"); 
else 
$ip = "UNKNOWN";
print $ip; 
?>
</pre>