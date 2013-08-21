<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range(10784,11150) as $id)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://www.delhimedicalassociation.com/memberDetails.php?mid=".$id);               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('td[width="43%"]') as $head_row){
            $table = $head_row->parent()->parent();
            $name_row = $table->children(2)->children(1)->plaintext;
            $gender_row = $table->children(3)->children(1)->plaintext;
            $quals_row = $table->children(6)->children(1)->plaintext;
            $specs_row = $table->children(7)->children(1)->plaintext;
            $add_row = $table->children(8)->children(1)->plaintext;
            $pin_row = $table->children(9)->children(1)->plaintext;
            $phone_row = $table->children(10)->children(1)->plaintext;
            $clinicadd_row = $table->children(12)->children(1)->plaintext;
            $mobile_row = $table->children(16)->children(1)->plaintext;
            $email_row = $table->children(18)->children(1)->plaintext;

            $record = array(
                    'name' => $name_row,
                    'gender' => $gender_row,
                     'quals' => $quals_row,
                     'specs' => $specs_row,
                     'address' => $add_row,
                     'pincode' => $pin_row,
                     'phone' => $phone_row,
                     'clinic_address' => $clinicadd_row,
                     'mobile' => $mobile_row,
                     'email' => $email_row                    
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("name"),$record,"Delhi_Docs");
    }    
    $dom->__destruct();
}
?>
