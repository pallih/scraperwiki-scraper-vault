<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 1458;
$i = 0;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);

    $url = "http://www.holidaylettings.co.uk/england/pageid.".$i."/";
    
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages
    foreach($dom->find('div[class=headline]') as $page){
      $cottageName = "";
      foreach($dom->find('H3') as $name)
        foreach($page->find('a') as $fragment)
          if($cottageName == "")
            $cottageName = $fragment->plaintext; 
       
      $cottageURL = "";
      foreach($page->find('a') as $fragment)
        if($cottageURL == "")
          $cottageURL = $fragment->href;

      $cottageID = "";
      foreach($page->find('a') as $fragment)
        if($cottageID == ""){
          $cottageID = $fragment->href;
          $cottageID = substr($cottageID,-6);
        }
    
      $record = array(
        'COTTAGE_URL'   => $cottageURL,
  # 'COTTAGE_NAME'   => $cottageName,
       'COTTAGE_ID'    => $cottageID,

            );
       scraperwiki::save(array('COTTAGE_URL'), $record);
    }


$i++;

}
?>
