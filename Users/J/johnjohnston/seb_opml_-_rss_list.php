<?php
######################################
# Manchester Hack Day, Music Finder
# Creates XSPF Playlist of music :)
# This is Part 1 of 3 : Fetch RSS DATA
######################################

require  'scraperwiki/simple_html_dom.php';

# Fecth the OPML list from the BBC website and search it for nodes
$html = scraperwiki::scrape("http://www.scotedublogs.org.uk/blogs/opml");

# Use the PHP Simple HTML DOM Parser :
$dom = new simple_html_dom();
$dom->load($html);

# Loop through nodes and get each artist's feed and stuff like images...
foreach($dom->find('outline') as $data)
{
    # show this outline's feed 
    $rssTitle        = $data->text;
    $rssUrl          = $data->xmlurl;
    $rssImage        = $data->imagehref;
    $rssDescription  = $data->description;
    $rssPageLink     = $data->htmlUrl;
    # get the name of the artist or some kind of ID
    //print $rssUrl . " - " . $rssDescription;

    # and now save in the database if the URL is valid :)
    $results = array('title'=>$rssTitle, 'feed' => $rssUrl, 'link'=>$rssPageLink );
    if ($rssUrl != "") scraperwiki::save(array('title','link'),$results);
}

?><?php
######################################
# Manchester Hack Day, Music Finder
# Creates XSPF Playlist of music :)
# This is Part 1 of 3 : Fetch RSS DATA
######################################

require  'scraperwiki/simple_html_dom.php';

# Fecth the OPML list from the BBC website and search it for nodes
$html = scraperwiki::scrape("http://www.scotedublogs.org.uk/blogs/opml");

# Use the PHP Simple HTML DOM Parser :
$dom = new simple_html_dom();
$dom->load($html);

# Loop through nodes and get each artist's feed and stuff like images...
foreach($dom->find('outline') as $data)
{
    # show this outline's feed 
    $rssTitle        = $data->text;
    $rssUrl          = $data->xmlurl;
    $rssImage        = $data->imagehref;
    $rssDescription  = $data->description;
    $rssPageLink     = $data->htmlUrl;
    # get the name of the artist or some kind of ID
    //print $rssUrl . " - " . $rssDescription;

    # and now save in the database if the URL is valid :)
    $results = array('title'=>$rssTitle, 'feed' => $rssUrl, 'link'=>$rssPageLink );
    if ($rssUrl != "") scraperwiki::save(array('title','link'),$results);
}

?>