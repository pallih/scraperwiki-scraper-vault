#!/usr/bin/php
<?php
error_reporting(E_ALL);
/* This code is free to use and modify as long as this comment is untouched
 * Original source and details: http://tdb.squabbel.com
 */
 
// ************************* Configuration variables *************************
// Your seo-proxies api credentials
$pwd="9fdbff13867303a9c774ae09ef46f76c";  // Your www.seo-proxies.com API password
$uid=7;                                   // Your www.seo-proxies.com API userid
// The  main keyword and additional sub keywords for the scraping
$main_keyword="inurl:forum";              // The main keyword
$extra_keywords="+phpbb,+hot,+games,+guns,+movie"; // alternatives to mix in to receive more than the average 1000 results from Google
$show_html=1;                             // Output either for console or in html for a website (0 / 1)
$max_results=10;                                                    // Stop script after a specific number of scraped search results
// ***************************************************************************


require "functions.php";



$page=0;
$PROXY=array();                                                        // after rotate api call it has the elements: [address](proxy host),[port](proxy port),[external_ip](the external IP),[ready](0/1)
$results=array();

if ($show_html) $NL="<br>\n"; else $NL="\n";
if ($show_html) $HR="<hr>\n"; else $HR="---------------------------------------------------------------------------------------------------\n";
if ($show_html) $B="<b>"; else $B="";
if ($show_html) $B_="</b>"; else $B_="";


/*
 * Start of main()
 */
 
if ($show_html)
{
    echo "<html><body>";
}

$keywords=explode(",",$extra_keywords);


echo "$NL$B Scraping max. $max_results results for the main keyword \"$main_keyword\" using ".count($keywords)." additional keywords $B_ $NL$NL";

/*
 * This loop iterates through all keyword combinations
 */
