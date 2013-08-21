<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 101;
$i = 0;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;
while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.pureholidayhomes.com/search/united+kingdom/page=".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
      foreach($dom->find('div[class=single-result]') as $result){
        foreach($result->find('H2') as $title)
          foreach($title->find('a') as $anchor){
            echo $counter;
            $counter++;
            $cottageURL = $anchor->href;
echo $cottageURL;
          }            

          foreach($result->find('span[class=price xs]') as $title){
           $priceLow = $title->plaintext;
           $priceLow = str_replace("from &#163;","",$priceLow);
           $priceLow = str_replace("per week","",$priceLow);
           $priceLow = str_replace(",","",$priceLow);
           if(strpos($priceLow,"(property"))
             $priceLow="";
          }



          $record = array(
             'COTTAGE_URL'   => $cottageURL,
             'PRICE_LOW'     => $priceLow,
          );
print_r($record);
          scraperwiki::save(array('COTTAGE_URL'), $record);
      } 
$i++;
}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 101;
$i = 0;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;
while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.pureholidayhomes.com/search/united+kingdom/page=".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
      foreach($dom->find('div[class=single-result]') as $result){
        foreach($result->find('H2') as $title)
          foreach($title->find('a') as $anchor){
            echo $counter;
            $counter++;
            $cottageURL = $anchor->href;
echo $cottageURL;
          }            

          foreach($result->find('span[class=price xs]') as $title){
           $priceLow = $title->plaintext;
           $priceLow = str_replace("from &#163;","",$priceLow);
           $priceLow = str_replace("per week","",$priceLow);
           $priceLow = str_replace(",","",$priceLow);
           if(strpos($priceLow,"(property"))
             $priceLow="";
          }



          $record = array(
             'COTTAGE_URL'   => $cottageURL,
             'PRICE_LOW'     => $priceLow,
          );
print_r($record);
          scraperwiki::save(array('COTTAGE_URL'), $record);
      } 
$i++;
}
?>
