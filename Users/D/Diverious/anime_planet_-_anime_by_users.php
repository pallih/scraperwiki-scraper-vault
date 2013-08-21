<?php

set_time_limit(0);

$html = scraperWiki::scrape("http://games.chruker.dk/eve_online/inventory.php?category_id=9");

preg_match_all(
    "|<a href=\"inventory.php\?group_id=(.+?)\">(.+?)</a>|s",
    $html,
    $matches, // will contain the pagination pages
    PREG_SET_ORDER // formats data into an array
);

foreach($matches as $match) {
    $groupId = $match[1];
    $group = $match[2];    

    $html = scraperWiki::scrape("http://games.chruker.dk/eve_online/inventory.php?group_id=".$groupId);

    preg_match_all(
        "|<a href='item.php\?type_id=(.+?)'>(.+?)</a>|s",
        $html,
        $matches2, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array
    );
    
    foreach($matches2 as $match2) {
        $itemId = $match2[1];
        $item = $match2[2];  

        $html = scraperWiki::scrape("http://games.chruker.dk/eve_online/item.php?type_id=".$itemId);

        $i = strpos($html, "Materials - Consumed");
        if ($i == false) continue;
        $j = strpos($html, "</tr>", $i);
        $k = strpos($html, "Time Efficiency Research", $j);

        $header = substr($html, $i, $j-$i);

        $body = str_replace("\n", "", substr($html, $j, $k-$j));

        preg_match_all(
            "|<td (.+?)'>(.+?)</td>|s",
            $header,
            $matches3, // will contain the pagination pages
            PREG_SET_ORDER // formats data into an array
        );

        $skills = array();
        
        foreach($matches3 as $match3) {
            $skills[] = strtolower($match3[2]);
        }

        preg_match_all(
            "|<tr>(\s)*<td(.+?)>(.+?)</td>(.+?)</tr>|s",
            $body,
            $matches3, // will contain the pagination pages
            PREG_SET_ORDER // formats data into an array
        );

        $un = 0;

        foreach($matches3 as $match3) {
            $un++;
            $materialItemId = "NA".$un;
            $materialItem = "";
            $material = $match3[3];

            preg_match_all(
                "|<a href='item.php\?type_id=(.+?)'>(.+?)</a>|s",
                $material,
                $matches5, // will contain the pagination pages
                PREG_SET_ORDER // formats data into an array
            );
    
            foreach($matches5 as $match5) {
                $materialItemId = $match5[1];
                $materialItem = $match5[2];
            }

            $matHtml = $match3[4];

            preg_match_all(
                "|<td (.+?)>(.+?)</td>|s",
                $matHtml,
                $matches4, // will contain the pagination pages
                PREG_SET_ORDER // formats data into an array
            );

            $skillValues = array();
    
            foreach($matches4 as $match4) {
                $skillValues[] = $match4[2];
            }

            $blueprintItem = array(
                "itemId" => trim($itemId),
                "item" => trim(mb_check_encoding($item, 'UTF-8') ? $item : utf8_encode($item)),
                "groupId" => trim($groupId),
                "group" => trim(mb_check_encoding($group, 'UTF-8') ? $group : utf8_encode($group)),
                "materialItemId" => trim($materialItemId),
                "materialItem" => trim(mb_check_encoding($materialItem, 'UTF-8') ? $materialItem : utf8_encode($materialItem))
            );

            for($v = 0; $v < count($skills); $v++) {
                $skill = trim(mb_check_encoding($skills[$v], 'UTF-8') ? $skills[$v] : utf8_encode($skills[$v]));
                $skillValue = trim(mb_check_encoding($skillValues[$v], 'UTF-8') ? $skillValues[$v] : utf8_encode($skillValues[$v]));
                $skillValue = str_replace(".", "", $skillValue);
                $blueprintItem[$skill] = $skillValue;
            }

            $saved = false;
            $delay = 0;
            while(!$saved && $delay < 600)
            {
                try
                {
                    @scraperwiki::save_sqlite(array('groupId', 'itemId', 'materialItemId'), $blueprintItem , 'eve_blueprint');
                    $saved = true;
                } catch (Exception $e) {
                    sleep(10);
                    $delay++;
                }
            }

        }

    }

}

?>
