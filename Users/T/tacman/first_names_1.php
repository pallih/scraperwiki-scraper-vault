<?php
# Blank PHP
$sourcescraper = 'common_names';
scraperwiki::attach($sourcescraper);

$limit = empty($_GET['limit']) ? 10 : $_GET['limit'];
$data = scraperwiki::select( "* from common_names.boy_names order by rank limit $limit" ); 

print json_encode($data);
?>
<?php
# Blank PHP
$sourcescraper = 'common_names';
scraperwiki::attach($sourcescraper);

$limit = empty($_GET['limit']) ? 10 : $_GET['limit'];
$data = scraperwiki::select( "* from common_names.boy_names order by rank limit $limit" ); 

print json_encode($data);
?>
