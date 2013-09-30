<?php

set_time_limit(0);

$visitedIds = array();

function scrapeMarketGroup($url) {
    global $visitedIds;

    $html = scraperWiki::scrape($url);
    $html = str_replace("\n", "", $html);
    
    preg_match_all(
        "|<a href=\"/importing/61000746/marketgroup/(\d+?)/\">(.+?)</a>|s",
        $html,
        $matches, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array
    );
    
    foreach($matches as $match) {
        $groupId = $match[1];
        $groupName = html_entity_decode($match[2]);
        //echo $groupName."\n";

        if (!in_array($groupId, $visitedIds)) {
            $visitedIds[] = $groupId;
            scrapeMarketGroup("http://goonmetrics.com/importing/61000746/marketgroup/".$groupId."/");
        }
    }

    preg_match_all(
        "|<tr(.*?)>(.*?)<td(.*?)><a href=\"http://games.chruker.dk/eve_online/item.php\?type_id=(.+?)\" target=\"_blank\">(.*?)<span class=\"dot\" onclick=\"CCPEVE.showMarketDetails\((.*?)\)\">(.+?)</span>(.*?)</td>(.*?)<td(.*?)>(.+?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.+?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)</tr>|s",
        $html,
        $matches, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array
    );
    
    foreach($matches as $match) {

        $item = array(
            "itemId" => trim($match[4]),
            "name" => trim(mb_check_encoding($match[7], 'UTF-8') ? $match[7] : utf8_encode($match[7])),
            "weekVol" => trim(mb_check_encoding($match[11], 'UTF-8') ? $match[11] : utf8_encode($match[11])),
            "k6Stock" => trim(mb_check_encoding($match[17], 'UTF-8') ? $match[17] : utf8_encode($match[17]))
        );

        $item['weekVol'] = str_replace(",", "", $item['weekVol']);
        $item['k6Stock'] = str_replace(",", "", $item['k6Stock']);

        $saved = false;
        $delay = 0;
        while(!$saved && $delay < 600)
        {
            try
            {
                @scraperwiki::save_sqlite(array('itemId'), $item , 'eve_goonmetrics');
                $saved = true;
            } catch (Exception $e) {
                sleep(10);
                $delay++;
            }
        }

    }
}

scrapeMarketGroup("http://goonmetrics.com/importing/61000746/marketgroup");

?>

<?php

set_time_limit(0);

$visitedIds = array();

function scrapeMarketGroup($url) {
    global $visitedIds;

    $html = scraperWiki::scrape($url);
    $html = str_replace("\n", "", $html);
    
    preg_match_all(
        "|<a href=\"/importing/61000746/marketgroup/(\d+?)/\">(.+?)</a>|s",
        $html,
        $matches, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array
    );
    
    foreach($matches as $match) {
        $groupId = $match[1];
        $groupName = html_entity_decode($match[2]);
        //echo $groupName."\n";

        if (!in_array($groupId, $visitedIds)) {
            $visitedIds[] = $groupId;
            scrapeMarketGroup("http://goonmetrics.com/importing/61000746/marketgroup/".$groupId."/");
        }
    }

    preg_match_all(
        "|<tr(.*?)>(.*?)<td(.*?)><a href=\"http://games.chruker.dk/eve_online/item.php\?type_id=(.+?)\" target=\"_blank\">(.*?)<span class=\"dot\" onclick=\"CCPEVE.showMarketDetails\((.*?)\)\">(.+?)</span>(.*?)</td>(.*?)<td(.*?)>(.+?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.+?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)<td(.*?)>(.*?)</td>(.*?)</tr>|s",
        $html,
        $matches, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array
    );
    
    foreach($matches as $match) {

        $item = array(
            "itemId" => trim($match[4]),
            "name" => trim(mb_check_encoding($match[7], 'UTF-8') ? $match[7] : utf8_encode($match[7])),
            "weekVol" => trim(mb_check_encoding($match[11], 'UTF-8') ? $match[11] : utf8_encode($match[11])),
            "k6Stock" => trim(mb_check_encoding($match[17], 'UTF-8') ? $match[17] : utf8_encode($match[17]))
        );

        $item['weekVol'] = str_replace(",", "", $item['weekVol']);
        $item['k6Stock'] = str_replace(",", "", $item['k6Stock']);

        $saved = false;
        $delay = 0;
        while(!$saved && $delay < 600)
        {
            try
            {
                @scraperwiki::save_sqlite(array('itemId'), $item , 'eve_goonmetrics');
                $saved = true;
            } catch (Exception $e) {
                sleep(10);
                $delay++;
            }
        }

    }
}

scrapeMarketGroup("http://goonmetrics.com/importing/61000746/marketgroup");

?>

