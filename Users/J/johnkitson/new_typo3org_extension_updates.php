<?php
//Function to trim the first 42 chars off the start of the author scrape
function deleteChars( $string ) {
    return substr( $string, 42 );
}
//Open and get HTML from Typo3 extension repository:
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://typo3.org/extensions/repository/");
$html = str_get_html($html_content);
$typo3url= "http://typo3.org";
//Loop through the extensions:
foreach($html->find("div.tx_terfe2_content div.ter-ext-list-row") as $data){    
    $titleraw = $data->find("div.ter-ext-list-row-head a",0);
    $titleprocessed = $titleraw->innertext;
    $extkeyraw = $data->find("div.ter-ext-list-row-head span.ter-ext-list-row-key",0);
    $extkey = $extkeyraw->innertext;
    $title = $titleprocessed." - ".$extkey;
    $versionraw = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-info table tbody tr td",0);
    $version = substr(strip_tags($versionraw),0,5);
    $status = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-info table tbody tr td span.ter-ext-state",0);
    $authorraw = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-description div.ter-ext-list-meta",0);
    $authorrawtrimmed = deleteChars($authorraw);
    $author = strip_tags($authorrawtrimmed);
    $linkraw = $data->find("div.ter-ext-list-row-head a",0);
    $linkhref = $linkraw->href;
    $linkfixed = $typo3url.$linkhref;
    //Get extra information from within extension details page:
    $extension_content = scraperwiki::scrape($linkfixed);
    $exthtml = str_get_html($extension_content);
        foreach($exthtml->find("div.ter-ext-single-content") as $data2){  
            $changelog = $data2->find("div.ter-ext-single-description div.ter-ext-single-lastUploadComment",0);
            //Un-comment these lines when they have implemented the Manual links from the details page:            
            $manualraw = $data2->find("div.ter-ext-single-info table tbody tr.ter-ext-single-info-manual td a",0);
            $manual = $manualraw->href;
            $manualhref = $typo3url.$manual;
            $manuallink = "<strong><a href=\"$manualhref\">Read manual</a></strong>";
            //Delete this line when they have implemented the Manual links:
            //$manuallink = "<strong><a href=\"http://typo3.org/\">Read manual</a></strong>";
        }
    $descriptionraw = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-description",0);
    $description = strip_tags($descriptionraw);
    $desc = "<strong>Author:</strong> ".$author."<br /><strong>Version:</strong> ".$version."<br /><strong>Status:</strong> ".$status->innertext."<br /><br /><strong>Description:</strong><br /><br />".stripslashes($description)."<br /><br />".$changelog->innertext."<br /><br />".$manuallink;
    $updated = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-info table tbody tr td",1);
    $updatedinner = $updated->innertext;
    $date = str_replace(",", "", $updatedinner);
    $timestamp = strtotime($date);
    $pubDate = date("c",$timestamp);
//print $titleprocessed ;
//die();
    $record = array(
        'title' => $title,
        'description' => $desc,
        'link' => $linkfixed,
        'pubDate' => $pubDate
    );
    //Save the data to the DB:
    scraperwiki::save(array('title'), $record);
}
?>
<?php
//Function to trim the first 42 chars off the start of the author scrape
function deleteChars( $string ) {
    return substr( $string, 42 );
}
//Open and get HTML from Typo3 extension repository:
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://typo3.org/extensions/repository/");
$html = str_get_html($html_content);
$typo3url= "http://typo3.org";
//Loop through the extensions:
foreach($html->find("div.tx_terfe2_content div.ter-ext-list-row") as $data){    
    $titleraw = $data->find("div.ter-ext-list-row-head a",0);
    $titleprocessed = $titleraw->innertext;
    $extkeyraw = $data->find("div.ter-ext-list-row-head span.ter-ext-list-row-key",0);
    $extkey = $extkeyraw->innertext;
    $title = $titleprocessed." - ".$extkey;
    $versionraw = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-info table tbody tr td",0);
    $version = substr(strip_tags($versionraw),0,5);
    $status = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-info table tbody tr td span.ter-ext-state",0);
    $authorraw = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-description div.ter-ext-list-meta",0);
    $authorrawtrimmed = deleteChars($authorraw);
    $author = strip_tags($authorrawtrimmed);
    $linkraw = $data->find("div.ter-ext-list-row-head a",0);
    $linkhref = $linkraw->href;
    $linkfixed = $typo3url.$linkhref;
    //Get extra information from within extension details page:
    $extension_content = scraperwiki::scrape($linkfixed);
    $exthtml = str_get_html($extension_content);
        foreach($exthtml->find("div.ter-ext-single-content") as $data2){  
            $changelog = $data2->find("div.ter-ext-single-description div.ter-ext-single-lastUploadComment",0);
            //Un-comment these lines when they have implemented the Manual links from the details page:            
            $manualraw = $data2->find("div.ter-ext-single-info table tbody tr.ter-ext-single-info-manual td a",0);
            $manual = $manualraw->href;
            $manualhref = $typo3url.$manual;
            $manuallink = "<strong><a href=\"$manualhref\">Read manual</a></strong>";
            //Delete this line when they have implemented the Manual links:
            //$manuallink = "<strong><a href=\"http://typo3.org/\">Read manual</a></strong>";
        }
    $descriptionraw = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-description",0);
    $description = strip_tags($descriptionraw);
    $desc = "<strong>Author:</strong> ".$author."<br /><strong>Version:</strong> ".$version."<br /><strong>Status:</strong> ".$status->innertext."<br /><br /><strong>Description:</strong><br /><br />".stripslashes($description)."<br /><br />".$changelog->innertext."<br /><br />".$manuallink;
    $updated = $data->find("div.ter-ext-list-row-regular div.ter-ext-list-row-info table tbody tr td",1);
    $updatedinner = $updated->innertext;
    $date = str_replace(",", "", $updatedinner);
    $timestamp = strtotime($date);
    $pubDate = date("c",$timestamp);
//print $titleprocessed ;
//die();
    $record = array(
        'title' => $title,
        'description' => $desc,
        'link' => $linkfixed,
        'pubDate' => $pubDate
    );
    //Save the data to the DB:
    scraperwiki::save(array('title'), $record);
}
?>
