<?php
/* =======================================
 * Adjust Parameters below
 * ======================================= */

/* Total number of results */
    $total = 10;

/* Results per SERP */
$perPage = 10;

/* Google URL to use*/
$googleUrl = "http://www.google.mx";

/* Paste 1 Keyword per line */

/*
$kws = <<<EOS
site:http://cleanfiles.net/?
EOS;
*/

$kws = <<<EOS
fuck the world
EOS;


/* =======================================
 * DO NOT CHANGE ANYTHING BELOW THIS LINE! 
 * ======================================= */

$today = date("Y-m-d");

$kws = explode("\n",$kws);

function DecodeData($curInput, array $headers)
    {
        $result = $curInput;
        //
        // first see if content length header has charset = value
        //
        $charset = "";
        $ctype = (isset($headers["content-type"])?$headers["content-type"]:"");
        if ($ctype != "")
        {
            $c = "charset=";
            $ind = strpos($ctype, $c);
            if ($ind !== false)
            {
                $charset = substr($ctype, $ind + strlen($c));
            }
        }
        $charsetEncname = $charset;

        //
        // we search in the body
        //
        //<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
        $pattern = "#<meta[^>]+content=[\"'][^\"']*charset=(?P<charset>[^\"']+)[\"'][^>]*>#Ui";
        preg_match($pattern, $result, $match);
        $meta = (isset($match["charset"])?$match["charset"]:"");
        
        $metaEncname = $meta;

        $internalEncoding = mb_internal_encoding();

        if($charsetEncname != ""){
            // check if we even have to convert anything
            if($charsetEncname != $internalEncoding){
                $result = mb_convert_encoding($result, $internalEncoding, $charsetEncname);
            }
        }
        elseif($metaEncname != ""){
            if($metaEncname != $internalEncoding){
                $result = mb_convert_encoding($result, $internalEncoding, $metaEncname);
            }
        }
        return $result;
    }

function IsValidURL($url) {
        $parts = parse_url($url);
        return (array_key_exists("scheme", $parts) && array_key_exists("host", $parts));
    }

function ToEncodedParamString(array $datas){
        $returns = array();

        foreach($datas as $key => $value) {
            if(is_array($value)){
                $i = 0;
                $result = "";
                foreach($value as $v){
                    $result .= rawurlencode($key."[]"). "=".rawurlencode($v);
                    if($i < count($value)-1)
                    $result.= "&";
                    $i++;
                }
                $returns[] = $result;
            }
            else{
                $returns[] = rawurlencode($key) .'='. rawurlencode($value);
            }

        }
        $res = implode('&', $returns);
        return $res;
    }

function AppendParamString($url, $paramString){

        $qmIdx = strrpos($url, "?");
        if($qmIdx === false)
        return $url."?".$paramString; // $url has no parameters
        if($qmIdx == (strlen($url)-1))
        return $url.$paramString; // $url ends with ?
        $asIdx = strrpos($url, "&");
        if($asIdx == (strlen($url)-1))
        return $url.$paramString; // $url ends with &
        return $url."&".$paramString; // $url has already parameters
    }

function BuildQueryList($keyword, $amount, $perPage, $queryString)
    {
        $queryUrl = BuildQueryUrl($keyword, $perPage, -1, $queryString);
        $queries = array();
        $queries[] = $queryUrl;
        $iterations = floor(($amount / $perPage));
        for ($i = 1; $i < $iterations; $i++)
        {
            $queries[] = BuildQueryUrl($keyword, $perPage, $i * $perPage, $queryString);
        }
        return $queries;
    }

    function BuildQueryUrl($keyword, $perPage, $pageNumber, $queryString) {
        $params = array();
         
        // add keyword
        $params["q"] = $keyword;
        if ($perPage > 1)
        $params["num"] = $perPage;
        if ($pageNumber > 0)
        $params["start"] = $pageNumber;
         
        $paramString = ToEncodedParamString($params);
        $queryUrl = AppendParamString($queryString, $paramString);
        return $queryUrl;
    }


function myexplode($delimiter, $string, $removeEmptyEntries){
        if(!$removeEmptyEntries)
        return explode($delimiter, $string);

        $regExDel = "/";
        $delimiter = preg_quote($delimiter, $regExDel);
        $pattern = $regExDel.$delimiter.$regExDel;
        return preg_split($pattern, $string, -1, PREG_SPLIT_NO_EMPTY);
}

