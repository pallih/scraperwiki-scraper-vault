<?php

/**
 * @package    GroupReaderApp
 * @subpackage Scraper
 * @author     Aleksander Wons
 **/
class GroupAppScraper
{
    const ENCODING_REGEXP = '/Content-Type: [^;]+; charset=([^\s;$]+)/';
    const META_ENCODING_REGEXP = '/<meta.*?content="[^;]+;*.?charset=([^"]+)"/is';
    const META_ENCODING_UNICODE_REGEXP = '/<meta.*?content="[^;]+;*.?charset=([^"]+)"/uis';
    const META_ENCODING_HTML5_REGEXP = '/<meta.*?charset="([^"]+)"/is';
    const META_ENCODING_UNICODE_HTML5_REGEXP = '/<meta.*?charset="([^"]+)"/uis';
    
    const WINDOW_OPEN_REGEXT = "/window\.open\('([^']+)'/uis";
    
    const KEY_LAST_SOURCE_ID = 'last_source_id';
    
    const SOURCES_URL = 'http://example.com/scraper/getSources'; // Update this when scraper is private
    const ERROR_REPORT_URL = 'http://example.com/scraper/reportError'; // Update this when scraper is private

    const SCRAPER_ERROR_CODE_NO_ARTICLE_ROWS = 1000;
    const SCRAPER_ERROR_MSG_NO_ARTICLE_ROWS = 'No article rows found on a given page';
    
    const SCRAPER_ERROR_CODE_NO_ARTICLE = 1001;
    const SCRAPER_ERROR_MSG_NO_ARTICLE = 'No article link found in a row';
    
    const SCRAPER_ERROR_CODE_NO_TITLE = 1002;
    const SCRAPER_ERROR_MSG_NO_TITLE = 'No article title found on a given page';
    
    private static $nonCriticalCURLErrors = array(CURLE_COULDNT_RESOLVE_PROXY, CURLE_COULDNT_RESOLVE_HOST, CURLE_COULDNT_CONNECT, CURLE_RECV_ERROR);
    
    /**
     * @var array
     */
    private $userAgents = array(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.0 Safari/535.11',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.126 Safari/535.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_3) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535.1',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.57 Safari/534.24',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
        'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
        'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
        'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
        'Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
        'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100215 Solaris/10.1 (GNU) Superswan/3.5.8 (Byte/me)',
        'Opera/9.80 (Series 60; Opera Mini/6.1.26266/26.1069; U; en) Presto/2.8.119 Version/10.54',
        'Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.13221/25.623; U; en) Presto/2.5.25 Version/10.54',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.10',
        'Opera/9.80 (Windows Mobile; WCE; Opera Mobi/WMD-50433; U; en) Presto/2.4.13 Version/10.00',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; GTB6.5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; chromeframe/13.0.782.218; chromeframe; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    );
    
    /**
     * @var Resource
     **/
    private $ch;
    
    /**
     * @var string
     */
    private $cookieJar;

    /**
     * @var string
     */
    private $encoding = null;
    
    public function __construct()
    {
        $this->initCurl();
        $this->initDatabase();
        $this->cleanupDatabase();
    }
    
    public function __destruct()
    {
        scraperwiki::save_var(self::KEY_LAST_SOURCE_ID, null);
    }
    
    /**
     * @return void 
     */
    private function initCurl()
    {
        $this->ch = curl_init();
        curl_setopt_array($this->ch, array(
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_USERAGENT => $this->userAgents[mt_rand(0, count($this->userAgents) - 1)],
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_COOKIEJAR => $this->cookieJar,
            CURLOPT_HEADERFUNCTION => array($this, 'readHeader'),
            CURLOPT_AUTOREFERER => true,
            CURLOPT_VERBOSE => false,
            CURLOPT_FAILONERROR => true,
        ));
    }
    
    /**
     * @param  array $source
     * @return string
     */
    private function curlExec(array $source = null)
    {
        $this->encoding = null;
        $html = curl_exec($this->ch);
        if(curl_errno($this->ch))
        {
            if($source && !in_array(curl_errno($this->ch), self::$nonCriticalCURLErrors))
            {
                $this->reportError($source, $this->createCurlError());
            } else
            {
                echo sprintf("%s (%d)\n", curl_error($this->ch), curl_errno($this->ch));
            }
            return null;
        }
        $this->detectEncoding($html);
        
        $headPos = mb_strpos($html, '<head>');
        if (false === $headPos)
            $headpos = mb_strpos($html, '<head>');
        if (false !== $headPos) {
            $headPos += 6;
            $html = mb_substr($html, 0, $headPos) . '<meta http-equiv="Content-Type" content="text/html; charset=' . $this->encoding . '">' . mb_substr($html, $headPos);
        }
        
        return $html;
    }
    
