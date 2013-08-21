<?php

$html = scraperWiki::scrape("http://www.bbc.co.uk/iplayer/tv/categories/films?sort=dateavailable");

require "scraperwiki/simple_html_dom.php";
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div[@id='category-results'] h3 a") as $Movie){
    $movTitle = $Movie->title;
    $movUrl = "http://www.bbc.co.uk" . $Movie->href;
    $movPage = file_get_html($movUrl);
    $movExpiry = $movPage->find("li[@class='available'] span", 0)->innertext;
    $movDate = date(DATE_ISO8601);

    getBingImdb($movTitle);

    $movInfo = array('movietitle' => $movTitle,
                     'imdbtitle' => $imdbTitle,
                     'imdbrelease' => $imdbRelease,
                     'imdbrating' => $imdbRating,
                     'movieexpiry' => $movExpiry,
                     'imdbid' => $imdbId,
                     'imdburl' => $imdbUrl,
                     'movielink' => $movUrl,
                     'date' => $movDate);

    print json_encode($movInfo) . "\n";

    scraperwiki::save(array('movietitle'), $movInfo);
}

function getBingImdb($moviename)
    {
    global $imdbTitle, $imdbRelease, $imdbId, $imdbUrl, $imdbRating;

    $bingUrl = "http://www.bing.com/search?q=" . urlencode($moviename) . "+imdb+NOT+intitle%3Atv+site%3Aimdb.com";
    $bingPage = file_get_html($bingUrl);
    $bingResult = $bingPage->find("div[@class='sa_mc']",0);
    $bingTitle = html_entity_decode($bingResult->find("h3 a",0)->plaintext);
    $imdbName = preg_replace('/^IMDb: | - IMDb$/', '', $bingTitle);
    if (preg_match('/\(.*?\)$/',$imdbName)){
        $imdbTitle = preg_replace('/(.*?) \(.*?\)$/','$1',$imdbName);
        $imdbRelease = preg_replace('/.*?\((.*?)\)$/','$1',$imdbName);
    }else{$imdbTitle=$imdbName;$imdbRelease="unknown";}
    $imdbUrl = $bingResult->find("h3 a",0)->href;
    preg_match('/(tt\d+)/',$imdbUrl,$imdbId);
    $imdbId = $imdbId[1];
    $bingRating = $bingResult->find("ul[@class='sp_pss'] li", 0)->plaintext;
    $imdbRating = preg_replace('/User rating: (.*?)\/10.*/', '$1', $bingRating);  
    }
?>
