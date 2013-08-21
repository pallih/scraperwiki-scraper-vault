<?php
require  'scraperwiki/simple_html_dom.php';

for($page = 1; $page < 24; $page++)
{
    print "*** Scraping page " . $page . "\n\n";

    $html = scraperwiki::scrape('http://dribbble.com/search/users?q=\"india\"&page=' . $page);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find('<a[rel=contact]') as $data)
    {
        $site = scraperwiki::scrape('http://dribbble.com' . $data->href);
    
        $locdom = new simple_html_dom();
        $locdom->load($site);
    
        foreach($locdom->find('<span[class=locality]') as $loc) {
            print $data->plaintext . '; ' . 'http://dribbble.com' . $data->href . '; ' . $loc->plaintext . "\n";
            scraperwiki::save(array('http'), array('http' => 'http://dribbble.com' . $data->href, 'name' => $data->plaintext, 'location' => $loc->plaintext, 'page' => $page . ""));
        }

        unset($site);

        $locdom->clear();
        unset($locdom);
    }

    unset($html);

    $dom->clear();
    unset($dom);
}

?>