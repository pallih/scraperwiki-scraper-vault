<?php
for ($pn = 1; $pn <= 10; $pn++) {
//    echo $pn;
$scrape = new Scraper('http://www.pool.com/viewlist.aspx?Page='.$pn);
}

class Scraper {
    protected $articles = array();
    protected $domain;
    
    // Set actions to run when the class is instantiated
    function __construct($url){
        // Set the maximum execution time of the script to unlimited so that it can grab all the articles if there are a lot of them to scrape
        set_time_limit(0);
        
        // Set the root domain of the URL to concatinate with URLs later
        $this->domain = explode("/", $url);
        $this->domain = 'http://' . $this->domain[2];
        
        // Pass the page URL you want to start scraping and start scraping through the section pages
        $this->getArticleUrls($url);
        
        //echo count($this->articles) . ' - Done counting articles items, now adding articles.';
        
        // Loop through the article pages and grab the full article to finish populating the articles array with data
        foreach ($this->articles as $item){
       // $item['article'] = $this->getArticles($item['url']);
            print_r($item['title']);
        }
        
        //echo count($this->articles) . ' - Done adding articles.';
         
        
        // Add function here to start adding items in the article array with articles to a database
    }
    
    // Start Get Article Urls
    private function getArticleUrls($url){
        // Instantiate next page variable to check at the end
        $nextPageUrl = NULL;
        
        // Instantiate cURL to grab the HTML page.
        $c = curl_init($url);
        curl_setopt($c, CURLOPT_HEADER, false);
        curl_setopt($c, CURLOPT_USERAGENT, $this->getUserAgent());
        curl_setopt($c, CURLOPT_FAILONERROR, true);
        curl_setopt($c, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($c, CURLOPT_AUTOREFERER, true);
        curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($c, CURLOPT_TIMEOUT, 10);
//WARNING: this would prevent curl from detecting a 'man in the middle' attack
curl_setopt ($c, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt ($c, CURLOPT_SSL_VERIFYPEER, 0); 
        // Add curl_setopt here to grab a proxy from your proxy list so that you don't get 403 errors from your IP being banned by the site
        
        // Grab the data.
        $html = curl_exec($c);
        
        // Check if the HTML didn't load right, if it didn't - report an error
        if (!$html) {
            echo "<p>cURL error number: " .curl_errno($c) . " on URL: " . $url ."</p>" .
                 "<p>cURL error: " . curl_error($c) . "</p>";
        }
        
        // Close connection.
        curl_close($c);
        
        // Parse the HTML information and return the results.
        $dom = new DOMDocument(); 
        @$dom->loadHtml($html);
        
        $xpath = new DOMXPath($dom);
        
        // Get a list of articles from the section page
        //$articleList = $xpath->query("//div[@class='ea-category-list']/ol/li");
        //$articleList = $xpath->query("//div[@class='category-list']/div[@class='article']");
        //$articleList = $xpath->query("/html/body/div[2]/div[2]/table/tbody/tr/td/div[2]/div/div/div/div/div/form/table[3]/tbody/tr/td[2]");
        $articleList = $xpath->query("//table[@id='DataGrid1']/tr/td[2]"); 
        //echo "count of articlelist :". count($articleList);
        //echo ":::::". $articleList->nodeValue;
        // Add each article to the Articles array
        $date1 = "01312012";
        foreach ($articleList as $item){

            echo "domain is:". $item->nodeValue;
            echo "\n";
            $record = array('status'=>$date1, 'dsn' => $item->nodeValue);
            //print_r($record);
            scraperwiki::save_sqlite(array("status","dsn"),$record,"pool");
         
        }
        
        // Check to see if the Next 30 link is active
   
        }
    // End Get Article Urls
    
   
    
    // Start Get Browser User Agent
    private function getUserAgent(){
        // Set an array with different browser user agents
         $agents = array(
                             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; bgft)",
                            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; User-agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; http://bsalsa.com) ; .NET CLR 2.0.50727)",
                            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Orange 8.0; GTB6.3; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Embedded Web Browser from: http://bsalsa.com/; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618; OfficeLiveConnector.1.3; OfficeLivePatch.1.3)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.8) Gecko/20100722 BTRS86393 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0C)",
                            "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)",
                            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
                            "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 3.0.04506.30)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; InfoPath.3; .NET4.0C; .NET4.0E)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E; Zune 4.7; InfoPath.3)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; Zune 4.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; yie8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; Zune 3.0; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; MS-RTC LM 8; Zune 4.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; FDM; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; .NET CLR 1.1.4322)",
                            "Opera/9.99 (Windows NT 5.1; U; pl) Presto/9.9.9",
                            "Opera/9.80 (J2ME/MIDP; Opera Mini/5.0 (Windows; U; Windows NT 5.1; en) AppleWebKit/886; U; en) Presto/2.4.15",
                            "Opera/9.70 (Linux ppc64 ; U; en) Presto/2.2.1",
                            "Opera/9.70 (Linux i686 ; U; zh-cn) Presto/2.2.0",
                            "Opera/9.70 (Linux i686 ; U; en-us) Presto/2.2.0",
                            "Opera/9.70 (Linux i686 ; U; en) Presto/2.2.1",
                            "Opera/9.70 (Linux i686 ; U; en) Presto/2.2.0",
                            "Opera/9.70 (Linux i686 ; U; ; en) Presto/2.2.1",
                            "Opera/9.70 (Linux i686 ; U; ; en) Presto/2.2.1",
                            "Mozilla/5.0 (Linux i686 ; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.70",
                            "Mozilla/4.0 (compatible; MSIE 6.0; Linux i686 ; en) Opera 9.70",
                            "Opera/9.64(Windows NT 5.1; U; en) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; pl) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; hr) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; en-GB) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; en) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; de) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; cs) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; tr) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; sv) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; pl) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; nb) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; Linux Mint; nb) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; Linux Mint; it) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; en) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; de) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; da) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.1; U; MRA 5.5 (build 02842); ru) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.1; U; de) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.0; U; zh-cn) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.0; U; pl) Presto/2.1.1",
                            "Opera 9.7 (Windows NT 5.2; U; en)",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; tr-TR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; da-dk) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                            "Mozilla/5.0 (X11; U; Linux x86_64; en-ca) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; zh-cn) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ru-ru) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ko-kr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/534.1+ (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-au) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; el-gr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ca-es) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-tw) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; fr-fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; es-es) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
                        );
                        
        return $agents[rand(0, (count($agents)-1))];
    }
    // End Get Browser User Agent
}
// End Scraper Class
?><?php
for ($pn = 1; $pn <= 10; $pn++) {
//    echo $pn;
$scrape = new Scraper('http://www.pool.com/viewlist.aspx?Page='.$pn);
}

