<?php
require 'scraperwiki/simple_html_dom.php';
$mainurl='http://www.infibeam.com';
$url='http://www.infibeam.com/Books/browse';
$html=file_get_html($url);
$count1=0;
$count2=0;
//echo gettype($url);
foreach($html->find('div[id=allcategories]') as $if_1_1)
{
//echo $if_1_1;
//counting to stop functions
$count1=$count1+1;
    $count2=0;
    foreach($if_1_1->find('h3') as $if_1_2)
    {
        //counting to stop function
        $count2=$count2+1;
        $link=$mainurl.$if_1_2->first_child()->href;
        //echo gettype($link);
        $category=$if_1_2->plaintext;
        //echo $link;
        $html1=file_get_html($link);
        if($html1==null)
        echo "not found";
        $count3=0;
        foreach($html1->find('div[id=allcategories]') as $if_2_1)
        {
            
            $count3=$count3+1;
            $count4=0;
            
            foreach($if_2_1->find('li') as $if_2_2)
            {
                $count4=$count4+1;
                $link1=$if_2_2->first_child()->href;
                $subcategory=$if_2_2->first_child()->plaintext;
                echo $subcategory;
           // if($count4==1)
           // break;   
            }
       // if($count3==1)
        //break;
            
        } 
     
     //if($count2==1)
    // break;
        
    }
//if($count1==1)
//break;
}

        

?>
