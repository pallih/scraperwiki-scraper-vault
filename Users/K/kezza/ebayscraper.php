<?php

// Save a record to the data store.
function saveData($unique, $record) {
scraperWiki::save_sqlite(array("Data_autocount", "data_blank", "data_Feedback"), $record);
}

// Setup variables
$Mypages=33;
$MyString = "";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

for ($Mypages=35; $Mypages<=35; $Mypages+= 1)
{
    $MyString = "http://feedback.ebay.co.uk/ws/eBayISAPI.dll?ViewFeedback2&ftab=FeedbackAsSeller&userid=thespiceworksteam&iid=270914025018&de=off&items=2300&interval=0&mPg=2345&page=".$Mypages;
    
    $html = scraperWiki::scrape($MyString);
    //print $html . "\n";
    print "MyPages = " . $Mypages . "\n";
    print "MyString = " . $MyString . "\n";
    
    
    // require 'scraperwiki/simple_html_dom.php';
    // $dom = new simple_html_dom();
    $dom->load($html);
        foreach($dom->find("table.FbOuterYukon") as $data){
        $tds = $data->find("td");
        
            for ($i=4; $i<=197; $i+= 8)
            {
// Negative row class is <tr class="fbOuterAddComm"><td class="fbOuterAddComm">
// If negrow then only save specified fields

 //               if($tds[$i+6]->plaintext !="&nbsp;") // Feedback from supplier
                

                  $record = array(
                    // Header
                    // 'data_Feedback/item' => $tds[1]->plaintext,
                    // 'data_From Buyer/price' => $tds[2]->plaintext,
                    // 'data_Date/time' => $tds[3]->plaintext,
                    //Record1
                    // Start at #4
                    'Data_autocount' =>$i,
                    'data_blank' => $tds[$i]->plaintext,
                    'data_Feedback' => $tds[$i+1]->plaintext,
                    'data_MemberID_AND_FeedbackScore' => $tds[$i+2]->plaintext,
                    'data_Date-Time' => $tds[$i+3]->plaintext,
                    'data_blank2' => $tds[$i+4]->plaintext,
                    'data_Item_Weight_Price_ItemNumber' => $tds[$i+5]->plaintext,
                    'data_Price' => $tds[$i+6]->plaintext,
                    'data_ViewItemLink' => $tds[$i+7]->plaintext
                    );
  //              else
  //              {
  //                  $record = array(
  //                  'Data_autocount' =>$i,
  //                  'data_blank' => $tds[$i]->plaintext,
  //                  'data_Feedback' => $tds[$i+1]->plaintext,
  //                  'data_MemberID_AND_FeedbackScore' => $tds[$i+2]->plaintext,
  //                  'data_Date-Time' => $tds[$i+3]->plaintext,
  //                  'data_blank2' => $tds[$i+4]->plaintext,
  //                  'data_Item_Weight_Price_ItemNumber' => $tds[$i+5]->plaintext
  //                  );
  //                  //$i -= 1;
  //              } 
            //print_r($record); 
            for ($d=1; $d<=10; $d++)
            { 
            //print_r($d); 
            
            // Save the record.
            saveData(array("Data_autocount"), $record);
            }
            } // for ($i=4; $i<=197; $i+= 8)
        } // foreach($dom->find("table.FbOuterYukon") as $data){
} // for ($paqes=1; $i<=3; $i+= 1)
// Save to magic SQL record

?>
<?php

// Save a record to the data store.
function saveData($unique, $record) {
scraperWiki::save_sqlite(array("Data_autocount", "data_blank", "data_Feedback"), $record);
}

// Setup variables
$Mypages=33;
$MyString = "";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

for ($Mypages=35; $Mypages<=35; $Mypages+= 1)
{
    $MyString = "http://feedback.ebay.co.uk/ws/eBayISAPI.dll?ViewFeedback2&ftab=FeedbackAsSeller&userid=thespiceworksteam&iid=270914025018&de=off&items=2300&interval=0&mPg=2345&page=".$Mypages;
    
    $html = scraperWiki::scrape($MyString);
    //print $html . "\n";
    print "MyPages = " . $Mypages . "\n";
    print "MyString = " . $MyString . "\n";
    
    
    // require 'scraperwiki/simple_html_dom.php';
    // $dom = new simple_html_dom();
    $dom->load($html);
        foreach($dom->find("table.FbOuterYukon") as $data){
        $tds = $data->find("td");
        
            for ($i=4; $i<=197; $i+= 8)
            {
// Negative row class is <tr class="fbOuterAddComm"><td class="fbOuterAddComm">
// If negrow then only save specified fields

 //               if($tds[$i+6]->plaintext !="&nbsp;") // Feedback from supplier
                

                  $record = array(
                    // Header
                    // 'data_Feedback/item' => $tds[1]->plaintext,
                    // 'data_From Buyer/price' => $tds[2]->plaintext,
                    // 'data_Date/time' => $tds[3]->plaintext,
                    //Record1
                    // Start at #4
                    'Data_autocount' =>$i,
                    'data_blank' => $tds[$i]->plaintext,
                    'data_Feedback' => $tds[$i+1]->plaintext,
                    'data_MemberID_AND_FeedbackScore' => $tds[$i+2]->plaintext,
                    'data_Date-Time' => $tds[$i+3]->plaintext,
                    'data_blank2' => $tds[$i+4]->plaintext,
                    'data_Item_Weight_Price_ItemNumber' => $tds[$i+5]->plaintext,
                    'data_Price' => $tds[$i+6]->plaintext,
                    'data_ViewItemLink' => $tds[$i+7]->plaintext
                    );
  //              else
  //              {
  //                  $record = array(
  //                  'Data_autocount' =>$i,
  //                  'data_blank' => $tds[$i]->plaintext,
  //                  'data_Feedback' => $tds[$i+1]->plaintext,
  //                  'data_MemberID_AND_FeedbackScore' => $tds[$i+2]->plaintext,
  //                  'data_Date-Time' => $tds[$i+3]->plaintext,
  //                  'data_blank2' => $tds[$i+4]->plaintext,
  //                  'data_Item_Weight_Price_ItemNumber' => $tds[$i+5]->plaintext
  //                  );
  //                  //$i -= 1;
  //              } 
            //print_r($record); 
            for ($d=1; $d<=10; $d++)
            { 
            //print_r($d); 
            
            // Save the record.
            saveData(array("Data_autocount"), $record);
            }
            } // for ($i=4; $i<=197; $i+= 8)
        } // foreach($dom->find("table.FbOuterYukon") as $data){
} // for ($paqes=1; $i<=3; $i+= 1)
// Save to magic SQL record

?>
