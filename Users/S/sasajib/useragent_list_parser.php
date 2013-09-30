<?php
//required setup
ob_implicit_flush(true);
set_time_limit(0);
ini_set('display_errors', true);
error_reporting(E_ALL);
require_once 'scraperwiki/simple_html_dom.php';

//scraperwiki::sqliteexecute("create table swdata(`userAgent` string)");


//print_r(scraperwiki::show_tables()); exit;



/**
 * UserAgentParser get user agent list from http://www.useragentstring.com/pages/Browserlist/
 * The listed item should be last checked within 2011
 *
 * @author Shakil Ahmed <sasajib@gmail.com>
 */
class UserAgentParser
{

    protected $_i =0;

    protected $_url = 'http://www.useragentstring.com/pages/Browserlist/';

    protected $_userAgentList = array(
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; EmbeddedWB 14.52 from: http://www.bsalsa.com/ EmbeddedWB 14.52; .NET CLR 2.0.50727; Alexa Toolbar; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; WoShiHoney.B; .NET CLR 1.1.4322; .NET CLR 2.0.50727; Toolhelp32Snapshot)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; QQDownload 734; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; XBLWP7; ZuneWP7)',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.70 Safari/537.17',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; MRA 6.0 (build 5993); MRA 8.0 (build 5784); InfoPath.2)',
        'Mozilla/5.0 http://fairshare.cc (X11; U; FreeBSD i386; en-US; rv:1.2a) Gecko/20021021',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.4; .NET CLR 1.1.4322; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows NT 5.1; rv:2.0b8pre) Gecko/20101127 Firefox/4.0b8pre'
    );

    protected $_lastCurlCallInfo;

    protected $_cookiesFile   = 'cookies.txt';

    public function start()
    {
        echo "\t\t\tGetting useragent list page....\n";
        $page = $this->_get_page($this->_url);
        $this->_get_full_page_user_agents($page);
    }



    protected function _check_cookies_file_exists()
    {
        if (!file_exists($this->_cookiesFile)) {
            $this->_create_file($this->_cookiesFile);
        }
    }

    protected function _create_file($fileName, $directory = null)
    {
        if ($directory != null) {
            $fileName = $directory . $fileName;
        }
        try {
            $fileHandler = fopen($fileName, 'a');
        } catch (Exception $error) {
            exit('Unable to create ' . $fileName . 'file. Details: ' . $error->getMessage());
        }
        fclose($fileHandler);
        $this->_destory_variable_or_object($fileHandler);
    }

    protected function _get_full_page_user_agents($page)
    {
       
        $html  = new simple_html_dom();
        $html->load($page);
        $links = $html->find('#liste li a');
        foreach ($links as $link) {
                $theLinks =  'http://www.useragentstring.com'. $link->href;
                echo "\tProcessing an userAgent \n";
                $page = $this->_get_page($theLinks);
                $this->_get_user_agents($page);
                $this->_destory_variable_or_object($page);
        }
        $this->_destory_variable_or_object($links);
        $this->_destory_variable_or_object($html);
        $this->_destory_variable_or_object($page);
    }  

    protected function _get_user_agents($page)
    {
         $html  = new simple_html_dom();
        $html->load($page);
        
        $lastCheckedTemp = $html->find('em');
        
        foreach ($lastCheckedTemp as $value) {
            
            if (preg_match('/Last visit/i', $value->plaintext)) {
                $lastChecked = $value->parent()->next_sibling()->plaintext;
                if ($this->_process_last_checked($lastChecked)) {
                    $userAgentString         = $html->find('textarea#uas_textfeld',
                                                           0)->plaintext;
                    echo "\t\tAdding an useragent\n";
                    //$record = array(
                    //    'userAgentString' => $userAgentString         
                    //);
                    //scraperwiki::save_sqlite(array("useragent"),array('userAgentString'=>$userAgentString));
                   //scraperwiki::save_sqlite(array("userAgent"=>  $userAgentString));
                    //scraperwiki::sqliteexecute("insert into swdata values (:userAgent)", array("userAgent"=>$userAgentString));
                   //scraperwiki::sqlitecommit();
                   //$uniqueKey = $this->_i + 1;
                    scraperwiki::save_sqlite(array("userAgent"), array("userAgent"=>$userAgentString));
                }
            }
        }


        $this->_destory_variable_or_object($html);
        $this->_destory_variable_or_object($page);
    }

    protected function _process_last_checked($lastChecked)
    {
        $splitTime = explode(' ', $lastChecked);
        $splitDate = explode('.', $splitTime[0]);

        if ($splitDate[0] >= 2011) {
            return true;
        }

        return false;
    }

    public function get_user_agent_list()
    {
        return $this->_userAgentLists;
    }
    




    protected function _get_page($url, $customOptions = null)
    {
        $standardOptions = array(
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS      => 5,
            CURLOPT_USERAGENT      => $this->_pick_random_user_agent(),
//            CURLOPT_HEADER         => 0,
            CURLOPT_REFERER        => "google.com",
            CURLOPT_AUTOREFERER    => true,
            CURLOPT_COOKIEFILE     => $this->_cookiesFile,
            CURLOPT_COOKIEJAR      => $this->_cookiesFile,
            CURLOPT_SSL_VERIFYHOST => false,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_CONNECTTIMEOUT => 10,
            CURLOPT_TIMEOUT        => 30,
            CURLOPT_URL            => $url
        );
        $options         = ($customOptions) ? ($standardOptions + $customOptions)
                    : $standardOptions;

        $curlHandler = curl_init();
        curl_setopt_array($curlHandler, $options);

        $excuteCurl              = curl_exec($curlHandler);
        $this->_lastCurlCallInfo = curl_getinfo($curlHandler);

        curl_close($curlHandler);
        $this->_destory_variable_or_object($curlHandler);

        return $excuteCurl;
    }

    public function get_last_curl_call_info()
    {
        return $this->_lastCurlCallInfo;
    }

    protected function _check_proxy_type($proxyType)
    {
        if ($proxyType == null) {
            return CURLPROXY_HTTP;
        }

        return CURLPROXY_SOCKS5;
    }

    protected function _get_page_with_proxy($url, $proxy, $proxyType = null,
                                            $customOptions = null)
    {

        $proxySplited = explode(':',
                                $this->_remove_spaces_without_html_decode($proxy));
        $proxyIp      = $proxySplited[0];
        $proxyPort    = $proxySplited[1];

        $standardOptions = array(
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS      => 5,
            CURLOPT_USERAGENT      => $this->_pick_random_user_agent(),
//            CURLOPT_HEADER         => 0,
            CURLOPT_REFERER        => "google.com",
            CURLOPT_AUTOREFERER    => true,
            CURLOPT_COOKIEFILE     => $this->_cookiesFile,
            CURLOPT_COOKIEJAR      => $this->_cookiesFile,
            CURLOPT_SSL_VERIFYHOST => false,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_CONNECTTIMEOUT => 10,
            CURLOPT_TIMEOUT        => 30,
            CURLOPT_PROXYTYPE      => $this->_check_proxy_type($proxyType), //for http CURLPROXY_HTTP and for socks CURLPROXY_SOCKS5
            CURLOPT_PROXYPORT      => $proxyPort,
            CURLOPT_PROXY          => $proxyIp,
            CURLOPT_URL            => $url,
        );
        $options         = ($customOptions) ? ($standardOptions + $customOptions)
                    : $standardOptions;

        $curlHandler = curl_init();
        curl_setopt_array($curlHandler, $options);

        $excuteCurl              = curl_exec($curlHandler);
        $this->_lastCurlCallInfo = curl_getinfo($curlHandler);

        curl_close($curlHandler);
        $this->_destory_variable_or_object($curlHandler);

        return $excuteCurl;
    }

    protected function _pick_random_user_agent()
    {
        $totalUserAgentList = count($this->_userAgentList) - 1;
        $randomIndex        = rand(0, $totalUserAgentList);
        $this->_destory_variable_or_object($totalUserAgentList);
        return $this->_userAgentList[$randomIndex];
    }

    protected function _simple_html_dom_object($page)
    {
        $j = new simple_html_dom();
        return $j->load($page);
    }

    /**
     * Destroy any variable/object to null and unset those to free memory
     * @param mixed $variableName
     */
    protected function _destory_variable_or_object($variableName)
    {
        $variableName = null;
        unset($variableName);
    }

    /**
     * Remove any comma from a string, it will arrange data properly for csv file
     *
     * Simple find replace from execl ---  to , will revert back to data's orginal form
     * @param string $theString
     * @return string
     */
    protected function _comma_remover($theString)
    {

        return html_entity_decode(preg_replace('/,/', '---', $theString),
                                               ENT_COMPAT, 'UTF-8');
    }

    protected function _remove_spaces($theString)
    {
        $centerTrim = preg_replace("/\\s+/", " ", $theString);
        $trimed     = trim($centerTrim, " ");
        return html_entity_decode($trimed);
    }

    protected function _remove_spaces_without_html_decode($theString)
    {
        $centerTrim = preg_replace("/\\s+/", " ", $theString);
        return trim($centerTrim, " ");
    }

} 
$userAgent = new UserAgentParser();
$userAgent->start();
?>



