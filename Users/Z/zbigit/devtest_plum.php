<?php

require  'scraperwiki/simple_html_dom.php';

$verbose = 0;

$url = "http://www.plumdistrict.com/deals/rss.xml?affiliate_url=http://gan.doubleclick.net/gan_click?lid=41000000032549767&pubid=21000000000320750";

$feed_html = scraperWiki::scrape($url);

if($feed_html)
{
    scraperwiki::sqliteexecute("drop table if exists plum"); 

    $feed_dom = new simple_html_dom();
    $feed_dom->load($feed_html);

    $arr = array();
    foreach($feed_dom->find('item') as $item)
    {   
        $row = array();
    
        $deep_link = $row['guid'] = $item->find('guid', 0)->plaintext;
        $row['deal_content_id'] = $item->find('deal_content_id', 0)->plaintext;
        
        if($deep_link)
        {        
            print $deep_link . "\n";
       
            $deep_html = scraperWiki::scrape($deep_link);
            
            if($deep_html)
            {
                if(preg_match('|Expires ([\d]{2}/[\d]{2}/[\d]{2})|si', $deep_html, $mm))
                {
                    $tmp = strtotime($mm[1]);                
                    $expire_date = date('Y-m-d', $tmp);
                    
                    $row['expire_date'] = $expire_date;
                    $row['_executed'] = date('Y-m-d H:i:s');
                }
            }
        }
        scraperwiki::save_sqlite(array('guid'), $row, "plum", $verbose);        
    }
}

?><?php

require  'scraperwiki/simple_html_dom.php';

$verbose = 0;

$url = "http://www.plumdistrict.com/deals/rss.xml?affiliate_url=http://gan.doubleclick.net/gan_click?lid=41000000032549767&pubid=21000000000320750";

$feed_html = scraperWiki::scrape($url);

if($feed_html)
{
    scraperwiki::sqliteexecute("drop table if exists plum"); 

    $feed_dom = new simple_html_dom();
    $feed_dom->load($feed_html);

    $arr = array();
    foreach($feed_dom->find('item') as $item)
    {   
        $row = array();
    
        $deep_link = $row['guid'] = $item->find('guid', 0)->plaintext;
        $row['deal_content_id'] = $item->find('deal_content_id', 0)->plaintext;
        
        if($deep_link)
        {        
            print $deep_link . "\n";
       
            $deep_html = scraperWiki::scrape($deep_link);
            
            if($deep_html)
            {
                if(preg_match('|Expires ([\d]{2}/[\d]{2}/[\d]{2})|si', $deep_html, $mm))
                {
                    $tmp = strtotime($mm[1]);                
                    $expire_date = date('Y-m-d', $tmp);
                    
                    $row['expire_date'] = $expire_date;
                    $row['_executed'] = date('Y-m-d H:i:s');
                }
            }
        }
        scraperwiki::save_sqlite(array('guid'), $row, "plum", $verbose);        
    }
}

?>