$ch=NULL;
foreach($keywords as $keyword)
{
    if ($max_results<=0) break;
    $search_string=urlencode($main_keyword." ".$keyword);


    // force new curl session
    
    echo "$NL";
    echo "===========================================================================================================================$NL";
    echo "Scraping for \"$main_keyword $keyword\" $NL";
    echo "===========================================================================================================================$NL";
    echo "$NL";


    $runs=0;
    $res=proxy_api("rotate");
    $ip="";
    if ($res <= 0)
    {
        echo "Error: Proxy API connection failed (Error $res).$NL$NL$NL";
        sleep(2);
        break;
    } else
    {
        echo "API: Received proxy IP $PROXY[external_ip] on port $PROXY[port]$NL";
    }
    $ch=new_curl_session($ch);
    


    $errors=0;
    $ip="";
    /*
     * This loop iterates through all available google result pages
     */
    while (1)
    {
        if ($max_results<=0) break;
        $runs++;
        echo "Run $runs \t Page $page \t loading$NL";
        if ((!$ip) || ($ip == ""))
            $ip=getip($ch);            // Test of the external IP and if the current proxy is ready
        if ((!$ip) || ($ip == ""))     // If the proxy didn't work: rotate to next proxy
        {
            echo "Proxy is not working, rotating ..$NL";
            
            $res=proxy_api("rotate");
            $ip="";
            if ($res <= 0)
            {
                echo "Error: API connection failed (Error $res), retry.$NL$NL$NL";
                sleep (10);
                continue;
            } else
            {
                echo "API: Received proxy IP $PROXY[external_ip] on port $PROXY[port]$NL";
            }
            
            $ch=new_curl_session($ch);
            continue;

        }
        
        echo "Current tested IP-Address: $ip$NL$NL";


        $google_ip="www.google.com"; // hidden potential left
        if ($page == 0)
        {
            // we imitate a firefox browser search and will query for 100 results
            $url="http://$google_ip/search?q=$search_string&amp;ie=utf-8&as_qdr=all&amp;aq=t&amp;rls=org:mozilla:us:official&amp;client=firefox&num=100";
        } else
        {
            $num=$page*100;
            $url="http://$google_ip/search?q=$search_string&ie=utf-8&as_qdr=all&aq=t&rls=org:mozilla:us:official&client=firefox&start=$num&num=100";
        }
        echo "Search URL: $url$NL";
        
        curl_setopt ($ch, CURLOPT_URL, $url);
        $htmdata = curl_exec ($ch);
        $newtry=0;
        if (!$htmdata)
        {
            $error = curl_error($ch);
            $info = curl_getinfo($ch);        
            echo "\tError browsing: $error [ $info ]$NL";
            sleep (3);
            $newtry=1;
        }
        if (strstr($htmdata,"computer virus or spyware application")) 
        {
            echo("Captcha error is popping up ! We need more proxies !");
            die();
            $newtry=1;
        }
        if (strstr($htmdata,"entire network is affected")) 
        {
            echo("Google blocked us, we need more proxies !$NL");
            die();
            $newtry=1;
        }    
        if (strstr($htmdata,"http://www.download.com/Antivirus")) 
        {
            echo("Google blocked us, we need more proxies !$NL");
            die();
            $newtry=1;
        }

        if ($newtry)
        {
            if ($errors++ > 3)
            {
                echo "Abort: too many google errors! $NL$NL";
                sleep(5);
                break;
            }
    
            $res=proxy_api("rotate");
            $ip="";
            if ($res <= 0)
            {
                echo "Error: API connection failed (Error $res), retry.$NL$NL$NL";
                sleep (10);
            } else
            {
                echo "API: Received proxy IP $PROXY[external_ip] on port $PROXY[port]$NL";
            }
            echo "Rotated IP and retrying$NL";
            $ch=new_curl_session($ch);
            continue;
        }
        $skip=0;
        // now we test if (more) results are available
        if (strstr($htmdata,"/images/yellow_warning.gif"))
        {
            echo "No (more) results left$NL";
            $skip=1;
        }
        if (!$skip)
        {
            $len=strlen($htmdata);
         echo "\t Received $len bytes$NL";
        // Now we parse the html content, putting it into a DOM tree
            $dom = new domDocument; 
            $dom->strictErrorChecking = false; 
            $dom->preserveWhiteSpace = true; 
            @$dom->loadHTML($htmdata); 
            $lists=$dom->getElementsByTagName('li'); 
           $num=0;
            
            foreach ($lists as $list)
            {
                unset($ar);unset($divs);unset($div);unset($cont);unset($result);unset($tmp);
                $result['main_keyword']=$main_keyword;
                $result['sub_keyword']=$keyword;
                $ar=dom2array_full($list);                
                if (count($ar) < 2) 
                {
                    echo "S";
                    continue; // skipping advertisement and similar spam
                }
                 if ((!isset($ar['class'])) || ($ar['class'] != 'g')) 
                {
                    echo "?";
                    continue; // skipping non-search results
                }
                // adaption to new google layout
//if ($num==2)var_dump($ar);
//if ($num==3)var_dump($ar);

                if (isset($ar['div'][1]))
                    $ar['div']=&$ar['div'][0];
                if (isset($ar['div'][1]))
                    $ar['div']=&$ar['div'][0];
                //$ar=&$ar['div']['span']; // Google removed the span
                $ar=&$ar['div'];
                // adaption finished

                $divs=$list->getElementsByTagName('div');
                $div=$divs->item(1);
                getContent($cont,$div);    
                $num++;
                $result['title']=&$ar['h3']['a']['textContent'];
                $tmp=strstr(&$ar['h3']['a']['@attributes']['href'],"http");
                $result['url']=$tmp;
                if (strstr(&$ar['h3']['a']['@attributes']['href'],"interstitial")) echo "!";
                
                $tmp=parse_url(&$result['url']);
                $result['host']=&$tmp['host'];
                if (strstr($cont,"<b >...</b><br >")) // remove some dirt behind the description
                {
                    $result['desc']=substr($cont,0,strpos($cont,"<b >...</b><br >"));
                } else
                if (strstr($cont,"<cite")) // remove some dirt behind the description in case the description was short
                {
                    $result['desc']=substr($cont,0,strpos($cont,"<span class='f'><cite"));
                } else
                    $result['desc']=$cont;
            
                echo "$B Result parsed:$B_ $result[title]$NL";
                flush();                    
                $results[]=$result; // This adds the result to our large result array
                if (!--$max_results) break;
            }
        }
        
        // Test if more results are available
        $next=0;
        if (!$skip)
        {
            $tables=$dom->getElementsByTagName('table');
            if (strstr($htmdata,"Next</a>")) $next=1;
            else
            {
                $needstart=($page+1)*100;
                $findstr="start=$needstart";
                if (strstr($htmdata,$findstr)) $next=1;
            }
            $page++;
        }

        if (!$next)
        {
            echo("Finished $runs runs on current search, last google page was $page$NL");
            break;
        }

    }
}



/* Instead of just outputting the data it might be more useful to put it into a database ? */
echo "$NL$NL";
echo "$B Scraping of keywords finished$B_ $NL";
foreach ($results as $result)
{
    echo $HR;
    echo "$B Keyword:$B_ $result[main_keyword] $result[sub_keyword]$NL";
    echo "$B Host:$B_ $result[host]$NL";
    echo "$B URL:$B_ $result[url]$NL";
    echo "$B Title:$B_ $result[title]$NL";
    echo "$B Desc:$B_ $result[desc]$NL";
    echo $NL;
}

if ($show_html)
{
    echo "</body></html>";
}



