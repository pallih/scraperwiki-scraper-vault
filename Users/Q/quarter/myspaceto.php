<?php
#######################################################
#
# Quarter Note 
# Scrape MySpace and return :
# Band Name (unicode) | Band Image | Band Genre 
# 
#######################################################

require  'scraperwiki/simple_html_dom.php';

$allArtists = "http://api.scraperwiki.com/api/1.0/datastore/getdata?format=xml&name=guardianopenplatformartistretriever";   
$allArtistsXML = scraperwiki::scrape( $allArtists );
# Use the PHP Simple HTML DOM Parser to extract <td> tags
$myspaceDOM      = new simple_html_dom();
$myspaceDOM->load( $allArtistsXML );

// Firstly, scrape myspace for Artist Name & genres :
foreach($myspaceDOM->find('artistname') as $artist)
{ 
    # Read in the data used to select an artist!    
    $artistName      = $artist->plaintext;  
    echo $artist;
        
    # These are the elements we are interested in receiving!
    $artistUnicodeName = "";
    $artistLocation  = "";
    $artistImage     = "";
    $artistGenre     = "";
      
    # Find the myspace url and parse it in...
    $myspaceURL      = "http://www.myspace.com/" . $artistName;
    $html            = scraperwiki::scrape( $myspaceURL );
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $myspaceDOM      = new simple_html_dom();
    $myspaceDOM->load($html);
    
    // Firstly, scrape myspace for Artist Name & genres :
    foreach($myspaceDOM->find('span.nametext') as $data)
    { 
        $artistUnicodeName  = $data->plaintext;
        // genre may not neccessarily exist
        $artistGenre = isset($data->parent()->find("font[size=1] strong",0)->plaintext) ? ($data->parent()->find("font[size=1] strong",0)->plaintext) : 'unknown';
    }
    
    // Secondly, scrape myspace for Arist Image :
    $artistImage = isset($myspaceDOM->find('a[id=ctl00_cpMain_ctl01_UserBasicInformation1_hlDefaultImage] img',0)->src) ? $myspaceDOM->find('a[id=ctl00_cpMain_ctl01_UserBasicInformation1_hlDefaultImage] img',0)->src : "";
        
    # Store data in the datastore
    scraperwiki::save(
        // Set Unique Key Identifiers
        array( 
            'myspaceID'
        ), 
        // Set the data
        array( 
            'name' => $artistUnicodeName,
            'genre' => $artistGenre,
            'image' => $artistImage,
            'myspaceID' => $artistName
        )
    );

}
?><?php
#######################################################
#
# Quarter Note 
# Scrape MySpace and return :
# Band Name (unicode) | Band Image | Band Genre 
# 
#######################################################

require  'scraperwiki/simple_html_dom.php';

$allArtists = "http://api.scraperwiki.com/api/1.0/datastore/getdata?format=xml&name=guardianopenplatformartistretriever";   
$allArtistsXML = scraperwiki::scrape( $allArtists );
# Use the PHP Simple HTML DOM Parser to extract <td> tags
$myspaceDOM      = new simple_html_dom();
$myspaceDOM->load( $allArtistsXML );

// Firstly, scrape myspace for Artist Name & genres :
foreach($myspaceDOM->find('artistname') as $artist)
{ 
    # Read in the data used to select an artist!    
    $artistName      = $artist->plaintext;  
    echo $artist;
        
    # These are the elements we are interested in receiving!
    $artistUnicodeName = "";
    $artistLocation  = "";
    $artistImage     = "";
    $artistGenre     = "";
      
    # Find the myspace url and parse it in...
    $myspaceURL      = "http://www.myspace.com/" . $artistName;
    $html            = scraperwiki::scrape( $myspaceURL );
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $myspaceDOM      = new simple_html_dom();
    $myspaceDOM->load($html);
    
    // Firstly, scrape myspace for Artist Name & genres :
    foreach($myspaceDOM->find('span.nametext') as $data)
    { 
        $artistUnicodeName  = $data->plaintext;
        // genre may not neccessarily exist
        $artistGenre = isset($data->parent()->find("font[size=1] strong",0)->plaintext) ? ($data->parent()->find("font[size=1] strong",0)->plaintext) : 'unknown';
    }
    
    // Secondly, scrape myspace for Arist Image :
    $artistImage = isset($myspaceDOM->find('a[id=ctl00_cpMain_ctl01_UserBasicInformation1_hlDefaultImage] img',0)->src) ? $myspaceDOM->find('a[id=ctl00_cpMain_ctl01_UserBasicInformation1_hlDefaultImage] img',0)->src : "";
        
    # Store data in the datastore
    scraperwiki::save(
        // Set Unique Key Identifiers
        array( 
            'myspaceID'
        ), 
        // Set the data
        array( 
            'name' => $artistUnicodeName,
            'genre' => $artistGenre,
            'image' => $artistImage,
            'myspaceID' => $artistName
        )
    );

}
?>