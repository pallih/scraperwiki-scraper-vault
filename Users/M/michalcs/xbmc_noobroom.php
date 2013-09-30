<?php

$html = scraperWiki::scrape("http://noobroom5.com/latest.php");

require "scraperwiki/simple_html_dom.php";
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[style=width:728px;]") as $movTable);

$i=0;
foreach($movTable->find("a") as $Movie){
    if($i==222) break;
    $noobId = preg_replace('/\/\?(\d+$)/', '$1', $Movie->href);

    $noobTitle = $Movie->plaintext;
    $noobUrl = "http://noobroom5.com" . $Movie->href;
    $noobPage = file_get_html($noobUrl);
    $noobImdb = $noobPage->find("a[@title='The Internet Movie Database']", 0)->href;
    $imdbId = preg_replace('/http:\/\/imdb.com\/title\/(tt.*?)/', '$1', $noobImdb);  
    $noobDate = date(DATE_ISO8601);

    getTmdb($imdbId);

    $movInfo = array('movietitle' => $movTitle,
                     'movienoobtitle' => $noobTitle,
                     'movierelease' => $movRelease,
                     'moviegenre' => $movGenre,
                     'movieposter' => $movPoster,
                     'moviefanart' => $movFanart,
                     'noobid' => $noobId,
                     'movieurl' => $noobUrl,
                     'movieplot' => $movPlot);

    print json_encode($movInfo) . "\n";

    

    scraperwiki::save(array('noobid'), $movInfo);

    $i++;

}

function getTmdb($noobImdb)
    {
    global $movTitle, $movRelease, $movGenre, $movPoster, $movFanart, $movPlot;

    $tmdbApi = "23e89da030a0ee8b25aaed20950a0c25";

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://api.themoviedb.org/3/movie/".$noobImdb."?api_key=".$tmdbApi);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_HEADER, FALSE);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array("Accept: application/json"));
    $tmdbResponse = curl_exec($ch);
    curl_close($ch);

    $tmdbResult = json_decode($tmdbResponse);
    $movTitle = $tmdbResult->original_title;
    $movRelease = date('d.m.Y', strtotime($tmdbResult->release_date));
    $movGenre = $tmdbResult->genres[0]->name;
    $movPoster = $tmdbResult->poster_path;
    $movFanart = $tmdbResult->backdrop_path;
    $movPlot = $tmdbResult->overview;

    }


?>
<?php

$html = scraperWiki::scrape("http://noobroom5.com/latest.php");

require "scraperwiki/simple_html_dom.php";
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[style=width:728px;]") as $movTable);

$i=0;
foreach($movTable->find("a") as $Movie){
    if($i==222) break;
    $noobId = preg_replace('/\/\?(\d+$)/', '$1', $Movie->href);

    $noobTitle = $Movie->plaintext;
    $noobUrl = "http://noobroom5.com" . $Movie->href;
    $noobPage = file_get_html($noobUrl);
    $noobImdb = $noobPage->find("a[@title='The Internet Movie Database']", 0)->href;
    $imdbId = preg_replace('/http:\/\/imdb.com\/title\/(tt.*?)/', '$1', $noobImdb);  
    $noobDate = date(DATE_ISO8601);

    getTmdb($imdbId);

    $movInfo = array('movietitle' => $movTitle,
                     'movienoobtitle' => $noobTitle,
                     'movierelease' => $movRelease,
                     'moviegenre' => $movGenre,
                     'movieposter' => $movPoster,
                     'moviefanart' => $movFanart,
                     'noobid' => $noobId,
                     'movieurl' => $noobUrl,
                     'movieplot' => $movPlot);

    print json_encode($movInfo) . "\n";

    

    scraperwiki::save(array('noobid'), $movInfo);

    $i++;

}

function getTmdb($noobImdb)
    {
    global $movTitle, $movRelease, $movGenre, $movPoster, $movFanart, $movPlot;

    $tmdbApi = "23e89da030a0ee8b25aaed20950a0c25";

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://api.themoviedb.org/3/movie/".$noobImdb."?api_key=".$tmdbApi);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    curl_setopt($ch, CURLOPT_HEADER, FALSE);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array("Accept: application/json"));
    $tmdbResponse = curl_exec($ch);
    curl_close($ch);

    $tmdbResult = json_decode($tmdbResponse);
    $movTitle = $tmdbResult->original_title;
    $movRelease = date('d.m.Y', strtotime($tmdbResult->release_date));
    $movGenre = $tmdbResult->genres[0]->name;
    $movPoster = $tmdbResult->poster_path;
    $movFanart = $tmdbResult->backdrop_path;
    $movPlot = $tmdbResult->overview;

    }


?>
