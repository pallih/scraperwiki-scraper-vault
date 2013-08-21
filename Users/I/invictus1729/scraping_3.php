<?php
require 'scraperwiki/simple_html_dom.php';
$mainurl='http://www.infibeam.com';
$url='http://www.infibeam.com/Books/browse';
$html=file_get_html($url);
$count1=0;
$count2=0;
//echo gettype($url);
$num_books=0;
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
                //echo $link1;
                $html2=file_get_html($mainurl.$link1);
                $count4=0;
                foreach($html2->find('div[id=search_result]') as $if_3_1)
                {
                    $tnum=$if_3_1->first_child()->plaintext;
                    //echo $tnum;
                    //echo $if_3_1;
                    $count4=$count4+1;
                    $count5=0;
                    $stop=20;
;
                    foreach($if_3_1->find('li') as $if_3_2)
                    {
                        $num_books=$num_books+1;
                        $count5=$count5+1;
                       // if($count5==$stop)
                        {
                        $check=$if_3_2->next_sibling();
                        if(!empty($check))
                       {
                       
                         if($if_3_2->next_sibling()->tag=="li")
                            $if_3_3=$if_3_2->children(3);
                           else
                            {
                            
                            $if_3_3=$if_3_2->next_sibling()->next_sibling()->next_sibling();
                           
                            }
                        }
                        else
                        $if_3_3=$if_3_2->children(3);
                            


                        
                        
                        
                      
                       
                         $start=$if_3_2->first_child()->children(1)->first_child();
                           $imagesrc=$start->src;
                           $if_3_6=$if_3_2->children(1)->children(0)->first_child();
                           $booksrc=$if_3_6->href;
                           $b_name=$if_3_6->plaintext;
                         $author=$if_3_2->children(1)->children(1)->plaintext;
                         $price=$if_3_2->children(2)->plaintext;
                        
                         if(preg_match("/%/",$price))
                        {
                         $exploded2=explode(" ",$price);
                           $a_price=$exploded2[2];
                           $d_price=$exploded2[4];
                           $discount=$exploded2[5];
                        }
                        else
                        {
                            $a_price="not available";
                            $d_price="not available";
                            $discount="not available";
                        }
                        $cost="not available";
                         $days="not available";
                        $txt=$if_3_3->find('b');
                        $num_e=count($txt);
                       if($num_e==1)
                        {
                            $status=$txt[0]->innertext;
                        }
                        elseif($num_e==2)
                        {
                            $status=$txt[0]->innertext;
                            $days=$txt[1]->innertext;
                        }
                        else
                        {
                            $status=$txt[0]->innertext;
                            $days=$txt[2]->innertext;
                            $cost=$txt[1]->innertext;
                         }

                            
                       
                         
                             /* $exploded3=explode(".",$if_3_3->plaintext,2); 
                               $status=$exploded3[0];
                               foreach($exploded3 as $elem)
                                 "hi=".$elem;
                              $exploded3=explode(" ",$if_3_3->plaintext);
                               if(count($exploded3)>7)
                                {
                              $status=$exploded3[1];
                              $cost=$exploded3[4];
                              $days=$exploded3[10];
                                }
                                else
                                {
                               $status=$if_3_3->plaintext;
                               $cost="not available";
                                $days="not available";
                                   } */
                       
                            
                            $codstat="not available";
                            $html3=file_get_html($mainurl.$booksrc);
                            foreach($html3->find('span[class=codSpan]') as $if_4_1)
                            {
                                foreach($if_4_1->find('a[title]') as $if_4_2)
                                {
                                 $cod=$if_4_1->title;
                                 str_replace(" ","",$cod);
                                if(strcmp($cod,"CashOnDeliveryAvailable"))
                                $codstat="available";
                                else $codstat= "not available";
                                }
                             }
                           /*echo "category=".$category."/n";
                           echo "subcategory=".$subcategory."/n";
                           echo "book name=".$b_name."/n"; 
                           echo "imagesource=".$imagesrc."/n";
                           echo "booksource=".$booksrc."/n";
                           echo "author=".$author."/n";
                           echo "actual price=".$a_price."/n";
                           echo "discounted price=".$d_price."/n";
                           echo "discount=".$discount."/n";
                           echo "status=".$status."/n";
                           echo "Shipping cost=".$cost."/n";
                           echo "days=".$days."/n";
                           echo "cash on delivery=".$codstat;*/
                           $record=array(
                            'id'=>$num_books,
                            'category'=>$category,
                            'subcategory'=>$subcategory,
                            'book_name'=>$b_name,
                            'Image_src'=>$imagesrc,
                            'Book_src'=>$booksrc,
                            'Author'=>$author,
                            'Actual_price'=>$a_price,
                            'discounted_price'=>$d_price,
                            'discount'=>$discount,
                            'status'=>$status,
                            'Shipping_cost'=>$cost,
                            'Days'=>$days,
                            'Cash_on_delievery'=>$codstat
                            );
                            scraperwiki::save(array('id'), $record);

                            
                    //if($count5==1)
                    //break;
                        }
                    }
                }
                    
                    
                
                
                
            if($count4==1)
            break;   
            }
        if($count3==1)
        break;
            
        } 
        
     
     if($count2==1)
     break;
        
    }
if($count1==1)
break;
}

        

?>
