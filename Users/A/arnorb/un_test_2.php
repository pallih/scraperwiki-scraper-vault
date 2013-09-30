<?php

$html = scraperWiki::scrape("http://atlas.lmi.is/islandskort-dana/atlaskortateikningar.php");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$id = 0;
foreach($dom->find("ul.media-grid li a") as $imgurl){

    $yr = substr($imgurl->href,21,4);
    $filename = substr($imgurl->href,21);

    $record = array( 
        'id' => $id,
        'yr' => $yr,
        'filename' => $filename,
        'url' => "http://atlas.lmi.is/islandskort-dana/" . $imgurl->href
    ) ;

    scraperwiki::save_sqlite(array('url'),$record);

    $id++;

    //print "<img src=\"http://atlas.lmi.is/islandskort-dana/" . $imgurl->href . "><br>" . "\n";
}

?>
<?php

$html = scraperWiki::scrape("http://atlas.lmi.is/islandskort-dana/atlaskortateikningar.php");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$id = 0;
foreach($dom->find("ul.media-grid li a") as $imgurl){

    $yr = substr($imgurl->href,21,4);
    $filename = substr($imgurl->href,21);

    $record = array( 
        'id' => $id,
        'yr' => $yr,
        'filename' => $filename,
        'url' => "http://atlas.lmi.is/islandskort-dana/" . $imgurl->href
    ) ;

    scraperwiki::save_sqlite(array('url'),$record);

    $id++;

    //print "<img src=\"http://atlas.lmi.is/islandskort-dana/" . $imgurl->href . "><br>" . "\n";
}

?>
