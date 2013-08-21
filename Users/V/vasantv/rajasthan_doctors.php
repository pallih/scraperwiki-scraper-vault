<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range(1,100) as $id)//30000
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://rmcjaipur.org/searchdetails.aspx?id=".$id);               
    
    $dom->load($html);

    //print "FOUND!";
            //$table = $tr_table->parent();
            $reg_row = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label8]',0)->plaintext;
            $first_name = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label1]',0)->plaintext;
            $sur_name = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label2]',0)->plaintext;
            $dob = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label4]',0)->plaintext;
            $add1 = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label5]',0)->plaintext;
            $add2 = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label6]',0)->plaintext;
            $add3 = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label7]',0)->plaintext;
            $add4 = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label12]',0)->plaintext;
            $add = $add1." ".$add2." ".$add3." ".$add4;
            $quals = $dom->find('span[id=ctl00_ContentPlaceHolder1_Label11]',0)->plaintext;

            $record = array(
                    'regd' => $reg_row,
                    'name' => $first_name." ".$sur_name,
                    'birthdate' => $dob,
                     'quals' => $quals,
                     'address' => $add,
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("regd"),$record,"Raj_Dentists");

    $dom->__destruct();
}
?>
