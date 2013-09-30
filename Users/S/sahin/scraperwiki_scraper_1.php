<?php

require 'scraperwiki/simple_html_dom.php';


$foundUl = true;
$pageNr = 1;
$recordId = 1;

echo 'begin scraping...' . "\n";

while ($foundUl){
    echo 'page: ' . $pageNr . "\n";
    echo date('H:i:s');
    $html_content = scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/?page=" . $pageNr);
    $html = str_get_html($html_content);
    
    $ul = $html->find("ul.scraper_list",0);

    if ($ul !== null){
        
        foreach($ul->find("li.code_object_line") as $li){
            $record = array('id' => $recordId);
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

            echo 'saving record nr: ' . $recordId . "\n";
            scraperwiki::save(array('id'), $record);
            $recordId++;
        }
    }else{
        $foundUl = false;
    }
    
    echo date('H:i:s');
    $pageNr++;
    $html->__destruct();
}

echo 'end scraping after ' . $pageNr-- . ' pages' . "\n";

function createTimeStamp($timevalueArray){
    return date('Y-m-d H:i:s', mktime(date("H")+$timevalueArray['hou'], 
                                        date("i")+$timevalueArray['min'], 
                                        date("s")+$timevalueArray['sec'],
                                        date("m")+$timevalueArray['mon'],
                                        date("d")+$timevalueArray['day'],
                                        date("y")+$timevalueArray['yea']));
}
?>


<?php

require 'scraperwiki/simple_html_dom.php';


$foundUl = true;
$pageNr = 1;
$recordId = 1;

echo 'begin scraping...' . "\n";

while ($foundUl){
    echo 'page: ' . $pageNr . "\n";
    echo date('H:i:s');
    $html_content = scraperwiki::scrape("https://scraperwiki.com/browse/scrapers/?page=" . $pageNr);
    $html = str_get_html($html_content);
    
    $ul = $html->find("ul.scraper_list",0);

    if ($ul !== null){
        
        foreach($ul->find("li.code_object_line") as $li){
            $record = array('id' => $recordId);
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

            echo 'saving record nr: ' . $recordId . "\n";
            scraperwiki::save(array('id'), $record);
            $recordId++;
        }
    }else{
        $foundUl = false;
    }
    
    echo date('H:i:s');
    $pageNr++;
    $html->__destruct();
}

echo 'end scraping after ' . $pageNr-- . ' pages' . "\n";

function createTimeStamp($timevalueArray){
    return date('Y-m-d H:i:s', mktime(date("H")+$timevalueArray['hou'], 
                                        date("i")+$timevalueArray['min'], 
                                        date("s")+$timevalueArray['sec'],
                                        date("m")+$timevalueArray['mon'],
                                        date("d")+$timevalueArray['day'],
                                        date("y")+$timevalueArray['yea']));
}
?>


