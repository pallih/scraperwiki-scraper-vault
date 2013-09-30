<?php
#Yes, this scraper needs help

require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.hcsheriff.gov/cor/display.php?day=0");
#print $html;
$dom = new simple_html_dom();
$dom->load($html);

$items = $dom->find('tr');    
  
foreach($items as $post) {  
    # remember comments count as nodes  
    $articles[] = array($post->children(0)->plaintext,  
                        $post->children(1)->plaintext,
                        $post->children(2)->plaintext,
                        $post->children(3)->plaintext,
                        $post->children(4)->plaintext); 
 
} 
$length = count($articles);
#echo $length;
print_r($articles);

  

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

#foreach($dom->find('tr') as $data)
#{
#    foreach($data->find('td') as $data2){
#   scraperwiki::save(array('data'), array('data' => $data2->plaintext . '|'));
#    }
#}


# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?><?php
#Yes, this scraper needs help

require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.hcsheriff.gov/cor/display.php?day=0");
#print $html;
$dom = new simple_html_dom();
$dom->load($html);

$items = $dom->find('tr');    
  
foreach($items as $post) {  
    # remember comments count as nodes  
    $articles[] = array($post->children(0)->plaintext,  
                        $post->children(1)->plaintext,
                        $post->children(2)->plaintext,
                        $post->children(3)->plaintext,
                        $post->children(4)->plaintext); 
 
} 
$length = count($articles);
#echo $length;
print_r($articles);

  

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

#foreach($dom->find('tr') as $data)
#{
#    foreach($data->find('td') as $data2){
#   scraperwiki::save(array('data'), array('data' => $data2->plaintext . '|'));
#    }
#}


# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?>