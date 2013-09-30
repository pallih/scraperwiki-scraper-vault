<?php
/**
 * Scraper for use on meine-demokratie.de, a german democracy participation webplatform
 * 
 * Output format of data is relatively targeted to meine-demokratie use, if you want to
 * use this scraper for other purposes, please consider copying the source code in a new
 * scraper and tailor it there for your purposes. Thanks!
 */

require_once 'scraperwiki/simple_html_dom.php';


// main url (take ajax url from the beginning)
$main_url = 'http://bewegung.taz.de/termine?&list_type=tiny&order=starts_at&page=';

define("STOP_STR", '<h2>Termine...</h2>');
define("NUM_PAGES", 1);

$url_base_str = 'http://bewegung.taz.de';
$url_start_str = '<div class="item-title"><a href="';
$url_end_str = '"';

$title_start_str = '<div class="fancy-header"><h1>';
$title_end_str = '</h1>';

$desc_start_str = '</h2>';
$desc_end_str = '<a href="';

$date_start_str = '<h4>Zeitraum:</h4>';
$date_end_str = '</div>';

$adress_start_str = '<h4>Adresse:</h4>';
$adress_end_str = '</div';



/**
 * Removes white spaces, tabs, ... from html to simplify scraping
 */
function prepareHtml($html) {
 
    // Replace white spaces at beginning and end of each row
    $html_array = preg_split("(\r\n|\n|\r)", $html);
    foreach($html_array as &$elem) {
            $elem = trim($elem);
    }
    $html = implode("", $html_array);
        
    // Replace line feeds and tabs
    $html = ereg_replace("(\r\n|\n|\r|\t)", "", $html);  
    return $html;
}


/* 
 * Extracts a string between $start_str and $end_str
 * Important: pass $html as reference to shorten it, otherwise endless loop is created
 */
function extractString($start_str, $end_str, $html) {
        
    $res = '';
    $pos_start_str = strpos($html, $start_str);
    
    // Check for stop str
    if(STOP_STR != '') {
        $pos_stop_str = strpos($html, STOP_STR);
        if($pos_stop_str > 0 && $pos_stop_str < $pos_start_str) {
            return $res;
        }
    }    
        
    if($pos_start_str >= 0  && @substr_count($html, $start_str) > 0 && @substr_count($html, $end_str) > 0) {
        $html = substr($html, $pos_start_str + strlen($start_str));
        $pos_end_str = strpos($html, $end_str);
        $res = substr($html, 0, $pos_end_str);        
        $html = substr($html, $pos_end_str + strlen($end_str));
    }

    return $res;             
}


// iterate through pages
for($page=1;$page<=NUM_PAGES;$page++) {
    
    // Read page url
    $html = scraperwiki::scrape($main_url.$page);  
    $html = prepareHtml($html);   
    
    // iterate through items (as long as first string to extract exists)
    do {
    
        // Read out data
        $url_str = extractString($url_start_str, $url_end_str, &$html);
        
        // Read rest of the stuff from detail page
        $html_detail_page = scraperwiki::scrape($url_base_str.$url_str);
        $html_detail_page = prepareHtml($html_detail_page); 
        
        $title_str = extractString($title_start_str, $title_end_str, &$html_detail_page);
        $desc_str = html_entity_decode(extractString($desc_start_str, $desc_end_str, &$html_detail_page));
        
        $date_str = extractString($date_start_str, $date_end_str, &$html_detail_page);
        
        $adress_str = extractString($adress_start_str, $adress_end_str, &$html_detail_page);
        $adress_str = str_replace('<br />', ', ', $adress_str);
    
        // Save new item
        if($url_str) {
            scraperwiki::save(
                array(
                    'guid'
                ),
                array(
                    'title' => $title_str,
                    'guid' => $url_base_str.$url_str,
                    'md:address' => $adress_str,
                    'md:zuordnung' => 'Strasse',
                    'md:start_date' => $date_str,
                    'md:author' => 'bewegung.taz.de',
                    'content' => utf8_encode($desc_str)
                )
            );
        }
    } while($url_str != '');

}
?>
<?php
/**
 * Scraper for use on meine-demokratie.de, a german democracy participation webplatform
 * 
 * Output format of data is relatively targeted to meine-demokratie use, if you want to
 * use this scraper for other purposes, please consider copying the source code in a new
 * scraper and tailor it there for your purposes. Thanks!
 */

