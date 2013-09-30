<?php
/**
 * Scraper for use on meine-demokratie.de, a german democracy participation webplatform
 *
 * Output format of data is relatively targeted to meine-demokratie use, if you want to
 * use this scraper for other purposes, please consider copying the source code in a new
 * scraper and tailor it there for your purposes. Thanks!
 *    
 * Kudos to Holger Drewes (http://scraperwiki.com/profiles/HolgerD/) who provided the major part of this code! THANK YOU!
 */

require_once 'scraperwiki/simple_html_dom.php';

date_default_timezone_set('Europe/Berlin');

// main url (take ajax url from the beginning)
$main_url = 'http://bewegung.taz.de/termine?&list_type=tiny&order=starts_at&page=';

define("STOP_STR", '<h2>Termine...</h2>');
define("NUM_PAGES", 4);

//what types of events are of interest?
//this is not the type of stuff we currently use, just some ideas - see below for what we actually filter out
$aktionen = array("Demo","Öffentlicher Piratenstammtisch","Diskussion","Onlineprotest","Unterschriften-Sammlung");

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

$aktion_start_str = '<h4>Aktionsform:</h4>';
$aktion_end_str = '</div';


function md_scrape2 ($url){
    $curl = curl_init ($url );
    curl_setopt ($curl, CURLOPT_RETURNTRANSFER, true);
    $res  = curl_exec ($curl);
    curl_close ($curl);
    return $res;
}

function md_scrape ($url,$encodeResponseUTF8 = true)
{
   $curl = curl_init ($url ) ;
   curl_setopt ($curl, CURLOPT_RETURNTRANSFER, true) ;
   $res  = curl_exec ($curl) ;
   curl_close ($curl) ;
    if($encodeResponseUTF8){
     return utf8_encode($res);
    }
    else{
     return $res;
    }
}

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
    $html = preg_replace("(\r\n|\n|\r|\t)", "", $html);  
    return $html;
}


/*
 * Extracts a string between $start_str and $end_str
 * Important: pass $html as reference to shorten it, otherwise endless loop is created
 */
