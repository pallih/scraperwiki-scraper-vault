<?php
//Open and get HTML from Typo3 extension repository:
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://typo3.org/extensions/repository/");
$html = str_get_html($html_content);
$typo3url= "http://typo3.org/";
//Loop through the extensions:
foreach($html->find("div.tx-terfe-pi1 ul.extensions li") as $data){    
    $titleraw = $data->find("dl.ext-header dd.ext-name a",0);
    $titleprocessed = $titleraw->innertext;
    $extkeyimg = $data->find("dl.ext-header dd img",0);
    $extkey = $extkeyimg->alt;
    $title = $titleprocessed." - ".$extkey;
    $version = $data->find("dl.ext-info dd.left dl dd",2);
    $status = $data->find("dl.ext-header span",0);
    $category = $data->find("dl.ext-info dd.left dl dd",1);
    $author = $data->find("dl.ext-info dd.left dl.first dd",0);
    $description = $data->find("dl.ext-info dd.bottom dl.description dd",0);
    $changelog = $data->find("dl.ext-info dd.right dl.changelog dd.changelog",0);
    //Find and fix manual href
    $manualraw = $data->find("dl.ext-info dd.left dl dd a",0);
    $manualhref = $manualraw->href;
    $manualhreffixed = $typo3url.$manualhref;
    $manual = "<strong><a href=\"$manualhreffixed\">Read manual</a></strong>";
    $desc = "<strong>Category:</strong> ".$category->innertext."<br /><strong>Author:</strong> ".$author->innertext."<br /><strong>Version:</strong> ".$version->innertext."<br /><strong>Status:</strong> ".$status->innertext."<br /><br /><strong>Description:</strong><br /><br />".stripslashes($description->innertext)."<br /><br /><strong>Change Log:</strong><br /><br />".stripslashes($changelog->innertext)."<br /><br />".$manual;
    //Find and fix link href   
    $linkraw = $data->find("dl.ext-header dd.ext-name a",0);
    $linkhref = $linkraw->href;
    $linkfixed = $typo3url.$linkhref;
    $updated = $data->find("dl.ext-info dd.right dl dd.updated",0);
    $updatedinner = $updated->innertext;
    list($day, $month, $year) = explode('.', $updatedinner);
    $timestamp = mktime(0, 0, 0, $month, $day, $year);
    $pubDate = date("c",$timestamp);
//print $author->innertext;
//die();
    $record = array(
        'title' => $title,
        'description' => $desc,
        'link' => $linkfixed,
        'pubDate' => $pubDate,
        'version ' => $version->innertext
    );
//print_r($record);

    //Save the data to the DB:
    scraperwiki::save(array('title'), $record);
}
?>