    /**
     * @return void 
     */
    private function initDatabase()
    {
        scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS article (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            source_id INTEGER NOT NULL,
            guid CHAR(40) NOT NULL UNIQUE,
            url VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            inserted_at INTEGER NOT NULL
        )");
        scraperwiki::sqliteexecute("CREATE INDEX IF NOT EXISTS source_id_idx ON article(source_id)");
        scraperwiki::sqliteexecute("CREATE INDEX IF NOT EXISTS guid_idx ON article(guid)");
        scraperwiki::sqlitecommit();
        scraperwiki::save_var('test', 1); // We have to save enything to variables table before we can use get_var for the first time
    }
    
    /**
     * @return void
     */
    private function cleanupDatabase()
    {
        scraperwiki::sqliteexecute("DELETE FROM article WHERE inserted_at<:insertedAt", array('insertedAt' => time() - (60 * 60 * 24 * 7))); // Remove articles inserted over a week ago
        scraperwiki::sqlitecommit();
    }
    
    /**
     * @param  array     $source
     * @param  Exception $e
     * @return void
     */
    private function reportError(array $source, Exception $e)
    {
        $params = array(
            sprintf("sourceId=%s", urlencode($source['id'])),
            sprintf("errorMessage=%s", urlencode($e->getMessage())),
        );
        curl_setopt_array($this->ch, array(
            CURLOPT_URL => self::ERROR_REPORT_URL,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => implode('&', $params),
        ));
        
        $this->curlExec();
    }

    /**
     * @return void
     */
    public function execute()
    {
        $sources = $this->getSources();
        foreach($sources as $source)
        {
            try{
                $this->fetchData($source);
            } catch(ScraperException $e){
                $this->reportError($source, $e);
            }
        }
    }

    /**
     * @return array
     * @throws CURLException
     */
    private function getSources()
    {
        /*curl_setopt($this->ch, CURLOPT_URL, self::SOURCES_URL);
        $content = $this->curlExec();
        
        $sources = json_decode($content, true);
        if(!isset($sources['sources']))
            return array();*/
        
        $sources = json_decode('{"sources":[{"id":2408,"url":"http:\/\/www.guardian.co.uk\/football\/grimsby","rowPath":"\/html\/body\/div\/div[2]\/div[2]\/ul[1]\/li","titlePath":"\/\/*[@id=\"main-article-info\"]\/h1","linkPath":"\/html\/body\/div\/div[2]\/div[2]\/ul[1]\/li\/div[contains(@class, \"trail-caption\")]\/div\/h3\/a","contentPath":"\/\/*[@id=\"article-body-blocks\"]","createdAtPath":"\/\/*[@id=\"content\"]\/ul\/\/li[@class=\"publication\"]\/time"},{"id":2411,"url":"http:\/\/english.cec.org.cn\/","rowPath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table[2]\/tr[2]\/td\/table\/tr\/td\/table\/tr[2]\/td\/table\/tr\/td[contains(@class, \"STYLE5\")]","titlePath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table\/tr[2]\/td\/div\/table\/tr\/td\/font","linkPath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table[2]\/tr[2]\/td\/table\/tr\/td\/table\/tr[2]\/td\/table\/tr\/td[contains(@class, \"STYLE5\")]\/a","contentPath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table\/\/tr[2]\/td\/div\/table\/tr[3]\/td\/div","createdAtPath":""},{"id":2412,"url":"http:\/\/www.welltech.com.cn\/en\/companynews.asp","rowPath":"\/html\/body\/table\/tr[5]\/td\/table\/tr\/td[2]\/table\/tr","titlePath":"\/html\/body\/table[2]\/tr\/td\/table\/tr[1]\/td","linkPath":"\/html\/body\/table\/tr[5]\/td\/table\/tr\/td[2]\/table\/tr\/td[2]\/span\/a","contentPath":"\/html\/body\/table[2]\/tr\/td\/table\/tr[2]\/td","createdAtPath":"\/html\/body\/table[2]\/tr\/td\/table\/tr[3]\/td"},{"id":2413,"url":"http:\/\/www.cidra.com\/?q=news-articles","rowPath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr","titlePath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr\/td[2]\/a","linkPath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr\/td[2]\/a","contentPath":"\/html\/body\/div\/div[3]\/section\/div\/div[contains(@class, \"field-type-text-long\")]","createdAtPath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr\/td[3]\/span"}]}', true);
        if(!isset($sources['sources']))
            return array();
        
        $sources = $sources['sources'];
        $lastSourceId = scraperwiki::get_var(self::KEY_LAST_SOURCE_ID, null);
        if(!$lastSourceId)
            return $sources;
        
        $tmp = array();
        foreach($sources as $source)
            if($source['id'] > $lastSourceId)
                $tmp[] = $source;
        return $tmp;
    }
    
