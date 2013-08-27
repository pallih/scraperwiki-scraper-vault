<?php
# Blank PHP
$sourcescraper = 'fys_api_1';

 # scraperwiki::attach('irish-epa-licenses', 'lic');
 #   $licenses = scraperwiki::select("* from lic.swdata");
//    $licenses = scraperwiki::getData('irish-epa-licenses');


$s = scraperwiki::attach($sourcescraper, $limit=250);
header('Content-type: application/json');
print "{ \"items\": ".json_encode($s) ."}";


?>
<?php
# Blank PHP
$sourcescraper = 'fys_api_1';

 # scraperwiki::attach('irish-epa-licenses', 'lic');
 #   $licenses = scraperwiki::select("* from lic.swdata");
//    $licenses = scraperwiki::getData('irish-epa-licenses');


$s = scraperwiki::attach($sourcescraper, $limit=250);
header('Content-type: application/json');
print "{ \"items\": ".json_encode($s) ."}";


?>
<?php
# Blank PHP
$sourcescraper = 'fys_api_1';

 # scraperwiki::attach('irish-epa-licenses', 'lic');
 #   $licenses = scraperwiki::select("* from lic.swdata");
//    $licenses = scraperwiki::getData('irish-epa-licenses');


$s = scraperwiki::attach($sourcescraper, $limit=250);
header('Content-type: application/json');
print "{ \"items\": ".json_encode($s) ."}";


?>
