<?php
// report all errors apart from Notices
ini_set('display_errors',1); 
error_reporting(E_ALL ^ E_NOTICE);
/*
* populateDOM()
* Author Russell Trafford
* Last updated: 18/07/2012 Version 1.10
* @arg src_link : Link to Scrape
* @arg htmlDOM : an instance of simple_html_dom()
* @arg upd_flag : Set TRUE for force-update of local cache which will initiate scraping and update local cache
*/
function populateDOM($htmlDOM, $src_link, $upd_flag = false)
{
    scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS sources (src_link TEXT PRIMARY KEY, timestamp DATETIME, src_dump TEXT)");
    echo "Checking local cache...<br>\n";
    $result = scraperwiki::sqliteexecute("SELECT src_link, timestamp, src_dump FROM sources WHERE src_link = :slnk", array("slnk"=>$src_link));
    if((empty($result->data[0][2])) || ($upd_flag == true))
    {
        echo "No Cache for this site (or force-update flag given), scraping live site for local cache...<br>\n";
        // Load the site and save it locally so that we dont end up crawling their site a million times during development
        $source = scraperWiki::scrape($src_link);           
        $htmlDOM->load($source);
        $save_source = $htmlDOM->save();
        echo "Scrape complete, storing into cache...<br>\n";
    
        scraperwiki::sqliteexecute("INSERT OR REPLACE INTO sources VALUES (:slnk, :stime, :sdmp)", array("slnk"=>$src_link, "stime"=>time(), "sdmp"=>$save_source));
        scraperwiki::sqlitecommit();
        echo "Cache saved.<br>\n";
        echo "Populate DOM Complete.";
        return $htmlDOM;
    }
    else
    {
        echo "Using local cache, as cached data exists from '".date(DATE_RFC822, $result->data[0][1]).".'<br>\n";
        echo "Loading...<br>\n";
        $htmlDOM->load($result->data[0][2]);
        echo "Populate DOM Complete.";
        return $htmlDOM;
    }
}

/*
// Load From File
$html->load_file('result.htm');
$rows = $html->find('form[id=login-form]');
echo "<pre>";
print_r($rows);
echo "</pre>";
*/

require_once("scraperwiki/simple_html_dom.php");
$html = new simple_html_dom();
//$html = populateDOM($html, "http://www.scraperwiki.com");
$html = populateDOM($html, "https://secure.citysocialising.com/user/user_login.html");
$rows = $html->find('form[id=login-form]');

$html->clear(); unset($html);
$htmlDOM->clear(); unset($htmlDOM);

echo "<pre>";
print_r($rows);
echo "</pre>";


$html->clear(); unset($html);
$htmlDOM->clear(); unset($htmlDOM);

?>
<?php
// report all errors apart from Notices
ini_set('display_errors',1); 
error_reporting(E_ALL ^ E_NOTICE);
/*
* populateDOM()
* Author Russell Trafford
* Last updated: 18/07/2012 Version 1.10
* @arg src_link : Link to Scrape
* @arg htmlDOM : an instance of simple_html_dom()
* @arg upd_flag : Set TRUE for force-update of local cache which will initiate scraping and update local cache
*/
function populateDOM($htmlDOM, $src_link, $upd_flag = false)
{
    scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS sources (src_link TEXT PRIMARY KEY, timestamp DATETIME, src_dump TEXT)");
    echo "Checking local cache...<br>\n";
    $result = scraperwiki::sqliteexecute("SELECT src_link, timestamp, src_dump FROM sources WHERE src_link = :slnk", array("slnk"=>$src_link));
    if((empty($result->data[0][2])) || ($upd_flag == true))
    {
        echo "No Cache for this site (or force-update flag given), scraping live site for local cache...<br>\n";
        // Load the site and save it locally so that we dont end up crawling their site a million times during development
        $source = scraperWiki::scrape($src_link);           
        $htmlDOM->load($source);
        $save_source = $htmlDOM->save();
        echo "Scrape complete, storing into cache...<br>\n";
    
        scraperwiki::sqliteexecute("INSERT OR REPLACE INTO sources VALUES (:slnk, :stime, :sdmp)", array("slnk"=>$src_link, "stime"=>time(), "sdmp"=>$save_source));
        scraperwiki::sqlitecommit();
        echo "Cache saved.<br>\n";
        echo "Populate DOM Complete.";
        return $htmlDOM;
    }
    else
    {
        echo "Using local cache, as cached data exists from '".date(DATE_RFC822, $result->data[0][1]).".'<br>\n";
        echo "Loading...<br>\n";
        $htmlDOM->load($result->data[0][2]);
        echo "Populate DOM Complete.";
        return $htmlDOM;
    }
}

/*
// Load From File
$html->load_file('result.htm');
$rows = $html->find('form[id=login-form]');
echo "<pre>";
print_r($rows);
echo "</pre>";
*/

require_once("scraperwiki/simple_html_dom.php");
$html = new simple_html_dom();
//$html = populateDOM($html, "http://www.scraperwiki.com");
$html = populateDOM($html, "https://secure.citysocialising.com/user/user_login.html");
$rows = $html->find('form[id=login-form]');

$html->clear(); unset($html);
$htmlDOM->clear(); unset($htmlDOM);

echo "<pre>";
print_r($rows);
echo "</pre>";


$html->clear(); unset($html);
$htmlDOM->clear(); unset($htmlDOM);

?>
