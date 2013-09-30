<?php

set_time_limit(0);

$tvUrl = "http://www.listal.com/lists/tv";
$listUrl = "http://www.listal.com/list";

$pages = array(0=>"http://www.listal.com/lists/tv");
$pageIndex = array("http://www.listal.com/lists/tv"=>false);
$pageCount = 1;

for($pNum = 0; $pNum < $pageCount; $pNum++)
{
    $html = scraperWiki::scrape($pages[$pNum]);
    
    $pageHtml = substr($html, strpos($html, "<div class='pages'>"));
    $pageHtml = substr($pageHtml, 0, strpos($pageHtml, "</div>"));
    
    
    preg_match_all(
        "|<a href='/lists/tv(.*?)'>|s",
        $pageHtml,
        $matches, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array 
    );
    
    foreach($matches as $match) {        
        $page = $tvUrl.trim($match[1]);
        if (!isset($pageIndex[$page])) 
        {
            $pageIndex[$page] = false;
            $pages[] = $page;
            $pageCount++;
        }
    }

    preg_match_all(
        "|<div><a href='http://www.listal.com/list(.*?)'><img src='(.*?)'(.*?)<b><a href='(.*?)' style='font-size:110%;'>(.*?)</a></b>(.*?)<span class='greytext'>  list by (.*?)</span>|s",
        $html,
        $matches, // will contain the lists
        PREG_SET_ORDER // formats data into an array 
    );
    
    $lists = array();
    foreach($matches as $match) {
        $lists[] = array("name"=>trim($match[5]), "link"=>$listUrl.trim($match[1]),"image"=>trim($match[2]),"author"=>trim($match[7]));
    }

    for($lNum = 0; $lNum < count($lists); $lNum++)
    {
        $l = $lists[$lNum];
        $listHtml = scraperWiki::scrape($l["link"]);
        
        preg_match_all(
            "|<span id='count_(.*?)' style='font-weight:bold;font-size:110%;'>(.*?). <a href='http://www.listal.com/tv(.*?)'>(.*?)</a></span> \((.*?)\)|s",
            $listHtml,
            $matches, // will contain the item data
            PREG_SET_ORDER // formats data into an array
        );
        
        foreach($matches as $match) {
            $match[1] = trim($match[1]);
            $match[2] = trim($match[2]);
            $match[3] = trim($match[3]);
            $match[4] = trim($match[4]);
            $match[5] = trim($match[5]);

            $listName = mb_check_encoding($l["name"], 'UTF-8') ? $l["name"] : utf8_encode($l["name"]);
            $listLink = mb_check_encoding($l["link"], 'UTF-8') ? $l["link"] : utf8_encode($l["link"]);
            $name = mb_check_encoding($match[4], 'UTF-8') ? $match[4] : utf8_encode($match[4]);
            $link = mb_check_encoding($match[3], 'UTF-8') ? $tvUrl.$match[3] : $tvUrl.utf8_encode($match[3]);
            $id = mb_check_encoding($match[1], 'UTF-8') ? $match[1] : utf8_encode($match[1]);
            $year = mb_check_encoding($match[5], 'UTF-8') ? $match[5] : utf8_encode($match[5]);
            $num = mb_check_encoding($match[2], 'UTF-8') ? $match[2] : utf8_encode($match[2]);

            $item = array("listName" => $listName, "listLink" => $listLink, "name"=>$name, "link"=>$link,"id"=>$id,"year"=>$year, "num"=>$num);
            
            $saved = false;
            $delay = 0;
            while(!$saved && $delay < 600)
            {
                try
                {
                    @scraperwiki::save_sqlite(array('id'), $item, 'item');
                    $saved = true;
                } catch (Exception $e) {
                    sleep(10);
                    $delay++;
                }
            }
        }
        
        $saved = false;
        $delay = 0;
        while(!$saved && $delay < 600)
        {
            try
            {
                @scraperwiki::save_sqlite(array('link'), $lists[$lNum], 'list');
                $saved = true;
            } catch (Exception $e) {
                sleep(10);
                $delay++;
            }
        }

    }

}


