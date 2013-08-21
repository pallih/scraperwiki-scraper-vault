<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 428;
$i = 0;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);

    $url = "http://www.sykescottages.co.uk/search.html?page=".$i."&&from_landing_0&landing_page_csv=0&groundfloor=0&sauna=0&indoorpool=0&outdoorpool=0&livestock=0&fishing=0&henstag=0&family=0&isolated=0&countryside=0&games=0&pooltable=0&tabletennis=0&snooker=0&thatched=0&broadband=0&gradetwo=0&gayfriendly=0&tenniscourts=0&ecofriendly=0&unusual=0&logcabin=0&seaview=0&seaside=0&beach=0&romantic=0&nearwalks=0&nearcycling=0&nearriver=0&nearcanal=0&nationalpark=0&neargolf=0&spagym=0&enclosedgarden=0&childfriendly=0&arable=0&rustic=0&offers_only=0&farm=0&new=0&luxury=0&ingroup=0&nationaltrust=0&nearlake=0&skytv=0&spajacuzzi=0&character=0&kids=0&coastal=0&cotavailable=0&dishwasher=0&extrabathrooms=0&extratoilets=0&fourposterbed=0&groundfloorbed=0&highchairavailable=0&noanimals=0&nearmainroad=0&nearrailway=0&offroadparking=0&smokefree=0&telephone=0&washingmachine=0&touristboardrated=0&changeoverday=&smallpartyreduction=0&shortbreaksallowed=0&lastminutebreakallowed=0&gradeticks=&gradetwolisted=0&gmaps_state=&gmaps_infowin=&simontest=&country=&region=&area=&subarea=&start_date=dd%2Fmm%2Fyyyy&end_date=dd%2Fmm%2Fyyyy&duration=7&sleeps=&single=&findlocation=Enter+a+town+or+village+name&findlocationdist=10&location_id=&findcottage=Enter+cottage+name+or+ref+no&bathrooms=&distancesea=&numpets=";
    
    
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages
    foreach($dom->find('div[id=homecontentwrap]') as $page){
      $items = ""; 
      $elements ="";
      // Get a cottage

      foreach($page->find('div[class=searchresult]') as $cottage){
        $cottageURL = "";
        foreach($cottage->find('p[class=more]') as $element)
        if($cottageURL==""){
          $cottageURL = substr($element,strpos($element,' href=')+7);
          $cottageURL = substr($cottageURL,0,strpos($cottageURL,'"'));
        }

     
       $items = "";
       foreach($cottage->find('div[class=col2]') as $element){
   
          $items .= $element->plaintext."|";  
          $itemArr = explode("\r\n",$items);
          $cottageID= $itemArr[0];
          $cottageID= str_replace("Ref: ","",$cottageID);
          $priceLow= @$itemArr[3];
          $priceLow = str_replace("From:","",$priceLow );
          $priceLow = str_replace("£","",$priceLow );
          $priceLow  = str_replace("&pound;","",$priceLow );       
       }


        $record = array(
            'COTTAGE_URL'   => $cottageURL,
            'COTTAGE_ID'    => $cottageID,
            'PRICE_LOW'     => $priceLow,
            );
        scraperwiki::save(array('COTTAGE_URL'), $record);
    }
}
$i++;
}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 428;
$i = 0;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);

    $url = "http://www.sykescottages.co.uk/search.html?page=".$i."&&from_landing_0&landing_page_csv=0&groundfloor=0&sauna=0&indoorpool=0&outdoorpool=0&livestock=0&fishing=0&henstag=0&family=0&isolated=0&countryside=0&games=0&pooltable=0&tabletennis=0&snooker=0&thatched=0&broadband=0&gradetwo=0&gayfriendly=0&tenniscourts=0&ecofriendly=0&unusual=0&logcabin=0&seaview=0&seaside=0&beach=0&romantic=0&nearwalks=0&nearcycling=0&nearriver=0&nearcanal=0&nationalpark=0&neargolf=0&spagym=0&enclosedgarden=0&childfriendly=0&arable=0&rustic=0&offers_only=0&farm=0&new=0&luxury=0&ingroup=0&nationaltrust=0&nearlake=0&skytv=0&spajacuzzi=0&character=0&kids=0&coastal=0&cotavailable=0&dishwasher=0&extrabathrooms=0&extratoilets=0&fourposterbed=0&groundfloorbed=0&highchairavailable=0&noanimals=0&nearmainroad=0&nearrailway=0&offroadparking=0&smokefree=0&telephone=0&washingmachine=0&touristboardrated=0&changeoverday=&smallpartyreduction=0&shortbreaksallowed=0&lastminutebreakallowed=0&gradeticks=&gradetwolisted=0&gmaps_state=&gmaps_infowin=&simontest=&country=&region=&area=&subarea=&start_date=dd%2Fmm%2Fyyyy&end_date=dd%2Fmm%2Fyyyy&duration=7&sleeps=&single=&findlocation=Enter+a+town+or+village+name&findlocationdist=10&location_id=&findcottage=Enter+cottage+name+or+ref+no&bathrooms=&distancesea=&numpets=";
    
    
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages
    foreach($dom->find('div[id=homecontentwrap]') as $page){
      $items = ""; 
      $elements ="";
      // Get a cottage

      foreach($page->find('div[class=searchresult]') as $cottage){
        $cottageURL = "";
        foreach($cottage->find('p[class=more]') as $element)
        if($cottageURL==""){
          $cottageURL = substr($element,strpos($element,' href=')+7);
          $cottageURL = substr($cottageURL,0,strpos($cottageURL,'"'));
        }

     
       $items = "";
       foreach($cottage->find('div[class=col2]') as $element){
   
          $items .= $element->plaintext."|";  
          $itemArr = explode("\r\n",$items);
          $cottageID= $itemArr[0];
          $cottageID= str_replace("Ref: ","",$cottageID);
          $priceLow= @$itemArr[3];
          $priceLow = str_replace("From:","",$priceLow );
          $priceLow = str_replace("£","",$priceLow );
          $priceLow  = str_replace("&pound;","",$priceLow );       
       }


        $record = array(
            'COTTAGE_URL'   => $cottageURL,
            'COTTAGE_ID'    => $cottageID,
            'PRICE_LOW'     => $priceLow,
            );
        scraperwiki::save(array('COTTAGE_URL'), $record);
    }
}
$i++;
}
?>
