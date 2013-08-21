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

        $author = substr(trim($item->find("h3", 0)->plaintext),3);
        print $author . "\n";

        $link = $item->find("a", 0);
        print "http://pitchfork.com" . $link->href . "\n";
       
        $albumhtml = scraperwiki::scrape(sprintf('http://pitchfork.com%s', $link->href));
        $albumdom = new simple_html_dom();
        $albumdom->load($albumhtml);

        $score = trim($albumdom->find("#main div.info span.score",0)->plaintext);
         print $score . "\n";

        $label = preg_split('/;/',trim($albumdom->find("#main div.info h3",0)->plaintext));
         print $label[0] . "\n";

        $text = trim($albumdom->find("#main div.editorial",0)->plaintext);
         print $text . "\n";

        $data = array('artist' => $artist, 'title' => $title, 'author' => $author, 'date' => $date, 'uid' => $link->href, 'url' => "http://pitchfork.com" . $link->href, 'year' => $year, 'score' => $score,  'label' => $label[0], 'text' => $text);
            scraperwiki::save(array('artist','title','author','date','uid','url','year','score'), $data);
    }

    /**$morelinks = $dom->find("#main div.pagination a.next");
    $next = null;       
    foreach ($morelinks as $morelink){
        if (strstr($morelink->plaintext, 'Next')){
            $next = $morelink->href;
            break;
        }
    }
    
    if (!$next)
       break;

    preg_match('!/reviews/albums/(\d+)/!i', $next, $matches);
    if (empty($matches))
      break;**/

    $page = $page + 1;

    $dom->clear(); 
    unset($dom);
} while ($page);
