<?php

    //$api = 'http://ex.fm/api/v3/trending?start=0&results=100';
  $api = 'http://ex.fm/api/v3/trending/tag/hip-hop?start=0&results=100';
  $profile =  file_get_contents($api);

  $results = json_decode($profile,true);
  
  $song = $results['songs'];


 foreach($song as $song) {

    $url = $song['url'];
    $timestamp = date("D, d/m/Y H:i:s T");
    
    echo $url;


    $record = array(
        'title' => $song['title'], 
        'artist' => $song['artist'],
        'link' => $url,
        'image' => $song['image']['large'],
        'guid' => $song['loved_count'],
        'tags' => $song['tags'][0],
        'album' => $song['album'],
        'date' => $timestamp
    ); 
   
   scraperwiki::save(array('title'), $record); 

}
    //print json_encode($url) . "\n";
?><?php

    //$api = 'http://ex.fm/api/v3/trending?start=0&results=100';
  $api = 'http://ex.fm/api/v3/trending/tag/hip-hop?start=0&results=100';
  $profile =  file_get_contents($api);

  $results = json_decode($profile,true);
  
  $song = $results['songs'];


 foreach($song as $song) {

    $url = $song['url'];
    $timestamp = date("D, d/m/Y H:i:s T");
    
    echo $url;


    $record = array(
        'title' => $song['title'], 
        'artist' => $song['artist'],
        'link' => $url,
        'image' => $song['image']['large'],
        'guid' => $song['loved_count'],
        'tags' => $song['tags'][0],
        'album' => $song['album'],
        'date' => $timestamp
    ); 
   
   scraperwiki::save(array('title'), $record); 

}
    //print json_encode($url) . "\n";
?>