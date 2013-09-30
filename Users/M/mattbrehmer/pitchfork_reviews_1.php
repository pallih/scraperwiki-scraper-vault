<?php
require 'scraperwiki/simple_html_dom.php';

$page = 1;

do {
    print $page . "\n";

    $html = scraperwiki::scrape(sprintf('http://pitchfork.com/reviews/albums/%d/', $page));
    $dom = new simple_html_dom();
    $dom->load($html);

    $items = $dom->find("#main ul li ul li");
    if (empty($items))
      break;

    foreach ($items as $item){
        $date = trim($item->find("h4", 0)->plaintext);
         print $date . "\n";

        preg_match('/(\d+)$/', $date, $matches);
        $year = $matches[1];
        print $year . "\n";

        $artist = trim($item->find("h1", 0)->plaintext);
         print $artist . "\n";

        $title = trim($item->find("h2", 0)->plaintext);
         print $title . "\n";

        $link = $item->find("a", 0);
         print $link->href . "\n";

        $data = array('artist' => $artist, 'title' => $title, 'date' => $date, 'url' => $link->href, 'year' => $year);
            scraperwiki::save(array('artist', 'title'), $data);
    }

    $morelinks = $dom->find("#main div.pagination a.next");
    $next = null;       
    foreach ($morelinks as $morelink){
        if (strstr($morelink->plaintext, ' Next ')){
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
<?php
require 'scraperwiki/simple_html_dom.php';

$page = 1;

do {
    print $page . "\n";

    $html = scraperwiki::scrape(sprintf('http://pitchfork.com/reviews/albums/%d/', $page));
    $dom = new simple_html_dom();
    $dom->load($html);

    $items = $dom->find("#main ul li ul li");
    if (empty($items))
      break;

    foreach ($items as $item){
        $date = trim($item->find("h4", 0)->plaintext);
         print $date . "\n";

        preg_match('/(\d+)$/', $date, $matches);
        $year = $matches[1];
        print $year . "\n";

        $artist = trim($item->find("h1", 0)->plaintext);
         print $artist . "\n";

        $title = trim($item->find("h2", 0)->plaintext);
         print $title . "\n";

        $link = $item->find("a", 0);
         print $link->href . "\n";

        $data = array('artist' => $artist, 'title' => $title, 'date' => $date, 'url' => $link->href, 'year' => $year);
            scraperwiki::save(array('artist', 'title'), $data);
    }

    $morelinks = $dom->find("#main div.pagination a.next");
    $next = null;       
    foreach ($morelinks as $morelink){
        if (strstr($morelink->plaintext, ' Next ')){
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
