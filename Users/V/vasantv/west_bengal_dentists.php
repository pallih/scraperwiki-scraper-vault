<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range(1,322) as $id)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://www.wbdc.org.in/search_name.php?regdno=".$id."-B");               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('table[bordercolor="#009900"]') as $table){
            $reg_row = $table->children(3)->children(1)->plaintext;
            $name_row = $table->children(5)->children(1)->plaintext;
            $birth_row = $table->children(6)->children(1)->plaintext;
            $gender_row = $table->children(7)->children(1)->plaintext;
            $add_row = $table->children(9)->children(1)->plaintext;
            $quals_row = $table->children(11)->children(1)->plaintext;
            $univ_row = $table->children(13)->children(1)->plaintext;
            $degreedate_row = $table->children(14)->children(1)->plaintext;
            $addquals_row = $table->children(15)->children(1)->plaintext;

            $record = array(
                    'regd' => $reg_row,
                    'name' => $name_row,
                    'birthdate' => $birth_row,
                    'gender' => $gender_row,
                     'quals' => $quals_row,
                     'univ' => $univ_row,
                     'address' => $add_row,
                     'degree_date' => $degreedate_row,
                     'additional_quals' => $addquals_row
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("regd"),$record,"WB_Dentists");
    }    
    $dom->__destruct();
}
?>
<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range(1,322) as $id)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://www.wbdc.org.in/search_name.php?regdno=".$id."-B");               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('table[bordercolor="#009900"]') as $table){
            $reg_row = $table->children(3)->children(1)->plaintext;
            $name_row = $table->children(5)->children(1)->plaintext;
            $birth_row = $table->children(6)->children(1)->plaintext;
            $gender_row = $table->children(7)->children(1)->plaintext;
            $add_row = $table->children(9)->children(1)->plaintext;
            $quals_row = $table->children(11)->children(1)->plaintext;
            $univ_row = $table->children(13)->children(1)->plaintext;
            $degreedate_row = $table->children(14)->children(1)->plaintext;
            $addquals_row = $table->children(15)->children(1)->plaintext;

            $record = array(
                    'regd' => $reg_row,
                    'name' => $name_row,
                    'birthdate' => $birth_row,
                    'gender' => $gender_row,
                     'quals' => $quals_row,
                     'univ' => $univ_row,
                     'address' => $add_row,
                     'degree_date' => $degreedate_row,
                     'additional_quals' => $addquals_row
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("regd"),$record,"WB_Dentists");
    }    
    $dom->__destruct();
}
?>
