<?php

require 'scraperwiki/simple_html_dom.php';

echo 'data initializing...' . "\n";
$itemsToScrape = 400;

try{
    $dbResult = scraperwiki::select('id FROM swdata ORDER BY id DESC LIMIT 1');
    $offset = $dbResult[0]['id'];
}catch (Exception $ex){
    //first run if datatable doesn't exists
    $offset = 0;
}

if ($offset > 0){
    $pageOffset = round(($offset / 20), 0) + 1;
    $itemOffset = ($offset % 20) + 1;
    $recordId = $offset+1;
}else{
    $pageOffset = 0;
    $itemOffset = 0;
    $recordId = 1;
}

echo 'init-data:' . "\n";
echo 'pageOffset: ' . $pageOffset . "\n";
echo 'itemOffset: ' . $itemOffset . "\n";
echo 'recordId: ' . $recordId. "\n";

echo 'begin scraping...' . "\n";
$html = str_get_html(scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/"));

$pagination = $html->find("div.pagination a");
$lastPage = $pagination[count($pagination)-2]->plaintext;

$page = $lastPage - $pageOffset;

$html = str_get_html(scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/?page=" . $page));
while (($itemsToScrape > 0) and ($ul = $html->find("ul.scraper_list",0))){
    echo 'scraping page: ' . $page . "\n";
    $liArray = $ul->find("li.code_object_line");
    while ($itemOffset < count($liArray)){
        $record = generateRecordData($recordId, $liArray[$itemOffset]);
        scraperwiki::save(array('id'), $record);
        echo 'saved recordId: ' . $recordId . "\n";
        $recordId++;
        $itemOffset++;
        $itemsToScrape--;
    }
    $itemOffset = 0;
    $page--;
    $html = str_get_html(scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/?page=" . $page));
}
echo 'ending scraping at page: ' . $page . "\n";

/* helper functions -------------------------------------------------------------------------------------*/
function generateRecordData($id, $li){
    $record = array();
    $record['id'] = $id;
    $record['owner'] = $li->find("h3 a.owner", 0)->plaintext;
    $record['ownerProfile'] = $li->find("h3 a.owner", 0)->href;
    $record['title'] = $li->find("h3 a", 1)->plaintext;
    $record['description'] = empty($li->find("p.description", 0)->plaintext) ? "" : $li->find("p.description", 0)->plaintext;

    $t = explode(".", $li->find("p.context", 0)->plaintext);
    $record['linesOfCode'] = preg_replace("/[^0-9]/","",$t[0]);
    $record['rowsOfData'] = preg_replace("/[^0-9]/","",$t[1]);

    $createdInfo = explode(",", $li->find("p.context", 1)->plaintext);
    $timevalueArray = array('hou' => 0, 'min' => 0, 'sec' => 0, 'day' => 0, 'mon' => 0, 'yea' => 0);
    if (count($createdInfo) == 1){
        //hours || days || weeks || monts || years
        $t = explode(" ", trim($createdInfo[0]));
        $timevalueArray[substr($t[2], 0, 3)] = -$t[1];
    }elseif (count($createdInfo) == 2){
        //hours + minutes || days + hours || weeks + days || month + weeks || 
        $t = explode(" ", trim($createdInfo[0]));
        $timevalueArray[substr($t[2], 0, 3)] = -$t[1];
        $t = explode(" ", trim($createdInfo[1]));
        $timevalueArray[substr($t[1], 0, 3)] = -$t[0];
    }
    $record['createdTime'] = createTimeStamp($timevalueArray);

    $record['type'] = $li->find("table.code_about tr.codewiki_type td.link", 0)->plaintext;
    $record['language'] = $li->find("table.code_about tr.language td.link", 0)->plaintext;
    $record['status'] = $li->find("table.code_about tr.status td.link", 0)->plaintext;

    return $record;
}

function createTimeStamp($timevalueArray){
    return date('Y-m-d H:i:s', mktime(date("H")+$timevalueArray['hou'], 
                                        date("i")+$timevalueArray['min'], 
                                        date("s")+$timevalueArray['sec'],
                                        date("m")+$timevalueArray['mon'],
                                        date("d")+$timevalueArray['day'],
                                        date("y")+$timevalueArray['yea']));
}
?><?php

require 'scraperwiki/simple_html_dom.php';

echo 'data initializing...' . "\n";
$itemsToScrape = 400;

try{
    $dbResult = scraperwiki::select('id FROM swdata ORDER BY id DESC LIMIT 1');
    $offset = $dbResult[0]['id'];
}catch (Exception $ex){
    //first run if datatable doesn't exists
    $offset = 0;
}

if ($offset > 0){
    $pageOffset = round(($offset / 20), 0) + 1;
    $itemOffset = ($offset % 20) + 1;
    $recordId = $offset+1;
}else{
    $pageOffset = 0;
    $itemOffset = 0;
    $recordId = 1;
}

echo 'init-data:' . "\n";
echo 'pageOffset: ' . $pageOffset . "\n";
echo 'itemOffset: ' . $itemOffset . "\n";
echo 'recordId: ' . $recordId. "\n";

echo 'begin scraping...' . "\n";
$html = str_get_html(scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/"));

$pagination = $html->find("div.pagination a");
$lastPage = $pagination[count($pagination)-2]->plaintext;

$page = $lastPage - $pageOffset;

$html = str_get_html(scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/?page=" . $page));
while (($itemsToScrape > 0) and ($ul = $html->find("ul.scraper_list",0))){
    echo 'scraping page: ' . $page . "\n";
    $liArray = $ul->find("li.code_object_line");
    while ($itemOffset < count($liArray)){
        $record = generateRecordData($recordId, $liArray[$itemOffset]);
        scraperwiki::save(array('id'), $record);
        echo 'saved recordId: ' . $recordId . "\n";
        $recordId++;
        $itemOffset++;
        $itemsToScrape--;
    }
    $itemOffset = 0;
    $page--;
    $html = str_get_html(scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/?page=" . $page));
}
echo 'ending scraping at page: ' . $page . "\n";

/* helper functions -------------------------------------------------------------------------------------*/
function generateRecordData($id, $li){
    $record = array();
    $record['id'] = $id;
    $record['owner'] = $li->find("h3 a.owner", 0)->plaintext;
    $record['ownerProfile'] = $li->find("h3 a.owner", 0)->href;
    $record['title'] = $li->find("h3 a", 1)->plaintext;
    $record['description'] = empty($li->find("p.description", 0)->plaintext) ? "" : $li->find("p.description", 0)->plaintext;

    $t = explode(".", $li->find("p.context", 0)->plaintext);
    $record['linesOfCode'] = preg_replace("/[^0-9]/","",$t[0]);
    $record['rowsOfData'] = preg_replace("/[^0-9]/","",$t[1]);

    $createdInfo = explode(",", $li->find("p.context", 1)->plaintext);
    $timevalueArray = array('hou' => 0, 'min' => 0, 'sec' => 0, 'day' => 0, 'mon' => 0, 'yea' => 0);
    if (count($createdInfo) == 1){
        //hours || days || weeks || monts || years
        $t = explode(" ", trim($createdInfo[0]));
        $timevalueArray[substr($t[2], 0, 3)] = -$t[1];
    }elseif (count($createdInfo) == 2){
        //hours + minutes || days + hours || weeks + days || month + weeks || 
        $t = explode(" ", trim($createdInfo[0]));
        $timevalueArray[substr($t[2], 0, 3)] = -$t[1];
        $t = explode(" ", trim($createdInfo[1]));
        $timevalueArray[substr($t[1], 0, 3)] = -$t[0];
    }
    $record['createdTime'] = createTimeStamp($timevalueArray);

    $record['type'] = $li->find("table.code_about tr.codewiki_type td.link", 0)->plaintext;
    $record['language'] = $li->find("table.code_about tr.language td.link", 0)->plaintext;
    $record['status'] = $li->find("table.code_about tr.status td.link", 0)->plaintext;

    return $record;
}

function createTimeStamp($timevalueArray){
    return date('Y-m-d H:i:s', mktime(date("H")+$timevalueArray['hou'], 
                                        date("i")+$timevalueArray['min'], 
                                        date("s")+$timevalueArray['sec'],
                                        date("m")+$timevalueArray['mon'],
                                        date("d")+$timevalueArray['day'],
                                        date("y")+$timevalueArray['yea']));
}
?>