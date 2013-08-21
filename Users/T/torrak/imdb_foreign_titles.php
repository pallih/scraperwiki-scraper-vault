<?php

# *************************** #
# IMDB Foreign Titles scraper #
# *************************** #
/** NOTES:
- We HAVE to use cURL, seeing as the Accept-Language header is without effect with file_get_contents().
- To prevent caching fro ScraperWiki, 'Cache-Control: no-cache' seems to be enough.
- If need be, we coul circumvent caching by using international versions of the site instead but this is of limited use (see next time).
- The Accept-Language header is only supported by IMDB.Com (not by the local sites).
- The IMDB source is encoded in iso-8859-1 as time of creation of this scraper and uses hexadecimal encoding for non-Latin chracter (eg: French accents, Russian alphabet).
- Currently, we get the original title of the movie if there is no translation available for our language (RU, FR, etc.). It's okay. If we need more precision, we'll tap into the list of translations (instead of merely the page title).
**/

# requirements
// print_r ($_SERVER);
require ( @$_SERVER['LOGNAME'] == 'scriptrunner' ? 'scraperwiki/' : '' ) . 'simple_html_dom.php';


# JUST RUN ONCE when datastore is empty. So as to create table manually just so as to set 'id' as the index key
## scraperwiki::sqliteexecute("create table swdata (`imdb_id` string ) "); die();
//scraperwiki::save_var('last_id', 0 ); // restart from the beginning

# Setting up the variables (static/manual)
# $imdb_id = "tt0076759"; // Star Wars (1977)
# $title['imdb_id'] = $imdb_id;

# Retrieve last run info. Note we do the last/fist row twice: whatever. 
$last_run_id = scraperwiki::get_var('last_id') + 0; // the addition is so to avoid having a non-set variable on first run

# Retrieve movie ids (imdb_id) from another scraper
scraperwiki::attach("imdb_all_top_movies");
$titles_list = scraperwiki::select("* from imdb_all_top_movies.swdata where id >= " . $last_run_id);
//$titles_list = scraperwiki::select("* from imdb_all_top_movies.swdata where id >= " . $last_run_id . " limit 1");
//$titles_list = scraperwiki::select("* from imdb_all_top_movies.swdata where id = 1194 limit 1"); // hack

