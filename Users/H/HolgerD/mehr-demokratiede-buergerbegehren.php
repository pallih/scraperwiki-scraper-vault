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
$main_url  = 'http://wissen.mehr-demokratie.de/datenbank-bb.html?&tx_mddbbbview_pi1[number]=100&tx_mddbbbview_pi1[single]=&tx_mddbbbview_pi1[start]=';

define(STOP_STR, '<div class="full-content-right">');
define(NUM_PAGES, 1); // change to 57 when scraper ready!
define(PAGE_MULTIPLIER, 100);

$url_base_str = 'http://wissen.mehr-demokratie.de/';
$url_start_str = '#d0d0d0; vertical-align: top; padding: 3px;"><a href="';
$url_end_str = '"';

$adress_start_str = 'Ort:</dt><dd>';
$adress_end_str = '</dd>';

$title_start_str = 'rgerbegehrens: </dt><dd>';
$title_end_str = '</dd>';

$desc_start_str = 'Fragestellung: </dt><dd>';
$desc_end_str = '</dd>';

$topic_start_str = 'Themenbereich: </dt><dd>';
$topic_end_str = '</dd>';

$proc_type_start_str = 'Verfahrenstyp: </dt><dd>';
$proc_type_end_str = '</dd>';

$year_start_str = 'Jahr: </dt><dd>';
$year_end_str = '</dd>';

$date_start_str = 'gungsdatum: </dt><dd>';
$date_end_str = '</dd>';

$collection_date_start_str = 'Start der Unterschriftensammlung: </dt><dd>';
$collection_date_end_str = '</dd>';

$submission_date_start_str = 'reichung der Unterschriften: </dt><dd>';
$submission_date_end_str = '</dd>';

$sign_nrs_start_str = 'Unterschriften insgesamt: </dt><dd>';
$sign_nrs_stop_str = '</dd>';

$exp_date_start_str = 'gerentscheids: </dt><dd>';
$exp_date_end_str = '</dd>';

$result_start_str = 'Ergebnis: </dt><dd>';
$result_end_str = '</dd>';

