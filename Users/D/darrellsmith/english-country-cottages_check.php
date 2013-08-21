<?php
// These are for info only
$MAX_ENGLAND_PAGES = 229;
$MAX_SCOTLAND_PAGES = 37;
$MAX_WALES_PAGES = 24;



// dummy savevar() to workaround the bug!
scraperwiki::save_var('dummy', 0);

// get the saved country
$country  = scraperwiki::get_var("currentcountry");

if($country=="" || $country == "england")
    runEngland();
elseif($country == "scotland"){
    runScotland();
}else{
    runWales();
}

function runEngland(){
    echo "England";
    // set the maximum number of pages to scrape
    $currentMaxPages = 229;

    // bookmark the current country
    scraperwiki::save_var("currentcountry","england");
    // The Url to Scrape
    $url = "http://www.english-country-cottages.co.uk/england?page=";
    // Call the scraper
    get_details($url,$currentMaxPages);

    // Reset the page counter and move on to the next country
    scraperwiki::save_var("page",1);
    runScotland($dom);
}


function runScotland(){
echo "Scotland";
    // set the maximum number of pages to scrape
    $currentMaxPages  =  37;
    // bookmark the current country
    scraperwiki::save_var("currentcountry","scotland");
    // The URL to scrape
    $url = "http://www.english-country-cottages.co.uk/scotland?page=";
    
    // Call the scraper
    get_details($url,$currentMaxPages);
            
    // Reset the page counter and move on to the next country
    scraperwiki::save_var("page",1);
    runWales();
}

function runWales(){
echo "Wales";
    // the maximum nuber of pages to scrape
    $currentMaxPages = 24;
    // bookmark the current country
    scraperwiki::save_var("currentcountry","wales");

    // The URL to scrape
    $url = "http://www.english-country-cottages.co.uk/wales?page=";
    
    // Call the scraper
    get_details($url,$currentMaxPages);
           
    // Reset the page counter and move on to the next country
    scraperwiki::save_var("page",1);
}


function get_details($url,$CurrentMaxPages){
    // get the scraperwiki methods and create a new intance
    require_once 'scraperwiki/simple_html_dom.php';
    $dom = new simple_html_dom();

    // Get the bookmarked page if there is one
    // else start at 1
    $getPage = scraperwiki::get_var("page");
    $page = 1;
    if($getPage  != ""){
        $page = $getPage;
    }
       
    while($page <= $CurrentMaxPages){
        // bookmark record
        scraperwiki::save_var("page",$page);

        //load the page into the scraper
        $html = scraperWiki::scrape($url.$page);
        $dom->load($html);
        
        // get Details
        $i=0;
        while($i < 12){
          // Get URL
          foreach($dom->find('a[id=SearchResult1_linkTo_'.$i.']') as $data){
            $element = $dom->find('a');
            $cotturl = $data->getAttribute( 'href' );
            $cotturl = str_replace("/cottages/","",$cotturl);
          }          
                
          // get High / Low Prices
          foreach($dom->find('span[id=featureBoxPropertyWasPricePoundPr_'.$i.']') as $data){
            $prices = str_replace("Prices from ","",$data->plaintext);
            $prices = str_replace(" based on available 7 nights","",$prices );   
            $prices = str_replace("£","",$prices );  
            $prices = explode("-",$prices);
            $price_low = $prices[0];
            $price_high = $prices[1];
          }
          
          // Put the records into an array
          $record = array(
             'COTTAGE_URL'  => trim($cotturl),
             'PRICE_HIGH'   => trim($price_high),
             'PRICE_LOW'    => trim($price_low),
          );
          
          # save the data
          scraperwiki::save(array('COTTAGE_URL'), $record);
          $i++;
        }
        // move on to the next record
        $page++;
    }
}



?>
<?php
// These are for info only
$MAX_ENGLAND_PAGES = 229;
$MAX_SCOTLAND_PAGES = 37;
$MAX_WALES_PAGES = 24;



// dummy savevar() to workaround the bug!
scraperwiki::save_var('dummy', 0);

// get the saved country
$country  = scraperwiki::get_var("currentcountry");

if($country=="" || $country == "england")
    runEngland();
elseif($country == "scotland"){
    runScotland();
}else{
    runWales();
}

function runEngland(){
    echo "England";
    // set the maximum number of pages to scrape
    $currentMaxPages = 229;

    // bookmark the current country
    scraperwiki::save_var("currentcountry","england");
    // The Url to Scrape
    $url = "http://www.english-country-cottages.co.uk/england?page=";
    // Call the scraper
    get_details($url,$currentMaxPages);

    // Reset the page counter and move on to the next country
    scraperwiki::save_var("page",1);
    runScotland($dom);
}


function runScotland(){
echo "Scotland";
    // set the maximum number of pages to scrape
    $currentMaxPages  =  37;
    // bookmark the current country
    scraperwiki::save_var("currentcountry","scotland");
    // The URL to scrape
    $url = "http://www.english-country-cottages.co.uk/scotland?page=";
    
    // Call the scraper
    get_details($url,$currentMaxPages);
            
    // Reset the page counter and move on to the next country
    scraperwiki::save_var("page",1);
    runWales();
}

function runWales(){
echo "Wales";
    // the maximum nuber of pages to scrape
    $currentMaxPages = 24;
    // bookmark the current country
    scraperwiki::save_var("currentcountry","wales");

    // The URL to scrape
    $url = "http://www.english-country-cottages.co.uk/wales?page=";
    
    // Call the scraper
    get_details($url,$currentMaxPages);
           
    // Reset the page counter and move on to the next country
    scraperwiki::save_var("page",1);
}


function get_details($url,$CurrentMaxPages){
    // get the scraperwiki methods and create a new intance
    require_once 'scraperwiki/simple_html_dom.php';
    $dom = new simple_html_dom();

    // Get the bookmarked page if there is one
    // else start at 1
    $getPage = scraperwiki::get_var("page");
    $page = 1;
    if($getPage  != ""){
        $page = $getPage;
    }
       
    while($page <= $CurrentMaxPages){
        // bookmark record
        scraperwiki::save_var("page",$page);

        //load the page into the scraper
        $html = scraperWiki::scrape($url.$page);
        $dom->load($html);
        
        // get Details
        $i=0;
        while($i < 12){
          // Get URL
          foreach($dom->find('a[id=SearchResult1_linkTo_'.$i.']') as $data){
            $element = $dom->find('a');
            $cotturl = $data->getAttribute( 'href' );
            $cotturl = str_replace("/cottages/","",$cotturl);
          }          
                
          // get High / Low Prices
          foreach($dom->find('span[id=featureBoxPropertyWasPricePoundPr_'.$i.']') as $data){
            $prices = str_replace("Prices from ","",$data->plaintext);
            $prices = str_replace(" based on available 7 nights","",$prices );   
            $prices = str_replace("£","",$prices );  
            $prices = explode("-",$prices);
            $price_low = $prices[0];
            $price_high = $prices[1];
          }
          
          // Put the records into an array
          $record = array(
             'COTTAGE_URL'  => trim($cotturl),
             'PRICE_HIGH'   => trim($price_high),
             'PRICE_LOW'    => trim($price_low),
          );
          
          # save the data
          scraperwiki::save(array('COTTAGE_URL'), $record);
          $i++;
        }
        // move on to the next record
        $page++;
    }
}



?>
