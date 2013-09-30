<?php
$remote = fopen("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=royalsocietyfellows1660-2007&query=select%20*%20from%20%60RoyalSocietyFellows%60%20where%20StartPresident%20not%20null%20order%20by%20StartPresident%20desc", "r");
fpassthru($remote);
?>
<?php
$remote = fopen("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=royalsocietyfellows1660-2007&query=select%20*%20from%20%60RoyalSocietyFellows%60%20where%20StartPresident%20not%20null%20order%20by%20StartPresident%20desc", "r");
fpassthru($remote);
?>