require_once 'scraperwiki/simple_html_dom.php';


// main url (take ajax url from the beginning)
$main_url = 'http://bewegung.taz.de/termine?&list_type=tiny&order=starts_at&page=';

define("STOP_STR", '<h2>Termine...</h2>');
define("NUM_PAGES", 1);

$url_base_str = 'http://bewegung.taz.de';
$url_start_str = '<div class="item-title"><a href="';
$url_end_str = '"';

$title_start_str = '<div class="fancy-header"><h1>';
$title_end_str = '</h1>';

$desc_start_str = '</h2>';
$desc_end_str = '<a href="';

$date_start_str = '<h4>Zeitraum:</h4>';
$date_end_str = '</div>';

$adress_start_str = '<h4>Adresse:</h4>';
$adress_end_str = '</div';



/**
 * Removes white spaces, tabs, ... from html to simplify scraping
 */
function prepareHtml($html) {
 
    // Replace white spaces at beginning and end of each row
    $html_array = preg_split("(\r\n|\n|\r)", $html);
    foreach($html_array as &$elem) {
            $elem = trim($elem);
    }
    $html = implode("", $html_array);
        
    // Replace line feeds and tabs
    $html = ereg_replace("(\r\n|\n|\r|\t)", "", $html);  
    return $html;
}


/* 
 * Extracts a string between $start_str and $end_str
 * Important: pass $html as reference to shorten it, otherwise endless loop is created
 */
function extractString($start_str, $end_str, $html) {
        
    $res = '';
    $pos_start_str = strpos($html, $start_str);
    
    // Check for stop str
    if(STOP_STR != '') {
        $pos_stop_str = strpos($html, STOP_STR);
        if($pos_stop_str > 0 && $pos_stop_str < $pos_start_str) {
            return $res;
        }
    }    
        
    if($pos_start_str >= 0  && @substr_count($html, $start_str) > 0 && @substr_count($html, $end_str) > 0) {
        $html = substr($html, $pos_start_str + strlen($start_str));
        $pos_end_str = strpos($html, $end_str);
        $res = substr($html, 0, $pos_end_str);        
        $html = substr($html, $pos_end_str + strlen($end_str));
    }

    return $res;             
}


// iterate through pages
for($page=1;$page<=NUM_PAGES;$page++) {
    
    // Read page url
    $html = scraperwiki::scrape($main_url.$page);  
    $html = prepareHtml($html);   
    
    // iterate through items (as long as first string to extract exists)
    do {
    
        // Read out data
        $url_str = extractString($url_start_str, $url_end_str, &$html);
        
        // Read rest of the stuff from detail page
        $html_detail_page = scraperwiki::scrape($url_base_str.$url_str);
        $html_detail_page = prepareHtml($html_detail_page); 
        
        $title_str = extractString($title_start_str, $title_end_str, &$html_detail_page);
        $desc_str = html_entity_decode(extractString($desc_start_str, $desc_end_str, &$html_detail_page));
        
        $date_str = extractString($date_start_str, $date_end_str, &$html_detail_page);
        
        $adress_str = extractString($adress_start_str, $adress_end_str, &$html_detail_page);
        $adress_str = str_replace('<br />', ', ', $adress_str);
    
        // Save new item
        if($url_str) {
            scraperwiki::save(
                array(
                    'guid'
                ),
                array(
                    'title' => $title_str,
                    'guid' => $url_base_str.$url_str,
                    'md:address' => $adress_str,
                    'md:zuordnung' => 'Strasse',
                    'md:start_date' => $date_str,
                    'md:author' => 'bewegung.taz.de',
                    'content' => utf8_encode($desc_str)
                )
            );
        }
    } while($url_str != '');

}
?>
