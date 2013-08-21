<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

$dom = new simple_html_dom();
$inner_dom = new simple_html_dom();
                

foreach (range(1,1) as $page_id)//739
{
    $html = scraperWiki::scrape("http://www.apmedicalcouncil.com/searchresults.php?sex=NR&qlfn=SQ&offset=".$page_id."00");               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   $counter = 0;
   foreach($dom->find('table[border="1"]') as $table){
        foreach($table->find('tr') as $tr) {
            $regd_num = trim($tr->children(0)->plaintext);
            $doc_name = trim($tr->children(1)->plaintext);
            $father_name = trim($tr->children(2)->plaintext);
            $quals_name = trim($tr->children(3)->plaintext);
            $univ_name = trim($tr->children(4)->plaintext);
            $link = $tr->find('a',0);
            if($link != null) { 
                $link_text = $link->href; 

                $inner_html = scraperWiki::scrape("http://www.apmedicalcouncil.com/".$link_text);
                $inner_dom->load($inner_html);

                $birth_date = trim($inner_dom->find('div[id="birth"]',0)->plaintext);
                $sex = trim($inner_dom->find('div[id="sex"]',0)->plaintext);
                $quals = trim($inner_dom->find('div[id="qualification"]',0)->plaintext);
                $quals2 = trim($inner_dom->find('div[id="addqualification"]',0)->plaintext);
                $add = trim($inner_dom->find('div[id="address"]',0)->plaintext);
                $add_more = trim($inner_dom->find('div[id="address2"]',0)->plaintext);

                $record = array(
                        'regd_num' => $regd_num,
                        'doc_name' => $doc_name,
                         'father_name' => $father_name,
                         'quals_name' => $quals_name,
                         'univ_name' => $univ_name,
                         'birth_date' => $birth_date,
                         'sex' => $sex,
                         'qualification' => $quals,
                         'advanced_quals' => $quals2,
                         'address' => $add,
                         'add_more' => $add_more
                        );
            }
            else {            
            $record = array(
                    'regd_num' => $regd_num,
                    'doc_name' => $doc_name,
                     'father_name' => $father_name,
                     'quals_name' => $quals_name,
                     'univ_name' => $univ_name,
                    );
            }
            print_r($record);
            $counter++;
            //print_r($link);
            //scraperwiki::save_sqlite(array("doc_name"),$record,"AP_Docs");
            if($counter == 2)
                break;
        }
    }    
    
}
$inner_dom->__destruct();
$dom->__destruct();
?>