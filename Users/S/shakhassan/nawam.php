<?php

require  'scraperwiki/simple_html_dom.php'; 

$html = scraperwiki::scrape("http://login.nawam.com.my/workshop/search_workshop/q"); 
//echo $html; 

# Use the PHP Simple HTML DOM Parser to extract <td> tags 
$dom = new simple_html_dom(); 
$dom->load($html); 

foreach($dom->find('td') as $data) 
{ 
    # Store data in the datastore 
    echo $data->plaintext . "\n"; 
    scraperwiki::save(array('data'), array('data' => $data->plaintext)); 
} 

$nextData=$dom->find('div[class=pagination]');
echo $nextData;

?>
<?php

require  'scraperwiki/simple_html_dom.php'; 

$html = scraperwiki::scrape("http://login.nawam.com.my/workshop/search_workshop/q"); 
//echo $html; 

# Use the PHP Simple HTML DOM Parser to extract <td> tags 
$dom = new simple_html_dom(); 
$dom->load($html); 

foreach($dom->find('td') as $data) 
{ 
    # Store data in the datastore 
    echo $data->plaintext . "\n"; 
    scraperwiki::save(array('data'), array('data' => $data->plaintext)); 
} 

$nextData=$dom->find('div[class=pagination]');
echo $nextData;

?>
