<?php
require  'scraperwiki/simple_html_dom.php';

$prevMonths = 2; //Number of weeks in the past
$numMonths = 4; //Number of weeks to scrape

//$events = "http://lichfield-cathedral.org/month.calendar/2011/12/06/112.html";

$d = new datetime();
$d->modify("-$prevMonths months");


for ($i=0; $i<$numMonths; $i++) {
    
    $value = "http://lichfield-cathedral.org/month.calendar/"  .$d->format("Y/m/d"). "/112.html";
    $html = scraperwiki::scrape($value);

    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('td[@class=cal_td_dayshasevents]') as $data) {
        $aDay = $data->find("a[@class=cal_daylink]");
        $date = $d->format("Y/m/").$aDay[0]->innertext;
        foreach ($data->find("a[@class=cal_titlelink]") as $event) {
            $e = array();
             $e['link'] = $event->href;
             $e['date'] = $date;
             $t = $event->innertext;
            if (preg_match("/^\d{1,2}:\d{1,2}/", $t, $matches) != 0) {
                $e['time'] = $matches[0];
            }
            $e['pubDate'] = date(DATE_RFC822, strtotime($e['date']." ".$e['time']));
            preg_match("/993399&quot;&gt;([\s\w]+)&lt;/", $event->parent->title, $matches);
            $e['title'] = $matches[1];
            $e['description'] = $matches[1];
            scraperwiki::save_sqlite(array('title', 'link', 'description', 'pubDate'), $e);
        }
    }
    
    $d->modify("+1 month");
}
?><?php
require  'scraperwiki/simple_html_dom.php';

$prevMonths = 2; //Number of weeks in the past
$numMonths = 4; //Number of weeks to scrape

//$events = "http://lichfield-cathedral.org/month.calendar/2011/12/06/112.html";

$d = new datetime();
$d->modify("-$prevMonths months");


for ($i=0; $i<$numMonths; $i++) {
    
    $value = "http://lichfield-cathedral.org/month.calendar/"  .$d->format("Y/m/d"). "/112.html";
    $html = scraperwiki::scrape($value);

    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('td[@class=cal_td_dayshasevents]') as $data) {
        $aDay = $data->find("a[@class=cal_daylink]");
        $date = $d->format("Y/m/").$aDay[0]->innertext;
        foreach ($data->find("a[@class=cal_titlelink]") as $event) {
            $e = array();
             $e['link'] = $event->href;
             $e['date'] = $date;
             $t = $event->innertext;
            if (preg_match("/^\d{1,2}:\d{1,2}/", $t, $matches) != 0) {
                $e['time'] = $matches[0];
            }
            $e['pubDate'] = date(DATE_RFC822, strtotime($e['date']." ".$e['time']));
            preg_match("/993399&quot;&gt;([\s\w]+)&lt;/", $event->parent->title, $matches);
            $e['title'] = $matches[1];
            $e['description'] = $matches[1];
            scraperwiki::save_sqlite(array('title', 'link', 'description', 'pubDate'), $e);
        }
    }
    
    $d->modify("+1 month");
}
?>