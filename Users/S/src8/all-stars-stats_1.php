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
    
        $loc = $locdom->find('<span[class=locality]', 0);
        $followers = $locdom->find('<a[href$=followers]', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $followers, $matches)){
$followers=$matches[1] . $matches[2];
} else { $followers="-1"; }
        $following = $locdom->find('<a[href$=following]', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $following, $matches)){
$following=$matches[1] . $matches[2];
} else { $following = "-1"; }
        $draftees = $locdom->find('<a[href$=draftees]', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $draftees, $matches)){
$draftees=$matches[1] . $matches[2];
} else { $draftees = "-1"; }
        $shots = $locdom->find('ul[class=tabs] a[href=' . $data->href . '] span[class=meta]', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $shots, $matches)){
$shots=$matches[1] . $matches[2];
} else { $shots = "-1"; }
        $projects = $locdom->find('ul[class=tabs] a[href$=projects] span[class=meta]', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $projects, $matches)){
$projects=$matches[1] . $matches[2];
} else { $projects = "-1"; }
        $likes = $locdom->find('ul[class=tabs] a[href$=likes] span[class=meta]', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $likes, $matches)){
$likes=$matches[1] . $matches[2];
} else { $likes = "-1"; }
        $tags = trim($locdom->find('ul[class=tabs] a[href$=tags] span[class=meta]', 0)->plaintext);
if(preg_match('/(\d+),{0,1}(\d*).*/', $tags, $matches)){
$tags=$matches[1] . $matches[2];
} else { $tags = "-1"; }
        $buckets = $locdom->find('ul[class=tabs] a[href$=buckets] span[class=meta]', 0)->plaintext;

if(preg_match('/(\d+),{0,1}(\d*).*/', $buckets, $matches)){ 
 $buckets=$matches[1] . $matches[2];
} else { $buckets = "-1"; }

            print $data->plaintext . '; ' . 'http://dribbble.com' . $data->href . '; ' . $loc->plaintext . ";" . $followers . ";" . $following . ";" . $draftees . ";" . $shots . ";" . $projects . ";" . $likes . ";" . $tags . ";" . $buckets . "\n";

            scraperwiki::save(array('http'), array('http' => 'http://dribbble.com' . $data->href, 'name' => $data->plaintext, 'location' => $loc->plaintext, 'page' => $page . "", 'followers' => $followers, 'following' => $following, 'draftees' => $draftees, 'shots' => $shots , 'projects' => $projects , 'likes' => $likes, 'tags' => $tags, 'buckets' => $buckets));
        

        unset($site);

        $locdom->clear();
        unset($locdom);
    }

    unset($html);

    $dom->clear();
    unset($dom);
}

?>