function extractString($start_str, $end_str, &$html) {
        
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
    $html = md_scrape($main_url.$page,false); 
    $html = prepareHtml($html);   
    
    // iterate through items (as long as first string to extract exists)
    do {
        sleep(1);
        // Read out data
        $url_str = extractString($url_start_str, $url_end_str, $html);
        //print "scrape " . $url_base_str.$url_str ."\n";
        // Read rest of the stuff from detail page
        //$html_detail_page = scraperwiki::scrape($url_base_str.$url_str);
        $html_detail_page = md_scrape($url_base_str.$url_str,false);
        //print $html_detail_page . "\n";
        $html_detail_page = prepareHtml($html_detail_page);
       
        $title_str = extractString($title_start_str, $title_end_str, $html_detail_page);

        //$desc_str = html_entity_decode(utf8_encode(extractString($desc_start_str, $desc_end_str, $html_detail_page)));
        $desc_str = extractString($desc_start_str, $desc_end_str, $html_detail_page);
        $desc_str = html_entity_decode($desc_str,ENT_QUOTES,'UTF-8');

        $date_str = extractString($date_start_str, $date_end_str, $html_detail_page);
        $date_str = str_replace("Uhr", "", $date_str);
        $dates=explode("-", $date_str);
        //print "DATE: $date_str \n";
        $date_str = strtotime($dates[0]);
        if(count($dates)<=1){
            $exp_date_str =strtotime("+1 day",$date_str);
        }
        else{
            $exp_date_str =strtotime($dates[1],$date_str);        
        }
        //print  strftime("%c",$date_str) . ":::" . strftime("%c",$exp_date_str) . "\n";

        
        $adress_str = extractString($adress_start_str, $adress_end_str, $html_detail_page);
        $adress_str = str_replace('<br />', ', ', $adress_str);

        //filter types of events
        $aktion_str = extractString($aktion_start_str, $aktion_end_str, $html_detail_page);
        //print $aktion_str . "\n";
        if(strpos($aktion_str,"Demo") !== false){
            $cat="Demonstration";
            $zuordnung="Ort";
        }
        else{
            continue;
        }

    
        // Save new item
        if($url_str) {
            scraperwiki::save(
                array(
                    'guid'
                ),
                array(
                    'title' => $title_str,
                    'guid' => $url_base_str.$url_str,
                    'date_scraped' => strftime("%Y-%m-%d %T"),
                    'md:address' => $adress_str,
                    'md:zuordnung' => $zuordnung,
                    'md:start_date' => strftime("%d-%m-%Y %H:%M",$date_str),
                    'md:expiration_date' => strftime("%d-%m-%Y %H:%M",$exp_date_str),
                    'md:author' => 'bewegung.taz.de',
                    'description' => $desc_str,
                    'category' => $cat
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
 *    
 * Kudos to Holger Drewes (http://scraperwiki.com/profiles/HolgerD/) who provided the major part of this code! THANK YOU!
 */

require_once 'scraperwiki/simple_html_dom.php';

date_default_timezone_set('Europe/Berlin');

// main url (take ajax url from the beginning)
$main_url = 'http://bewegung.taz.de/termine?&list_type=tiny&order=starts_at&page=';

define("STOP_STR", '<h2>Termine...</h2>');
define("NUM_PAGES", 4);

//what types of events are of interest?
//this is not the type of stuff we currently use, just some ideas - see below for what we actually filter out
$aktionen = array("Demo","Öffentlicher Piratenstammtisch","Diskussion","Onlineprotest","Unterschriften-Sammlung");

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

$aktion_start_str = '<h4>Aktionsform:</h4>';
$aktion_end_str = '</div';


function md_scrape2 ($url){
    $curl = curl_init ($url );
    curl_setopt ($curl, CURLOPT_RETURNTRANSFER, true);
    $res  = curl_exec ($curl);
    curl_close ($curl);
    return $res;
}

function md_scrape ($url,$encodeResponseUTF8 = true)
{
   $curl = curl_init ($url ) ;
   curl_setopt ($curl, CURLOPT_RETURNTRANSFER, true) ;
   $res  = curl_exec ($curl) ;
   curl_close ($curl) ;
    if($encodeResponseUTF8){
     return utf8_encode($res);
    }
    else{
     return $res;
    }
}

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
    $html = preg_replace("(\r\n|\n|\r|\t)", "", $html);  
    return $html;
}


/*
 * Extracts a string between $start_str and $end_str
 * Important: pass $html as reference to shorten it, otherwise endless loop is created
 */
function extractString($start_str, $end_str, &$html) {
        
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
    $html = md_scrape($main_url.$page,false); 
    $html = prepareHtml($html);   
    
    // iterate through items (as long as first string to extract exists)
    do {
        sleep(1);
        // Read out data
        $url_str = extractString($url_start_str, $url_end_str, $html);
        //print "scrape " . $url_base_str.$url_str ."\n";
        // Read rest of the stuff from detail page
        //$html_detail_page = scraperwiki::scrape($url_base_str.$url_str);
        $html_detail_page = md_scrape($url_base_str.$url_str,false);
        //print $html_detail_page . "\n";
        $html_detail_page = prepareHtml($html_detail_page);
       
        $title_str = extractString($title_start_str, $title_end_str, $html_detail_page);

        //$desc_str = html_entity_decode(utf8_encode(extractString($desc_start_str, $desc_end_str, $html_detail_page)));
        $desc_str = extractString($desc_start_str, $desc_end_str, $html_detail_page);
        $desc_str = html_entity_decode($desc_str,ENT_QUOTES,'UTF-8');

        $date_str = extractString($date_start_str, $date_end_str, $html_detail_page);
        $date_str = str_replace("Uhr", "", $date_str);
        $dates=explode("-", $date_str);
        //print "DATE: $date_str \n";
        $date_str = strtotime($dates[0]);
        if(count($dates)<=1){
            $exp_date_str =strtotime("+1 day",$date_str);
        }
        else{
            $exp_date_str =strtotime($dates[1],$date_str);        
        }
        //print  strftime("%c",$date_str) . ":::" . strftime("%c",$exp_date_str) . "\n";

        
        $adress_str = extractString($adress_start_str, $adress_end_str, $html_detail_page);
        $adress_str = str_replace('<br />', ', ', $adress_str);

        //filter types of events
        $aktion_str = extractString($aktion_start_str, $aktion_end_str, $html_detail_page);
        //print $aktion_str . "\n";
        if(strpos($aktion_str,"Demo") !== false){
            $cat="Demonstration";
            $zuordnung="Ort";
        }
        else{
            continue;
        }

    
        // Save new item
        if($url_str) {
            scraperwiki::save(
                array(
                    'guid'
                ),
                array(
                    'title' => $title_str,
                    'guid' => $url_base_str.$url_str,
                    'date_scraped' => strftime("%Y-%m-%d %T"),
                    'md:address' => $adress_str,
                    'md:zuordnung' => $zuordnung,
                    'md:start_date' => strftime("%d-%m-%Y %H:%M",$date_str),
                    'md:expiration_date' => strftime("%d-%m-%Y %H:%M",$exp_date_str),
                    'md:author' => 'bewegung.taz.de',
                    'description' => $desc_str,
                    'category' => $cat
                )
            );
        }
    } while($url_str != '');

}
?>
