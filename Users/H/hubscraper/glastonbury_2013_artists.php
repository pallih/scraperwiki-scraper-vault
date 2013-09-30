<?php

define('API_KEY', '5dd37b26667b8528149a4e95e795e22e');

$event = '3162700';
$artists = event_artists($event);

foreach ($artists as $artist) {
    $data = artist_info($artist);
    scraperwiki::save_sqlite(array('name'), $data);
}

function event_artists($event) {
    $params = array(
        'event' => $event,
        'api_key' => API_KEY,
        'format' => 'json',
        'method' => 'event.getinfo',
    );

    $data = json_decode(file_get_contents('http://ws.audioscrobbler.com/2.0/?' . http_build_query($params)), true);

    return $data['event']['artists']['artist'];
}

function artist_info($name) {
    $params = array(
        'artist' => $name,
        'autocorrect' => 0,
        'api_key' => API_KEY,
        'format' => 'json',
        'method' => 'artist.getinfo',
    );

    $data = json_decode(file_get_contents('http://ws.audioscrobbler.com/2.0/?' . http_build_query($params)), true);
    $artist = $data['artist'];

    return array(
        'name' => $artist['name'],
        'url' => $artist['url'],
        'listeners' => $artist['stats']['listeners'],
        'tags' => implode(', ', array_map(function($item) { return $item['name']; }, $artist['tags']['tag'])),
        'similar' => implode(', ', array_map(function($item) { return $item['name']; }, $artist['similar']['artist'])),
        //'bio' => $artist['bio']['content'],
        'formed' => $artist['bio']['yearformed'],
    );
}<?php

define('API_KEY', '5dd37b26667b8528149a4e95e795e22e');

$event = '3162700';
$artists = event_artists($event);

foreach ($artists as $artist) {
    $data = artist_info($artist);
    scraperwiki::save_sqlite(array('name'), $data);
}

function event_artists($event) {
    $params = array(
        'event' => $event,
        'api_key' => API_KEY,
        'format' => 'json',
        'method' => 'event.getinfo',
    );

    $data = json_decode(file_get_contents('http://ws.audioscrobbler.com/2.0/?' . http_build_query($params)), true);

    return $data['event']['artists']['artist'];
}

function artist_info($name) {
    $params = array(
        'artist' => $name,
        'autocorrect' => 0,
        'api_key' => API_KEY,
        'format' => 'json',
        'method' => 'artist.getinfo',
    );

    $data = json_decode(file_get_contents('http://ws.audioscrobbler.com/2.0/?' . http_build_query($params)), true);
    $artist = $data['artist'];

    return array(
        'name' => $artist['name'],
        'url' => $artist['url'],
        'listeners' => $artist['stats']['listeners'],
        'tags' => implode(', ', array_map(function($item) { return $item['name']; }, $artist['tags']['tag'])),
        'similar' => implode(', ', array_map(function($item) { return $item['name']; }, $artist['similar']['artist'])),
        //'bio' => $artist['bio']['content'],
        'formed' => $artist['bio']['yearformed'],
    );
}