class Scraper {
    protected $articles = array();
    protected $domain;
    
    // Set actions to run when the class is instantiated
    function __construct($url){
        // Set the maximum execution time of the script to unlimited so that it can grab all the articles if there are a lot of them to scrape
        set_time_limit(0);
        
        // Set the root domain of the URL to concatinate with URLs later
        $this->domain = explode("/", $url);
        $this->domain = 'http://' . $this->domain[2];
        
        // Pass the page URL you want to start scraping and start scraping through the section pages
        $this->getArticleUrls($url);
        
        //echo count($this->articles) . ' - Done counting articles items, now adding articles.';
        
        // Loop through the article pages and grab the full article to finish populating the articles array with data
        foreach ($this->articles as $item){
       // $item['article'] = $this->getArticles($item['url']);
            print_r($item['title']);
        }
        
        //echo count($this->articles) . ' - Done adding articles.';
         
        
        // Add function here to start adding items in the article array with articles to a database
    }
    
    // Start Get Article Urls
    private function getArticleUrls($url){
        // Instantiate next page variable to check at the end
        $nextPageUrl = NULL;
        
        // Instantiate cURL to grab the HTML page.
        $c = curl_init($url);
        curl_setopt($c, CURLOPT_HEADER, false);
        curl_setopt($c, CURLOPT_USERAGENT, $this->getUserAgent());
        curl_setopt($c, CURLOPT_FAILONERROR, true);
        curl_setopt($c, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($c, CURLOPT_AUTOREFERER, true);
        curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($c, CURLOPT_TIMEOUT, 10);
//WARNING: this would prevent curl from detecting a 'man in the middle' attack
curl_setopt ($c, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt ($c, CURLOPT_SSL_VERIFYPEER, 0); 
        // Add curl_setopt here to grab a proxy from your proxy list so that you don't get 403 errors from your IP being banned by the site
        
        // Grab the data.
        $html = curl_exec($c);
        
        // Check if the HTML didn't load right, if it didn't - report an error
        if (!$html) {
            echo "<p>cURL error number: " .curl_errno($c) . " on URL: " . $url ."</p>" .
                 "<p>cURL error: " . curl_error($c) . "</p>";
        }
        
        // Close connection.
        curl_close($c);
        
        // Parse the HTML information and return the results.
        $dom = new DOMDocument(); 
        @$dom->loadHtml($html);
        
        $xpath = new DOMXPath($dom);
        
        // Get a list of articles from the section page
        //$articleList = $xpath->query("//div[@class='ea-category-list']/ol/li");
        //$articleList = $xpath->query("//div[@class='category-list']/div[@class='article']");
        //$articleList = $xpath->query("/html/body/div[2]/div[2]/table/tbody/tr/td/div[2]/div/div/div/div/div/form/table[3]/tbody/tr/td[2]");
        $articleList = $xpath->query("//table[@id='DataGrid1']/tr/td[2]"); 
        //echo "count of articlelist :". count($articleList);
        //echo ":::::". $articleList->nodeValue;
        // Add each article to the Articles array
        $date1 = "01312012";
        foreach ($articleList as $item){

            echo "domain is:". $item->nodeValue;
            echo "\n";
            $record = array('status'=>$date1, 'dsn' => $item->nodeValue);
            //print_r($record);
            scraperwiki::save_sqlite(array("status","dsn"),$record,"pool");
         
        }
        
        // Check to see if the Next 30 link is active
   
        }
    // End Get Article Urls
    
   
    
    // Start Get Browser User Agent
    private function getUserAgent(){
        // Set an array with different browser user agents
         $agents = array(
                             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; bgft)",
                            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; User-agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; http://bsalsa.com) ; .NET CLR 2.0.50727)",
                            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Orange 8.0; GTB6.3; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Embedded Web Browser from: http://bsalsa.com/; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618; OfficeLiveConnector.1.3; OfficeLivePatch.1.3)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.8) Gecko/20100722 BTRS86393 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0C)",
                            "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)",
                            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
                            "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 3.0.04506.30)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; InfoPath.3; .NET4.0C; .NET4.0E)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E; Zune 4.7; InfoPath.3)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; Zune 4.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; yie8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; Zune 3.0; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; MS-RTC LM 8; Zune 4.0)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
                            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; FDM; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; .NET CLR 1.1.4322)",
                            "Opera/9.99 (Windows NT 5.1; U; pl) Presto/9.9.9",
                            "Opera/9.80 (J2ME/MIDP; Opera Mini/5.0 (Windows; U; Windows NT 5.1; en) AppleWebKit/886; U; en) Presto/2.4.15",
                            "Opera/9.70 (Linux ppc64 ; U; en) Presto/2.2.1",
                            "Opera/9.70 (Linux i686 ; U; zh-cn) Presto/2.2.0",
                            "Opera/9.70 (Linux i686 ; U; en-us) Presto/2.2.0",
                            "Opera/9.70 (Linux i686 ; U; en) Presto/2.2.1",
                            "Opera/9.70 (Linux i686 ; U; en) Presto/2.2.0",
                            "Opera/9.70 (Linux i686 ; U; ; en) Presto/2.2.1",
                            "Opera/9.70 (Linux i686 ; U; ; en) Presto/2.2.1",
                            "Mozilla/5.0 (Linux i686 ; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.70",
                            "Mozilla/4.0 (compatible; MSIE 6.0; Linux i686 ; en) Opera 9.70",
                            "Opera/9.64(Windows NT 5.1; U; en) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; pl) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; hr) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; en-GB) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; en) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; de) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux x86_64; U; cs) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; tr) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; sv) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; pl) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; nb) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; Linux Mint; nb) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; Linux Mint; it) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; en) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; de) Presto/2.1.1",
                            "Opera/9.64 (X11; Linux i686; U; da) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.1; U; MRA 5.5 (build 02842); ru) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.1; U; de) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.0; U; zh-cn) Presto/2.1.1",
                            "Opera/9.64 (Windows NT 6.0; U; pl) Presto/2.1.1",
                            "Opera 9.7 (Windows NT 5.2; U; en)",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; tr-TR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; da-dk) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                            "Mozilla/5.0 (X11; U; Linux x86_64; en-ca) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; zh-cn) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ru-ru) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ko-kr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/534.1+ (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-au) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; el-gr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ca-es) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-tw) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; fr-fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
                            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; es-es) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16"
                        );
                        
        return $agents[rand(0, (count($agents)-1))];
    }
    // End Get Browser User Agent
}
// End Scraper Class
?>