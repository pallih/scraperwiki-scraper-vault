<?php

//  Chemical Supplier Index
//  written 2012-08-03 by Conrad Sorenson

//  OUTLINE
//    1  Retrieve current supplier pointer
//    2  Link to data from chemical_supplier_index_a
//       2.1  Create table to store results
//    3  Look up supplier_index, increment by 1, then look up next supplier
//    4  Scrape in-depth record
//       4.1  Molecule
//       4.2  CAS
//       4.3  IUPAC
//       4.4  Address line 2
//       4.5  City
//       4.6  State/Province/Region
//       4.7  Zip/Postal code
//       4.8  Country
//       4.9  Web page
//    5  Update supplier record

//    FUTURE WORK
//    Scrape chemicals through multiple pages






//    1  Retrieve current supplier pointer
require 'scraperwiki/simple_html_dom.php';
scraperwiki::attach("chemical_supplier_index_a", "suppliers");
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `indepth_chem_suppliers` ('supplier_index' integer, 'supplier_name' text, 'description' text, 'link' text, 'phone' text, 'fax' text, 'address1' text, 'address2' text, 'city' text, 'state' text, 'zip' text, 'country' text, 'url' text, 'logo' text, 'last_update' text)");



for ($iCount=1; $iCount<=236; $iCount++) {




$sql_new = "* FROM indepth_chem_suppliers ORDER BY supplier_index DESC;";
$supplier_new = scraperwiki::select($sql_new);

//var_dump($supplier_new);

$record_new = $supplier_new[0];

if (! $record_new) {
    $supplier_index = 1;
} else {
    $supplier_index = $record_new["supplier_index"];
    //echo $record_new["supplier_index"] . " = " . $record_new["supplier_name"] . ",  " . $record_new["country"] . "\n";
    $supplier_index = $supplier_index + 1;
}

//$supplier_index=1;

//    2  Link to data from chemical_supplier_index_a
//       2.1  Create table to store results

$sql = "* FROM suppliers.chem_suppliers WHERE (chem_suppliers.supplier_index=$supplier_index) ORDER BY chem_suppliers.supplier_index;";

$supplier = scraperwiki::select($sql);
$record = $supplier[0];

//var_dump($record);

echo $record["supplier_index"] . " = " . $record["supplier_name"] . ",  " . $record["country"] . "\n";

//$supplier_index = $record["supplier_index"];
$supplier_name = $record["supplier_name"];
$country = $record["country"];
$description = $record["description"];
$link = $record["link"];
$last_update = $record["last_update"]; 

//echo $supplier_index . "  " . $supplier_name . "  " . $link . "\n";


//    4  Scrape in-depth record
$chem_suppliers = scraperwiki::scrape($link);
$chem_suppliers_dom = new simple_html_dom();
$chem_suppliers_dom->load($chem_suppliers);

$tableCount = 1;
$logo = "";

foreach($chem_suppliers_dom->find("div[@class='layout-right-column boxContainerText'] table") as $data){
    
    $stringTest = str_get_html($data);

    if (strlen($logo) == 0){
        if (strpos($stringTest,"Company Logo", 0) !== false) {
            foreach($data->find('img') as $element) {
                $logo = "http://www.molport.com/buy-chemicals/" . $element->src;
            }
        } else {
            $logo = "NA";
        }
    }

    $stringTest = trim($data->plaintext);

    //break 2;
    //echo "stringTest = " . $stringTest . "\n";

    if (strpos($stringTest,"Phone number", 0) !== false){
        
        $td_count = 1;
        foreach($data->find("td") as $tds){
            if ($td_count == 2) {
                $phone = trim($tds->plaintext);
            }

            if ($td_count == 4) {
                $fax = trim($tds->plaintext);
            }

            if ($td_count == 6) {
                $address1 = trim($tds->plaintext);
            }

            if ($td_count == 8) {
                $address2 = trim($tds->plaintext);
            }

            if ($td_count == 10) {
                $city = trim($tds->plaintext);
            }

            if ($td_count == 12) {
                $state = trim($tds->plaintext);
            }

            if ($td_count == 14) {
                $zip = trim($tds->plaintext);
            }

            if ($td_count == 16) {
                $country = trim($tds->plaintext);
            }

            if ($td_count == 18) {
                $url = trim($tds->plaintext);
            }

            $td_count++;
        }

    }
    $tableCount++;

}


//    5  Update supplier record

        if ($logo == "NA") {
            $logo = "";
        }

        //echo "Supplier_Index = " . $supplier_index . "\n";
        //echo "Supplier_Name = " . $supplier_name . "\n";
        //echo "Description = " . $description . "\n";
        //echo "Link = " . $link . "\n";
        //echo "Phone = " . $phone . "\n";

        //echo "Fax = " . $fax . "\n";
        //echo "Address1 = " . $address1 . "\n";
        //echo "Address2 = " . $address2 . "\n";
        //echo "City = " . $city . "\n";
        //echo "State = " . $state . "\n";

        //echo "Zip = " . $zip . "\n";
        //echo "Country = " . $country . "\n";
        //echo "URL = " . $url . "\n";
        //echo "Last Update = " . $last_update . "\n";

        $indepth_record = array (

            'supplier_index' => $supplier_index,
            'supplier_name' => $supplier_name,
            'description' => $description,
            'link' => $link,
            'phone' => $phone,

            'fax' => $fax,
            'address1' => $address1,
            'address2' => $address2,
            'city' => $city,
            'state' => $state,

            'zip' => $zip,
            'country' => $country,
            'url' => $url,
            'logo' => $logo,
            'last_update' => $last_update

        );

        $logo = "";

        //var_dump ($indepth_record);

        scraperwiki::save_sqlite(array('supplier_index', 'supplier_name', 'description', 'link', 'phone', 'fax', 'address1', 'address2', 'city', 'state', 'zip', 'country', 'url', 'last_update'), $indepth_record, "indepth_chem_suppliers", 2);

}