?>
<?php

set_time_limit(0);

$tvUrl = "http://www.listal.com/lists/tv";
$listUrl = "http://www.listal.com/list";

$pages = array(0=>"http://www.listal.com/lists/tv");
$pageIndex = array("http://www.listal.com/lists/tv"=>false);
$pageCount = 1;

for($pNum = 0; $pNum < $pageCount; $pNum++)
{
    $html = scraperWiki::scrape($pages[$pNum]);
    
    $pageHtml = substr($html, strpos($html, "<div class='pages'>"));
    $pageHtml = substr($pageHtml, 0, strpos($pageHtml, "</div>"));
    
    
    preg_match_all(
        "|<a href='/lists/tv(.*?)'>|s",
        $pageHtml,
        $matches, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array 
    );
    
    foreach($matches as $match) {        
        $page = $tvUrl.trim($match[1]);
        if (!isset($pageIndex[$page])) 
        {
            $pageIndex[$page] = false;
            $pages[] = $page;
            $pageCount++;
        }
    }

    preg_match_all(
        "|<div><a href='http://www.listal.com/list(.*?)'><img src='(.*?)'(.*?)<b><a href='(.*?)' style='font-size:110%;'>(.*?)</a></b>(.*?)<span class='greytext'>  list by (.*?)</span>|s",
        $html,
        $matches, // will contain the lists
        PREG_SET_ORDER // formats data into an array 
    );
    
    $lists = array();
    foreach($matches as $match) {
        $lists[] = array("name"=>trim($match[5]), "link"=>$listUrl.trim($match[1]),"image"=>trim($match[2]),"author"=>trim($match[7]));
    }

    for($lNum = 0; $lNum < count($lists); $lNum++)
    {
        $l = $lists[$lNum];
        $listHtml = scraperWiki::scrape($l["link"]);
        
        preg_match_all(
            "|<span id='count_(.*?)' style='font-weight:bold;font-size:110%;'>(.*?). <a href='http://www.listal.com/tv(.*?)'>(.*?)</a></span> \((.*?)\)|s",
            $listHtml,
            $matches, // will contain the item data
            PREG_SET_ORDER // formats data into an array
        );
        
        foreach($matches as $match) {
            $match[1] = trim($match[1]);
            $match[2] = trim($match[2]);
            $match[3] = trim($match[3]);
            $match[4] = trim($match[4]);
            $match[5] = trim($match[5]);

            $listName = mb_check_encoding($l["name"], 'UTF-8') ? $l["name"] : utf8_encode($l["name"]);
            $listLink = mb_check_encoding($l["link"], 'UTF-8') ? $l["link"] : utf8_encode($l["link"]);
            $name = mb_check_encoding($match[4], 'UTF-8') ? $match[4] : utf8_encode($match[4]);
            $link = mb_check_encoding($match[3], 'UTF-8') ? $tvUrl.$match[3] : $tvUrl.utf8_encode($match[3]);
            $id = mb_check_encoding($match[1], 'UTF-8') ? $match[1] : utf8_encode($match[1]);
            $year = mb_check_encoding($match[5], 'UTF-8') ? $match[5] : utf8_encode($match[5]);
            $num = mb_check_encoding($match[2], 'UTF-8') ? $match[2] : utf8_encode($match[2]);

            $item = array("listName" => $listName, "listLink" => $listLink, "name"=>$name, "link"=>$link,"id"=>$id,"year"=>$year, "num"=>$num);
            
            $saved = false;
            $delay = 0;
            while(!$saved && $delay < 600)
            {
                try
                {
                    @scraperwiki::save_sqlite(array('id'), $item, 'item');
                    $saved = true;
                } catch (Exception $e) {
                    sleep(10);
                    $delay++;
                }
            }
        }
        
        $saved = false;
        $delay = 0;
        while(!$saved && $delay < 600)
        {
            try
            {
                @scraperwiki::save_sqlite(array('link'), $lists[$lNum], 'list');
                $saved = true;
            } catch (Exception $e) {
                sleep(10);
                $delay++;
            }
        }

    }

}


?>
