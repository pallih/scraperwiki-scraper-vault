<?php
# Blank PHP

require  'scraperwiki/simple_html_dom.php';

$pageNumber = 0;
$max_pages = 10;
    
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
    /* <tag type="keyword" web-title="Sandy Denny" id="music/sandy-denny" api-url="http://content.guardianapis.com/music/sandy-denny" web-url="http://www.guardian.co.uk/music/sandy-denny" section-id="music" section-name="Music"/> */
    foreach( $dom->find('tag') as $data )
    {
        # Store data in the datastore
        $attributes = $data->attr;//=> ;
        $artist = $attributes['web-title'];
        $guardianID = $data->id;
 
        scraperwiki::save(array('artist'), array('artist' => $artist, 'guardianID'=>$guardianID));
    }
    
    $pageNumber++;
}


?>
<?php
# Blank PHP

require  'scraperwiki/simple_html_dom.php';

$pageNumber = 0;
$max_pages = 10;
    
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
    /* <tag type="keyword" web-title="Sandy Denny" id="music/sandy-denny" api-url="http://content.guardianapis.com/music/sandy-denny" web-url="http://www.guardian.co.uk/music/sandy-denny" section-id="music" section-name="Music"/> */
    foreach( $dom->find('tag') as $data )
    {
        # Store data in the datastore
        $attributes = $data->attr;//=> ;
        $artist = $attributes['web-title'];
        $guardianID = $data->id;
 
        scraperwiki::save(array('artist'), array('artist' => $artist, 'guardianID'=>$guardianID));
    }
    
    $pageNumber++;
}


?>
