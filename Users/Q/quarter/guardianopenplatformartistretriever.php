<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$pageNumber = 0;
$max_pages = 4;
    
while ($pageNumber < $max_pages)
{   
    //echo $pageNumber;
    $API = "http://content.guardianapis.com/tags.xml?section=music&reference-type=musicbrainz";
    if ($pageNumber > 0) $API .= "&page=".$pageNumber;
    
    $html = scraperwiki::scrape( $API );
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    
     # Set the amount of page numbers available :
    $response = $dom->find('response',0);
    //print $response ;
    $max_pages = isset($response->pages) ? intval($response->pages) : 4;
    //print $max_pages;
    
    foreach( $dom->find('tag') as $data )
    {
        # Store data in the datastore
        $artist = $data->id;
        // strip off the first 6 chars
        $artist = substr($artist , 6);
        // remove hyphens!
        $artist = str_replace( '-','',$artist );
        //print $artist;
        scraperwiki::save(array('artistname'), array('artistname' => $artist));
    }
    
    $pageNumber++;
}
?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$pageNumber = 0;
$max_pages = 4;
    
while ($pageNumber < $max_pages)
{   
    //echo $pageNumber;
    $API = "http://content.guardianapis.com/tags.xml?section=music&reference-type=musicbrainz";
    if ($pageNumber > 0) $API .= "&page=".$pageNumber;
    
    $html = scraperwiki::scrape( $API );
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    
     # Set the amount of page numbers available :
    $response = $dom->find('response',0);
    //print $response ;
    $max_pages = isset($response->pages) ? intval($response->pages) : 4;
    //print $max_pages;
    
    foreach( $dom->find('tag') as $data )
    {
        # Store data in the datastore
        $artist = $data->id;
        // strip off the first 6 chars
        $artist = substr($artist , 6);
        // remove hyphens!
        $artist = str_replace( '-','',$artist );
        //print $artist;
        scraperwiki::save(array('artistname'), array('artistname' => $artist));
    }
    
    $pageNumber++;
}
?>