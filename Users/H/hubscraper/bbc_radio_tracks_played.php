<?php

$stations = array(
    'radio1',
    'radio2',
    'radio3',
    '1xtra',
    '6music',
);

foreach ($stations as $station) {
    $data = json_decode(file_get_contents('http://www.bbc.co.uk/' . $station . '/nowplaying/latest.json'), true);
    foreach ((array) $data['nowplaying'] as $track) {
        scraperwiki::save_sqlite(array('artist', 'title'), array('artist' => html_entity_decode($track['artist']), 'title' => html_entity_decode($track['title'])), $station);
    }
}<?php

$stations = array(
    'radio1',
    'radio2',
    'radio3',
    '1xtra',
    '6music',
);

foreach ($stations as $station) {
    $data = json_decode(file_get_contents('http://www.bbc.co.uk/' . $station . '/nowplaying/latest.json'), true);
    foreach ((array) $data['nowplaying'] as $track) {
        scraperwiki::save_sqlite(array('artist', 'title'), array('artist' => html_entity_decode($track['artist']), 'title' => html_entity_decode($track['title'])), $station);
    }
}