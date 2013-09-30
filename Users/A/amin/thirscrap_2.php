<?php
@set_time_limit(0);
require 'scraperwiki/simple_html_dom.php';
//require 'insert.php';

function amin($url){
 $ch = curl_init();
 sleep(2);
 curl_setopt($ch, CURLOPT_URL, $url);
 curl_setopt($ch, CURLOPT_HEADER, 0);
$agents = array(
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100508 SeaMonkey/2.0.4',
    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
);
curl_setopt($ch,CURLOPT_USERAGENT,$agents[array_rand($agents)]);
//set the header params
    $header[0] = "Accept: text/xml,application/xml,application/xhtml+xml,";
    $header[0] .= "text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5";
    $header[] = "Cache-Control: max-age=0";
    $header[] = "Connection: keep-alive";
    $header[] = "Keep-Alive: 10";
    $header[] = "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7";
    $header[] = "Accept-Language: en-us,en;q=0.5";
    $header[] = "Pragma: ";
//assign to the curl request.
    curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1); // ADD THIS
curl_setopt ($ch, CURLOPT_CONNECTTIMEOUT, 20);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
 $output = curl_exec($ch);
 curl_close($ch);
 return $output;
}
function readlog(){
$my_file = 'log.dat';
$handle = fopen($my_file, 'r');
$data = fread($handle,20);
fclose($handle);
return $data;
}
function writelog($da){
$my_file = 'log.dat';
$handle = fopen($my_file, 'w') or die('Cannot open file:  '.$my_file);
fwrite($handle, $da);
fclose($handle);
}
$log=intval(0);
$perpage=intval(100);
$start=$log/$perpage;
$continu=($log%$perpage)+1;

$html = new simple_html_dom(); 
for($i=$start;$i<50;$i++){
$maind = file_get_contents("http://m.flipkart.com/m/store/bks/loadmore?p%5B0%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&layout=grid&store=bks&count=100&start=".(($i*$perpage)+$continu));

$maind=json_decode($maind,TRUE);
$html = new simple_html_dom(); 
$html->load("<html><body>".$maind['html']."</body></html>");
//echo $data['html'];
foreach($html->find('li') as $data){
unset($record);

$t= $data->children(0)->href;
$new = new simple_html_dom();
$url="http://www.flipkart.com".$t;
echo $url."<br>";
$ind=(string) amin($url);
$find=strpos($ind,'<div class="page-content"',0);
$ind=substr($ind,$find);
$ind="<html><body>".preg_replace('/<script(.*?)<\/script>/','',$ind);

$new->load($ind);
$record["link"]=$t;
//$new->load_file("http://www.flipkart.com/the-secret-of-the-nagas/p/itmdh937ugrp7fnv?pid=9789381626344&icmpid=reco_pp_same_bundle_book_1");
foreach($new->find('div.page-content') as $in){
//echo $in->innertext;
$record["name"]=$in->children(0)->children(0)->children(0)->plaintext;
$record["author"]=trim($in->children(0)->children(0)->children(1)->plaintext);
$l=0;
foreach($in->find("div.m2-bottom") as $descc){
if($l==1){
echo $record["description"]=$descc->innertext;
}
$l++;
}
//$record["simg"]=$in->find("div.product-images",0)->children(0)->src;

foreach($in->find("div.table-row-generic") as $spec){
unset($r1);
unset($r2);
$r1=$spec->children(0)->plaintext;
$r2=$spec->children(1)->plaintext;
$r1=trim($r1);
$r2=trim($r2);
    switch($r1)
    {
        case "Publisher": $record["publisher"]=$r2;break;
        case "Publication Year": $record["YOP"]=$r2;break;
        case "ISBN-13": $record["ISBN-13"]=$r2;break;
        case "ISBN-10": $record["ISBN-10"]=$r2;break;
        case "Language":$record["language"]=$r2;break;
        case "Binding": $record["binding"]=$r2;break;
        case "Number of Pages": $record["pages"]=$r2;break;
        default: break;
    }
}
$record["publisher"]=(strlen($record["publisher"])>1)?$record["publisher"]:"";
$record["YOP"]=(strlen($record["YOP"])>1)?$record["YOP"]:"";
$record["ISBN-13"]=(strlen($record["ISBN-13"])>1)?$record["ISBN-13"]:"";
$record["ISBN-10"]=(strlen($record["ISBN-10"])>1)?$record["ISBN-10"]:"";
$record["language"]=(strlen($record["language"])>1)?$record["language"]:"";
$record["binding"]=(strlen($record["binding"])>1)?$record["binding"]:"";
$record["pages"]=(strlen($record["pages"])>1)?$record["pages"]:"";
$record["description"]=(strlen($record["description"])>1)?$record["description"]:"";
unset($in);
}
unset($new);
//insertnow($record);
writelog(++$log);
$data->clear();
unset($data);
}
$html->clear();
unset($html);
unset($maind);
}

