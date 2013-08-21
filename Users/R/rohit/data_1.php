<?php
$open=0;
$start=201;
$finish=400;
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
        $searchword=trim($title);
       
        $searchword=str_replace(" ","+",$title);
       
        $url="http://www.flipkart.com/search/a/books?query=".$searchword."&vertical=books&dd=0&autosuggest%5Bas%5D=off&autosuggest%5Bas-submittype%5D=entered&autosuggest%5Bas-grouprank%5D=0&autosuggest%5Bas-overallrank%5D=0&Search=%C2%A0&_r=bfDT57r_iDeBGffsiFEs2A--&_l=MHzwajeMCXBPHY1KaGPeZQ--&ref=4eddcc77-6705-4e8b-b805-1b6ace4f3911&selmitem=";
        $html1=file_get_html($url);
        if(isset($html1))
        {
            $if=$html1->find('div[class=fk-srch-item fk-inf-scroll-item]',0);
            if(!empty($if))
            {
                $book_src=$if->first_child()->children(1)->children(0)->first_child()->href;
                $title1=$if->first_child()->children(1)->children(0)->plaintext;
                $info=$if->first_child()->children(2)->plaintext;
                $record=array(
                 'id'=>$i,
                 'src'=>$book_src,
                 'title'=>$title1,
                 'info'=>$info,
                 'book'=>$title
                );
                scraperwiki::save(array('id'),$record);
            }
            else
            {
                $record=array(
                 'id'=>$i,
                 'src'=>"NA",
                 'title'=>"NA",
                 'info'=>"NA",
                  'book'=>$title
                );
                scraperwiki::save(array('id'),$record);
            }
            $html1->clear();
        }
            
    //break;
   }
}

?>