?>#!/usr/bin/php
<?php
error_reporting(E_ALL);
/* This code is free to use and modify as long as this comment is untouched
 * Original source and details: http://tdb.squabbel.com
 */
 
// ************************* Configuration variables *************************
// Your seo-proxies api credentials
$pwd="9fdbff13867303a9c774ae09ef46f76c";  // Your www.seo-proxies.com API password
$uid=7;                                   // Your www.seo-proxies.com API userid
// The  main keyword and additional sub keywords for the scraping
$main_keyword="inurl:forum";              // The main keyword
$extra_keywords="+phpbb,+hot,+games,+guns,+movie"; // alternatives to mix in to receive more than the average 1000 results from Google
$show_html=1;                             // Output either for console or in html for a website (0 / 1)
$max_results=10;                                                    // Stop script after a specific number of scraped search results
// ***************************************************************************


require "functions.php";



$page=0;
$PROXY=array();                                                        // after rotate api call it has the elements: [address](proxy host),[port](proxy port),[external_ip](the external IP),[ready](0/1)
$results=array();

if ($show_html) $NL="<br>\n"; else $NL="\n";
if ($show_html) $HR="<hr>\n"; else $HR="---------------------------------------------------------------------------------------------------\n";
if ($show_html) $B="<b>"; else $B="";
if ($show_html) $B_="</b>"; else $B_="";


/*
 * Start of main()
 */
 
if ($show_html)
{
    echo "<html><body>";
}

$keywords=explode(",",$extra_keywords);


echo "$NL$B Scraping max. $max_results results for the main keyword \"$main_keyword\" using ".count($keywords)." additional keywords $B_ $NL$NL";

/*
 * This loop iterates through all keyword combinations
 */
