<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range(9759,47816) as $id)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://www.gmcgujarat.org/Profile.asp?Id=".$id);               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('table[bordercolor="red"]') as $outer_table){
            $table = $outer_table->children(2)->children(0)->children(0);
            $name_row = $table->children(2)->children(2)->plaintext;
            $id_row = $table->children(2)->children(5)->plaintext;
            
            $gender_row = $table->children(3)->children(2)->plaintext;
            $dob_row = $table->children(3)->children(5)->plaintext;
  }

  foreach($dom->find('td[colspan="5"]') as $add_td){
            $add_row = $add_td->plaintext;
            $city_row = $add_td->parent()->parent()->children(3)->children(2)->plaintext;
            $state_row = $add_td->parent()->parent()->children(3)->children(5)->plaintext;
  }
  foreach($dom->find('td[colspan="10"]') as $next_td){
            $degree_row = $next_td->parent()->parent()->children(4)->children(2)->plaintext;
            $univ_row = $next_td->parent()->parent()->children(5)->children(2)->plaintext;
            $passyear_row = $next_td->parent()->parent()->children(6)->children(5)->plaintext;
  }
            $record = array(
                    'name' => $name_row,
                    'id' => $id_row,
                     'gender' => $gender_row,
                     'dob' => $dob_row,
                     'address' => $add_row,
                     'city' => $city_row,
                     'state' => $state_row,
                     'degree' => $degree_row,
                     'univ' => $univ_row,
                     'passing year' => $passyear_row                    
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("name"),$record,"Gujarat_Docs");
        
    $dom->__destruct();
}
?>