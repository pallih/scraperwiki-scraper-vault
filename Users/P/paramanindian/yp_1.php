<?php
    
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.yellowpages.com.au/search/listings?clue=restaurant&locationClue=sydney&x=0&y=0");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('li[class=listingContainer]') as $container)
{
    $name = $container->find('div[class=listingName]', 0)->find('div[class=omnitureListingNameLink]', 0)->plaintext;
    $desc = $container->find('div[class=listingInfoPanel]', 0)->find('div[class=textDesc]', 0)->plaintext;
    $website = $container->find('a[id=websiteLink]', 0)->href;
      
    $biz = array('name'=>trim($name),'description'=>trim($desc), 'website'=>trim($website));
    
    # Store data in the datastore
    scraperwiki::save(array('name'), $biz);
   
}
?>
<?php
    
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.yellowpages.com.au/search/listings?clue=restaurant&locationClue=sydney&x=0&y=0");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('li[class=listingContainer]') as $container)
{
    $name = $container->find('div[class=listingName]', 0)->find('div[class=omnitureListingNameLink]', 0)->plaintext;
    $desc = $container->find('div[class=listingInfoPanel]', 0)->find('div[class=textDesc]', 0)->plaintext;
    $website = $container->find('a[id=websiteLink]', 0)->href;
      
    $biz = array('name'=>trim($name),'description'=>trim($desc), 'website'=>trim($website));
    
    # Store data in the datastore
    scraperwiki::save(array('name'), $biz);
   
}
?>