$ch=NULL;
foreach($keywords as $keyword)
{
    if ($max_results<=0) break;
    $search_string=urlencode($main_keyword." ".$keyword);


    // force new curl session
    
    echo "$NL";
    echo "===========================================================================================================================$NL";
    echo "Scraping for \"$main_keyword $keyword\" $NL";
    echo "===========================================================================================================================$NL";
    echo "$NL";


    $runs=0;
    $res=proxy_api("rotate");
    $ip="";
    if ($res <= 0)
    {
        echo "Error: Proxy API connection failed (Error $res).$NL$NL$NL";
        sleep(2);
        break;
    } else
    {
        echo "API: Received proxy IP $PROXY[external_ip] on port $PROXY[port]$NL";
    }
    $ch=new_curl_session($ch);
    


    $errors=0;
    $ip="";
    /*
     * This loop iterates through all available google result pages
     */
    while (1)
    {
        if ($max_results<=0) break;
        $runs++;
        echo "Run $runs \t Page $page \t loading$NL";
        if ((!$ip) || ($ip == ""))
            $ip=getip($ch);            // Test of the external IP and if the current proxy is ready
        if ((!$ip) || ($ip == ""))     // If the proxy didn't work: rotate to next proxy
        {
            echo "Proxy is not working, rotating ..$NL";
            
            $res=proxy_api("rotate");
            $ip="";
            if ($res <= 0)
            {
                echo "Error: API connection failed (Error $res), retry.$NL$NL$NL";
                sleep (10);
                continue;
            } else
            {
                echo "API: Received proxy IP $PROXY[external_ip] on port $PROXY[port]$NL";
            }
            
            $ch=new_curl_session($ch);
            continue;

        }
        
        echo "Current tested IP-Address: $ip$NL$NL";


        $google_ip="www.google.com"; // hidden potential left
        if ($page == 0)
        {
            // we imitate a firefox browser search and will query for 100 results
            $url="http://$google_ip/search?q=$search_string&amp;ie=utf-8&as_qdr=all&amp;aq=t&amp;rls=org:mozilla:us:official&amp;client=firefox&num=100";
        } else
        {
            $num=$page*100;
            $url="http://$google_ip/search?q=$search_string&ie=utf-8&as_qdr=all&aq=t&rls=org:mozilla:us:official&client=firefox&start=$num&num=100";
        }
        echo "Search URL: $url$NL";
        
        curl_setopt ($ch, CURLOPT_URL, $url);
        $htmdata = curl_exec ($ch);
        $newtry=0;
        if (!$htmdata)
        {
            $error = curl_error($ch);
            $info = curl_getinfo($ch);        
            echo "\tError browsing: $error [ $info ]$NL";
            sleep (3);
            $newtry=1;
        }
        if (strstr($htmdata,"computer virus or spyware application")) 
        {
            echo("Captcha error is popping up ! We need more proxies !");
            die();
            $newtry=1;
        }
        if (strstr($htmdata,"entire network is affected")) 
        {
            echo("Google blocked us, we need more proxies !$NL");
            die();
            $newtry=1;
        }    
        if (strstr($htmdata,"http://www.download.com/Antivirus")) 
        {
            echo("Google blocked us, we need more proxies !$NL");
            die();
            $newtry=1;
        }

        if ($newtry)
        {
            if ($errors++ > 3)
            {
                echo "Abort: too many google errors! $NL$NL";
                sleep(5);
                break;
            }
    
            $res=proxy_api("rotate");
            $ip="";
            if ($res <= 0)
            {
                echo "Error: API connection failed (Error $res), retry.$NL$NL$NL";
                sleep (10);
            } else
            {
                echo "API: Received proxy IP $PROXY[external_ip] on port $PROXY[port]$NL";
            }
            echo "Rotated IP and retrying$NL";
            $ch=new_curl_session($ch);
            continue;
        }
        $skip=0;
        // now we test if (more) results are available
        if (strstr($htmdata,"/images/yellow_warning.gif"))
        {
            echo "No (more) results left$NL";
            $skip=1;
        }
        if (!$skip)
        {
            $len=strlen($htmdata);
         echo "\t Received $len bytes$NL";
        // Now we parse the html content, putting it into a DOM tree
            $dom = new domDocument; 
            $dom->strictErrorChecking = false; 
            $dom->preserveWhiteSpace = true; 
            @$dom->loadHTML($htmdata); 
            $lists=$dom->getElementsByTagName('li'); 
           $num=0;
            
            foreach ($lists as $list)
            {
                unset($ar);unset($divs);unset($div);unset($cont);unset($result);unset($tmp);
                $result['main_keyword']=$main_keyword;
                $result['sub_keyword']=$keyword;
                $ar=dom2array_full($list);                
                if (count($ar) < 2) 
                {
                    echo "S";
                    continue; // skipping advertisement and similar spam
                }
                 if ((!isset($ar['class'])) || ($ar['class'] != 'g')) 
                {
                    echo "?";
                    continue; // skipping non-search results
                }
                // adaption to new google layout
//if ($num==2)var_dump($ar);
//if ($num==3)var_dump($ar);

                if (isset($ar['div'][1]))
                    $ar['div']=&$ar['div'][0];
                if (isset($ar['div'][1]))
                    $ar['div']=&$ar['div'][0];
                //$ar=&$ar['div']['span']; // Google removed the span
                $ar=&$ar['div'];
                // adaption finished

                $divs=$list->getElementsByTagName('div');
                $div=$divs->item(1);
                getContent($cont,$div);    
                $num++;
                $result['title']=&$ar['h3']['a']['textContent'];
                $tmp=strstr(&$ar['h3']['a']['@attributes']['href'],"http");
                $result['url']=$tmp;
                if (strstr(&$ar['h3']['a']['@attributes']['href'],"interstitial")) echo "!";
                
                $tmp=parse_url(&$result['url']);
                $result['host']=&$tmp['host'];
                if (strstr($cont,"<b >...</b><br >")) // remove some dirt behind the description
                {
                    $result['desc']=substr($cont,0,strpos($cont,"<b >...</b><br >"));
                } else
                if (strstr($cont,"<cite")) // remove some dirt behind the description in case the description was short
                {
                    $result['desc']=substr($cont,0,strpos($cont,"<span class='f'><cite"));
                } else
                    $result['desc']=$cont;
            
                echo "$B Result parsed:$B_ $result[title]$NL";
                flush();                    
                $results[]=$result; // This adds the result to our large result array
                if (!--$max_results) break;
            }
        }
        
        // Test if more results are available
        $next=0;
        if (!$skip)
        {
            $tables=$dom->getElementsByTagName('table');
            if (strstr($htmdata,"Next</a>")) $next=1;
            else
            {
                $needstart=($page+1)*100;
                $findstr="start=$needstart";
                if (strstr($htmdata,$findstr)) $next=1;
            }
            $page++;
        }

        if (!$next)
        {
            echo("Finished $runs runs on current search, last google page was $page$NL");
            break;
        }

    }
}



/* Instead of just outputting the data it might be more useful to put it into a database ? */
echo "$NL$NL";
echo "$B Scraping of keywords finished$B_ $NL";
foreach ($results as $result)
{
    echo $HR;
    echo "$B Keyword:$B_ $result[main_keyword] $result[sub_keyword]$NL";
    echo "$B Host:$B_ $result[host]$NL";
    echo "$B URL:$B_ $result[url]$NL";
    echo "$B Title:$B_ $result[title]$NL";
    echo "$B Desc:$B_ $result[desc]$NL";
    echo $NL;
}

if ($show_html)
{
    echo "</body></html>";
}



?>