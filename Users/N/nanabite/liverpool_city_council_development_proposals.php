<?php 

date_default_timezone_set('Australia/Sydney');
require 'scraperwiki/simple_html_dom.php';

$mainUrl = scraperWiki::scrape("http://www.liverpool.nsw.gov.au/developmentapplications.htm");

$dom = new simple_html_dom();
$dom->load($mainUrl);
//$container = $dom->find("table td.bodyCopy", 0);

$start = false;
foreach($dom->find("p p") as $paragraph)
{
    if(strstr($paragraph->innertext, "DEVELOPMENT PROPOSALS") > -1)
    {
        $start = true;
    }

    if(stristr($paragraph->innertext, "The following applications are on public exhibition from") > -1
        || stristr($paragraph->innertext, "The following application is on public exhibition from") > -1)
    {
        $dateString = html_entity_decode($paragraph->innertext);
        print($dateString . "\n");
        preg_match('/exhibition from( *)<STRONG>(.+)to(.+)<BR><\/STRONG>/im', $dateString, $dateArray);
        print_r($dateArray);
        $date = date('Y-m-d', strtotime(trim($dateArray[3])));
        print($date . "\n");
    }

    if($start)
    {
        $record = array();
        $record['on_notice_to'] = $date;
        $record['council_reference'] = '';
        $record['description'] = '';
    }
}

?><?php 

date_default_timezone_set('Australia/Sydney');
require 'scraperwiki/simple_html_dom.php';

$mainUrl = scraperWiki::scrape("http://www.liverpool.nsw.gov.au/developmentapplications.htm");

$dom = new simple_html_dom();
$dom->load($mainUrl);
//$container = $dom->find("table td.bodyCopy", 0);

$start = false;
foreach($dom->find("p p") as $paragraph)
{
    if(strstr($paragraph->innertext, "DEVELOPMENT PROPOSALS") > -1)
    {
        $start = true;
    }

    if(stristr($paragraph->innertext, "The following applications are on public exhibition from") > -1
        || stristr($paragraph->innertext, "The following application is on public exhibition from") > -1)
    {
        $dateString = html_entity_decode($paragraph->innertext);
        print($dateString . "\n");
        preg_match('/exhibition from( *)<STRONG>(.+)to(.+)<BR><\/STRONG>/im', $dateString, $dateArray);
        print_r($dateArray);
        $date = date('Y-m-d', strtotime(trim($dateArray[3])));
        print($date . "\n");
    }

    if($start)
    {
        $record = array();
        $record['on_notice_to'] = $date;
        $record['council_reference'] = '';
        $record['description'] = '';
    }
}

?>