<?php
# Blank PHP
//$sourcescraper = 'irish_president_engagementstest';

//$s = scraperwiki::scrape($sourcescraper, $limit=250);
// = scraperwiki::attach($sourcescraper, $limit=250);
scraperwiki::attach('openlearn_xml_processor'); 

$data = scraperwiki::select("* from glossary");


scraperWiki::httpresponseheader('Content-Type', 'application/json');
print "{ \"items\": ".json_encode($data) ."}";

?> <?php
# Blank PHP
//$sourcescraper = 'irish_president_engagementstest';

//$s = scraperwiki::scrape($sourcescraper, $limit=250);
// = scraperwiki::attach($sourcescraper, $limit=250);
scraperwiki::attach('openlearn_xml_processor'); 

$data = scraperwiki::select("* from glossary");


scraperWiki::httpresponseheader('Content-Type', 'application/json');
print "{ \"items\": ".json_encode($data) ."}";

?> 