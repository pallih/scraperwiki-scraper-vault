<?php
require  'scraperwiki/simple_html_dom.php';

$prevMonths = 0; //Number of weeks in the past
$numMonths = 1; //Number of weeks to scrape

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
             $e['link'] = "http://lichfield-cathedral.org".$event->href;
             $dt['date'] = $date;
             $t = $event->innertext;
            if (preg_match("/^\d{1,2}:\d{1,2}/", $t, $matches) != 0) {
                $dt['time'] = $matches[0];
            } else {
                $dt['time'] = '0:00'; // no time set so all day event
            }
            $e['pubDate'] = date('Y-m-d H:i:s', strtotime($dt['date']." ".$dt['time']));
            preg_match("/993399&quot;&gt;(((?!&lt;).)+)/", $event->parent->title, $matches);
            $e['title'] = trim(ucwords($matches[1]));
            $e['description'] = $matches[1];
            scraperwiki::save_sqlite(array('title', 'link', 'description', 'pubDate'), $e);
        }
    }
    
    $d->modify("+1 month");
}
?>