function endsWith($haystack, $needle)
{
    $length = strlen($needle);
    $start  = $length * -1; //negative
    return (substr($haystack, $start) === $needle);
}

function GetQueryParameters($url) {
    $params = array();
    $parsedUrl = parse_url(trim($url));
    if(!isset($parsedUrl["query"]))
    return $params;
    $query = $parsedUrl["query"];
    $query = trim($query);
    if($query == "")
    return $params;
    $queryParts = explode('&', $query);

    foreach ($queryParts as $param) {
        $item = myexplode('=', $param, true);
        $key = urldecode($item[0]);
        $value = (isset($item[1])?urldecode($item[1]):"");
        if(endsWith($key, "[]")){
            $key = substr($key, 0, strlen($key)-2);
            if(!array_key_exists($key, $params))
            $params = array();
            $params[$key][] = $value;
        }
        else{
            $params[$key] = $value;
        }
    }

    return $params;
}

function rel2abs($rel, $base)
{
    if (parse_url($rel, PHP_URL_SCHEME) != '')
    return $rel;
    else if ($rel[0] == '#' || $rel[0] == '?')
    return $base.$rel;

    //temporary save the params
    $firstQuestionmark = strpos($rel, "?");
    $params ="";
    if($firstQuestionmark !== false){
        $params = substr($rel, $firstQuestionmark);
        $rel = substr($rel, 0, $firstQuestionmark);
    }

    $parsed = parse_url($base);
   
    $scheme = isset($parsed["scheme"])?$parsed["scheme"]:"";
    $host = isset($parsed["host"])?$parsed["host"]:"";;
    $port = isset($parsed["port"])?$parsed["port"]:"";;
    $user = isset($parsed["user"])?$parsed["user"]:"";;
    $pass = isset($parsed["pass"])?$parsed["pass"]:"";;
    $path = isset($parsed["path"])?$parsed["path"]:"";
    $query = isset($parsed["query"])?$parsed["query"]:"";;
    $fragment = isset($parsed["fragment"])?$parsed["fragment"]:"";;

    $abs = ($rel[0] == '/' ? '' : preg_replace('#/[^/]*$#', '', $path) );
    $abs .= "/".$rel;
    $re  = array('#(/\.?/)#', '#/(?!\.\.)[^/]+/\.\./#');

    for ($n = 1; $n > 0; $abs = preg_replace($re, '/', $abs, -1, $n));
    return $scheme.'://'.$host.str_replace('../', '', $abs).$params;
}

foreach($kws as $kw){
$urls = BuildQueryList($kw, $total, $perPage, $googleUrl);
$scrapedUrls = array();
foreach($urls as $url){
$urlToScrape = $url;
//$urlToScrape = "http://www.ipv6proxy.net/go.php?u=".urlencode($url);
$html = scraperWiki::scrape($urlToScrape);
echo $html;
$html = DecodeData($html,array());
$doc = new DOMDocument();
libxml_use_internal_errors(TRUE);
$doc->loadHTML($html);
libxml_use_internal_errors(FALSE);
$xpath = new DOMXpath($doc);

$links = $xpath->query(".//a[@class='l']/@href");
if($links->length != 0)
{
    foreach($links as $link){
        $scrapedUrls[] = $link->nodeValue;
    }
}
else{
    $links = $xpath->query(".//h3[@class='r']/a/@href");
    foreach($links as $link){
        $theLink = $link->nodeValue;
        $theLink = rel2abs($theLink,$url);
        $parts = GetQueryParameters(trim($theLink));
        $foundUrl = "EMPTY";
        if(isset($parts['url'])){
            $foundUrl = urldecode($parts['url']);
        }elseif(isset($parts['q'])){
            $foundUrl = urldecode($parts['q']);           
        }
  
        if(isValidUrl($foundUrl)){
            //$converter = new idna_convert(); << used to decode punycode
            //$foundUrl = $converter->decode($foundUrl); << used to decode punycode
            $scrapedUrls[] = $foundUrl;
            //echo "\n$foundUrl\t$theLink\n";
        }
        
    }
}
}
echo "\nKeyword $kw done!\n";
$records = array();
foreach($scrapedUrls as $p => $u){
    echo "$u\n";
    $records[] = array("Date"=> $today, "Keyword" => $kw, "Position" => $p+1, "URL" => $u);
}
scraperwiki::save_sqlite(array("Date","Keyword","Position"),$records);
}
?>