?>
<?php

//  Chemical Supplier Index
//  written 2012-08-03 by Conrad Sorenson

//  OUTLINE
//    1  Retrieve current supplier pointer
//    2  Link to data from chemical_supplier_index_a
//       2.1  Create table to store results
//    3  Look up supplier_index, increment by 1, then look up next supplier
//    4  Scrape in-depth record
//       4.1  Molecule
//       4.2  CAS
//       4.3  IUPAC
//       4.4  Address line 2
//       4.5  City
//       4.6  State/Province/Region
//       4.7  Zip/Postal code
//       4.8  Country
//       4.9  Web page
//    5  Update supplier record

//    FUTURE WORK
//    Scrape chemicals through multiple pages






//    1  Retrieve current supplier pointer
require 'scraperwiki/simple_html_dom.php';
scraperwiki::attach("chemical_supplier_index_a", "suppliers");
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `indepth_chem_suppliers` ('supplier_index' integer, 'supplier_name' text, 'description' text, 'link' text, 'phone' text, 'fax' text, 'address1' text, 'address2' text, 'city' text, 'state' text, 'zip' text, 'country' text, 'url' text, 'logo' text, 'last_update' text)");



for ($iCount=1; $iCount<=236; $iCount++) {




$sql_new = "* FROM indepth_chem_suppliers ORDER BY supplier_index DESC;";
$supplier_new = scraperwiki::select($sql_new);

//var_dump($supplier_new);

$record_new = $supplier_new[0];

if (! $record_new) {
    $supplier_index = 1;
} else {
    $supplier_index = $record_new["supplier_index"];
    //echo $record_new["supplier_index"] . " = " . $record_new["supplier_name"] . ",  " . $record_new["country"] . "\n";
    $supplier_index = $supplier_index + 1;
}

//$supplier_index=1;

//    2  Link to data from chemical_supplier_index_a
//       2.1  Create table to store results

$sql = "* FROM suppliers.chem_suppliers WHERE (chem_suppliers.supplier_index=$supplier_index) ORDER BY chem_suppliers.supplier_index;";

$supplier = scraperwiki::select($sql);
$record = $supplier[0];

//var_dump($record);

echo $record["supplier_index"] . " = " . $record["supplier_name"] . ",  " . $record["country"] . "\n";

//$supplier_index = $record["supplier_index"];
$supplier_name = $record["supplier_name"];
$country = $record["country"];
$description = $record["description"];
$link = $record["link"];
$last_update = $record["last_update"]; 

//echo $supplier_index . "  " . $supplier_name . "  " . $link . "\n";


//    4  Scrape in-depth record
$chem_suppliers = scraperwiki::scrape($link);
$chem_suppliers_dom = new simple_html_dom();
$chem_suppliers_dom->load($chem_suppliers);

$tableCount = 1;
$logo = "";

foreach($chem_suppliers_dom->find("div[@class='layout-right-column boxContainerText'] table") as $data){
    
    $stringTest = str_get_html($data);

    if (strlen($logo) == 0){
        if (strpos($stringTest,"Company Logo", 0) !== false) {
            foreach($data->find('img') as $element) {
                $logo = "http://www.molport.com/buy-chemicals/" . $element->src;
            }
        } else {
            $logo = "NA";
        }
    }

    $stringTest = trim($data->plaintext);

    //break 2;
    //echo "stringTest = " . $stringTest . "\n";

    if (strpos($stringTest,"Phone number", 0) !== false){
        
        $td_count = 1;
        foreach($data->find("td") as $tds){
            if ($td_count == 2) {
                $phone = trim($tds->plaintext);
            }

            if ($td_count == 4) {
                $fax = trim($tds->plaintext);
            }

            if ($td_count == 6) {
                $address1 = trim($tds->plaintext);
            }

            if ($td_count == 8) {
                $address2 = trim($tds->plaintext);
            }

            if ($td_count == 10) {
                $city = trim($tds->plaintext);
            }

            if ($td_count == 12) {
                $state = trim($tds->plaintext);
            }

            if ($td_count == 14) {
                $zip = trim($tds->plaintext);
            }

            if ($td_count == 16) {
                $country = trim($tds->plaintext);
            }

            if ($td_count == 18) {
                $url = trim($tds->plaintext);
            }

            $td_count++;
        }

    }
    $tableCount++;

}


//    5  Update supplier record

        if ($logo == "NA") {
            $logo = "";
        }

        //echo "Supplier_Index = " . $supplier_index . "\n";
        //echo "Supplier_Name = " . $supplier_name . "\n";
        //echo "Description = " . $description . "\n";
        //echo "Link = " . $link . "\n";
        //echo "Phone = " . $phone . "\n";

        //echo "Fax = " . $fax . "\n";
        //echo "Address1 = " . $address1 . "\n";
        //echo "Address2 = " . $address2 . "\n";
        //echo "City = " . $city . "\n";
        //echo "State = " . $state . "\n";

        //echo "Zip = " . $zip . "\n";
        //echo "Country = " . $country . "\n";
        //echo "URL = " . $url . "\n";
        //echo "Last Update = " . $last_update . "\n";

        $indepth_record = array (

            'supplier_index' => $supplier_index,
            'supplier_name' => $supplier_name,
            'description' => $description,
            'link' => $link,
            'phone' => $phone,

            'fax' => $fax,
            'address1' => $address1,
            'address2' => $address2,
            'city' => $city,
            'state' => $state,

            'zip' => $zip,
            'country' => $country,
            'url' => $url,
            'logo' => $logo,
            'last_update' => $last_update

        );

        $logo = "";

        //var_dump ($indepth_record);

        scraperwiki::save_sqlite(array('supplier_index', 'supplier_name', 'description', 'link', 'phone', 'fax', 'address1', 'address2', 'city', 'state', 'zip', 'country', 'url', 'last_update'), $indepth_record, "indepth_chem_suppliers", 2);

}

?>
