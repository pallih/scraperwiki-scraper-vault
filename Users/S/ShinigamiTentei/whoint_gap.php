<?php
require 'scraperwiki/simple_html_dom.php';           

global $counter;
$counter = 0;

function removeSpecialChars($text){
    $chars = array("á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú", "ñ", "Ñ");
    $replace = array("a", "e", "i", "o", "u", "A", "E", "I", "O", "U", "n", "N");
    return str_replace($chars , $replace, $text);
}

/**
 * scrapes countrylist.net for country - continent combinations and stores stuff in static list
 */
function getCountryList(){
    static $list = array();

    if(empty($list)){
        $html = scraperWiki::scrape("http://countrylist.net/");
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find("table[@class='Countrylist'] tr") as $data){
            $country = $data->find("td[@class='Country']");
            $continent= $data->find("td[@class='Continent']");

            if(count($country) == 1 && count($continent) == 1){
                $country = removeSpecialChars(strtolower(trim($country[0]->plaintext)));
                $list[$country] = removeSpecialChars(strtolower(trim($continent[0]->plaintext)));
            }
        }
    }

    return $list;
}

/**
 * tries to fetch location information out of text in html
 */
function getLocation($href){
    global $counter;

    $unknown = array(
        'country' => 'unknown',
        'continent' => 'unknown'
    );

    if(!$href || $href == ""){
        return $unknown;
    }

    // check store for known
    $store = getData("* FROM swdata where link LIKE '$href'");

    if($store && count(array_diff_assoc($store, $unknown))){
        return array(
            'country' => $store[0]['country'],
            'continent' => $store[0]['continent']
        );
    }
    $counter++;

    $list = getCountryList();   
    $html = scraperWiki::scrape("http://www.who.int/$href");
    $dom = new simple_html_dom();
    $dom->load($html);

    // seek location in text
    foreach($dom->find("div[@id='primary']") as $data){
        $text = removeSpecialChars(strtolower($data->plaintext));

        // tries to find a country name in the text
        foreach($list as $key => $value){ 
            // stripos = case insensitive strpos
            if(stripos($text, $key) !== false){
                return array(
                    'country' => $key,
                    'continent' => $value
                );                
            }
        }
    }

    // seek location in link
    foreach($dom->find("div[@id='primary'] a") as $data){
        $result = getLocation($data->href);
        if(count(array_diff_assoc($result, $unknown))){
            return $result;
        }
    }

    return $unknown;
}

function fetchGARArchive($href, $disease){
    if(!$href || $href == ""){
        return;
    }

    if(!$disease || $disease == ""){
        $disease = "unknown";
    }

    $html = scraperWiki::scrape("http://www.who.int/$href");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("ul[@class='auto_archive'] li") as $data){
        $link = $data->find("a");
        $summary = $data->find("span");
    
        if(count($link) == 1 && count($summary) == 1){
            // skip known entries
            /*if(count(getData("link FROM swdata where link LIKE '".$link[0]->href."'"))){
                continue;
            }*/

            $location = getLocation($link[0]->href);
            $record = array(
                'date' => $link[0]->plaintext,
                'link' => $link[0]->href,
                'summary' => $summary[0]->plaintext,
                'country' => $location['country'],
                'continent' => $location['continent'],
                'disease' => $disease
            );        
            scraperwiki::save(array('link'), $record);
        }
    }
}

function getData($query){
    if(!count(scraperwiki::table_info("swdata"))){
        return false;
    }

    return scraperWiki::select($query);
}

if(!count(scraperwiki::table_info("swvariables"))){
    // if no stored variables are available, start from beginning
    $start = '';
} else {
    // else, load last disease from database
    $start = scraperWiki::get_var('disease', '');
}

$html = scraperWiki::scrape("http://www.who.int/csr/don/archive/disease/en/index.html");
$dom = new simple_html_dom();
$dom->load($html);

$handleNextEntry = false;
// no previous entries -> start from beginning
if($start == ''){
    $handleNextEntry = true;
} else {
    print "starting after: $start\n\n";
}

foreach($dom->find("ul[@class='a_z'] li a") as $data){
    $disease = trim($data->plaintext);
    print "fetching data for disease: $disease";

    if($handleNextEntry){
        print "\n";

        // saves entries themselves
        fetchGARArchive($data->href, $disease);
        // saves last scraped disease
        scraperWiki::save_var('disease', $disease);

        if($counter >= 600){
            exit;
        }        
    } else {
        print " - skipped\n";
        if($disease == $start){
            $handleNextEntry = true;
        }
    }
}
scraperWiki::save_var('disease', '');

