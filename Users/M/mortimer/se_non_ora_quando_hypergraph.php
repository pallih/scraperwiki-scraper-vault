<?php

# attach the base DB

scraperwiki::attach("se_non_ora_quando_flickr"); 

#
# build the API URL to call
#
$api_key = $_GET['API_KEY'];

$api_secret = $_GET['API_SECRET'];

$params = array(
    'api_key'    => $api_key,
    'format'    => 'php_serial',
    'method'    => 'flickr.photos.getInfo'
); 
           
$photos = scraperwiki::select("id, secret from se_non_ora_quando_flickr.photos"); 
$tags_rows = array();

foreach($photos as $photo) {
    #
    # call the API and decode the response
    #

    $params[ 'photo_id'] = $photo['id'];
    $params[ 'secret'] = $photo['secret'];

    $encoded_params = array();
    foreach ($params as $k => $v){
      $encoded_params[] = urlencode($k).'='.urlencode($v);
    }
    $url = "http://api.flickr.com/services/rest/?".implode('&', $encoded_params);
    $rsp = file_get_contents($url);
    $rsp_obj = unserialize($rsp);
    
    if ($rsp_obj['stat'] == 'ok'){
        foreach($rsp_obj['photo']['tags']['tag'] as $tag) {
            $tags_rows[] = array(
                'photo_id' => $photo['id'],
                'tag_id' => $tag['id'],
                'author' => $tag['author'],
                'raw' => $tag['raw'],
                'clean' => $tag['_content'],
            );
        }
    } else {
        print_r($rsp_obj);
    }
    sleep(rand(1,5));
}
scraperwiki::save_sqlite(array('tag_id', 'photo_id'), $tags_rows);

?>
