<?php

scraperwiki::sqliteexecute("CREATE TABLE links2 (`id` int,`url` string,`status` int,`title` string,`description` string,`keywords` string,`kcount` int,`density` string,`headers` string, `ip` string, `dns` string, `records` string, PRIMARY KEY (`url`))");
scraperwiki::sqlitecommit();           


print_r(scraperwiki::show_tables());

exit;

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

}
function closeLink($id)
{

   // $links = $dbh->query('UPDATE `links` SET `status` = 1 WHERE `id`="'.$id.'"');
}
function getUrl($body)
{

    global $dbh;
    global $current;
    
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
                    //$dbh->query('INSERT INTO `links` SET `url`="'.$url.'"');
                }
            }
        }
    }
}


$curl_arr = array();
$master = curl_multi_init(); //initiem multi curl
 $links = array(array('id'=>'1','url'=>'http://www.trafic.ro/'));

    $finalresult = array();
    $returnedOrder = array();
    do{
        print_r($tlinks);
            if (!count($curl_arr) && !count($links))
            {
                echo "gather" . "\n";
            }
            echo "1";
            //extragem contentul
            if (count($curl_arr) < 10 && count($links))
            {
                $link = array_pop($links);
                $curl_arr[$link['id']] = curl($link['url'],$master);
                $tlinks[$link['id']] = $link['url'];
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
                        $header = array_pop(array_reverse($tcontent));
                        $body = implode(" ",$tcontent);
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
                    $input['id'] = $found;
                    
                    saveData($input);
                }
                else
                {
                    closeLink($found);
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


