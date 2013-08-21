<?php

set_time_limit(0);

$user_url = "http://www.anime-planet.com/users";

$html = scraperWiki::scrape($user_url."/all");

$i = strrpos(substr($html, 0, strpos($html, "<li class='next'>")), "rel='nofollow'") + 15;
$j = strpos($html, "<", $i);

$page_count = trim(substr($html, $i, $j - $i));
$pages_scraped = array();

for($user_page = 1; $user_page <= $page_count; $user_page++) {

    //$page_num = rand(1, $page_count);
    //while(in_array($page_num, $pages_scraped)) {
    //    $page_num = rand(1, $page_count);
    //}
    //$pages_scraped[] = $page_num;

    $page_num = $user_page;

    $html = scraperWiki::scrape($user_url."/all?page=".$page_num); 

    preg_match_all(
        "|<td class=\"tableUserName\"><a href='/users/(.+?)'>|s",
        $html,
        $matches, // will contain the pagination pages
        PREG_SET_ORDER // formats data into an array 
    );

    foreach($matches as $match) {    
        $user = $match[1];

        $anime_html = scraperWiki::scrape($user_url."/".$user."/anime"); 

        $i = strrpos(substr($anime_html, 0, strpos($anime_html, "<li class='next'>")), "rel='nofollow'") + 15;
        $j = strpos($anime_html, "<", $i);
        
        $anime_page_count = trim(substr($anime_html, $i, $j - $i));

        for($anime_page = 1; $anime_page <= $anime_page_count; $anime_page++) {
            $anime_html = scraperWiki::scrape($user_url."/".$user."/anime?page=".$anime_page); 
            
            $pattern =  "|<td class=\"tableTitle\"><a href='(.*?)'>(.*?)</a></td>(.*?)<td class=\"tableType\">(.*?)</td>(.*?)<td class=\"tableYear\">(.*?)</td>(.*?)<!-- status box -->";
            $pattern .= "(.*?)</td><td class=\"tableEps\">(.*?)</td><td class=\"tableRating\">(.*?)title=\"(.*?)\"|s";

            preg_match_all(
                $pattern,
                $anime_html,
                $anime_matches, 
                PREG_SET_ORDER 
            );

            foreach($anime_matches as $anime_match) {    
                $anime_match[1] = trim($anime_match[1]);
                $anime_match[2] = trim($anime_match[2]);
                $anime_match[4] = trim($anime_match[4]);
                $anime_match[6] = trim($anime_match[6]);
                $anime_match[8] = trim($anime_match[8]);
                $anime_match[9] = trim($anime_match[9]);
                $anime_match[11] = trim($anime_match[11]);

                if ($anime_match[9] == "&nbsp;") $anime_match[9] = null;
    
                $rating = $anime_match[11];
                if ($rating == "not rated") {
                    $rating = null;
                } else {
                    $rating = trim(substr($rating, 0, strpos($rating, "star")));
                }
    
                $anime = array(
                    "user" => $user,
                    "title" => mb_check_encoding($anime_match[2], 'UTF-8') ? $anime_match[2] : utf8_encode($anime_match[2]),
                    "link" => mb_check_encoding($anime_match[1], 'UTF-8') ? "http://www.anime-planet.com".$anime_match[1] : "http://www.anime-planet.com".utf8_encode($anime_match[1]),
                    "type" => mb_check_encoding($anime_match[4], 'UTF-8') ? $anime_match[4] : utf8_encode($anime_match[4]),
                    "year" => mb_check_encoding($anime_match[6], 'UTF-8') ? $anime_match[6] : utf8_encode($anime_match[6]),
                    "status" => mb_check_encoding($anime_match[8], 'UTF-8') ? $anime_match[8] : utf8_encode($anime_match[8]),
                    "episodes_watched" => mb_check_encoding($anime_match[9], 'UTF-8') ? $anime_match[9] : utf8_encode($anime_match[9]),
                    "rating" => $rating
                );
                
                $saved = false;
                $delay = 0;
                while(!$saved && $delay < 600)
                {
                    try
                    {
                        @scraperwiki::save_sqlite(array('user', 'link'), $anime , 'user_anime');
                        $saved = true;
                    } catch (Exception $e) {
                        sleep(10);
                        $delay++;
                    }
                }
            }
        }
    }
}


?>
