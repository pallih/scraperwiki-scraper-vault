<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.femdom-fetish-clips.com");
print $html;
print "\n\nEND OF HTML\n\n"; 

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div.post') as $article) {
     $item['post_title']     = $article->find('div.post_title', 0)->plaintext;
     $item['post_text']    = $article->find('div.post_text', 0)->plaintext;
     $item['img']    = $article->find('img',0)->src;
     $item['a']    = $article->find('a',1)->href;
     $item['post_keywords'] = $article->find('div.post_keywords', 0)->plaintext;
     $articles[] = $item;
         }
         
         scraperwiki::save(array('post_title','post_text','img','a','post_keywords'), $articles);         



?><?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.femdom-fetish-clips.com");
print $html;
print "\n\nEND OF HTML\n\n"; 

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div.post') as $article) {
     $item['post_title']     = $article->find('div.post_title', 0)->plaintext;
     $item['post_text']    = $article->find('div.post_text', 0)->plaintext;
     $item['img']    = $article->find('img',0)->src;
     $item['a']    = $article->find('a',1)->href;
     $item['post_keywords'] = $article->find('div.post_keywords', 0)->plaintext;
     $articles[] = $item;
         }
         
         scraperwiki::save(array('post_title','post_text','img','a','post_keywords'), $articles);         



?>