$jastimmen_start_str = 'Ja-Stimmen: </dt><dd>';
$jastimmen_end_str = '</dd>';

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
    $num = $page * PAGE_MULTIPLIER;
    $html = scraperwiki::scrape($main_url.$num);  
    $html = prepareHtml($html);   
    
    // iterate through items (as long as first string to extract exists)
    do {
    
        // Read out data
        $url_str = html_entity_decode(extractString($url_start_str, $url_end_str, &$html));
        
        // Read rest of the stuff from detail page
        $html_detail_page = scraperwiki::scrape($url_base_str.$url_str);
        $html_detail_page = prepareHtml($html_detail_page); 


        $adress_str = extractString($adress_start_str, $adress_end_str, &$html_detail_page);        
        $title_str = extractString($title_start_str, $title_end_str, &$html_detail_page);
        $desc_str = extractString($desc_start_str, $desc_end_str, &$html_detail_page);
        if($desc_str==''){
            $desc_str=$title_str;
        }
        //$topic_str = extractString($topic_start_str, $topic_end_str, &$html_detail_page);        
    
        $proc_type_str = extractString($proc_type_start_str, $proc_type_end_str, &$html_detail_page);
        $proc_type_str = preg_replace('/^\d*\.\s*/','', $proc_type_str);
        $proc_type_str = preg_replace('/^.*\(.*:\)\s/','', $proc_type_str);        

        $year = extractString($year_start_str, $year_end_str, &$html_detail_page);
        $date_str = extractString($date_start_str, $date_end_str, &$html_detail_page);
        $collection_date_str = extractString($collection_date_start_str, $collection_date_end_str, &$html_detail_page);        

        $submission_date_str = extractString($submission_date_start_str, $submission_date_end_str, &$html_detail_page);

        //start date difficult as multiple options possible and often lack of data
        //the following represent a hierarchy of possible entries to use and resorts to the year as start date
        //all to make sure that we have a start date on which basis to calculate the expiry date
        if($date_str == '0000-00-00 00:00:00'){ $date_str= $collection_date_str;}
        if($date_str == '0000-00-00 00:00:00'){ $date_str= $submission_date_str;}                                               
        if($date_str == '0000-00-00 00:00:00'){ $date_str= date('Y-m-d H:i:s', strtotime("$year-07-15 00:00:00"));}                                               
        
        $sign_nrs_str = extractString($sign_nrs_start_str, $sign_nrs_end_str, &$html_detail_page);
        
        if($sign_nrs_str != '') {
            $desc_str .= '\nUnterschriften insgesamt: '.$sign_nrs_str;   
        }
        
        $exp_date_str = extractString($exp_date_start_str, $exp_date_end_str, &$html_detail_page);
        
        /*Datum des Bürgerentscheids (Ist der Entscheid noch
        als offen gekennzeichnet, so wird das expiration_date automatisch auf
        ein Jahr nach dem start_date gelegt - sollte ausreichen und sorgt dafür,
        dass Einträge verschwinden, die nicht ordnungsgemäss aktualisiert sind) 
        */
        if($exp_date_str == '0000-00-00 00:00:00') {
            $exp_date_str = date('Y-m-d H:i:s', strtotime('+1 year', strtotime($date_str)));   
        }
        
        $result_str = extractString($result_start_str, $result_end_str, &$html_detail_page);
        $jastimmen_str = extractString($jastimmen_start_str, $jastimmen_end_str, &$html_detail_page);     
        if($jastimmen_str != '') {
            $desc_str .= '\nJa-Stimmen: '.$jastimmen_str;   
        }
    
        // Save new item
        if($url_str) {
            scraperwiki::save(
                array(
                    'guid'
                ),
                array(
                    'title' => utf8_encode($title_str),
                    'guid' => $url_base_str.$url_str,
                    'md:address' => utf8_encode($adress_str),
                    //'md:zuordnung' => 'Ort',
                    'md:author' => 'mehr-demokratie.de',
                    'md:start_date' => $date_str,
                    'md:expiration_date' => $exp_date_str,
                    'description' => utf8_encode($desc_str),
                    'md:tag1' => 'bb-'.utf8_encode($result_str),
                    'md:tag2' => 'bb-'.utf8_encode($proc_type_str)

                    
                    //'md:tag' => 'bb-'.utf8_encode($result_str),
                    //'md:tag' => 'bb-'.utf8_encode($proc_type_str)
                )
            );
        }
    } while($url_str != '');

}
?><?php
/**
 * Scraper for use on meine-demokratie.de, a german democracy participation webplatform
 * 
 * Output format of data is relatively targeted to meine-demokratie use, if you want to
 * use this scraper for other purposes, please consider copying the source code in a new
 * scraper and tailor it there for your purposes. Thanks!
 */

require_once 'scraperwiki/simple_html_dom.php';


// main url (take ajax url from the beginning)
$main_url  = 'http://wissen.mehr-demokratie.de/datenbank-bb.html?&tx_mddbbbview_pi1[number]=100&tx_mddbbbview_pi1[single]=&tx_mddbbbview_pi1[start]=';

define(STOP_STR, '<div class="full-content-right">');
define(NUM_PAGES, 1); // change to 57 when scraper ready!
define(PAGE_MULTIPLIER, 100);

$url_base_str = 'http://wissen.mehr-demokratie.de/';
$url_start_str = '#d0d0d0; vertical-align: top; padding: 3px;"><a href="';
$url_end_str = '"';

$adress_start_str = 'Ort:</dt><dd>';
$adress_end_str = '</dd>';

$title_start_str = 'rgerbegehrens: </dt><dd>';
$title_end_str = '</dd>';

$desc_start_str = 'Fragestellung: </dt><dd>';
$desc_end_str = '</dd>';

$topic_start_str = 'Themenbereich: </dt><dd>';
$topic_end_str = '</dd>';

$proc_type_start_str = 'Verfahrenstyp: </dt><dd>';
$proc_type_end_str = '</dd>';

$year_start_str = 'Jahr: </dt><dd>';
$year_end_str = '</dd>';

$date_start_str = 'gungsdatum: </dt><dd>';
$date_end_str = '</dd>';

$collection_date_start_str = 'Start der Unterschriftensammlung: </dt><dd>';
$collection_date_end_str = '</dd>';

$submission_date_start_str = 'reichung der Unterschriften: </dt><dd>';
$submission_date_end_str = '</dd>';

$sign_nrs_start_str = 'Unterschriften insgesamt: </dt><dd>';
$sign_nrs_stop_str = '</dd>';

$exp_date_start_str = 'gerentscheids: </dt><dd>';
$exp_date_end_str = '</dd>';

$result_start_str = 'Ergebnis: </dt><dd>';
$result_end_str = '</dd>';

