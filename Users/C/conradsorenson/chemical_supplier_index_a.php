<?php

//  Chemical Supplier Index
//  written 2012-07-31 by Conrad Sorenson

//  OUTLINE
//    1  Create database
//    2  Scrape data for ABC and store results in database
//       2.1  http://www.molport.com/buy-chemicals/suppliers/by-first-letters/abc
//    3  Repeat for DEF ... YZ
//       3.1  abc    def    ghi    jkl    mno    pqr    stu    vwx    yz
//    4  Scrape supplier data
//    5  Scrape chemicals



//    1  Create database
require 'scraperwiki/simple_html_dom.php';    
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `chem_suppliers` ('supplier_index' integer, 'supplier_name' text, 'country' text, 'last_update' text, 'description' text, 'link' text)");


//    2  Scrape data for ABC and store results in database 
//       2.1  http://www.molport.com/buy-chemicals/suppliers/by-first-letters/abc
$suffix[0] = "abc";
$suffix[1] = "def";
$suffix[2] = "ghi";
$suffix[3] = "jkl";
$suffix[4] = "mno";
$suffix[5] = "pqr";
$suffix[6] = "stu";
$suffix[7] = "vwx";
$suffix[8] = "yz";
$chem_supplier_count = 1;


//  INSERT ITERATOR HERE
for ($iterator=0; $iterator<=8; $iterator++){
    $surl = str_replace("XXX",strtolower($suffix[$iterator]),"http://www.molport.com/buy-chemicals/suppliers/by-first-letters/XXX");
    $chem_suppliers = scraperwiki::scrape($surl);
    $chem_suppliers_dom = new simple_html_dom();
    $chem_suppliers_dom->load($chem_suppliers);
    
    //echo $chem_suppliers_dom;
    //echo trim($chem_suppliers_dom->plaintext);
    
    $tr_count = 0;
    
    //$data = $chem_suppliers_dom->find("table[@class='suppliers-record-container'] tr");
    
    //echo $data;
    //var_dump($data);
    //echo "$data count = " . count($data) . "\n";
    
    
    
    foreach($chem_suppliers_dom->find("table[@class='suppliers-record-container'] tr") as $data){
    
        $stringTest = trim($data->plaintext);

        //echo $tr_count . "    " . $stringTest . "\n";
        //echo $data . "\n";
    
        if ($tr_count == 0) {
            $start = strpos($data,"<b>") + 3;
            $end = strpos($data,"</b>");
            $company_name = trim(substr($data, $start , ($end - $start)));
    
            $start = strpos($data,"</b></a></u>,") + 14;
            $end = strpos($data,",", $start);
            $company_country = trim(substr($data, $start , ($end - $start) ));
    
            $start = strpos($stringTest,"last updated on") + 15;
            $end = strlen($stringTest);
            $last_update = trim(substr($stringTest, $start , ($end - $start) ));

            $start = strpos($data,"<a href=\"supplier") + 9;
            $end = strpos($data,"\"", $start);
            $link = trim(substr($data, $start , ($end - $start) ));

            //echo $link . "\n";

            $link = "http://www.molport.com/buy-chemicals/" . $link;
    
        }
    
        if ($tr_count == 1) {
            $company_description = trim(str_replace("More...","",$stringTest));
            //$start = strpos($data,"<a href=\"supplier") + 9;
            //$end = strpos($data,"\"", $start);
            //$link = trim(substr($data, $start , ($end - $start) ));

            //echo $data . "\n";

            //$link = "http://www.molport.com/buy-chemicals/" . $link;
            
        }
    
    
        if ($stringTest == "&nbsp;ddd") {
            //echo "Supplier Count = " . $chem_supplier_count . "\n";
            //echo "Company Name = " . $company_name . "\n";
            //echo "Company Country = " . $company_country . "\n";
            //echo "Last Update = " . $last_update . "\n";
            //echo "Company Description = " . $company_description . "\n";
            //echo "Link = " . $link . "\n\n";
    
            $record = array (
                'supplier_index' => $chem_supplier_count,
                'supplier_name' => $company_name,
                'country' => $company_country,
                'last_update' => $last_update, 
                'description' => $company_description,
                'link' => $link
    
            );
    
            scraperwiki::save_sqlite(array('supplier_index', 'supplier_name', 'country', 'last_update', 'description', 'link'), $record, "chem_suppliers", 2);
            $tr_count=0;
            $chem_supplier_count++;
    
        } else {
            $tr_count++;
        }

    }

        $record = array (
            'supplier_index' => $chem_supplier_count,
            'supplier_name' => $company_name,
            'country' => $company_country,
            'last_update' => $last_update, 
            'description' => $company_description,
            'link' => $link

        );

        scraperwiki::save_sqlite(array('supplier_index', 'supplier_name', 'country', 'last_update', 'description', 'link'), $record, "chem_suppliers", 2);
        $chem_supplier_count++;

        //var_dump($record);

}

?>
