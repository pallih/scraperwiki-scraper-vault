<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range(10848,12800) as $id)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://imaupstate.co.in/view.php?id=".$id);               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('table[class="SearchResult"]') as $table){
            $id_row = $table->children(1)->children(1)->plaintext;
            $name_row = $table->children(3)->children(1)->plaintext;
            $memnum_row = $table->children(5)->children(1)->plaintext;
            $mcinum_row = $table->children(6)->children(1)->plaintext;
            $clinadd_row = $table->children(8)->children(1)->plaintext;
            $clincity_row = $table->children(9)->children(1)->plaintext;
            $clinphone_row = $table->children(10)->children(1)->plaintext;
            $resphone_row = $table->children(11)->children(1)->plaintext;
            $mobile_row = $table->children(13)->children(1)->plaintext;
            $email_row = $table->children(14)->children(1)->plaintext;

            $otheradd_row = $table->children(15)->children(1)->plaintext;
            $dob_row = $table->children(18)->children(1)->plaintext;
            $spec_row = $table->children(21)->children(1)->plaintext;
            $notes_row = $table->children(25)->children(1)->plaintext;


            $record = array(
                    'id' => $id_row,
                    'name' => $name_row,
                    'membership num' => $memnum_row,
                    'mci number' => $mcinum_row,
                    'clinic address' => $clinadd_row,
                        'clinic city' => $clincity_row,
                    'clinic phone' => $clinphone_row,
                    'residence phone' => $resphone_row,
                    'mobile' => $mobile_row,
                        'email'=> $email_row,
                    'other address' => $otheradd_row,
                    'birthdate' => $dob_row,
                    'specialization' => $spec_row,
                    'notes' => $notes_row                    
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("id"),$record,"UPDocs");
    }    
    $dom->__destruct();
}
?>
<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range(10848,12800) as $id)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://imaupstate.co.in/view.php?id=".$id);               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('table[class="SearchResult"]') as $table){
            $id_row = $table->children(1)->children(1)->plaintext;
            $name_row = $table->children(3)->children(1)->plaintext;
            $memnum_row = $table->children(5)->children(1)->plaintext;
            $mcinum_row = $table->children(6)->children(1)->plaintext;
            $clinadd_row = $table->children(8)->children(1)->plaintext;
            $clincity_row = $table->children(9)->children(1)->plaintext;
            $clinphone_row = $table->children(10)->children(1)->plaintext;
            $resphone_row = $table->children(11)->children(1)->plaintext;
            $mobile_row = $table->children(13)->children(1)->plaintext;
            $email_row = $table->children(14)->children(1)->plaintext;

            $otheradd_row = $table->children(15)->children(1)->plaintext;
            $dob_row = $table->children(18)->children(1)->plaintext;
            $spec_row = $table->children(21)->children(1)->plaintext;
            $notes_row = $table->children(25)->children(1)->plaintext;


            $record = array(
                    'id' => $id_row,
                    'name' => $name_row,
                    'membership num' => $memnum_row,
                    'mci number' => $mcinum_row,
                    'clinic address' => $clinadd_row,
                        'clinic city' => $clincity_row,
                    'clinic phone' => $clinphone_row,
                    'residence phone' => $resphone_row,
                    'mobile' => $mobile_row,
                        'email'=> $email_row,
                    'other address' => $otheradd_row,
                    'birthdate' => $dob_row,
                    'specialization' => $spec_row,
                    'notes' => $notes_row                    
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("id"),$record,"UPDocs");
    }    
    $dom->__destruct();
}
?>