    /**
     * @param  array $source
     * @return void
     * @throws Exception
     */
    private function fetchData($source)
    {
        $this->initCurl();
        curl_setopt($this->ch, CURLOPT_REFERER, $source['url']);
        
        // Open main page
        curl_setopt($this->ch, CURLOPT_URL, $source['url']);
        $html = $this->curlExec($source);
        if($html)
        {
            libxml_clear_errors();
            libxml_use_internal_errors(true);

            $domDocument = new DOMDocument();
            $domDocument->loadHTML($html);
            $xPath = new DOMXPath($domDocument);

            $aricles = array();
            try{
                $aricles = $this->parsePage($xPath, $source, $source['url']);
            } catch(RuntimeException $e){
                $this->reportError($source, $e);
            }

            if($aricles)
            {
                scraperwiki::save_var(self::KEY_LAST_SOURCE_ID, $source['id']);
                $this->updateResults($aricles);
            }

            libxml_clear_errors();
        }
    }
    
    /**
     * @param  DOMXPath $xPath
     * @param  array    $source
     * @param  string   $baseUrl
     * @return array
     * @throws Excpetion
     */
    private function parsePage(DOMXPath $originalXPath, $source, $baseUrl)
    {
        $articles = array();
        
        $rowNodes = $originalXPath->query($source['rowPath']);
        if($rowNodes->length > 0)
        {
            foreach($rowNodes as $rowNode)
            {
                $linkPath = substr($source['linkPath'], strlen($source['rowPath']) + 1);
                $linkNodes = $originalXPath->evaluate($linkPath, $rowNode);
                if($linkNodes && $linkNodes->length === 1)
                {
                    $url = $this->getUrlFromLink($linkNodes->item(0), $baseUrl);
                    curl_setopt($this->ch, CURLOPT_URL, $url);
                    $html = $this->curlExec($source);
                    if($html)
                    {
                        $domDocument = new DOMDocument();
                        $domDocument->loadHTML($html);
                        $xPath = new DOMXPath($domDocument);

                        $title = null;
                        // First look for a title inside selected row
                        $titlePath = substr($source['titlePath'], strlen($source['rowPath']) + 1);
                        if($titlePath)
                        {
                            $titleNodes = $originalXPath->evaluate($titlePath, $rowNode);
                            if($titleNodes && $titleNodes->length === 1)
                                $title = strip_tags($titleNodes->item(0)->nodeValue);
                        }
                        if(!$title) // If we couldn't find a title inside selected row we will look for it inside article page
                        {
                            $titleNodes = $xPath->query($source['titlePath']);
                            if($titleNodes && $titleNodes->length === 1)
                            {
                                $title = strip_tags($titleNodes->item(0)->nodeValue);
                            }
                        }

                        // If we have found a title we are going to look for other fields
                        if($title)
                        {
                            if($source['createdAtPath'])
                            {
                                $createdAt = null;
                                // First we look for a publication date inside selected row
                                $createdAtPath = substr($source['titlePath'], strlen($source['rowPath']) + 1);
                                if($createdAtPath)
                                {
                                    $createdAtNodes = $originalXPath->evaluate($createdAtPath, $rowNode);
                                    if($createdAtNodes && $createdAtNodes->length === 1)
                                        $createdAt = strtotime(strip_tags($createdAtNodes->item(0)->nodeValue));
                                }
                                if(!$createdAt) // If we couldn't find a publication date inside selected row we will look for it inside article page
                                {
                                    $createdAtNodes = $xPath->query($source['createdAtPath']);
                                    if($createdAtNodes && $createdAtNodes->length > 0)
                                    {
                                        $createdAt = strtotime($createdAtNodes->item(0)->nodeValue);
                                    } else
                                    {
                                        $createdAt = time();
                                    }
                                }
                            } else
                            {
                                $createdAt = time();
                            }
                            if(!$createdAt)
                                $createdAt = time();

                            // We are looking for an article content
                            $contentNodes = $xPath->query($source['contentPath']);
                            if($contentNodes && $contentNodes->length > 0)
                            {
                                $articleContent = mb_substr(strip_tags($contentNodes->item(0)->nodeValue), 0, 4000);
                            } else
                            {
                                $articleContent = '';
                            }

                            $articles[] = array(
                                'sourceId' => $source['id'],
                                'url' => $url,
                                'title' => $title,
                                'content' => $articleContent,
                                'createdAt' => $createdAt,
                            );
                        } else
                        {
                            $this->reportError($source, $this->createScraperError($url, self::SCRAPER_ERROR_MSG_NO_TITLE, self::SCRAPER_ERROR_CODE_NO_TITLE));
                        }
                    }
                } else
                {
                    $this->reportError($source, $this->createScraperError($baseUrl, self::SCRAPER_ERROR_MSG_NO_ARTICLE, self::SCRAPER_ERROR_CODE_NO_ARTICLE));
                }
            }
        } else
        {
            throw $this->createScraperError($baseUrl, self::SCRAPER_ERROR_MSG_NO_ARTICLE_ROWS, self::SCRAPER_ERROR_CODE_NO_ARTICLE_ROWS);
        }
        
        return $articles;
    }
    
