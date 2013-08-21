<?php
require 'scraperwiki/simple_html_dom.php';

$page = 1;

do {
    print $page . "\n";

    $html = scraperwiki::scrape(sprintf('http://www.outdoorsmagic.com/reviews/', $page));
    $dom = new simple_html_dom();
    $dom->load($html);

    $items = $dom->find("#content .center .album-review-list");
    if (empty($items))
      break;

    foreach ($items as $item){
        $date = trim($item->find("p strong", 0)->plaintext);
         print $date . "\n";

        preg_match('/(\d+)$/', $date, $matches);
        $year = $matches[1];
  
        foreach ($item->find("ul li") as $album){
            $link = $album->find("a", 0);
            preg_match('!<strong>(.+?)</strong>: (.+)!i', trim($link->innertext), $matches);
            if (count($matches) !== 3)
              continue;

            list(, $artist, $title) = $matches;
            $data = array('artist' => $artist, 'title' => $title, 'date' => $date, 'url' => $link->href, 'year' => $year);
            scraperwiki::save(array('artist', 'title'), $data);
        }
    }

    $morelinks = $dom->find("#content .center a.more-link");
    $next = null;       
    foreach ($morelinks as $morelink){
        if (strstr($morelink->plaintext, 'Next Page')){
            $next = $morelink->href;
            break;
        }
    }
    
    if (!$next)
       break;

    preg_match('!/reviews/albums/(\d+)/!i', $next, $matches);
    if (empty($matches))
      break;

    $page = $matches[1];

    $dom->clear(); 
    unset($dom);
} while ($page);
