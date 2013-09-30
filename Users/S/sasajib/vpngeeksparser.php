<?php
//required setup
ob_implicit_flush(true);
set_time_limit(0);
ini_set('display_errors', true);
error_reporting(E_ALL);
require_once 'scraperwiki/simple_html_dom.php';


/**
 *
 * @author Shakil Ahmed <sasajib@gmail.com>
 */
class VpnGeeksParser
{

    protected $_i =0;
    
    protected $_usingProxy;

    protected $_url = 'http://www.vpngeeks.com/proxylist.php?from=1';

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

    public function start($proxy = null)
    {
        if(is_null($proxy)){
            $page = $this->_get_page($this->_url);
        }else{
            $this->_usingProxy = $proxy;
            $page = $this->_get_page_with_proxy($this->_url, $proxy);
        }
        echo "\t\t\tGetting proxy lists page....\n";        
        //echo $page;exit;
        $this->_get_proxies_from_page($page);
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

    protected function _get_proxies_from_page($page)
    {
        
        $html  = new simple_html_dom();
        $html->load($page);
        
        $proxyList = array();
        
        $oddList = $html->find('.tr_style1');
        foreach ($oddList as $list) {
            $proxy['ip'] = $list->find('td',0)->plaintext;
            $proxy['port'] = $list->find('td', 1)->plaintext;
            $proxy['type'] = $list->find('td',8)->plaintext;
            $proxy['anonimity'] = $list->find('td', 9)->plaintext;            
            //$mes = scraperwiki::save_sqlite(array('type', "ip",'port','anonimity'), $proxy);
            //echo "Done Parsing proxy\n";
            array_push($proxyList, $proxy);
        }
        
        $evenList = $html->find('.tr_style2');
        foreach ($evenList as $list) {
            $proxy['ip'] = $list->find('td',0)->plaintext;
            $proxy['port'] = $list->find('td', 1)->plaintext;
            $proxy['type'] = $list->find('td',8)->plaintext;
            $proxy['anonimity'] = $list->find('td', 9)->plaintext;            
            //$mes = scraperwiki::save_sqlite(array('type', "ip",'port','anonimity'), $proxy);
            //echo "Done Parsing proxy\n";
            array_push($proxyList, $proxy);
        }
        $mes = scraperwiki::save_sqlite(array('type', "ip",'port','anonimity'), $proxyList);
        $this->_destory_variable_or_object($html);
        $this->_check_pagination($page);
        
        
    }  
    
    protected function _check_pagination($page)
    {
        //next
        $html  = new simple_html_dom();
        $html->load($page);
        
        $this->_destory_variable_or_object($page);
        
        $nextPageExists = count($html->find('.next'));
        if($nextPageExists > 0){
            $url = 'http://www.vpngeeks.com/'.$html->find('.next',0)->parent()->href;
            $this->_url = preg_replace('/&#pagination/i', '', $url);
            $this->_destory_variable_or_object($html);
            $this->start($this->_usingProxy);
        }
        
        $this->_destory_variable_or_object($html);
        echo 'All parsing done!!!';
        
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
            //CURLOPT_REFERER        => "google.com",
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
            //CURLOPT_REFERER        => "google.com",
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

//This site already blocked scrapper wikis ip. So please use your own proxy...to parse the page...

$j = new VpnGeeksParser();
$proxy = '62.173.37.204:8080';
$j->start($proxy);

?><?php
//required setup
ob_implicit_flush(true);
set_time_limit(0);
ini_set('display_errors', true);
error_reporting(E_ALL);
require_once 'scraperwiki/simple_html_dom.php';


/**
 *
 * @author Shakil Ahmed <sasajib@gmail.com>
 */
class VpnGeeksParser
{

    protected $_i =0;
    
    protected $_usingProxy;

    protected $_url = 'http://www.vpngeeks.com/proxylist.php?from=1';

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

    public function start($proxy = null)
    {
        if(is_null($proxy)){
            $page = $this->_get_page($this->_url);
        }else{
            $this->_usingProxy = $proxy;
            $page = $this->_get_page_with_proxy($this->_url, $proxy);
        }
        echo "\t\t\tGetting proxy lists page....\n";        
        //echo $page;exit;
        $this->_get_proxies_from_page($page);
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

    protected function _get_proxies_from_page($page)
    {
        
        $html  = new simple_html_dom();
        $html->load($page);
        
        $proxyList = array();
        
        $oddList = $html->find('.tr_style1');
        foreach ($oddList as $list) {
            $proxy['ip'] = $list->find('td',0)->plaintext;
            $proxy['port'] = $list->find('td', 1)->plaintext;
            $proxy['type'] = $list->find('td',8)->plaintext;
            $proxy['anonimity'] = $list->find('td', 9)->plaintext;            
            //$mes = scraperwiki::save_sqlite(array('type', "ip",'port','anonimity'), $proxy);
            //echo "Done Parsing proxy\n";
            array_push($proxyList, $proxy);
        }
        
        $evenList = $html->find('.tr_style2');
        foreach ($evenList as $list) {
            $proxy['ip'] = $list->find('td',0)->plaintext;
            $proxy['port'] = $list->find('td', 1)->plaintext;
            $proxy['type'] = $list->find('td',8)->plaintext;
            $proxy['anonimity'] = $list->find('td', 9)->plaintext;            
            //$mes = scraperwiki::save_sqlite(array('type', "ip",'port','anonimity'), $proxy);
            //echo "Done Parsing proxy\n";
            array_push($proxyList, $proxy);
        }
        $mes = scraperwiki::save_sqlite(array('type', "ip",'port','anonimity'), $proxyList);
        $this->_destory_variable_or_object($html);
        $this->_check_pagination($page);
        
        
    }  
    
    protected function _check_pagination($page)
    {
        //next
        $html  = new simple_html_dom();
        $html->load($page);
        
        $this->_destory_variable_or_object($page);
        
        $nextPageExists = count($html->find('.next'));
        if($nextPageExists > 0){
            $url = 'http://www.vpngeeks.com/'.$html->find('.next',0)->parent()->href;
            $this->_url = preg_replace('/&#pagination/i', '', $url);
            $this->_destory_variable_or_object($html);
            $this->start($this->_usingProxy);
        }
        
        $this->_destory_variable_or_object($html);
        echo 'All parsing done!!!';
        
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
            //CURLOPT_REFERER        => "google.com",
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
            //CURLOPT_REFERER        => "google.com",
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

//This site already blocked scrapper wikis ip. So please use your own proxy...to parse the page...

$j = new VpnGeeksParser();
$proxy = '62.173.37.204:8080';
$j->start($proxy);

?>