<?php
date_default_timezone_set('Europe/London');
//ScraperWiki.httpresponseheader('Content-Type', 'text/csv');
header("Content-type: text/csv");
scraperwiki::attach("ucb_playlists");
$channels = array('uk','inspirational','gospel');

// $_GET['month'] is the YYYY-mm date to look for chart data
if(!isset($_GET['month'])) $_GET['month'] = date('Y-m',strtotime('Last Month'));
$start = $_GET['month'].'-01';
$end = $_GET['month'].'-31';
if(!isset($_GET['channel']) OR !in_array($_GET['channel'],$channels)) $_GET['channel'] = 'uk';

$data = scraperwiki::select("*,count(*) as plays from swdata where channel='".$_GET['channel']."' and date >= '".$start."' and date <= '".$end."' GROUP BY artist,title having plays > 1 order by plays desc limit 100");
echo '<h1>Airplay Chart Data For Channel '.$_GET['channel'].' From Month '.$_GET['month'].'</h1>';
echo '<form action="https://views.scraperwiki.com/run/ucb_airplay_charts" method="get">';
echo 'Select a channel <select name="channel">';
foreach($channels as $channel) echo '<option value="'.$channel.'">'.$channel.'</option>';
echo '</select><input type="submit" value="View" /></form>';
echo '<ol>';
foreach($data as $d){
    echo '<li>'.$d['artist'].' - '.$d['title'].' ('.$d['plays'].')</li>';
}
echo '</ol>';
?><?php
date_default_timezone_set('Europe/London');
//ScraperWiki.httpresponseheader('Content-Type', 'text/csv');
header("Content-type: text/csv");
scraperwiki::attach("ucb_playlists");
$channels = array('uk','inspirational','gospel');

// $_GET['month'] is the YYYY-mm date to look for chart data
if(!isset($_GET['month'])) $_GET['month'] = date('Y-m',strtotime('Last Month'));
$start = $_GET['month'].'-01';
$end = $_GET['month'].'-31';
if(!isset($_GET['channel']) OR !in_array($_GET['channel'],$channels)) $_GET['channel'] = 'uk';

$data = scraperwiki::select("*,count(*) as plays from swdata where channel='".$_GET['channel']."' and date >= '".$start."' and date <= '".$end."' GROUP BY artist,title having plays > 1 order by plays desc limit 100");
echo '<h1>Airplay Chart Data For Channel '.$_GET['channel'].' From Month '.$_GET['month'].'</h1>';
echo '<form action="https://views.scraperwiki.com/run/ucb_airplay_charts" method="get">';
echo 'Select a channel <select name="channel">';
foreach($channels as $channel) echo '<option value="'.$channel.'">'.$channel.'</option>';
echo '</select><input type="submit" value="View" /></form>';
echo '<ol>';
foreach($data as $d){
    echo '<li>'.$d['artist'].' - '.$d['title'].' ('.$d['plays'].')</li>';
}
echo '</ol>';
?>