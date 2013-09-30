<?php /* FWIW: ScraperWiki is running PHP v5.3.5 */

require_once 'scraperwiki/simple_html_dom.php';

function _hash($content)
{
    $input_encoding = mb_detect_encoding($content);
    if ($input_encoding) $content = mb_convert_encoding($content, $input_encoding);
    
    return hash("sha256", utf8_encode($content));
}

/**
* GaspHelper
*/
class GaspHelper
{
    
    function __construct($sunlight_key, $bioguide_id)
    {
        $this->sunlight_key = $sunlight_key;
        $this->bioguide_id = $bioguide_id;
        
        $this->updates = array();
    }
    
    public function add_biography($content, $kwargs=null)
    {
        $kwargs_type = gettype($kwargs);
        if ($kwargs_type !== "array" && $kwargs_type !== "object") $kwargs = "";
        $data = array(
            'content' => $content,
            'content_hash' => _hash($content),
            'extra' => json_encode($kwargs)
        );
        
        print_r($data);
        scraperwiki::save_sqlite( array('content_hash'), $data );
    }
}

/**
 * Scraping code below.
 */

$URL_BASE = "http://www.landrieu.senate.gov/";

$bio_path = 'about/biography.cfm';
$bio_div_id = 'cs_control_1919';

$press_releases_path = 'mediacenter/pressreleases/';
$press_releases_list_class = 'pressrelease';

$gasp = new GaspHelper("YOUR_SUNLIGHT_KEY", "L000550");

$theurl = $URL_BASE . $bio_path;

function scrape($url)
   {
      $curl = curl_init($url);
      curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
      curl_setopt($curl, CURLOPT_MAXREDIRS, 10);
      curl_setopt($curl, CURLINFO_HEADER_OUT, true);
      // disable SSL checking to match behaviour in Python/Ruby.
      // ideally would be fixed by configuring curl to use a proper 
      // reverse SSL proxy, and making our http proxy support that.
      curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
      $res = curl_exec($curl);
      $info = curl_getinfo($curl, CURLINFO_HEADER_OUT);
      print $info;
      curl_close($curl);
      return $res;
   }

//$html = scrape($URL_BASE . $bio_path);

$curl = curl_init($URL_BASE . $bio_path);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($curl, CURLOPT_MAXREDIRS, 10);
curl_setopt($curl, CURLINFO_HEADER_OUT, true);
//curl_setopt($curl, CURLOPT_TIMEOUT, 20);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
print "Retrieving...\n";
$res = curl_exec($curl);
print curl_getinfo($curl, CURLINFO_EFFECTIVE_URL) . "\n";
print curl_getinfo($curl, CURLINFO_HTTP_CODE) . "\n";
print curl_getinfo($curl, CURLINFO_HEADER_OUT) . "\n";
curl_close($curl);

$html = $res;
print "\n" . $html . "\n";

//$html = scraperwiki::scrape($URL_BASE . $bio_path);

$dom = new simple_html_dom();
$dom->load($html);

$bio_div = $dom->find('div[id='. $bio_div_id .']');

print_r($bio_div);

$bio_txt = $bio_div[0]->plaintext;

print "Bio text:\n" . $bio_txt . "\n";

// print_r($bio_txt) . "\n\n";

//$gasp->add_biography($bio_txt);
?><?php /* FWIW: ScraperWiki is running PHP v5.3.5 */

require_once 'scraperwiki/simple_html_dom.php';

function _hash($content)
{
    $input_encoding = mb_detect_encoding($content);
    if ($input_encoding) $content = mb_convert_encoding($content, $input_encoding);
    
    return hash("sha256", utf8_encode($content));
}

/**
* GaspHelper
*/
class GaspHelper
{
    
    function __construct($sunlight_key, $bioguide_id)
    {
        $this->sunlight_key = $sunlight_key;
        $this->bioguide_id = $bioguide_id;
        
        $this->updates = array();
    }
    
    public function add_biography($content, $kwargs=null)
    {
        $kwargs_type = gettype($kwargs);
        if ($kwargs_type !== "array" && $kwargs_type !== "object") $kwargs = "";
        $data = array(
            'content' => $content,
            'content_hash' => _hash($content),
            'extra' => json_encode($kwargs)
        );
        
        print_r($data);
        scraperwiki::save_sqlite( array('content_hash'), $data );
    }
}

/**
 * Scraping code below.
 */

$URL_BASE = "http://www.landrieu.senate.gov/";

$bio_path = 'about/biography.cfm';
$bio_div_id = 'cs_control_1919';

$press_releases_path = 'mediacenter/pressreleases/';
$press_releases_list_class = 'pressrelease';

$gasp = new GaspHelper("YOUR_SUNLIGHT_KEY", "L000550");

$theurl = $URL_BASE . $bio_path;

function scrape($url)
   {
      $curl = curl_init($url);
      curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
      curl_setopt($curl, CURLOPT_MAXREDIRS, 10);
      curl_setopt($curl, CURLINFO_HEADER_OUT, true);
      // disable SSL checking to match behaviour in Python/Ruby.
      // ideally would be fixed by configuring curl to use a proper 
      // reverse SSL proxy, and making our http proxy support that.
      curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
      $res = curl_exec($curl);
      $info = curl_getinfo($curl, CURLINFO_HEADER_OUT);
      print $info;
      curl_close($curl);
      return $res;
   }

//$html = scrape($URL_BASE . $bio_path);

$curl = curl_init($URL_BASE . $bio_path);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($curl, CURLOPT_MAXREDIRS, 10);
curl_setopt($curl, CURLINFO_HEADER_OUT, true);
//curl_setopt($curl, CURLOPT_TIMEOUT, 20);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
print "Retrieving...\n";
$res = curl_exec($curl);
print curl_getinfo($curl, CURLINFO_EFFECTIVE_URL) . "\n";
print curl_getinfo($curl, CURLINFO_HTTP_CODE) . "\n";
print curl_getinfo($curl, CURLINFO_HEADER_OUT) . "\n";
curl_close($curl);

$html = $res;
print "\n" . $html . "\n";

//$html = scraperwiki::scrape($URL_BASE . $bio_path);

$dom = new simple_html_dom();
$dom->load($html);

$bio_div = $dom->find('div[id='. $bio_div_id .']');

print_r($bio_div);

$bio_txt = $bio_div[0]->plaintext;

print "Bio text:\n" . $bio_txt . "\n";

// print_r($bio_txt) . "\n\n";

//$gasp->add_biography($bio_txt);
?>