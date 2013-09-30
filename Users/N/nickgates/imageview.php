<?php

$sourcescraper = 'testscraper_12';

scraperwiki::attach($sourcescraper); 

$data = scraperwiki::select( "* from testscraper_12.swdata order by reputation desc" );
print_r($data);


?>
<?php

$sourcescraper = 'testscraper_12';

scraperwiki::attach($sourcescraper); 

$data = scraperwiki::select( "* from testscraper_12.swdata order by reputation desc" );
print_r($data);


?>
