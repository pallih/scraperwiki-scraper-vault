<?php
require  'scraperwiki/simple_html_dom.php';

// v5 - trying to calculate ALL likes

$chel=0;
for($page = 1; $page < 4; $page++)
{
    print "*** Scraping all-stars page " . $page . "\n\n";

    $html = scraperwiki::scrape('http://dribbble.com/members/all-stars?page=' . $page);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find('<a[rel=contact]') as $data)
    {
$chel++;
$place++;
if($chel < 42) {continue;};
$lastpage = $dom->find('li[class=stat-shots] a[href=' . $data->href . ']', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $lastpage, $matches)){
$lastpage=$matches[1] . $matches[2];
$lastpage=ceil($lastpage/15);
//$lastpage = sprintf("%d", $lastpage/15+1);
} else { $lastpage="-1"; }
//print 'Last portfolio page is ' . $lastpage . "\n";
$likes_all=0;
$views_all=0;
$comments_all=0;

for($portfoliopage = 1; $portfoliopage <= $lastpage; $portfoliopage++){
print "*** Scraping stats from " . $data->plaintext . "'s portfolio page #" . $portfoliopage . " (from " . $lastpage . ")\n\n";
//usleep(200000);}
        $site = scraperwiki::scrape('http://dribbble.com' . $data->href . "?page=" . $portfoliopage);
    
        $locdom = new simple_html_dom();
        $locdom->load($site);
foreach($locdom->find('li[class=fav] a') as $likes_shot_p){
$likes_shot = preg_replace('/,/',"", $likes_shot_p->plaintext);
$likes_all += $likes_shot;
}

foreach($locdom->find('li[class=views]') as $views_shot_p){
// $views_shot=$views_shot_p->plaintext;
// $views_shot = preg_replace('/(\d+)\(,){0,1}(\d+){0,1}/',"$1$3", $views_shot_p->plaintext);
$views_shot = preg_replace('/,/',"", $views_shot_p->plaintext);
 $views_all += $views_shot;
//print "Views all: " . $views_all . " Views: " . $views_shot_p->plaintext . "\n";
}

foreach($locdom->find('li[class^=cmnt] a') as $comments_shot_p){
$comments_shot = preg_replace('/,/',"", $comments_shot_p->plaintext);
$comments_all += $comments_shot;
//print "comments all: " . $comments_all . " comments: " . $comments_shot_p->plaintext . "\n";
}

}
//print "Views: " . $views_all . " Likes: " . $likes_all . " Comments: " . $comments_all . "\n";

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


        foreach($locdom->find('a[class=dribbble-over] em') as $firstshotdate){}

            print $place . ";" . $data->plaintext . '; ' . 'http://dribbble.com' . $data->href . '; ' . $loc->plaintext . ";" . $firstshotdate->plaintext . ";" . $followers . ";" . $following . ";" . $draftees . ";" . $shots . ";" . $projects . ";" . $likes . ";" . $tags . ";" . $buckets . $views_all . $likes_all . $comments_all . "\n";

            scraperwiki::save(array('http'), array('place' => $place, 'http' => 'http://dribbble.com' . $data->href, 'name' => $data->plaintext, 'location' => $loc->plaintext,  'first_shot' => $firstshotdate->plaintext, 'followers' => $followers, 'following' => $following, 'draftees' => $draftees, 'shots' => $shots , 'projects' => $projects , 'likes' => $likes, 'tags' => $tags, 'buckets' => $buckets, 'views_rcvd' => $views_all, 'likes_rcvd' => $likes_all, 'comments_rcvd' => $comments_all));
        

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

// v5 - trying to calculate ALL likes

$chel=0;
for($page = 1; $page < 4; $page++)
{
    print "*** Scraping all-stars page " . $page . "\n\n";

    $html = scraperwiki::scrape('http://dribbble.com/members/all-stars?page=' . $page);
    
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find('<a[rel=contact]') as $data)
    {
$chel++;
$place++;
if($chel < 42) {continue;};
$lastpage = $dom->find('li[class=stat-shots] a[href=' . $data->href . ']', 0)->plaintext;
if(preg_match('/(\d+),{0,1}(\d*).*/', $lastpage, $matches)){
$lastpage=$matches[1] . $matches[2];
$lastpage=ceil($lastpage/15);
//$lastpage = sprintf("%d", $lastpage/15+1);
} else { $lastpage="-1"; }
//print 'Last portfolio page is ' . $lastpage . "\n";
$likes_all=0;
$views_all=0;
$comments_all=0;

for($portfoliopage = 1; $portfoliopage <= $lastpage; $portfoliopage++){
print "*** Scraping stats from " . $data->plaintext . "'s portfolio page #" . $portfoliopage . " (from " . $lastpage . ")\n\n";
//usleep(200000);}
        $site = scraperwiki::scrape('http://dribbble.com' . $data->href . "?page=" . $portfoliopage);
    
        $locdom = new simple_html_dom();
        $locdom->load($site);
foreach($locdom->find('li[class=fav] a') as $likes_shot_p){
$likes_shot = preg_replace('/,/',"", $likes_shot_p->plaintext);
$likes_all += $likes_shot;
}

foreach($locdom->find('li[class=views]') as $views_shot_p){
// $views_shot=$views_shot_p->plaintext;
// $views_shot = preg_replace('/(\d+)\(,){0,1}(\d+){0,1}/',"$1$3", $views_shot_p->plaintext);
$views_shot = preg_replace('/,/',"", $views_shot_p->plaintext);
 $views_all += $views_shot;
//print "Views all: " . $views_all . " Views: " . $views_shot_p->plaintext . "\n";
}

foreach($locdom->find('li[class^=cmnt] a') as $comments_shot_p){
$comments_shot = preg_replace('/,/',"", $comments_shot_p->plaintext);
$comments_all += $comments_shot;
//print "comments all: " . $comments_all . " comments: " . $comments_shot_p->plaintext . "\n";
}

}
//print "Views: " . $views_all . " Likes: " . $likes_all . " Comments: " . $comments_all . "\n";

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


        foreach($locdom->find('a[class=dribbble-over] em') as $firstshotdate){}

            print $place . ";" . $data->plaintext . '; ' . 'http://dribbble.com' . $data->href . '; ' . $loc->plaintext . ";" . $firstshotdate->plaintext . ";" . $followers . ";" . $following . ";" . $draftees . ";" . $shots . ";" . $projects . ";" . $likes . ";" . $tags . ";" . $buckets . $views_all . $likes_all . $comments_all . "\n";

            scraperwiki::save(array('http'), array('place' => $place, 'http' => 'http://dribbble.com' . $data->href, 'name' => $data->plaintext, 'location' => $loc->plaintext,  'first_shot' => $firstshotdate->plaintext, 'followers' => $followers, 'following' => $following, 'draftees' => $draftees, 'shots' => $shots , 'projects' => $projects , 'likes' => $likes, 'tags' => $tags, 'buckets' => $buckets, 'views_rcvd' => $views_all, 'likes_rcvd' => $likes_all, 'comments_rcvd' => $comments_all));
        

        unset($site);

        $locdom->clear();
        unset($locdom);
    }

    unset($html);

    $dom->clear();
    unset($dom);
}

?>