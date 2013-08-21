<?php

//  USPTO Patent Classification Index
//  written 2012-07-22 by Conrad Sorenson

//  OUTLINE
//    1  Retrieve current CCL Class from stored data
//    2  Link to data from uspto_patent_classifications_ccl_class_codes
//       2.1  Create table to store results
//    3  Look up class_index, increment by 1, then look up next class_num
//    4  Scrape Subclassifications for new class_num
//       4.1  Subclassification titles
//       4.2  Subclassification indent levels
//    5  Update class_num



//    1  Retrieve current CCL Class from stored data
$Value = scraperwiki::get_var("Current_CCL");


//    2  Link to data from uspto_patent_classifications_ccl_class_codes
//       2.1  Create table to store results
scraperwiki::attach("uspto_patent_classifications_ccl_class_codes", "class");

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `subclass_data` ('class_index' integer, 'subclass_index' integer, 'class_num' text, 'subclass_num' text, 'indent' integer, 'title' text)");


//    3  Look up class_index, increment by 1, then look up next class_num
if ($Value == "RESET"){
    $Value = 1;
} else {
    $sql = "* from class.swdata WHERE class.swdata.class_num LIKE '" . $Value . "'";
    $class = scraperwiki::select($sql);
    $record = $class[0];
    
    $Value = $record["class_index"] + 1;
    // $Value = $record["class_index"];
}

//       NOTE:  Last record, class_index = 473
if ($Value == "474"){
    break 10;
}

$sql = "* from class.swdata WHERE class.swdata.class_index LIKE '" . $Value . "'";
$class = scraperwiki::select($sql);

$record = $class[0];
$class_index = $record["class_index"];
$class_num = $record["class_num"];

echo $class_index . "    " . $class_num . "    " . $record["class_title"] . "\n";


//    4  Scrape Subclassifications for new class_num
//       4.1  Subclassification titles
//       4.2  Subclassification indent levels

require 'scraperwiki/simple_html_dom.php';           

$subclass_url = str_replace("XXX",strtolower($class_num),"http://www.uspto.gov/web/patents/classification/uspcXXX/schedXXX.htm");

$html_subclass = scraperwiki::scrape($subclass_url);

$subclass_dom = new simple_html_dom();
$subclass_dom->load($html_subclass);

$subclass_count = 0;

foreach($subclass_dom->find("table[@width='100%'] tr") as $subclass_data){
    $subclass_tds = $subclass_data->find("td");
    
    if(count($subclass_tds)>3){

        $scn = $subclass_tds[3]->plaintext;
        $sct = $subclass_tds[4]->plaintext;
        $indent = $subclass_tds[4];
        
        if(count($subclass_tds)>5){

            $scn = $subclass_tds[4]->plaintext;
            $sct = $subclass_tds[5]->plaintext;
            $indent = $subclass_tds[5];

        }

        $scn = str_replace("&nbsp;", " ", $scn);
        $scn = trim($scn);

        $sct = str_replace("&nbsp;", " ", $sct);
        $sct = trim($sct);


        $needle = "indent level is ";
        $pos = strpos($indent,$needle);
        
        if($pos === false) {
         // string needle NOT found in haystack
            $indent = "0";
            //echo $scn . " indent level = " . $indent . "\n";
        }
        else {
         // string needle found in haystack
            $indent = substr($indent, $pos + 16, 2);
            $indent = str_replace("\"", "", $indent);
            //echo $scn . " indent level = " . $indent . "\n";
        }

        //echo $class_num . "/" . $scn . "\n";

        $subclass_count++;
        

        $record = array (
            'subclass_index' => $subclass_count,
            'class_index' => $class_index,
            'class_num' => $class_num,
            'subclass_num' => $scn, 
            'indent' => $indent,
            'title' => $sct
        );
        //scraperwiki::save(array('subclass_index'), $record);
        scraperwiki::save_sqlite(array('class_index', 'subclass_index', 'class_num', 'subclass_num', 'indent', 'title'), $record, "subclass_data", 2);
        //scraperwiki::save_sqlite(array('subclass_index'), $record);

       //   echo "$subclass_count    $class_index    $class_num    $scn    $indent    $sct    \n";

    }
}


//    5  Update class_num
scraperwiki::save_var("Current_CCL", $record["class_num"])



//scraperwiki::save_var("Current_CCL", "RESET")
//scraperwiki::save_var("Current_CCL", "139")



?>
