<?php
require  'scraperwiki/simple_html_dom.php';
# Welcome to the second ScraperWiki PHP tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

//spider a site
//find email addresses
//find who is for domain
//store post code
//map on maps

//$site_list = array('paulmiller.it', 'amazon.com', 'google.com', 'catswhiskerstours.com');

//$results = array();

//foreach($site_list as $site){

  //  $results[] = scraperwiki::scrape("http://" . $site);
  //  print_r($results);
//print($site);
//};

////////////////


//get proxy list from site
//use proxy list to through for requests




$useragent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1";

//$postfields= null; 
//$postfields["noneed"] = "";
//$api_url= "http://www.whois.net/whois/hotmail.com";
$api_url= "http://www.whois.net/whois/catswhiskerstours.co.uk";
//$api_url= "http://paulmiller.it";

//$results= getUrlContent($postfields, $queryurl);
//echo $results;


$ch = curl_init();  
curl_setopt($ch, CURLOPT_USERAGENT, $useragent);
  curl_setopt($ch, CURLOPT_URL, $api_url); // set the url to fetch
  curl_setopt($ch, CURLOPT_HEADER, 0); // set headers (0 = no headers in result)
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); // type of transfer (1 = to string)
  curl_setopt($ch, CURLOPT_TIMEOUT, 10); // time to wait in seconds
 // curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);  
  $content = curl_exec($ch); // make the call  
  curl_close($ch);  


//if we get lucky, this will match
$whois_starts = 'Whois Server Version 2.0';
$whois_ends   = '<<';

//replace strings with ints 
$whois_starts = stripos($content, $whois_starts);
$whois_ends   = stripos($content , $whois_ends );

$whois_length = $whois_ends - $whois_starts;

$whois =  substr ($content , $whois_starts, $whois_length);


$detail_types = array('Domain Name', 'Registrar', 'Whois Server', 'Referral URL' ,
                      'Name Server' , 'Creation Date', 'Expiration Date', 'Updated Date');

foreach($detail_types as $type){

$reg_ex = '@'.$type.'\:.*@';

$matches = '';
preg_match($reg_ex, $whois, $matches);

$info = explode(': ', $matches[0]);

$whois_details[$type] = $info[1];

};

print_r($whois_details);








//$whois = scraperwiki::scrape("http://www.whois.net/whois/hotmail.com");
//print $whois;

//$html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html");
//print $html;

//print_r($results);

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML 
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

//$dom = new simple_html_dom();
//$dom->load($html);
//foreach($dom->find('td') as $data)
//{
//    print $data->plaintext . "\n";
//}

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

//foreach($dom->find('td') as $data)
//{
//    scraperwiki::save(array('data'), array('data' => $data->plaintext));//
//}

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?>