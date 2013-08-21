<?php
date_default_timezone_set('Europe/London');

function clean_it($string) {
    $string = html_entity_decode(trim($string));
    return $string;
}
$channels = array('uk','gospel','inspirational');

foreach($channels as $channel) {
    $html = scraperwiki::scrape('http://www.ucbmedia.co.uk/play/playlists_ajax.php?day=1&channel='.$channel);
    $songs = explode('<br><br>',$html);
    foreach($songs as $id => $song) {
        $line = explode('<br>',$song);
        foreach($line as $i => $part) {
            $part = explode('</b>',$part);
            if($i == 0) $output[$id]['time'] = clean_it($part[1]);
            if($i == 1) $output[$id]['title'] = clean_it($part[1]);
            if($i == 2) $output[$id]['artist'] = clean_it($part[1]);
        }
    }
    $date = date('Y-m-d',strtotime('Yesterday'));
    foreach($output as $item) {
        if(!empty($item['title']) && !empty($item['time'])) {
            $data = array('date'=>$date,'time'=>$item['time'],'channel'=>$channel,'artist'=>$item['artist'],'title'=>$item['title']);
            scraperwiki::save_sqlite(array('date','time'),$data);
        }
    }
}
?>
