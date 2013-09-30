<?php
/*
//scraperwiki::sqliteexecute("delete from `links`");
scraperwiki::sqliteexecute("insert into `links` values (?,?,?,?,?,?,?,?,?,?,?)", array('http://www.economist.com/', 0,'','','',0,'','','','',''));
    scraperwiki::sqlitecommit();
*/

global $current;
global $dbh;

$i = 0;
  set_time_limit(0);
//functia curl de procesare in paralel
function curl($link,&$master)
{
  // atentie la functia asta daca aveti safe mode on nu functioneaza

    //cream linkul
    $cr = curl_init($link);
    curl_setopt($cr,CURLOPT_HEADER,true);
    curl_setopt($cr,CURLOPT_CONNECTTIMEOUT,2);
    curl_setopt($cr,CURLOPT_FOLLOWLOCATION,true);
    curl_setopt($cr,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($cr, CURLOPT_USERAGENT, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729'); 
    curl_setopt($cr,CURLOPT_TIMEOUT,2);
    //il adaugam la masterul multi-curl
    curl_multi_add_handle($master, $cr);
    return $cr;
}
function getIp($link)
{
    $temp = parse_url($link);
    $ip = gethostbyname($temp['host']);  //record
    if (!empty($ip))
    {
        //$addr = gethostbyaddr($ip);  //record  hosting
        $addr = exec('host '.$ip);
        echo $addr."\n";
    }
    $records = dns_get_record ($temp['host']);    //record dns records
    $output['ip'] = $ip;
    $output['dns'] = $addr;
    $output['records'] = $records;
    return $output;
}
function getInfo($content)
{

    preg_match('/<title[^>]*>(.*?)<\/title[^>]*>/iU',$content,$output);
    $result['title'] = strip_tags($output[1]);
    preg_match('/<meta[\s]+[^>]*?name[\s]?=[\s\"\']description[\s\"\']+content[\s]?=[\s\"\']+(.*?)[\"\']+.*?>/miU',$content,$output);
    $result['description'] = strip_tags($output[1]);
    preg_match('/<meta[\s]+[^>]*?name[\s]?=[\s\"\']keywords[\s\"\']+content[\s]?=[\s\"\']+(.*?)[\"\']+.*?>/miU',$content,$output);
    $result['keywords'] = strip_tags($output[1]);
    return $result;
}

function getDensity($content)
{

    global $current;
    
    $find = get_html_translation_table(HTML_ENTITIES, ENT_QUOTES);
    
    preg_match('/<body[^>]*>(.*?)<\/body>/smi',$content,$match);
    if (isset($match[1])) $content = $match[1];
    $content=preg_replace('/<script[^>]*>.*?<\/script>/is','',$content);
    $content=preg_replace('/\s\s+/', ' ', $content);
    $content = str_replace($find,'',$content);
    
    $content = strip_tags($content);
    $current = explode(" ",$content);
    $found = array();
    foreach($current as $word)
    {
        if (!empty($word) && strlen(trim($word)) > 4)
        {
            $found["'".trim(strip_tags($word))."'"] ++;
        }
    }
    asort($found);
    $output['count'] = count($found);                //record keyword count
    $output['keywords'] = array_slice($found,-20);        //record keyword density
    return $output;
}
function getHeader($header)
{

    global $current;
    $header = explode("\n",$header);    //record
    if (is_array($header) && count($header))
    {
        return implode("\n",$header);
    }
    else
    {
        return '';
    }
    
    
}
function saveData($input)
{
print_r($input);exit;
  /*  $replace = array(
        ':title'=>$input['info']['title'],
        ':description'=>$input['info']['description'],
        ':keywords'=>$input['info']['keywords'],
        ':kcount'=>$input['density']['count'],
        ':density'=>base64_encode(serialize($input['density']['keywords'])),
        ':headers'=>$input['header'],
        ':ip'=>$input['ip']['ip'],
        ':dns'=>$input['ip']['dns'],
        ':records'=>base64_encode(serialize($input['ip']['records'])),
    );

    scraperwiki::sqliteexecute('UPDATE `links` SET `status` = 1,`title`=:title, `description`=:description, `keywords`=:keywords, `kcount`=:kcount, `density`=:density, `headers`=:headers, `ip`=:ip, `dns`=:dns, `records`=:records WHERE `url`=":url"',$replace);
    scraperwiki::sqlitecommit();
*/

}
function closeLink($id)
{

    scraperwiki::sqliteexecute('UPDATE `links` SET `status` = 1 WHERE `url`="'.$id.'"');
    scraperwiki::sqlitecommit();
}
function getUrl($body)
{

    global $dbh;
    global $current;
    
    $flag = false;
        
    $output = array();
    $regexp = "<a\s[^>]*href=(\"??)([http|https][^\" >]*?)\\1[^>]*>(.*)<\/a>";
    preg_match_all("/$regexp/siU",$body,$output);

    if (is_array($output[2]))
    {
        foreach($output[2] as $value)
        {
            $temp = parse_url($value);
            if (isset($temp['scheme']) && isset($temp['host']))
            {
                $url = $temp['scheme'].'://'.$temp['host'].'/';        //record
                if ($url != $current) 
                {
                    $flag = true;
                    try{
                        //scraperwiki::sqliteexecute("insert into `links` values (?,?,?,?,?,?,?,?,?,?,?)", array($url, 0,'','','',0,'','','','',''));
                    }
                    catch (Exception $e) {};
                }
            }
        }
    }
//scraperwiki::sqlitecommit();
}


$curl_arr = array();
$master = curl_multi_init(); //initiem multi curl
$i = 0;
    $finalresult = array();
    $returnedOrder = array();
    do{
            if (!count($curl_arr) && !count($links))
            {
                $links = scraperwiki::sqliteexecute("select * from `links`");
                $links = $links->data;
                echo "gather" . "\n";
            }
            echo "1";
            //extragem contentul
            if (count($curl_arr) < 10 && count($links))
            {
                $link = array_pop($links);
                $curl_arr[$i] = curl($link[0],$master);
                $tlinks[$i] = $link[0];
                $i++;
            }
            curl_multi_exec($master, $running);
            $info = curl_multi_info_read($master);
            if($info['handle']) 
            {
                $content = curl_multi_getcontent($info['handle']);
                
                $found = array_search($info['handle'], $curl_arr, true);
                $current = $tlinks[$found];
                
                if (!empty($content)) 
                {
                    if (strpos($content, "\r\n\r\n") > 0) // has header
                    {
                        $tcontent = explode("\r\n\r\n", $content);
                        $header = $tcontent[0];
                        $body = $tcontent[1];
                        $fheader = getHeader($header);
                    }
                    else
                    {
                        $body = $response;
                        $fheader = '';
                    }
                    
                    echo $current . "\n";
                    
                    getUrl($body);
                    $fdensity = getDensity($body);
                    $fip = getIp($tlinks[$found]);
                    $finfo = getInfo($body);
                    
                    $input = array();
                    $input['header'] = $fheader;
                    $input['density'] = $fdensity;
                    $input['ip'] = $fip;
                    $input['info'] = $finfo;
                    saveData($input);
exit;
                }
                else
                {
                    closeLink($current);
                }
                curl_multi_remove_handle($master, $info['handle']);
                curl_close($curl_arr[$found]);
                
                unset($curl_arr[$found]);
                unset($tlinks[$found]);
            }
        usleep(1000);
    }
    while(1);
curl_multi_close($master);


<?php
/*
//scraperwiki::sqliteexecute("delete from `links`");
scraperwiki::sqliteexecute("insert into `links` values (?,?,?,?,?,?,?,?,?,?,?)", array('http://www.economist.com/', 0,'','','',0,'','','','',''));
    scraperwiki::sqlitecommit();
*/

global $current;
global $dbh;

$i = 0;
  set_time_limit(0);
//functia curl de procesare in paralel
function curl($link,&$master)
{
  // atentie la functia asta daca aveti safe mode on nu functioneaza

    //cream linkul
    $cr = curl_init($link);
    curl_setopt($cr,CURLOPT_HEADER,true);
    curl_setopt($cr,CURLOPT_CONNECTTIMEOUT,2);
    curl_setopt($cr,CURLOPT_FOLLOWLOCATION,true);
    curl_setopt($cr,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($cr, CURLOPT_USERAGENT, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729'); 
    curl_setopt($cr,CURLOPT_TIMEOUT,2);
    //il adaugam la masterul multi-curl
    curl_multi_add_handle($master, $cr);
    return $cr;
}
function getIp($link)
{
    $temp = parse_url($link);
    $ip = gethostbyname($temp['host']);  //record
    if (!empty($ip))
    {
        //$addr = gethostbyaddr($ip);  //record  hosting
        $addr = exec('host '.$ip);
        echo $addr."\n";
    }
    $records = dns_get_record ($temp['host']);    //record dns records
    $output['ip'] = $ip;
    $output['dns'] = $addr;
    $output['records'] = $records;
    return $output;
}
function getInfo($content)
{

    preg_match('/<title[^>]*>(.*?)<\/title[^>]*>/iU',$content,$output);
    $result['title'] = strip_tags($output[1]);
    preg_match('/<meta[\s]+[^>]*?name[\s]?=[\s\"\']description[\s\"\']+content[\s]?=[\s\"\']+(.*?)[\"\']+.*?>/miU',$content,$output);
    $result['description'] = strip_tags($output[1]);
    preg_match('/<meta[\s]+[^>]*?name[\s]?=[\s\"\']keywords[\s\"\']+content[\s]?=[\s\"\']+(.*?)[\"\']+.*?>/miU',$content,$output);
    $result['keywords'] = strip_tags($output[1]);
    return $result;
}

function getDensity($content)
{

    global $current;
    
    $find = get_html_translation_table(HTML_ENTITIES, ENT_QUOTES);
    
    preg_match('/<body[^>]*>(.*?)<\/body>/smi',$content,$match);
    if (isset($match[1])) $content = $match[1];
    $content=preg_replace('/<script[^>]*>.*?<\/script>/is','',$content);
    $content=preg_replace('/\s\s+/', ' ', $content);
    $content = str_replace($find,'',$content);
    
    $content = strip_tags($content);
    $current = explode(" ",$content);
    $found = array();
    foreach($current as $word)
    {
        if (!empty($word) && strlen(trim($word)) > 4)
        {
            $found["'".trim(strip_tags($word))."'"] ++;
        }
    }
    asort($found);
    $output['count'] = count($found);                //record keyword count
    $output['keywords'] = array_slice($found,-20);        //record keyword density
    return $output;
}
function getHeader($header)
{

    global $current;
    $header = explode("\n",$header);    //record
    if (is_array($header) && count($header))
    {
        return implode("\n",$header);
    }
    else
    {
        return '';
    }
    
    
}
function saveData($input)
{
print_r($input);exit;
  /*  $replace = array(
        ':title'=>$input['info']['title'],
        ':description'=>$input['info']['description'],
        ':keywords'=>$input['info']['keywords'],
        ':kcount'=>$input['density']['count'],
        ':density'=>base64_encode(serialize($input['density']['keywords'])),
        ':headers'=>$input['header'],
        ':ip'=>$input['ip']['ip'],
        ':dns'=>$input['ip']['dns'],
        ':records'=>base64_encode(serialize($input['ip']['records'])),
    );

    scraperwiki::sqliteexecute('UPDATE `links` SET `status` = 1,`title`=:title, `description`=:description, `keywords`=:keywords, `kcount`=:kcount, `density`=:density, `headers`=:headers, `ip`=:ip, `dns`=:dns, `records`=:records WHERE `url`=":url"',$replace);
    scraperwiki::sqlitecommit();
*/

}
function closeLink($id)
{

    scraperwiki::sqliteexecute('UPDATE `links` SET `status` = 1 WHERE `url`="'.$id.'"');
    scraperwiki::sqlitecommit();
}
function getUrl($body)
{

    global $dbh;
    global $current;
    
    $flag = false;
        
    $output = array();
    $regexp = "<a\s[^>]*href=(\"??)([http|https][^\" >]*?)\\1[^>]*>(.*)<\/a>";
    preg_match_all("/$regexp/siU",$body,$output);

    if (is_array($output[2]))
    {
        foreach($output[2] as $value)
        {
            $temp = parse_url($value);
            if (isset($temp['scheme']) && isset($temp['host']))
            {
                $url = $temp['scheme'].'://'.$temp['host'].'/';        //record
                if ($url != $current) 
                {
                    $flag = true;
                    try{
                        //scraperwiki::sqliteexecute("insert into `links` values (?,?,?,?,?,?,?,?,?,?,?)", array($url, 0,'','','',0,'','','','',''));
                    }
                    catch (Exception $e) {};
                }
            }
        }
    }
//scraperwiki::sqlitecommit();
}


$curl_arr = array();
$master = curl_multi_init(); //initiem multi curl
$i = 0;
    $finalresult = array();
    $returnedOrder = array();
    do{
            if (!count($curl_arr) && !count($links))
            {
                $links = scraperwiki::sqliteexecute("select * from `links`");
                $links = $links->data;
                echo "gather" . "\n";
            }
            echo "1";
            //extragem contentul
            if (count($curl_arr) < 10 && count($links))
            {
                $link = array_pop($links);
                $curl_arr[$i] = curl($link[0],$master);
                $tlinks[$i] = $link[0];
                $i++;
            }
            curl_multi_exec($master, $running);
            $info = curl_multi_info_read($master);
            if($info['handle']) 
            {
                $content = curl_multi_getcontent($info['handle']);
                
                $found = array_search($info['handle'], $curl_arr, true);
                $current = $tlinks[$found];
                
                if (!empty($content)) 
                {
                    if (strpos($content, "\r\n\r\n") > 0) // has header
                    {
                        $tcontent = explode("\r\n\r\n", $content);
                        $header = $tcontent[0];
                        $body = $tcontent[1];
                        $fheader = getHeader($header);
                    }
                    else
                    {
                        $body = $response;
                        $fheader = '';
                    }
                    
                    echo $current . "\n";
                    
                    getUrl($body);
                    $fdensity = getDensity($body);
                    $fip = getIp($tlinks[$found]);
                    $finfo = getInfo($body);
                    
                    $input = array();
                    $input['header'] = $fheader;
                    $input['density'] = $fdensity;
                    $input['ip'] = $fip;
                    $input['info'] = $finfo;
                    saveData($input);
exit;
                }
                else
                {
                    closeLink($current);
                }
                curl_multi_remove_handle($master, $info['handle']);
                curl_close($curl_arr[$found]);
                
                unset($curl_arr[$found]);
                unset($tlinks[$found]);
            }
        usleep(1000);
    }
    while(1);
curl_multi_close($master);


