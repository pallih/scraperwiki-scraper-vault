<?php
$infibeam="";
$flipkart="";
$nbc="";
$mainurl="http://www.infibeam.com";
$mincat=1;
$maxcat=100;
$minpage=1;
$maxpage=1;
function print_array($ar)
{
    foreach($ar as $p)
    echo $p."\n";
}
$book_num=0;
//antiques and collectibles
ini_set('display_errors', '1');
    ini_set('log_errors', 1);
    ini_set('error_log', dirname(__FILE__) . '/error_log.txt');
    error_reporting(E_ALL);
require 'scraperwiki/simple_html_dom.php';
$html2 = file_get_html('http://www.infibeam.com/Books/browse/Antiques_and_Collectibles');
if(isset($html2))
{
//echo "successful";
}
else echo "not successful";
$html3=$html2->find('div[id=allcategories]',0);

$rest=$html3->find('li');
$tcatnum=count($rest);
for($z=$mincat;$z<=$maxcat || $z<=$tcatnum;$z++)
{
    $res=$rest[$z-1];
     
    
    $link= $res->first_child()->href;
    $linkf=$mainurl.$link;
        //$link
    
     for($i=$minpage;$i<=$maxpage;$i++)
     {  
         
        $html4=file_get_html($linkf."/search?page=".($i));
        if(empty($html4))
        {
        //echo "could not get subcategory";
        break;
        }
        else
        {
            $i1=$html4->find('ul[class=search_result]',0);
         if(empty($i1)) break;
        
            $book_list=$i1->find('li');
           if(empty($book_list) || count($book_list)==0) break;
           foreach($book_list as $searchtag)
           {
               $book_num=$book_num+1;
                $temp=$searchtag->next_sibling();
                if(empty($temp) || $temp->tag=='li')
                $infibeam=(string)$searchtag;
                else
                {
                    $searchtag1=(string)$searchtag->next_sibling();
                   $searchtag2=(string)$searchtag->next_sibling()->next_sibling();
                   $searchtag3=(string)$searchtag->next_sibling()->next_sibling()->next_sibling();
                   $infibeam=(string)$searchtag.$searchtag1.$searchtag2.$searchtag3;
                 }
            
           
               $title=$searchtag->find('span[class=title]',0);
               $temp1=explode("By",$title->plaintext);
               $search1=$temp1[0];
               $find=array("&nbsp;"," ");
               $replace=array("","%20");
               $search2=str_replace($find, $replace,$search1);   //iplaza
               $search1=str_replace(array(":","&"),array("%60","%26"),$search2);   //hshop
               $search3=str_replace(array("%20","%60"),array("+","%3A"),$search1);  //bookadda
           
               $searchword=str_replace(" ","+",$temp1[0]);
               //echo $searchword;
               //$searchword=substr($searchword,0,-1);
               $flipurl="http://www.flipkart.com/search/a/books?query=".$searchword."&vertical=books&dd=0&autosuggest%5Bas%5D=off&autosuggest%5Bas-submittype%5D=entered&autosuggest%5Bas-grouprank%5D=0&autosuggest%5Bas-overallrank%5D=0&Search=%C2%A0&_r=bfDT57r_iDeBGffsiFEs2A--&_l=MHzwajeMCXBPHY1KaGPeZQ--&ref=4eddcc77-6705-4e8b-b805-1b6ace4f3911&selmitem=";
               $nbcurl="http://www.nbcindia.com/Search.aspx?q=".$searchword."&StoreId=1";
               $hshopurl="http://www.homeshop18.com/".$search1."/search:".$search1."/categoryid:10000";
               $iplazaurl="http://www.indiaplaza.com/searchproducts.aspx?sn=books&q=".$search2;
               $baddaurl="http://www.bookadda.com/general-search?searchkey=".$search3;
              // echo $baddaurl;
              /* $html5=file_get_html($baddaurl);
              if(isset($html5))
            echo "successful";
            else echo "not successful";*/
            
               $html5=file_get_html($flipurl);   //$flipurl
               if(!empty($html5))
               {
                   $i2=$html5->find('div[class=fk-srch-item fk-inf-scroll-item]',0);
                   if(!empty($i2))
                   {
           
                       $flipkart=(string)$i2;
           
                   }
                }
            $html5->clear();
            $html5=file_get_html($nbcurl);
            if(!empty($html5))
            {
            $i3=$html5->find('div[class=fictiong-grid-content-2]',0);
            if(!empty($i3))
            {
                $nbc=(string)$i3;
            }
            }
            $html5->clear();
            $html5=file_get_html($hshopurl);
            if(!empty($html5))
            {
            $i4=$html5->find('div[class=listView_details]',0);
            if(!empty($i4))
            {
                $hshop=(string)$i4;
            }
            }
            $html5->clear();
            $html5=file_get_html($iplazaurl);
            if(!empty($html5))
            {
            $i5=$html5->find('div[class=skuAreaRt]',0);
            if(!empty($i5))
            {
                $iplaza=(string)$i5;
            }
            }
            $html5->clear();
            $html5=file_get_html($baddaurl);
            if(!empty($html5))
            {
            $i6=$html5->find('div[class=details]',0);
            if(!empty($i6))
            {
                $badda=(string)$i6;
            }
            }

            
           /* $record=array(
            'id'=>$book_num,
            'infibeam'=>$infibeam,
            'flipkart'=>$flipkart,
            'nbc'=>$nbc,
            'hshop'=>$hshop,
            'iplaza'=>$iplaza,
            'badda'=>$badda
            );
            scraperwiki::save(array('id'),$record); */
         // break;
           }
        }
        $html4->clear();
        
    break;
    }
    break;
}

?>