    /**
     * @param  array $articles
     * @return void
     */
    private function updateResults($articles)
    {
        foreach($articles as $article)
        {
            $guid = sha1($article['url']);
            scraperwiki::sqliteexecute("INSERT OR IGNORE INTO article (source_id, guid, url, title, content, created_at, inserted_at) VALUES (:sourceId, :guid, :url, :title, :content, :createdAt, :insertedAt)",
                array_merge($article, array('guid' => $guid, 'insertedAt' => time()))
            );
            scraperwiki::sqlitecommit();
        }
    }
    
    /**
     * @return CURLException 
     */
    private function createCurlError()
    {
        return new CURLException(sprintf("Unable to execute CURL request: (%s) %s", curl_errno($this->ch), curl_error($this->ch)));
    }
    
    /**
     * @param  string $url
     * @param  string $message
     * @param  int    $code
     * @return ScraperException
     */
    private function createScraperError($url, $message, $code)
    {
        return new ScraperException(sprintf("Error while scraping URL '%s': (%s)%s", $url, $code, $message), $code);
    }
    
    /**
     * Read http headers
     * 
     * @param  ch resource $ch
     * @param  string      $string
     * @return integer     Header length
     */
    public function readHeader($ch, $string)
    {
        $length = strlen($string);
        
        if(preg_match(self::ENCODING_REGEXP, $string, $matches))
            $this->encoding = $matches[1];

        return $length;
    }
    
