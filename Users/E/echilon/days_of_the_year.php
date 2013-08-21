<?php

require 'scraperwiki/simple_html_dom.php';
//scraperwiki::sqliteexecute("alter table events add Column Resources TEXT");
//die();
//$html = scraperWiki::scrape("http://www.daysoftheyear.com.nyud.net/days/2012/".date('m')."/");

//$todaysData = scraperwiki::sqliteexecute('SELECT * FROM events WHERE date = '.date('Ymd'));
//$todaysHtml = scraperWiki::scrape($todaysData['link']);
//$todaysHtml = scraperWiki::scrape('http://www.daysoftheyear.com.nyud.net/days/hug-your-cat-day/');
#var_dump(scraperWiki);

//scraperwiki::sqliteexecute("create table if not exists eventdays (DayID INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, name TEXT, link TEXT, Description TEXT, AlternateDates TEXT, Founded TEXT, Resources TEXT) ");
//scraperwiki::sqliteexecute("insert into `eventdays` (date, name, link, description, alternatedates, founded, resources) select * from `events`");
//scraperwiki::sqlitecommit();

//die();
//scraperwiki::sqliteexecute("delete from eventdays where date > '20130101'");
$useNyud = true;
if($useNyud){
    $html = scraperWiki::scrape("http://www.daysoftheyear.com.nyud.net/days/2013/".date('m')."/");
} else {
    $html = scraperWiki::scrape("http://webcache.googleusercontent.com/search?q=cache:www.daysoftheyear.com/days/2013/".date('m')."/");
}
$dom = new simple_html_dom();
$dom->load($html);
//print_r($html);
print_r("Starting parse\r\n");
$events = $dom->find('ul.listing li.listPost');
print('Found '.count($events)." events\r\n");
foreach($events as $data){
    $anchor = $data->find("h3 a");
    $eventDate= $data->find("div.dateRange");
    $eventName = $anchor[0]->plaintext;
    $timestamp= strtotime($eventDate[0]->plaintext);

    $record = array(
        'eventname' => $eventName,
        'link' => $anchor[0]->href,
        'date' =>date('Y-m-d',$timestamp)
    );
    $record = array(
        date('Ymd',$timestamp),
        $eventName,
        $anchor[0]->href
    );
    $dayid = scraperwiki::sqliteexecute("select dayid from eventdays where date = ? and name = ?",array(date('Ymd',$timestamp), $eventName))->data;
//print("ID: ".$dayid);
    if(count($dayid) > 0) {
        scraperwiki::sqliteexecute("update eventdays set link = ? where dayid = ?",array($anchor[0]->href, strval($dayid[0])));
        print "Event day ".strval($dayid[0])." exists - ". $eventName;
    } else {
        scraperwiki::sqliteexecute("insert into eventdays (date, name, link) values (?,?,?)",array(date('Ymd',$timestamp), $eventName, $anchor[0]->href));
        print "Found new event day: ".$eventName;
    }
    print($eventDate[0]->plaintext . ' - ' . date('Y-m-d',$timestamp) . ' - <a href="' . $anchor[0]->href . '">' . $eventName . "</a>\r\n");
}
scraperwiki::sqlitecommit(); 
//die();

// now go back to fill in the blanks
$emptyDays = scraperwiki::sqliteexecute('SELECT * FROM eventdays WHERE LENGTH(IFNULL(Description,\'\')) = 0');
print "Found ".count($emptyDays->data)." empty days\n\n";
$i=0;
foreach($emptyDays->data as $emptyDay){
    $dayid = $emptyDay[0];
    $date = $emptyDay[1];
    $name = $emptyDay[2];
    $url = $emptyDay[3];
    if($useNyud){
        $url = str_replace('http://www.daysoftheyear.com/','http://www.daysoftheyear.com.nyud.net/',$url);
    } else {
        $url = str_replace('http://www.daysoftheyear.com/','http://webcache.googleusercontent.com/search?q=cache:www.daysoftheyear.com/',$url);
    }
    $description = $emptyDay[4];
    $altDates = $emptyDay[5];
    $founded = $emptyDay[6];//[2];
    print($url."\n");
    if(strlen($url)==0)
        continue;
    $todaysHtml = scraperWiki::scrape($url);
    if(strlen($todaysHtml) == 0)
        continue;
    $dom = str_get_html($todaysHtml);
    $foundedNode = $dom->find("div.founded",0);
    $altDatesNode = $dom->find("div.alternateDates",0);
    $resourcesNode = $dom->find("div.otherResources",0);
    $descriptionNode = $dom->find('/html/body/div[3]/div[2]/div[3]/div[2]/p',0);
    //$eg->root->first_child()->children(0)->next_sibling()->tag . "\n";
    //print($description[0]->plaintext);
    $emptyDayRecord = array(
        $descriptionNode ? $descriptionNode->outertext : '',
        $altDatesNode ? $altDatesNode->outertext : '',
        $foundedNode ? $foundedNode->outertext : '',
        $resourcesNode ? $resourcesNode->outertext : '',
//        $date,
        strval($dayid),
        $name
    );
    var_dump($emptyDayRecord);
    scraperwiki::sqliteexecute('UPDATE eventdays SET Description = ?, AlternateDates = ?, Founded = ?, Resources = ? WHERE dayid = ? and name = ?', $emptyDayRecord);
    $i++;
    //if($i>5)
      //  break;
}
scraperwiki::sqlitecommit(); 

?>