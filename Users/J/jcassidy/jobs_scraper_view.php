<?php
# Jobs Scraper View
$sourcescraper = 'jobs_scraper';
scraperwiki::attach($sourcescraper);

$job= scraperwiki::select(
    "* from jobs_scraper.swdata 
    order by title desc"
);
foreach($job as $j){ 
    print "<h3 class='hpcuExpand'>" . "\n";
    print "<a href='http://www.indeed.com" . $j['href'] . "'>" . $j['title'] . "</a>" . "\n";
    print "</h3>" . "\n";
    print "<ul>" . "\n";
    print "<b>Institution:</b> " . $j['institution'] . "<br/>" . "\n";
    print $j['summary'] . "<br/><br/>" . "\n";
    print "</ul>" . "\n";
    print "<hr /><br/>" . "\n";
}

?>
