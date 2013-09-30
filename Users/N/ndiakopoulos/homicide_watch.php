<?php

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();
$url = "http://www.kickstarter.com/projects/1368665357/a-one-year-student-reporting-lab-within-homicide-w/backers?page=";
$pages = 22;
$locs = array();

for($j = 1;$j <= $pages; $j++)
{
    $html = scraperWiki::scrape($url . $j);
    $dom->load($html);

    $locations = $dom->find("p.location");
    //print $locations;
    foreach($locations as $location)
    {
        //print $location->plaintext;
        $locs[] = $location->plaintext;
        //print $locs[count($locs)-1];
    }

    for($i = 0;$i < count($locs);$i++)
    {
        $record = array(
            'locID' => $i,
            'location' => $locs[$i]
        );
        scraperwiki::save_sqlite(array('locID'), $record); 
    }
    

}

?>
<?php

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();
$url = "http://www.kickstarter.com/projects/1368665357/a-one-year-student-reporting-lab-within-homicide-w/backers?page=";
$pages = 22;
$locs = array();

for($j = 1;$j <= $pages; $j++)
{
    $html = scraperWiki::scrape($url . $j);
    $dom->load($html);

    $locations = $dom->find("p.location");
    //print $locations;
    foreach($locations as $location)
    {
        //print $location->plaintext;
        $locs[] = $location->plaintext;
        //print $locs[count($locs)-1];
    }

    for($i = 0;$i < count($locs);$i++)
    {
        $record = array(
            'locID' => $i,
            'location' => $locs[$i]
        );
        scraperwiki::save_sqlite(array('locID'), $record); 
    }
    

}

?>