$jastimmen_start_str = 'Ja-Stimmen: </dt><dd>';
$jastimmen_end_str = '</dd>';

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
    $num = $page * PAGE_MULTIPLIER;
    $html = scraperwiki::scrape($main_url.$num);  
    $html = prepareHtml($html);   
    
    // iterate through items (as long as first string to extract exists)
    do {
    
        // Read out data
        $url_str = html_entity_decode(extractString($url_start_str, $url_end_str, &$html));
        
        // Read rest of the stuff from detail page
        $html_detail_page = scraperwiki::scrape($url_base_str.$url_str);
        $html_detail_page = prepareHtml($html_detail_page); 


        $adress_str = extractString($adress_start_str, $adress_end_str, &$html_detail_page);        
        $title_str = extractString($title_start_str, $title_end_str, &$html_detail_page);
        $desc_str = extractString($desc_start_str, $desc_end_str, &$html_detail_page);
        if($desc_str==''){
            $desc_str=$title_str;
        }
        //$topic_str = extractString($topic_start_str, $topic_end_str, &$html_detail_page);        
    
        $proc_type_str = extractString($proc_type_start_str, $proc_type_end_str, &$html_detail_page);
        $proc_type_str = preg_replace('/^\d*\.\s*/','', $proc_type_str);
        $proc_type_str = preg_replace('/^.*\(.*:\)\s/','', $proc_type_str);        

        $year = extractString($year_start_str, $year_end_str, &$html_detail_page);
        $date_str = extractString($date_start_str, $date_end_str, &$html_detail_page);
        $collection_date_str = extractString($collection_date_start_str, $collection_date_end_str, &$html_detail_page);        

        $submission_date_str = extractString($submission_date_start_str, $submission_date_end_str, &$html_detail_page);

        //start date difficult as multiple options possible and often lack of data
        //the following represent a hierarchy of possible entries to use and resorts to the year as start date
        //all to make sure that we have a start date on which basis to calculate the expiry date
        if($date_str == '0000-00-00 00:00:00'){ $date_str= $collection_date_str;}
        if($date_str == '0000-00-00 00:00:00'){ $date_str= $submission_date_str;}                                               
        if($date_str == '0000-00-00 00:00:00'){ $date_str= date('Y-m-d H:i:s', strtotime("$year-07-15 00:00:00"));}                                               
        
        $sign_nrs_str = extractString($sign_nrs_start_str, $sign_nrs_end_str, &$html_detail_page);
        
        if($sign_nrs_str != '') {
            $desc_str .= '\nUnterschriften insgesamt: '.$sign_nrs_str;   
        }
        
        $exp_date_str = extractString($exp_date_start_str, $exp_date_end_str, &$html_detail_page);
        
        /*Datum des Bürgerentscheids (Ist der Entscheid noch
        als offen gekennzeichnet, so wird das expiration_date automatisch auf
        ein Jahr nach dem start_date gelegt - sollte ausreichen und sorgt dafür,
        dass Einträge verschwinden, die nicht ordnungsgemäss aktualisiert sind) 
        */
        if($exp_date_str == '0000-00-00 00:00:00') {
            $exp_date_str = date('Y-m-d H:i:s', strtotime('+1 year', strtotime($date_str)));   
        }
        
        $result_str = extractString($result_start_str, $result_end_str, &$html_detail_page);
        $jastimmen_str = extractString($jastimmen_start_str, $jastimmen_end_str, &$html_detail_page);     
        if($jastimmen_str != '') {
            $desc_str .= '\nJa-Stimmen: '.$jastimmen_str;   
        }
    
        // Save new item
        if($url_str) {
            scraperwiki::save(
                array(
                    'guid'
                ),
                array(
                    'title' => utf8_encode($title_str),
                    'guid' => $url_base_str.$url_str,
                    'md:address' => utf8_encode($adress_str),
                    //'md:zuordnung' => 'Ort',
                    'md:author' => 'mehr-demokratie.de',
                    'md:start_date' => $date_str,
                    'md:expiration_date' => $exp_date_str,
                    'description' => utf8_encode($desc_str),
                    'md:tag1' => 'bb-'.utf8_encode($result_str),
                    'md:tag2' => 'bb-'.utf8_encode($proc_type_str)

                    
                    //'md:tag' => 'bb-'.utf8_encode($result_str),
                    //'md:tag' => 'bb-'.utf8_encode($proc_type_str)
                )
            );
        }
    } while($url_str != '');

}
?>