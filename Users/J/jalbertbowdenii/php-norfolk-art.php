<?php
require 'scraperwiki/simple_html_dom.php'; 
$html = scraperWiki::scrape("http://norfolkpublicart.org/public-art/installed-projects/");           
          
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='postarea'] p") as $data){
    $links = $data->find("a");
    $linksImg = $data->find("img");

    // grab all links; get link title, href and text
    if(count($links)==1){

        $record = array(
            'linktitle' => $links[0]->title,
            'linktext' => $links[0]->plaintext, 
            'linkhref' => $links[0]->href);
        // print json_encode($record) . "\n";
scraperwiki::save(array('linktitle', 'linktext', 'linkhref'), $record);  
    }
    // grab all images; get src and title
    if(count($linksImg)==1){

        $record2 = array(
            'linksimgtitle' => $linksImg[0]->title,
            'linksimgsrc' => $linksImg[0]->src);
        // print json_encode($record2) . "\n";
        scraperwiki::save(array('linksimgtitle', 'linksimgsrc'), $record2);
    }
}

// print $html . "\n";
?>
<?php
require 'scraperwiki/simple_html_dom.php'; 
$html = scraperWiki::scrape("http://norfolkpublicart.org/public-art/installed-projects/");           
          
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='postarea'] p") as $data){
    $links = $data->find("a");
    $linksImg = $data->find("img");

    // grab all links; get link title, href and text
    if(count($links)==1){

        $record = array(
            'linktitle' => $links[0]->title,
            'linktext' => $links[0]->plaintext, 
            'linkhref' => $links[0]->href);
        // print json_encode($record) . "\n";
scraperwiki::save(array('linktitle', 'linktext', 'linkhref'), $record);  
    }
    // grab all images; get src and title
    if(count($linksImg)==1){

        $record2 = array(
            'linksimgtitle' => $linksImg[0]->title,
            'linksimgsrc' => $linksImg[0]->src);
        // print json_encode($record2) . "\n";
        scraperwiki::save(array('linksimgtitle', 'linksimgsrc'), $record2);
    }
}

// print $html . "\n";
?>
