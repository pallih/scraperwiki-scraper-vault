<?php
# Blank PHP
$sourcescraper = 'common_names';
scraperwiki::attach($sourcescraper);

$data = scraperwiki::select( "* from common_names.boy_names limit 3" );

print_r($data);
?>
<?php
# Blank PHP
$sourcescraper = 'common_names';
scraperwiki::attach($sourcescraper);

$data = scraperwiki::select( "* from common_names.boy_names limit 3" );

print_r($data);
?>
