<?php
require  'scraperwiki/simple_html_dom.php';

for($page = 1; $page < 5; $page++)
{
    print "*** Scraping page " . $page . "\n\n";

    $html = scraperwiki::scrape('http://dribbble.com/members/all-stars?page=' . $page);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find('<a[rel=contact]') as $data)
    {
        $site = scraperwiki::scrape('http://dribbble.com' . $data->href);
    
        $locdom = new simple_html_dom();
        $locdom->load($site);
    
        foreach($locdom->find('<span[class=locality]') as $loc){};
        foreach($locdom->find('<a[href$=followers]') as $followers){};
//$followers=trim($followers);
        foreach($locdom->find('<a[href$=following]') as $following){};
        foreach($locdom->find('<a[href$=draftees]') as $draftees){};
        foreach($locdom->find('ul[class=tabs] a[href=' . $data->href . ']') as $shots){};
        foreach($locdom->find('ul[class=tabs] a[href$=projects]') as $projects){};
        foreach($locdom->find('ul[class=tabs] a[href$=likes]') as $likes){};
        foreach($locdom->find('ul[class=tabs] a[href$=tags]') as $tags){};
        foreach($locdom->find('ul[class=tabs] a[href$=buckets]') as $buckets){};

            print $data->plaintext . '; ' . 'http://dribbble.com' . $data->href . '; ' . $loc->plaintext . ";" . trim($followers->plaintext) . ";" . trim($following->plaintext) . ";" . trim($draftees->plaintext) . ";" . trim($shots->plaintext) . ";" . trim($projects->plaintext) . ";" . trim($likes->plaintext) . ";" . trim($tags->plaintext) . ";" . trim($buckets->plaintext) . "\n";

            scraperwiki::save(array('http'), array('http' => 'http://dribbble.com' . $data->href, 'name' => $data->plaintext, 'location' => $loc->plaintext, 'page' => $page . "", 'followers' => trim($followers->plaintext), 'following' => trim($following->plaintext), 'draftees' => trim($draftees->plaintext), 'shots' => trim($shots->plaintext) , 'projects' => trim($projects->plaintext) , 'likes' => trim($likes->plaintext) , 'tags' => trim($tags->plaintext) , 'buckets' => trim($buckets->plaintext)));
        

        unset($site);

        $locdom->clear();
        unset($locdom);
    }

    unset($html);

    $dom->clear();
    unset($dom);
}

?><?php
require  'scraperwiki/simple_html_dom.php';

for($page = 1; $page < 5; $page++)
{
    print "*** Scraping page " . $page . "\n\n";

    $html = scraperwiki::scrape('http://dribbble.com/members/all-stars?page=' . $page);
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find('<a[rel=contact]') as $data)
    {
        $site = scraperwiki::scrape('http://dribbble.com' . $data->href);
    
        $locdom = new simple_html_dom();
        $locdom->load($site);
    
        foreach($locdom->find('<span[class=locality]') as $loc){};
        foreach($locdom->find('<a[href$=followers]') as $followers){};
//$followers=trim($followers);
        foreach($locdom->find('<a[href$=following]') as $following){};
        foreach($locdom->find('<a[href$=draftees]') as $draftees){};
        foreach($locdom->find('ul[class=tabs] a[href=' . $data->href . ']') as $shots){};
        foreach($locdom->find('ul[class=tabs] a[href$=projects]') as $projects){};
        foreach($locdom->find('ul[class=tabs] a[href$=likes]') as $likes){};
        foreach($locdom->find('ul[class=tabs] a[href$=tags]') as $tags){};
        foreach($locdom->find('ul[class=tabs] a[href$=buckets]') as $buckets){};

            print $data->plaintext . '; ' . 'http://dribbble.com' . $data->href . '; ' . $loc->plaintext . ";" . trim($followers->plaintext) . ";" . trim($following->plaintext) . ";" . trim($draftees->plaintext) . ";" . trim($shots->plaintext) . ";" . trim($projects->plaintext) . ";" . trim($likes->plaintext) . ";" . trim($tags->plaintext) . ";" . trim($buckets->plaintext) . "\n";

            scraperwiki::save(array('http'), array('http' => 'http://dribbble.com' . $data->href, 'name' => $data->plaintext, 'location' => $loc->plaintext, 'page' => $page . "", 'followers' => trim($followers->plaintext), 'following' => trim($following->plaintext), 'draftees' => trim($draftees->plaintext), 'shots' => trim($shots->plaintext) , 'projects' => trim($projects->plaintext) , 'likes' => trim($likes->plaintext) , 'tags' => trim($tags->plaintext) , 'buckets' => trim($buckets->plaintext)));
        

        unset($site);

        $locdom->clear();
        unset($locdom);
    }

    unset($html);

    $dom->clear();
    unset($dom);
}

?>