# Set up cURL
$ch = curl_init();
curl_setopt($ch, CURLOPT_USERAGENT, "Lynx/2.8.4dev.7 libwww-FM/2.14");    // just in case
curl_setopt($ch, CURLOPT_FAILONERROR, true);
curl_setopt($ch, CURLOPT_AUTOREFERER, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
//curl_setopt($ch, CURLOPT_TIMEOUT, 10);

### Start the loop!
foreach ( $titles_list as $title ) {

    $imdb_id = $title['imdb_id'];
    
    # Grab data for the Hungarian version
    curl_setopt($ch, CURLOPT_URL, "http://www.imdb.com/title/" . $imdb_id . "/releaseinfo#akas");
    curl_setopt($ch,CURLOPT_HTTPHEADER, array('Accept-Language: hu-hu', 'Cache-Control: no-cache'));
    $page = curl_exec($ch);
    if (!$page) {
        echo "<br />cURL error number:" .curl_errno($ch);
        echo "<br />cURL error:" . curl_error($ch);
        exit;
    }
    $html = str_get_html($page);
    foreach($html->find('meta[property=og:title]') as $element) {
        if ( $element ) {
            $title['HU'] = $element->content;
        } else {
            $title['HU'] = "N/A";
        }
    }
    
    
    # Grab data for the French version
    curl_setopt($ch, CURLOPT_URL, "http://www.imdb.com/title/" . $imdb_id . "/releaseinfo#akas");
    curl_setopt($ch,CURLOPT_HTTPHEADER, array('Accept-Language: fr-fr', 'Cache-Control: no-cache'));
    $page = curl_exec($ch);
    if (!$page) {
        echo "<br />cURL error number:" .curl_errno($ch);
        echo "<br />cURL error:" . curl_error($ch);
        exit;
    }
    $html = str_get_html($page);
    foreach($html->find('meta[property=og:title]') as $element) {
        if ( $element ) {
            $title['FR'] = $element->content;
        } else {
            $title['FR'] = "N/A";
        }
    }
    
    
    # Grab data for the English version -- use imdb.it to prevent cache use
    curl_setopt($ch, CURLOPT_URL, "http://www.imdb.com/title/" . $imdb_id . "/releaseinfo#akas");
    curl_setopt($ch,CURLOPT_HTTPHEADER, array('Accept-Language: en-en', 'Cache-Control: no-cache'));
    $page = curl_exec($ch);
    if (!$page) {
        echo "<br />cURL error number:" .curl_errno($ch);
        echo "<br />cURL error:" . curl_error($ch);
        exit;
    }
    $html = str_get_html($page);
    foreach($html->find('meta[property=og:title]') as $element) {
        if ( $element ) {
            $title['EN'] = $element->content;
        } else {
            $title['EN'] = "N/A";
        }
    }
    
    
    # Grab data for the Spanish version -- use imdb.it to prevent cache use
    curl_setopt($ch, CURLOPT_URL, "http://www.imdb.com/title/" . $imdb_id . "/releaseinfo#akas");
    curl_setopt($ch,CURLOPT_HTTPHEADER, array('Accept-Language: es-es', 'Cache-Control: no-cache'));
    $page = curl_exec($ch);
    if (!$page) {
        echo "<br />cURL error number:" .curl_errno($ch);
        echo "<br />cURL error:" . curl_error($ch);
        exit;
    }
    $html = str_get_html($page);
    foreach($html->find('meta[property=og:title]') as $element) {
        if ( $element ) {
            $title['ES'] = $element->content;
        } else {
            $title['ES'] = "N/A";
        }
    }
    
    
    # Grab data for the Russian version
    curl_setopt($ch, CURLOPT_URL, "http://www.imdb.com/title/" . $imdb_id . "/releaseinfo#akas");
    curl_setopt($ch,CURLOPT_HTTPHEADER, array('Accept-Language: ru-ru', 'Cache-Control: no-cache'));
    $page = curl_exec($ch);
    if (!$page) {
        echo "<br />cURL error number:" .curl_errno($ch);
        echo "<br />cURL error:" . curl_error($ch);
        exit;
    }
    $html = str_get_html($page);
    foreach($html->find('meta[property=og:title]') as $element) {
        if ( $element ) {
            $title['RU'] = $element->content;
        } else {
            $title['RU'] = "N/A";
        }
    }

    // save the year
    preg_match( "/ \(([0-9]{4})\) - Release dates/", $title['EN'], $matches);
    $year = $matches[1]; // $variable[1] holds the first backreference
    
    
    # Clean up the data
    
    // Get rid of trailing release dates info. Seeing as we use preg_replace on an array, the function is actually applied t each entry in the array
    $title = preg_replace( "/ \([0-9]{4}\) - Release dates/", "", $title);
    
    // Change the encoding (from HTML hexadecimal entities to UTF8)
    foreach ( $title as &$movie ) { // mind the access by reference, else we be working on a copy of the array item
        //$movie = html_entity_decode ( $movie, NULL, 'UTF-8' );
        $movie = html_entity_decode ( $movie, ENT_QUOTES, 'UTF-8' ); // decode single and double quotes too
    }
    
    
    # Here are the results!
    $title['year'] = $year;
    scraperwiki::save_sqlite( array("imdb_id"), $title);
    print_r( $title );
    // NEXT = run the job again to scrap the date

// save metadata
echo $title['id'] . "\n";
scraperwiki::save_var('last_id', $title['id']); 
}
### end of the loop

?>