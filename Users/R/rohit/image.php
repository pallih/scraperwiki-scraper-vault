<?php
require 'scraperwiki/simple_html_dom.php';
$url="http://econkart.webatu.com/next.php?start=1&finish=4000&submit=Submit";
$html=file_get_html($url);
$record=$html->plaintext;

$data=explode("++",$record);
//echo count($data);
$i=0;
foreach($data as $value)
{
   if(strlen($value)>3)
   {
       $i=$i+1;
       $match=explode("#",$value);
       $id=$match[0];
       $add=$match[1];
       $ht=chunk_split(base64_encode(file_get_contents($add)));
       $record1=array(
        'id'=>$i,
        'bid'=>$id,
        'img'=>$ht
        );
       scraperwiki::save(array('id'),$record1);
        sleep(1);
    }
}


?>
