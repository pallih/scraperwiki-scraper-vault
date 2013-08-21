<?php

require 'scraperwiki/simple_html_dom.php'; 
    
// Get a list of all sites on mediaqueri.es and save it to the datastore. (All sites is not automated you how to update the for statement to the amount of pages on mediaqueri.es)
for ($i=1; $i<=41; $i++)
{
    $mediaPage = "http://mediaqueri.es/" . $i . "/" . "\n";
    
    $html_content = scraperwiki::scrape($mediaPage);
    $html = str_get_html($html_content);

    $urls = array();

    // Get all the desired links on the page
    foreach ($html->find("article.site div.shots a") as $link) {    
        $urls[] = $link->getAttribute("href");
    }
    
    // Delete dublicates
    $result = array_unique($urls);

    // Save the data
    foreach ($result as $url) {
        // get host name from URL
        $pattern = '@^(?:http://)?([^/]+)@i';
        preg_match($pattern, $url, $matches);
        $host = $matches[1];
        //print "$matches[1] \n";
    
        // get last two segments of host name
        $pattern = '/[^.]+\.[^.]+$/';
        preg_match($pattern, $host, $matches);
        $sitename = $matches[0];
        //print "$matches[0] \n";
    
        if ($sitename == "co.uk" || $sitename == "ac.uk" || $sitename == "asu.edu" || $sitename == "com.au" || $sitename == "org.uk") {
            
            if (substr($host, 0, 4) == 'www.') {
                $sitename = substr($host, 4);
            }
            elseif (substr($host, 0, 3) == 'www') {
                $sitename = substr($host, 3);
            }
            else {
                $sitename = $host;
            }
        }
        
        // The actual saving
        $site = array('a_name' => $sitename, 'a_url' => $url, 'a_pagenumber' => $i);
        scraperwiki::save_sqlite(array("a_name"),$site);
    }
}

?>
