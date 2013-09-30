<?php
$open=0;
$k=0;
$start=1101;
$finish=1200;
$num=$finish-$start+1;
$seconds=10*60*60;
set_time_limit($seconds);
require 'scraperwiki/simple_html_dom.php';
$mainurl="http://econkart.webatu.com/next.php?start=".$start."&finish=".$finish."&submit=Submit";
$html=file_get_html($mainurl);
if(isset($html))
{
    $open=1;
    $titles=explode("+",$html->plaintext);
    
    
}
if($open==1)
{
   for($i=1;$i<=$num;$i++)
   {
        $title=$titles[$i-1];
        
       // echo $title;
       
        $searchword=str_replace(" ","+",$title);
       $t_count=0;
        $k1=0;
        while($t_count==0)
        {
         $s=10*$k1;
         
        
        $url="http://www.flipkart.com/search/a/books?query=".$searchword."&vertical=books&dd=0&autosuggest[as]=off&autosuggest[as-submittype]=default-search&autosuggest[as-grouprank]=0&autosuggest[as-overallrank]=0&Search=%C2%A0&_r=QBqWnedXBuVmMqNi_xE95g--&_l=MHzwajeMCXBPHY1KaGPeZQ--&ref=fa0db999-8bdb-4bec-9127-a3c0b6a0e371&selmitem=&response-type=json&start=".$s;


           // echo $url;
            //echo $url;
            $html1=file_get_contents($url);
            if(isset($html1))
            {
            
            
            
                $json=json_decode($html1);
                $html2=str_get_html($json->html);
                $terminate=$json->count;
                if($terminate==0)
                {
                    
                    $t_count=1;
                    break;
                    
                }
                $list=$html2->find('div[class=fk-srch-item fk-inf-scroll-item]');
                
                if(!empty($list))
                {
            
                    foreach($list as $src)
                    {
                        $k=$k+1;
                        $linki=$src->find('h2',0);
                        $link=$linki->first_child()->href;
                        $title1=$linki->first_child()->plaintext;
                        $author=$linki->next_sibling()->plaintext;
                        $info=$src->first_child()->children(2)->plaintext;
                        $record=array(
                       'id'=>$k,
                       'link'=>$link,
                       'title'=>$title1,
                       'author'=>$author,
                       'info'=>$info,
                       'search_word'=>$title
                        );
                        scraperwiki::save(array('id'),$record);
                    $linki="NA";
                    $link="NA";
                    $title1="NA";
                    $author="NA";
                    $info="NA";
            
                    }
         
                 }
                $html2->clear();
                 
            //if loop
            }
            
            $k1=$k1+1;
            //break;
         //while loop
         }
            
            
            
            
   // break;
   }
}


?><?php
$open=0;
$k=0;
$start=1101;
$finish=1200;
$num=$finish-$start+1;
$seconds=10*60*60;
set_time_limit($seconds);
require 'scraperwiki/simple_html_dom.php';
$mainurl="http://econkart.webatu.com/next.php?start=".$start."&finish=".$finish."&submit=Submit";
$html=file_get_html($mainurl);
if(isset($html))
{
    $open=1;
    $titles=explode("+",$html->plaintext);
    
    
}
if($open==1)
{
   for($i=1;$i<=$num;$i++)
   {
        $title=$titles[$i-1];
        
       // echo $title;
       
        $searchword=str_replace(" ","+",$title);
       $t_count=0;
        $k1=0;
        while($t_count==0)
        {
         $s=10*$k1;
         
        
        $url="http://www.flipkart.com/search/a/books?query=".$searchword."&vertical=books&dd=0&autosuggest[as]=off&autosuggest[as-submittype]=default-search&autosuggest[as-grouprank]=0&autosuggest[as-overallrank]=0&Search=%C2%A0&_r=QBqWnedXBuVmMqNi_xE95g--&_l=MHzwajeMCXBPHY1KaGPeZQ--&ref=fa0db999-8bdb-4bec-9127-a3c0b6a0e371&selmitem=&response-type=json&start=".$s;


           // echo $url;
            //echo $url;
            $html1=file_get_contents($url);
            if(isset($html1))
            {
            
            
            
                $json=json_decode($html1);
                $html2=str_get_html($json->html);
                $terminate=$json->count;
                if($terminate==0)
                {
                    
                    $t_count=1;
                    break;
                    
                }
                $list=$html2->find('div[class=fk-srch-item fk-inf-scroll-item]');
                
                if(!empty($list))
                {
            
                    foreach($list as $src)
                    {
                        $k=$k+1;
                        $linki=$src->find('h2',0);
                        $link=$linki->first_child()->href;
                        $title1=$linki->first_child()->plaintext;
                        $author=$linki->next_sibling()->plaintext;
                        $info=$src->first_child()->children(2)->plaintext;
                        $record=array(
                       'id'=>$k,
                       'link'=>$link,
                       'title'=>$title1,
                       'author'=>$author,
                       'info'=>$info,
                       'search_word'=>$title
                        );
                        scraperwiki::save(array('id'),$record);
                    $linki="NA";
                    $link="NA";
                    $title1="NA";
                    $author="NA";
                    $info="NA";
            
                    }
         
                 }
                $html2->clear();
                 
            //if loop
            }
            
            $k1=$k1+1;
            //break;
         //while loop
         }
            
            
            
            
   // break;
   }
}


?>