<?php
$seconds=4*60*60;
set_time_limit($seconds);
$min=101;
$max=150;
$min=$min-1;
$max=$max-1;
$k=0;
require 'scraperwiki/simple_html_dom.php';
$url="http://www.flipkart.com/science-technology-books-2751?response-type=json&inf-start=";
for($i=$min;$i<=$max;$i++)
{
    $j=$i*20;
    $url1=$url.$j;
    //echo $url1;
    $json=file_get_contents($url1);
    $json1=json_decode($json);
    $html1=$json1->html;
    $html=str_get_html($html1);
    if(isset($html))
    {
       
       $list=$html->find('div[class=fk-srch-item fk-inf-scroll-item]');
        if(!empty($list))
        {
            
            foreach($list as $src)
            {
                $k=$k+1;
                $linki=$src->find('h2',0);
                $link=$linki->first_child()->href;
                $title=$linki->first_child()->plaintext;
                $author=$linki->next_sibling()->plaintext;
                $info=$src->first_child()->children(2)->plaintext;
                $record=array(
                'id'=>$k,
                'link'=>$link,
                'title'=>$title,
                'author'=>$author,
                'info'=>$info
                );
                scraperwiki::save(array('id'),$record);
            
            }
         
         }
        
    }
   
}

?>
<?php
$seconds=4*60*60;
set_time_limit($seconds);
$min=101;
$max=150;
$min=$min-1;
$max=$max-1;
$k=0;
require 'scraperwiki/simple_html_dom.php';
$url="http://www.flipkart.com/science-technology-books-2751?response-type=json&inf-start=";
for($i=$min;$i<=$max;$i++)
{
    $j=$i*20;
    $url1=$url.$j;
    //echo $url1;
    $json=file_get_contents($url1);
    $json1=json_decode($json);
    $html1=$json1->html;
    $html=str_get_html($html1);
    if(isset($html))
    {
       
       $list=$html->find('div[class=fk-srch-item fk-inf-scroll-item]');
        if(!empty($list))
        {
            
            foreach($list as $src)
            {
                $k=$k+1;
                $linki=$src->find('h2',0);
                $link=$linki->first_child()->href;
                $title=$linki->first_child()->plaintext;
                $author=$linki->next_sibling()->plaintext;
                $info=$src->first_child()->children(2)->plaintext;
                $record=array(
                'id'=>$k,
                'link'=>$link,
                'title'=>$title,
                'author'=>$author,
                'info'=>$info
                );
                scraperwiki::save(array('id'),$record);
            
            }
         
         }
        
    }
   
}

?>
