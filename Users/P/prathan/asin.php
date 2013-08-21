<?php

$html = scraperWiki::scrape("http://www.amazon.com/s/ref=sr_nr_p_36_5?bbn=165796011&qid=1334198836&rh=n%3A165796011&rnid=386430011&low-price=100&high-price=&x=0&y=0");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[class='image'] a") as $obj)
{
    if(preg_match('#http://www.amazon.com/([\w-]+/)?(dp|gp/product)/(\w+/)?(\w{10})#', $obj->href, $matches))            
    {
        $record['title']= str_replace('-', ' ', $matches[1]);
        $record['title']= str_replace('/', '', $record['title']);
        $record['asin']= $matches[4];
        
        scraperwiki::save(array('asin'), $record); 

    }
}
?>
