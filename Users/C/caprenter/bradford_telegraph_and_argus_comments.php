<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

#Put your URL here. Can't guarantee it will work, especially if not on the telegraphandargus site - although this is the same type
#of site used by many local newspapers.
#Please leave other URL's in, cos someone might want to run their old data again.
#$html = scraperwiki::scrape("http://hotair.com/archives/2011/04/23/quotes-of-the-day-663/#comments");
$html = scraperwiki::scrape("http://hotair.com/archives/2011/04/23/quotes-of-the-day-663/#comments");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('<divid = "comment') as $data)
{
    #$comment = $data->find('div.q');
    $comment = $data->find('span',1);
    # Store data in the datastore
    #print_r ($articles);
    #scraperwiki::save(array('comment'), array('comment' => $articles));
    print $comment->plaintext . "\n";
    scraperwiki::save(array('comment'), array('comment' => $comment->plaintext));
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

#Put your URL here. Can't guarantee it will work, especially if not on the telegraphandargus site - although this is the same type
#of site used by many local newspapers.
#Please leave other URL's in, cos someone might want to run their old data again.
#$html = scraperwiki::scrape("http://hotair.com/archives/2011/04/23/quotes-of-the-day-663/#comments");
$html = scraperwiki::scrape("http://hotair.com/archives/2011/04/23/quotes-of-the-day-663/#comments");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('<divid = "comment') as $data)
{
    #$comment = $data->find('div.q');
    $comment = $data->find('span',1);
    # Store data in the datastore
    #print_r ($articles);
    #scraperwiki::save(array('comment'), array('comment' => $articles));
    print $comment->plaintext . "\n";
    scraperwiki::save(array('comment'), array('comment' => $comment->plaintext));
}

?>