?>
<?php
require 'scraperwiki/simple_html_dom.php';           

global $counter;
$counter = 0;

function removeSpecialChars($text){
    $chars = array("á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú", "ñ", "Ñ");
    $replace = array("a", "e", "i", "o", "u", "A", "E", "I", "O", "U", "n", "N");
    return str_replace($chars , $replace, $text);
}

/**
 * scrapes countrylist.net for country - continent combinations and stores stuff in static list
 */
function getCountryList(){
    static $list = array();

    if(empty($list)){
        $html = scraperWiki::scrape("http://countrylist.net/");
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find("table[@class='Countrylist'] tr") as $data){
            $country = $data->find("td[@class='Country']");
            $continent= $data->find("td[@class='Continent']");

            if(count($country) == 1 && count($continent) == 1){
                $country = removeSpecialChars(strtolower(trim($country[0]->plaintext)));
                $list[$country] = removeSpecialChars(strtolower(trim($continent[0]->plaintext)));
            }
        }
    }

    return $list;
}

/**
 * tries to fetch location information out of text in html
 */
function getLocation($href){
    global $counter;

    $unknown = array(
        'country' => 'unknown',
        'continent' => 'unknown'
    );

    if(!$href || $href == ""){
        return $unknown;
    }

    // check store for known
    $store = getData("* FROM swdata where link LIKE '$href'");

    if($store && count(array_diff_assoc($store, $unknown))){
        return array(
            'country' => $store[0]['country'],
            'continent' => $store[0]['continent']
        );
    }
    $counter++;

    $list = getCountryList();   
    $html = scraperWiki::scrape("http://www.who.int/$href");
    $dom = new simple_html_dom();
    $dom->load($html);

    // seek location in text
    foreach($dom->find("div[@id='primary']") as $data){
        $text = removeSpecialChars(strtolower($data->plaintext));

        // tries to find a country name in the text
        foreach($list as $key => $value){ 
            // stripos = case insensitive strpos
            if(stripos($text, $key) !== false){
                return array(
                    'country' => $key,
                    'continent' => $value
                );                
            }
        }
    }

    // seek location in link
    foreach($dom->find("div[@id='primary'] a") as $data){
        $result = getLocation($data->href);
        if(count(array_diff_assoc($result, $unknown))){
            return $result;
        }
    }

    return $unknown;
}

function fetchGARArchive($href, $disease){
    if(!$href || $href == ""){
        return;
    }

    if(!$disease || $disease == ""){
        $disease = "unknown";
    }

    $html = scraperWiki::scrape("http://www.who.int/$href");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("ul[@class='auto_archive'] li") as $data){
        $link = $data->find("a");
        $summary = $data->find("span");
    
        if(count($link) == 1 && count($summary) == 1){
            // skip known entries
            /*if(count(getData("link FROM swdata where link LIKE '".$link[0]->href."'"))){
                continue;
            }*/

            $location = getLocation($link[0]->href);
            $record = array(
                'date' => $link[0]->plaintext,
                'link' => $link[0]->href,
                'summary' => $summary[0]->plaintext,
                'country' => $location['country'],
                'continent' => $location['continent'],
                'disease' => $disease
            );        
            scraperwiki::save(array('link'), $record);
        }
    }
}

function getData($query){
    if(!count(scraperwiki::table_info("swdata"))){
        return false;
    }

    return scraperWiki::select($query);
}

if(!count(scraperwiki::table_info("swvariables"))){
    // if no stored variables are available, start from beginning
    $start = '';
} else {
    // else, load last disease from database
    $start = scraperWiki::get_var('disease', '');
}

$html = scraperWiki::scrape("http://www.who.int/csr/don/archive/disease/en/index.html");
$dom = new simple_html_dom();
$dom->load($html);

$handleNextEntry = false;
// no previous entries -> start from beginning
if($start == ''){
    $handleNextEntry = true;
} else {
    print "starting after: $start\n\n";
}

foreach($dom->find("ul[@class='a_z'] li a") as $data){
    $disease = trim($data->plaintext);
    print "fetching data for disease: $disease";

    if($handleNextEntry){
        print "\n";

        // saves entries themselves
        fetchGARArchive($data->href, $disease);
        // saves last scraped disease
        scraperWiki::save_var('disease', $disease);

        if($counter >= 600){
            exit;
        }        
    } else {
        print " - skipped\n";
        if($disease == $start){
            $handleNextEntry = true;
        }
    }
}
scraperWiki::save_var('disease', '');

?>