<?php
//required setup
ob_implicit_flush(true);
set_time_limit(0);
ini_set('display_errors', true);
error_reporting(E_ALL);
require_once 'scraperwiki/simple_html_dom.php';

//scraperwiki::sqliteexecute("create table swdata(`userAgent` string)");


//print_r(scraperwiki::show_tables()); exit;



/**
 * UserAgentParser get user agent list from http://www.useragentstring.com/pages/Browserlist/
 * The listed item should be last checked within 2011
 *
 * @author Shakil Ahmed <sasajib@gmail.com>
 */
class UserAgentParser
{

    protected $_i =0;

    protected $_url = 'http://www.useragentstring.com/pages/Browserlist/';

    protected $_userAgentList = array(
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; EmbeddedWB 14.52 from: http://www.bsalsa.com/ EmbeddedWB 14.52; .NET CLR 2.0.50727; Alexa Toolbar; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; WoShiHoney.B; .NET CLR 1.1.4322; .NET CLR 2.0.50727; Toolhelp32Snapshot)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; QQDownload 734; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; XBLWP7; ZuneWP7)',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.70 Safari/537.17',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; MRA 6.0 (build 5993); MRA 8.0 (build 5784); InfoPath.2)',
        'Mozilla/5.0 http://fairshare.cc (X11; U; FreeBSD i386; en-US; rv:1.2a) Gecko/20021021',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.4; .NET CLR 1.1.4322; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows NT 5.1; rv:2.0b8pre) Gecko/20101127 Firefox/4.0b8pre'
    );

    protected $_lastCurlCallInfo;

    protected $_cookiesFile   = 'cookies.txt';

    public function start()
    {
        echo "\t\t\tGetting useragent list page....\n";
        $page = $this->_get_page($this->_url);
        $this->_get_full_page_user_agents($page);
    }



    protected function _check_cookies_file_exists()
    {
        if (!file_exists($this->_cookiesFile)) {
            $this->_create_file($this->_cookiesFile);
        }
    }

    protected function _create_file($fileName, $directory = null)
    {
        if ($directory != null) {
            $fileName = $directory . $fileName;
        }
        try {
            $fileHandler = fopen($fileName, 'a');
        } catch (Exception $error) {
            exit('Unable to create ' . $fileName . 'file. Details: ' . $error->getMessage());
        }
        fclose($fileHandler);
        $this->_destory_variable_or_object($fileHandler);
    }

    protected function _get_full_page_user_agents($page)
    {
       
        $html  = new simple_html_dom();
        $html->load($page);
        $links = $html->find('#liste li a');
        foreach ($links as $link) {
                $theLinks =  'http://www.useragentstring.com'. $link->href;
                echo "\tProcessing an userAgent \n";
                $page = $this->_get_page($theLinks);
                $this->_get_user_agents($page);
                $this->_destory_variable_or_object($page);
        }
        $this->_destory_variable_or_object($links);
        $this->_destory_variable_or_object($html);
        $this->_destory_variable_or_object($page);
    }  

    protected function _get_user_agents($page)
    {
         $html  = new simple_html_dom();
        $html->load($page);
        
        $lastCheckedTemp = $html->find('em');
        
        foreach ($lastCheckedTemp as $value) {
            
            if (preg_match('/Last visit/i', $value->plaintext)) {
                $lastChecked = $value->parent()->next_sibling()->plaintext;
                if ($this->_process_last_checked($lastChecked)) {
                    $userAgentString         = $html->find('textarea#uas_textfeld',
                                                           0)->plaintext;
                    echo "\t\tAdding an useragent\n";
                    //$record = array(
                    //    'userAgentString' => $userAgentString         
                    //);
                    //scraperwiki::save_sqlite(array("useragent"),array('userAgentString'=>$userAgentString));
                   //scraperwiki::save_sqlite(array("userAgent"=>  $userAgentString));
                    //scraperwiki::sqliteexecute("insert into swdata values (:userAgent)", array("userAgent"=>$userAgentString));
                   //scraperwiki::sqlitecommit();
                   //$uniqueKey = $this->_i + 1;
                    scraperwiki::save_sqlite(array("userAgent"), array("userAgent"=>$userAgentString));
                }
            }
        }


        $this->_destory_variable_or_object($html);
        $this->_destory_variable_or_object($page);
    }

    protected function _process_last_checked($lastChecked)
    {
        $splitTime = explode(' ', $lastChecked);
        $splitDate = explode('.', $splitTime[0]);

        if ($splitDate[0] >= 2011) {
            return true;
        }

        return false;
    }

    public function get_user_agent_list()
    {
        return $this->_userAgentLists;
    }
    




    protected function _get_page($url, $customOptions = null)
    {
        $standardOptions = array(
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS      => 5,
            CURLOPT_USERAGENT      => $this->_pick_random_user_agent(),
//            CURLOPT_HEADER         => 0,
            CURLOPT_REFERER        => "google.com",
            CURLOPT_AUTOREFERER    => true,
            CURLOPT_COOKIEFILE     => $this->_cookiesFile,
            CURLOPT_COOKIEJAR      => $this->_cookiesFile,
            CURLOPT_SSL_VERIFYHOST => false,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_CONNECTTIMEOUT => 10,
            CURLOPT_TIMEOUT        => 30,
            CURLOPT_URL            => $url
        );
        $options         = ($customOptions) ? ($standardOptions + $customOptions)
                    : $standardOptions;

        $curlHandler = curl_init();
        curl_setopt_array($curlHandler, $options);

        $excuteCurl              = curl_exec($curlHandler);
        $this->_lastCurlCallInfo = curl_getinfo($curlHandler);

        curl_close($curlHandler);
        $this->_destory_variable_or_object($curlHandler);

        return $excuteCurl;
    }

    public function get_last_curl_call_info()
    {
        return $this->_lastCurlCallInfo;
    }

    protected function _check_proxy_type($proxyType)
    {
        if ($proxyType == null) {
            return CURLPROXY_HTTP;
        }

        return CURLPROXY_SOCKS5;
    }

    protected function _get_page_with_proxy($url, $proxy, $proxyType = null,
                                            $customOptions = null)
    {

        $proxySplited = explode(':',
                                $this->_remove_spaces_without_html_decode($proxy));
        $proxyIp      = $proxySplited[0];
        $proxyPort    = $proxySplited[1];

        $standardOptions = array(
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS      => 5,
            CURLOPT_USERAGENT      => $this->_pick_random_user_agent(),
//            CURLOPT_HEADER         => 0,
            CURLOPT_REFERER        => "google.com",
            CURLOPT_AUTOREFERER    => true,
            CURLOPT_COOKIEFILE     => $this->_cookiesFile,
            CURLOPT_COOKIEJAR      => $this->_cookiesFile,
            CURLOPT_SSL_VERIFYHOST => false,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_CONNECTTIMEOUT => 10,
            CURLOPT_TIMEOUT        => 30,
            CURLOPT_PROXYTYPE      => $this->_check_proxy_type($proxyType), //for http CURLPROXY_HTTP and for socks CURLPROXY_SOCKS5
            CURLOPT_PROXYPORT      => $proxyPort,
            CURLOPT_PROXY          => $proxyIp,
            CURLOPT_URL            => $url,
        );
        $options         = ($customOptions) ? ($standardOptions + $customOptions)
                    : $standardOptions;

        $curlHandler = curl_init();
        curl_setopt_array($curlHandler, $options);

        $excuteCurl              = curl_exec($curlHandler);
        $this->_lastCurlCallInfo = curl_getinfo($curlHandler);

        curl_close($curlHandler);
        $this->_destory_variable_or_object($curlHandler);

        return $excuteCurl;
    }

    protected function _pick_random_user_agent()
    {
        $totalUserAgentList = count($this->_userAgentList) - 1;
        $randomIndex        = rand(0, $totalUserAgentList);
        $this->_destory_variable_or_object($totalUserAgentList);
        return $this->_userAgentList[$randomIndex];
    }

    protected function _simple_html_dom_object($page)
    {
        $j = new simple_html_dom();
        return $j->load($page);
    }

    /**
     * Destroy any variable/object to null and unset those to free memory
     * @param mixed $variableName
     */
    protected function _destory_variable_or_object($variableName)
    {
        $variableName = null;
        unset($variableName);
    }

    /**
     * Remove any comma from a string, it will arrange data properly for csv file
     *
     * Simple find replace from execl ---  to , will revert back to data's orginal form
     * @param string $theString
     * @return string
     */
    protected function _comma_remover($theString)
    {

        return html_entity_decode(preg_replace('/,/', '---', $theString),
                                               ENT_COMPAT, 'UTF-8');
    }

    protected function _remove_spaces($theString)
    {
        $centerTrim = preg_replace("/\\s+/", " ", $theString);
        $trimed     = trim($centerTrim, " ");
        return html_entity_decode($trimed);
    }

    protected function _remove_spaces_without_html_decode($theString)
    {
        $centerTrim = preg_replace("/\\s+/", " ", $theString);
        return trim($centerTrim, " ");
    }

} 
$userAgent = new UserAgentParser();
$userAgent->start();
?>



