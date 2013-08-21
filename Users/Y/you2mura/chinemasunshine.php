<?php
require 'scraperwiki/simple_html_dom.php';           
$html = file_get_html('http://www.cinemasunshine.co.jp/next_showing/?theaterSelect=2', false, getContext());

foreach ($html->find('div[class="movieListArea"]') as $movie) {
    $record = array(
        'url' => getMovieURL($movie),
        'openDay' => getMovieOpenDay($movie),
        'title' => getMovieTitle($movie),
        'imageUrl' => getMovieImageURL($movie),
    );
    scraperwiki::save(array('url'), $record); 
}
$html->__destruct();

function getMovieURL($movie) {
    $url = trim($movie->find('div[class="right"] p[class="name"] a', 0)->href);
    return $url;
}

function getMovieOpenDay($movie) {
    $day = $movie->find('div[class="right"] p[class="day"]', 0)->plaintext;
    preg_match('/^([0-9]{4}\/[0-9]{1,2}\/[0-9]{1,2}).*$/', $day, $matcher);
    return (count($matcher) > 0) ? $matcher[1] : '';
}

function getMovieTitle($movie) {
    $title = trim($movie->find('div[class="right"] p[class="name"] a', 0)->plaintext);
    return $title;
}

function getMovieImageURL($movie) {
    $url = trim($movie->find('div[class="left"] p', 0)->find('img', 0)->src);
    return sprintf("http://www.cinemasunshine.co.jp%s", $url);
}

function getContext() {
        $opts = array(
                'http'=>array(
                        'method'=>"GET",
                        'header'=>"User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)"
                )
        );
        return stream_context_create($opts);
}

?>
