<?php
######################################
# Manchester Hack Day, Music Finder
# Creates XSPF Playlist of music :)
# This is Part 2 of 3 : Fetch MP3 DATA
######################################

require  'scraperwiki/simple_html_dom.php';

// This is from http://scraperwiki.com/api/1.0/explore/scraperwiki.datastore.getdata
$OPML = "http://api.scraperwiki.com/api/1.0/datastore/getdata?format=xml&name=bbc-radio-opml-rss-scraper";
$html = scraperwiki::scrape( $OPML );

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);


foreach($dom->find('resource') as $resource)
{
    # get the url for THIS feed
    $feedURL    = $resource->find('feed', 0)->plaintext;
   
    $itemArtwork = $resource->find('artwork', 0)->plaintext;
    $itemBranch = $resource->find('title', 0)->plaintext;
    $itemLink = $resource->find('link',0)->plaintext;
    // print "itemLink = ". $itemLink . "\n";

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $feed = scraperwiki::scrape( $feedURL );
    $feedDom = new simple_html_dom();
    $feedDom->load( $feed );


    # Loop through nodes and get each artist's feed and stuff like images...
    foreach($feedDom->find('item') as $item)
    {
        $itemTitle = $item->find('title', 0)->plaintext;
        $itemDescription = $item->find('description', 0)->plaintext;
        $itemData = $item->find('media:content', 0);  
        $itemTrack = $itemData -> url;
        $itemDuration= ($itemData -> duration)*60*1000;              // convert to milliseconds
 
        $itemResults = array(
            'author'=>$itemBranch, 
            'url' => $itemTrack, 
            'title'=> $itemTitle, 
            'artwork' => $itemArtwork, 
            'duration' => $itemDuration, 
            'description' => $itemDescription,
            'link' => $itemLink
        );
        // echo $itemLink . "\n";//;
     //  var_dump( $itemResults );
          scraperwiki::save(array('url', 'title'),$itemResults);
    }
    # end
}
