<?php
require 'scraperwiki/simple_html_dom.php';

for($jahr=1985; $jahr<2014; $jahr++){  
    for($monat=1; $monat<12; $monat++){
        for($page=1; $page<40; $page++){        
            print "Currently scraping /releases.html?archive=".$jahr."-".$monat."&page=".$page."" . "\n";
        
            $html_content = scraperWiki::scrape("http://www.xrel.to/releases.html?archive=".$jahr."-".$monat."&page=".$page."");
            $html = str_get_html($html_content);

            foreach ($html->find("div.release_title a span") as $rls)
            {
                if (empty($rls->title))
                {
                    $save = scraperwiki::save_sqlite(array("release"),array("release"=> $rls->plaintext));
                }
                else
                {    
                    $save = scraperwiki::save_sqlite(array("release"),array("release"=> $rls->title));
                }
            }
    
            $html->__destruct();
        }
    }
}
?><?php
require 'scraperwiki/simple_html_dom.php';

for($jahr=1985; $jahr<2014; $jahr++){  
    for($monat=1; $monat<12; $monat++){
        for($page=1; $page<40; $page++){        
            print "Currently scraping /releases.html?archive=".$jahr."-".$monat."&page=".$page."" . "\n";
        
            $html_content = scraperWiki::scrape("http://www.xrel.to/releases.html?archive=".$jahr."-".$monat."&page=".$page."");
            $html = str_get_html($html_content);

            foreach ($html->find("div.release_title a span") as $rls)
            {
                if (empty($rls->title))
                {
                    $save = scraperwiki::save_sqlite(array("release"),array("release"=> $rls->plaintext));
                }
                else
                {    
                    $save = scraperwiki::save_sqlite(array("release"),array("release"=> $rls->title));
                }
            }
    
            $html->__destruct();
        }
    }
}
?>