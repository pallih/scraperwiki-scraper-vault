<?php
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

//This doesn't seem to work
//scraperwiki::sqliteexecute("delete from swdata where 'index'=1");
//scraperwiki::sqlitecommit();

//A simple for loop was able to initially populate the list.  After that, it's faster to only query the URLs that are already in the list
//for ($i = 1; $i <= 3000; $i++) {

$dbTable = scraperwiki::select("* from swdata");
foreach($dbTable as $dbRow) {
    $html = scraperWiki::scrape("http://thedimsumdiaries.com/?p=" . $dbRow['index']);
    $dom->load($html);
    $content = $dom->find("div.post");
    if ($content[0]->plaintext == "Sorry, no posts matched your criteria.") {continue;}

    $idElem = $dom->find("#comment_post_ID");
    $id = $idElem[0]->value;
    $titleElems = $dom->find("h1.title a");
    if (count($titleElems)!=1) {continue;}

    $rating = -1;
    $ratingElems = $dom->find("div.entry p a img.alignleft");
    if (count($ratingElems)>0) {
        preg_match('/(\d)\_oh/', $ratingElems[0]->src, $matches);
        if (count($matches)>1) $rating = intval($matches[1]);
    }

    //Figure out a better way to find the address (look for <strong> around the title)
    $paraElems = $dom->find("div.entry p");

    $address = 'unknown';
    $lat = 0.0;
    $lng = 0.0;
    for ($j = count($paraElems)-1; $j >= 0; $j--) {
        //print $paraElems[$j];
        if (strpos($paraElems[$j], "<br />")) {
            $address = str_replace("&#8211", "-", str_replace("&#8217;", "a", str_replace(array("\r", "\r\n", "\n"), "", $paraElems[$j]->plaintext ) ) );
            $geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='.urlencode($address).'&sensor=false&output=json';
            $geocode_res = json_decode(scraperWiki::scrape($geocode_url), true);
            if (isset($geocode_res['results'][0]['geometry']['location'])) {
                $lat = $geocode_res['results'][0]['geometry']['location']['lat'];
                $lng = $geocode_res['results'][0]['geometry']['location']['lng'];
            }
        }
    }


    $record = array(
        'index'       => $id,
        'title'       => str_replace("&#8211", "-", str_replace("&#8217;", "a", str_replace("&nbsp;", " ", $titleElems[0]->plaintext) ) ),
        'url'         => $titleElems[0]->href,
        'date'        => date_create( str_replace("/", "-", substr($titleElems[0]->href, 28, 10) ) ),
        'rating'      => $rating,
        'address'     => $address,
        'lat'         => $lat,
        'lng'         => $lng,
    );
    scraperwiki::save(array('index'), $record);

    $tags = $dom->find("p.entry-tags a");
    foreach($tags as $t) {
        scraperwiki::save_sqlite(array('tag','id'), array('id'=>$i, 'tag'=>$t->plaintext), $table_name="tags");
    }
}

          



?>
