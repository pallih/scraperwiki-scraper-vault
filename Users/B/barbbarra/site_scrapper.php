<?php
require  'scraperwiki/simple_html_dom.php';
# Welcome to the second ScraperWiki PHP tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page
#$html = scraperwiki::scrape("http://www.hamleys.com/sitemap1_default.xml");
$html = scraperwiki::scrape("http://direct.asda.com/sitemap1_default.xml");
#var $token = "&access_token=AAACEdEose0cBAItoy6FyTNxX4EsL2v46gfPMoh0hVHMJOCqq6AqUfLRNwLckw1Gs30qsGCnFonPGV86Wqh3ZCYkkoAek9827wIsBdZAijgBhCZAUurl";
#var $apiPrefix = "https://api.facebook.com/method/fql.query?query=SELECT url, normalized_url, share_count, like_count FROM link_stat WHERE url=";
#var $facebookapiURL = NULL;

#print $html;

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML 
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
print $dom;
#foreach($dom->find('loc') as $data)
#{
#     print $data->plaintext;
#    print 'https://api.facebook.com/method/fql.query?query=SELECT url, normalized_url, share_count, like_count FROM link_stat WHERE url='. '"' . $data->plaintext . '"' .'&access_token=AAACEdEose0cBAItoy6FyTNxX4EsL2v46gfPMoh0hVHMJOCqq6AqUfLRNwLckw1Gs30qsGCnFonPGV86Wqh3ZCYkkoAek9827wIsBdZAijgBhCZAUurl' . '\n';
    
#    $facebookhtml = scraperwiki::scrape('https://api.facebook.com/method/fql.query?query=SELECT url, normalized_url, share_count, like_count FROM link_stat WHERE url='. '"' . $data->plaintext . '"' .'&access_token=AAACEdEose0cBAItoy6FyTNxX4EsL2v46gfPMoh0hVHMJOCqq6AqUfLRNwLckw1Gs30qsGCnFonPGV86Wqh3ZCYkkoAek9827wIsBdZAijgBhCZAUurl');
#    $facebookdom = new simple_html_dom();
#    $facebookdom->load($facebookhtml);
#    foreach($facebookdom->find('share_count') as $shareCount)
#      {
#         print $shareCount->plaintext;
#      }
#}

#foreach($data as $data1)
#{
#     $facebookapiURL = $apiPrefix . '"' . $data1 . '"' . $token;
#     print facebookapiURL;
#}

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

#foreach($dom->find('td') as $data)
#{
#    scraperwiki::save(array('data'), array('data' => $data->plaintext));
#}

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?><?php
require  'scraperwiki/simple_html_dom.php';
# Welcome to the second ScraperWiki PHP tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page
#$html = scraperwiki::scrape("http://www.hamleys.com/sitemap1_default.xml");
$html = scraperwiki::scrape("http://direct.asda.com/sitemap1_default.xml");
#var $token = "&access_token=AAACEdEose0cBAItoy6FyTNxX4EsL2v46gfPMoh0hVHMJOCqq6AqUfLRNwLckw1Gs30qsGCnFonPGV86Wqh3ZCYkkoAek9827wIsBdZAijgBhCZAUurl";
#var $apiPrefix = "https://api.facebook.com/method/fql.query?query=SELECT url, normalized_url, share_count, like_count FROM link_stat WHERE url=";
#var $facebookapiURL = NULL;

#print $html;

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML 
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
print $dom;
#foreach($dom->find('loc') as $data)
#{
#     print $data->plaintext;
#    print 'https://api.facebook.com/method/fql.query?query=SELECT url, normalized_url, share_count, like_count FROM link_stat WHERE url='. '"' . $data->plaintext . '"' .'&access_token=AAACEdEose0cBAItoy6FyTNxX4EsL2v46gfPMoh0hVHMJOCqq6AqUfLRNwLckw1Gs30qsGCnFonPGV86Wqh3ZCYkkoAek9827wIsBdZAijgBhCZAUurl' . '\n';
    
#    $facebookhtml = scraperwiki::scrape('https://api.facebook.com/method/fql.query?query=SELECT url, normalized_url, share_count, like_count FROM link_stat WHERE url='. '"' . $data->plaintext . '"' .'&access_token=AAACEdEose0cBAItoy6FyTNxX4EsL2v46gfPMoh0hVHMJOCqq6AqUfLRNwLckw1Gs30qsGCnFonPGV86Wqh3ZCYkkoAek9827wIsBdZAijgBhCZAUurl');
#    $facebookdom = new simple_html_dom();
#    $facebookdom->load($facebookhtml);
#    foreach($facebookdom->find('share_count') as $shareCount)
#      {
#         print $shareCount->plaintext;
#      }
#}

#foreach($data as $data1)
#{
#     $facebookapiURL = $apiPrefix . '"' . $data1 . '"' . $token;
#     print facebookapiURL;
#}

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

#foreach($dom->find('td') as $data)
#{
#    scraperwiki::save(array('data'), array('data' => $data->plaintext));
#}

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?>