?>
<?php
@set_time_limit(0);
require 'scraperwiki/simple_html_dom.php';
//require 'insert.php';

function amin($url){
 $ch = curl_init();
 sleep(2);
 curl_setopt($ch, CURLOPT_URL, $url);
 curl_setopt($ch, CURLOPT_HEADER, 0);
$agents = array(
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100508 SeaMonkey/2.0.4',
    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
);
curl_setopt($ch,CURLOPT_USERAGENT,$agents[array_rand($agents)]);
//set the header params
    $header[0] = "Accept: text/xml,application/xml,application/xhtml+xml,";
    $header[0] .= "text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5";
    $header[] = "Cache-Control: max-age=0";
    $header[] = "Connection: keep-alive";
    $header[] = "Keep-Alive: 10";
    $header[] = "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7";
    $header[] = "Accept-Language: en-us,en;q=0.5";
    $header[] = "Pragma: ";
//assign to the curl request.
    curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1); // ADD THIS
curl_setopt ($ch, CURLOPT_CONNECTTIMEOUT, 20);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
 $output = curl_exec($ch);
 curl_close($ch);
 return $output;
}
function readlog(){
$my_file = 'log.dat';
$handle = fopen($my_file, 'r');
$data = fread($handle,20);
fclose($handle);
return $data;
}
function writelog($da){
$my_file = 'log.dat';
$handle = fopen($my_file, 'w') or die('Cannot open file:  '.$my_file);
fwrite($handle, $da);
fclose($handle);
}
$log=intval(0);
$perpage=intval(100);
$start=$log/$perpage;
$continu=($log%$perpage)+1;

$html = new simple_html_dom(); 
for($i=$start;$i<50;$i++){
$maind = file_get_contents("http://m.flipkart.com/m/store/bks/loadmore?p%5B0%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&layout=grid&store=bks&count=100&start=".(($i*$perpage)+$continu));

$maind=json_decode($maind,TRUE);
$html = new simple_html_dom(); 
$html->load("<html><body>".$maind['html']."</body></html>");
//echo $data['html'];
foreach($html->find('li') as $data){
unset($record);

$t= $data->children(0)->href;
$new = new simple_html_dom();
$url="http://www.flipkart.com".$t;
echo $url."<br>";
$ind=(string) amin($url);
$find=strpos($ind,'<div class="page-content"',0);
$ind=substr($ind,$find);
$ind="<html><body>".preg_replace('/<script(.*?)<\/script>/','',$ind);

$new->load($ind);
$record["link"]=$t;
//$new->load_file("http://www.flipkart.com/the-secret-of-the-nagas/p/itmdh937ugrp7fnv?pid=9789381626344&icmpid=reco_pp_same_bundle_book_1");
foreach($new->find('div.page-content') as $in){
//echo $in->innertext;
$record["name"]=$in->children(0)->children(0)->children(0)->plaintext;
$record["author"]=trim($in->children(0)->children(0)->children(1)->plaintext);
$l=0;
foreach($in->find("div.m2-bottom") as $descc){
if($l==1){
echo $record["description"]=$descc->innertext;
}
$l++;
}
//$record["simg"]=$in->find("div.product-images",0)->children(0)->src;

foreach($in->find("div.table-row-generic") as $spec){
unset($r1);
unset($r2);
$r1=$spec->children(0)->plaintext;
$r2=$spec->children(1)->plaintext;
$r1=trim($r1);
$r2=trim($r2);
    switch($r1)
    {
        case "Publisher": $record["publisher"]=$r2;break;
        case "Publication Year": $record["YOP"]=$r2;break;
        case "ISBN-13": $record["ISBN-13"]=$r2;break;
        case "ISBN-10": $record["ISBN-10"]=$r2;break;
        case "Language":$record["language"]=$r2;break;
        case "Binding": $record["binding"]=$r2;break;
        case "Number of Pages": $record["pages"]=$r2;break;
        default: break;
    }
}
$record["publisher"]=(strlen($record["publisher"])>1)?$record["publisher"]:"";
$record["YOP"]=(strlen($record["YOP"])>1)?$record["YOP"]:"";
$record["ISBN-13"]=(strlen($record["ISBN-13"])>1)?$record["ISBN-13"]:"";
$record["ISBN-10"]=(strlen($record["ISBN-10"])>1)?$record["ISBN-10"]:"";
$record["language"]=(strlen($record["language"])>1)?$record["language"]:"";
$record["binding"]=(strlen($record["binding"])>1)?$record["binding"]:"";
$record["pages"]=(strlen($record["pages"])>1)?$record["pages"]:"";
$record["description"]=(strlen($record["description"])>1)?$record["description"]:"";
unset($in);
}
unset($new);
//insertnow($record);
writelog(++$log);
$data->clear();
unset($data);
}
$html->clear();
unset($html);
unset($maind);
}

?>