    /**
     * @param  string $doc
     * @return void
     */
    private function detectEncoding($doc)
    {
        if($this->encoding)
        {
            
        } elseif(preg_match(self::META_ENCODING_UNICODE_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(preg_match(self::META_ENCODING_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(preg_match(self::META_ENCODING_HTML5_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(preg_match(self::META_ENCODING_UNICODE_HTML5_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(!$this->encoding)
        {
            $encoding = mb_detect_encoding($doc);
            if($encoding)
            {
                $this->encoding = $encoding;
            }
        }
        
        if(!$this->encoding)
            $this->encoding = 'UTF-8';
        
        mb_internal_encoding($this->encoding);
    }
    
    /**
     * @param  DOMNode $linkNode
     * @param  string  $baseUrl
     * @return string
     */
    private function getUrlFromLink(DOMNode $linkNode, $baseUrl)
    {
        $url = null;
        
        $href = $linkNode->getAttribute('href');
        if(!empty($href) && '#' != $href && false === mb_strpos($href, 'javascript:void'))
        {
            $url = $href;
        } else
        {
            $onclick = $linkNode->getAttribute('onclick');
            if(preg_match(self::WINDOW_OPEN_REGEXT, $onclick, $matches))
                $url = $matches[1];
        }
        
        if(null !== $url && false === mb_strpos($url, 'http'))
        {
            if(0 === mb_strpos($url, '/'))
            {
                $url = mb_substr($url, 1);
                $url = sprintf("%s://%s/%s", parse_url($baseUrl, PHP_URL_SCHEME), parse_url($baseUrl, PHP_URL_HOST), $url);
            } else
            {
                $pos = mb_strrpos($baseUrl, '/');
                $url = mb_substr($baseUrl, 0, $pos).'/'.$url;
            }
        }
        
        return $url;
    }
}

/**
 * @package    GroupReaderApp
 * @subpackage Scraper
 * @author     Aleksander Wons
 **/
class ScraperException extends RuntimeException
{
    
}

$scraper = new GroupAppScraper();
$scraper->execute();

?>
<?php

/**
 * @package    GroupReaderApp
 * @subpackage Scraper
 * @author     Aleksander Wons
 **/
class GroupAppScraper
{
    const ENCODING_REGEXP = '/Content-Type: [^;]+; charset=([^\s;$]+)/';
    const META_ENCODING_REGEXP = '/<meta.*?content="[^;]+;*.?charset=([^"]+)"/is';
    const META_ENCODING_UNICODE_REGEXP = '/<meta.*?content="[^;]+;*.?charset=([^"]+)"/uis';
    const META_ENCODING_HTML5_REGEXP = '/<meta.*?charset="([^"]+)"/is';
    const META_ENCODING_UNICODE_HTML5_REGEXP = '/<meta.*?charset="([^"]+)"/uis';
    
    const WINDOW_OPEN_REGEXT = "/window\.open\('([^']+)'/uis";
    
    const KEY_LAST_SOURCE_ID = 'last_source_id';
    
    const SOURCES_URL = 'http://example.com/scraper/getSources'; // Update this when scraper is private
    const ERROR_REPORT_URL = 'http://example.com/scraper/reportError'; // Update this when scraper is private

    const SCRAPER_ERROR_CODE_NO_ARTICLE_ROWS = 1000;
    const SCRAPER_ERROR_MSG_NO_ARTICLE_ROWS = 'No article rows found on a given page';
    
    const SCRAPER_ERROR_CODE_NO_ARTICLE = 1001;
    const SCRAPER_ERROR_MSG_NO_ARTICLE = 'No article link found in a row';
    
    const SCRAPER_ERROR_CODE_NO_TITLE = 1002;
    const SCRAPER_ERROR_MSG_NO_TITLE = 'No article title found on a given page';
    
    private static $nonCriticalCURLErrors = array(CURLE_COULDNT_RESOLVE_PROXY, CURLE_COULDNT_RESOLVE_HOST, CURLE_COULDNT_CONNECT, CURLE_RECV_ERROR);
    
    /**
     * @var array
     */
    private $userAgents = array(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.0 Safari/535.11',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.126 Safari/535.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_3) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535.1',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.57 Safari/534.24',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
        'Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1',
        'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
        'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
        'Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
        'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100215 Solaris/10.1 (GNU) Superswan/3.5.8 (Byte/me)',
        'Opera/9.80 (Series 60; Opera Mini/6.1.26266/26.1069; U; en) Presto/2.8.119 Version/10.54',
        'Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.13221/25.623; U; en) Presto/2.5.25 Version/10.54',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.10',
        'Opera/9.80 (Windows Mobile; WCE; Opera Mobi/WMD-50433; U; en) Presto/2.4.13 Version/10.00',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; GTB6.5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; chromeframe/13.0.782.218; chromeframe; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    );
    
    /**
     * @var Resource
     **/
    private $ch;
    
    /**
     * @var string
     */
    private $cookieJar;

    /**
     * @var string
     */
    private $encoding = null;
    
    public function __construct()
    {
        $this->initCurl();
        $this->initDatabase();
        $this->cleanupDatabase();
    }
    
    public function __destruct()
    {
        scraperwiki::save_var(self::KEY_LAST_SOURCE_ID, null);
    }
    
    /**
     * @return void 
     */
    private function initCurl()
    {
        $this->ch = curl_init();
        curl_setopt_array($this->ch, array(
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_USERAGENT => $this->userAgents[mt_rand(0, count($this->userAgents) - 1)],
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_COOKIEJAR => $this->cookieJar,
            CURLOPT_HEADERFUNCTION => array($this, 'readHeader'),
            CURLOPT_AUTOREFERER => true,
            CURLOPT_VERBOSE => false,
            CURLOPT_FAILONERROR => true,
        ));
    }
    
    /**
     * @param  array $source
     * @return string
     */
    private function curlExec(array $source = null)
    {
        $this->encoding = null;
        $html = curl_exec($this->ch);
        if(curl_errno($this->ch))
        {
            if($source && !in_array(curl_errno($this->ch), self::$nonCriticalCURLErrors))
            {
                $this->reportError($source, $this->createCurlError());
            } else
            {
                echo sprintf("%s (%d)\n", curl_error($this->ch), curl_errno($this->ch));
            }
            return null;
        }
        $this->detectEncoding($html);
        
        $headPos = mb_strpos($html, '<head>');
        if (false === $headPos)
            $headpos = mb_strpos($html, '<head>');
        if (false !== $headPos) {
            $headPos += 6;
            $html = mb_substr($html, 0, $headPos) . '<meta http-equiv="Content-Type" content="text/html; charset=' . $this->encoding . '">' . mb_substr($html, $headPos);
        }
        
        return $html;
    }
    
    /**
     * @return void 
     */
    private function initDatabase()
    {
        scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS article (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            source_id INTEGER NOT NULL,
            guid CHAR(40) NOT NULL UNIQUE,
            url VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            inserted_at INTEGER NOT NULL
        )");
        scraperwiki::sqliteexecute("CREATE INDEX IF NOT EXISTS source_id_idx ON article(source_id)");
        scraperwiki::sqliteexecute("CREATE INDEX IF NOT EXISTS guid_idx ON article(guid)");
        scraperwiki::sqlitecommit();
        scraperwiki::save_var('test', 1); // We have to save enything to variables table before we can use get_var for the first time
    }
    
    /**
     * @return void
     */
    private function cleanupDatabase()
    {
        scraperwiki::sqliteexecute("DELETE FROM article WHERE inserted_at<:insertedAt", array('insertedAt' => time() - (60 * 60 * 24 * 7))); // Remove articles inserted over a week ago
        scraperwiki::sqlitecommit();
    }
    
    /**
     * @param  array     $source
     * @param  Exception $e
     * @return void
     */
    private function reportError(array $source, Exception $e)
    {
        $params = array(
            sprintf("sourceId=%s", urlencode($source['id'])),
            sprintf("errorMessage=%s", urlencode($e->getMessage())),
        );
        curl_setopt_array($this->ch, array(
            CURLOPT_URL => self::ERROR_REPORT_URL,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => implode('&', $params),
        ));
        
        $this->curlExec();
    }

    /**
     * @return void
     */
    public function execute()
    {
        $sources = $this->getSources();
        foreach($sources as $source)
        {
            try{
                $this->fetchData($source);
            } catch(ScraperException $e){
                $this->reportError($source, $e);
            }
        }
    }

    /**
     * @return array
     * @throws CURLException
     */
    private function getSources()
    {
        /*curl_setopt($this->ch, CURLOPT_URL, self::SOURCES_URL);
        $content = $this->curlExec();
        
        $sources = json_decode($content, true);
        if(!isset($sources['sources']))
            return array();*/
        
        $sources = json_decode('{"sources":[{"id":2408,"url":"http:\/\/www.guardian.co.uk\/football\/grimsby","rowPath":"\/html\/body\/div\/div[2]\/div[2]\/ul[1]\/li","titlePath":"\/\/*[@id=\"main-article-info\"]\/h1","linkPath":"\/html\/body\/div\/div[2]\/div[2]\/ul[1]\/li\/div[contains(@class, \"trail-caption\")]\/div\/h3\/a","contentPath":"\/\/*[@id=\"article-body-blocks\"]","createdAtPath":"\/\/*[@id=\"content\"]\/ul\/\/li[@class=\"publication\"]\/time"},{"id":2411,"url":"http:\/\/english.cec.org.cn\/","rowPath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table[2]\/tr[2]\/td\/table\/tr\/td\/table\/tr[2]\/td\/table\/tr\/td[contains(@class, \"STYLE5\")]","titlePath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table\/tr[2]\/td\/div\/table\/tr\/td\/font","linkPath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table[2]\/tr[2]\/td\/table\/tr\/td\/table\/tr[2]\/td\/table\/tr\/td[contains(@class, \"STYLE5\")]\/a","contentPath":"\/html\/body\/div\/table[2]\/tr\/td\/div\/table\/tr\/td[2]\/div\/table\/\/tr[2]\/td\/div\/table\/tr[3]\/td\/div","createdAtPath":""},{"id":2412,"url":"http:\/\/www.welltech.com.cn\/en\/companynews.asp","rowPath":"\/html\/body\/table\/tr[5]\/td\/table\/tr\/td[2]\/table\/tr","titlePath":"\/html\/body\/table[2]\/tr\/td\/table\/tr[1]\/td","linkPath":"\/html\/body\/table\/tr[5]\/td\/table\/tr\/td[2]\/table\/tr\/td[2]\/span\/a","contentPath":"\/html\/body\/table[2]\/tr\/td\/table\/tr[2]\/td","createdAtPath":"\/html\/body\/table[2]\/tr\/td\/table\/tr[3]\/td"},{"id":2413,"url":"http:\/\/www.cidra.com\/?q=news-articles","rowPath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr","titlePath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr\/td[2]\/a","linkPath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr\/td[2]\/a","contentPath":"\/html\/body\/div\/div[3]\/section\/div\/div[contains(@class, \"field-type-text-long\")]","createdAtPath":"\/html\/body\/div\/div[3]\/section\/div\/div[2]\/table\/tbody\/tr\/td[3]\/span"}]}', true);
        if(!isset($sources['sources']))
            return array();
        
        $sources = $sources['sources'];
        $lastSourceId = scraperwiki::get_var(self::KEY_LAST_SOURCE_ID, null);
        if(!$lastSourceId)
            return $sources;
        
        $tmp = array();
        foreach($sources as $source)
            if($source['id'] > $lastSourceId)
                $tmp[] = $source;
        return $tmp;
    }
    
    /**
     * @param  array $source
     * @return void
     * @throws Exception
     */
    private function fetchData($source)
    {
        $this->initCurl();
        curl_setopt($this->ch, CURLOPT_REFERER, $source['url']);
        
        // Open main page
        curl_setopt($this->ch, CURLOPT_URL, $source['url']);
        $html = $this->curlExec($source);
        if($html)
        {
            libxml_clear_errors();
            libxml_use_internal_errors(true);

            $domDocument = new DOMDocument();
            $domDocument->loadHTML($html);
            $xPath = new DOMXPath($domDocument);

            $aricles = array();
            try{
                $aricles = $this->parsePage($xPath, $source, $source['url']);
            } catch(RuntimeException $e){
                $this->reportError($source, $e);
            }

            if($aricles)
            {
                scraperwiki::save_var(self::KEY_LAST_SOURCE_ID, $source['id']);
                $this->updateResults($aricles);
            }

            libxml_clear_errors();
        }
    }
    
    /**
     * @param  DOMXPath $xPath
     * @param  array    $source
     * @param  string   $baseUrl
     * @return array
     * @throws Excpetion
     */
    private function parsePage(DOMXPath $originalXPath, $source, $baseUrl)
    {
        $articles = array();
        
        $rowNodes = $originalXPath->query($source['rowPath']);
        if($rowNodes->length > 0)
        {
            foreach($rowNodes as $rowNode)
            {
                $linkPath = substr($source['linkPath'], strlen($source['rowPath']) + 1);
                $linkNodes = $originalXPath->evaluate($linkPath, $rowNode);
                if($linkNodes && $linkNodes->length === 1)
                {
                    $url = $this->getUrlFromLink($linkNodes->item(0), $baseUrl);
                    curl_setopt($this->ch, CURLOPT_URL, $url);
                    $html = $this->curlExec($source);
                    if($html)
                    {
                        $domDocument = new DOMDocument();
                        $domDocument->loadHTML($html);
                        $xPath = new DOMXPath($domDocument);

                        $title = null;
                        // First look for a title inside selected row
                        $titlePath = substr($source['titlePath'], strlen($source['rowPath']) + 1);
                        if($titlePath)
                        {
                            $titleNodes = $originalXPath->evaluate($titlePath, $rowNode);
                            if($titleNodes && $titleNodes->length === 1)
                                $title = strip_tags($titleNodes->item(0)->nodeValue);
                        }
                        if(!$title) // If we couldn't find a title inside selected row we will look for it inside article page
                        {
                            $titleNodes = $xPath->query($source['titlePath']);
                            if($titleNodes && $titleNodes->length === 1)
                            {
                                $title = strip_tags($titleNodes->item(0)->nodeValue);
                            }
                        }

                        // If we have found a title we are going to look for other fields
                        if($title)
                        {
                            if($source['createdAtPath'])
                            {
                                $createdAt = null;
                                // First we look for a publication date inside selected row
                                $createdAtPath = substr($source['titlePath'], strlen($source['rowPath']) + 1);
                                if($createdAtPath)
                                {
                                    $createdAtNodes = $originalXPath->evaluate($createdAtPath, $rowNode);
                                    if($createdAtNodes && $createdAtNodes->length === 1)
                                        $createdAt = strtotime(strip_tags($createdAtNodes->item(0)->nodeValue));
                                }
                                if(!$createdAt) // If we couldn't find a publication date inside selected row we will look for it inside article page
                                {
                                    $createdAtNodes = $xPath->query($source['createdAtPath']);
                                    if($createdAtNodes && $createdAtNodes->length > 0)
                                    {
                                        $createdAt = strtotime($createdAtNodes->item(0)->nodeValue);
                                    } else
                                    {
                                        $createdAt = time();
                                    }
                                }
                            } else
                            {
                                $createdAt = time();
                            }
                            if(!$createdAt)
                                $createdAt = time();

                            // We are looking for an article content
                            $contentNodes = $xPath->query($source['contentPath']);
                            if($contentNodes && $contentNodes->length > 0)
                            {
                                $articleContent = mb_substr(strip_tags($contentNodes->item(0)->nodeValue), 0, 4000);
                            } else
                            {
                                $articleContent = '';
                            }

                            $articles[] = array(
                                'sourceId' => $source['id'],
                                'url' => $url,
                                'title' => $title,
                                'content' => $articleContent,
                                'createdAt' => $createdAt,
                            );
                        } else
                        {
                            $this->reportError($source, $this->createScraperError($url, self::SCRAPER_ERROR_MSG_NO_TITLE, self::SCRAPER_ERROR_CODE_NO_TITLE));
                        }
                    }
                } else
                {
                    $this->reportError($source, $this->createScraperError($baseUrl, self::SCRAPER_ERROR_MSG_NO_ARTICLE, self::SCRAPER_ERROR_CODE_NO_ARTICLE));
                }
            }
        } else
        {
            throw $this->createScraperError($baseUrl, self::SCRAPER_ERROR_MSG_NO_ARTICLE_ROWS, self::SCRAPER_ERROR_CODE_NO_ARTICLE_ROWS);
        }
        
        return $articles;
    }
    
    /**
     * @param  array $articles
     * @return void
     */
    private function updateResults($articles)
    {
        foreach($articles as $article)
        {
            $guid = sha1($article['url']);
            scraperwiki::sqliteexecute("INSERT OR IGNORE INTO article (source_id, guid, url, title, content, created_at, inserted_at) VALUES (:sourceId, :guid, :url, :title, :content, :createdAt, :insertedAt)",
                array_merge($article, array('guid' => $guid, 'insertedAt' => time()))
            );
            scraperwiki::sqlitecommit();
        }
    }
    
    /**
     * @return CURLException 
     */
    private function createCurlError()
    {
        return new CURLException(sprintf("Unable to execute CURL request: (%s) %s", curl_errno($this->ch), curl_error($this->ch)));
    }
    
    /**
     * @param  string $url
     * @param  string $message
     * @param  int    $code
     * @return ScraperException
     */
    private function createScraperError($url, $message, $code)
    {
        return new ScraperException(sprintf("Error while scraping URL '%s': (%s)%s", $url, $code, $message), $code);
    }
    
    /**
     * Read http headers
     * 
     * @param  ch resource $ch
     * @param  string      $string
     * @return integer     Header length
     */
    public function readHeader($ch, $string)
    {
        $length = strlen($string);
        
        if(preg_match(self::ENCODING_REGEXP, $string, $matches))
            $this->encoding = $matches[1];

        return $length;
    }
    
    /**
     * @param  string $doc
     * @return void
     */
    private function detectEncoding($doc)
    {
        if($this->encoding)
        {
            
        } elseif(preg_match(self::META_ENCODING_UNICODE_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(preg_match(self::META_ENCODING_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(preg_match(self::META_ENCODING_HTML5_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(preg_match(self::META_ENCODING_UNICODE_HTML5_REGEXP, $doc, $matches))
        {
            $this->encoding = $matches[1];
        } elseif(!$this->encoding)
        {
            $encoding = mb_detect_encoding($doc);
            if($encoding)
            {
                $this->encoding = $encoding;
            }
        }
        
        if(!$this->encoding)
            $this->encoding = 'UTF-8';
        
        mb_internal_encoding($this->encoding);
    }
    
    /**
     * @param  DOMNode $linkNode
     * @param  string  $baseUrl
     * @return string
     */
    private function getUrlFromLink(DOMNode $linkNode, $baseUrl)
    {
        $url = null;
        
        $href = $linkNode->getAttribute('href');
        if(!empty($href) && '#' != $href && false === mb_strpos($href, 'javascript:void'))
        {
            $url = $href;
        } else
        {
            $onclick = $linkNode->getAttribute('onclick');
            if(preg_match(self::WINDOW_OPEN_REGEXT, $onclick, $matches))
                $url = $matches[1];
        }
        
        if(null !== $url && false === mb_strpos($url, 'http'))
        {
            if(0 === mb_strpos($url, '/'))
            {
                $url = mb_substr($url, 1);
                $url = sprintf("%s://%s/%s", parse_url($baseUrl, PHP_URL_SCHEME), parse_url($baseUrl, PHP_URL_HOST), $url);
            } else
            {
                $pos = mb_strrpos($baseUrl, '/');
                $url = mb_substr($baseUrl, 0, $pos).'/'.$url;
            }
        }
        
        return $url;
    }
}

/**
 * @package    GroupReaderApp
 * @subpackage Scraper
 * @author     Aleksander Wons
 **/
class ScraperException extends RuntimeException
{
    
}

$scraper = new GroupAppScraper();
$scraper->execute();

?>
