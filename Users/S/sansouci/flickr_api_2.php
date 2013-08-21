<?php
#
# build the API URL to call
#
$api_key = 'fcb2815e8f2baa16d15bf11ce38c4aea';
$api_secret = '932665a59434b61f';

$params = array(
    'api_key'    => $api_key,
    'method'    => 'flickr.photos.search',
    'text'    => '"you only live once"',
    'format'    => 'php_serial',
    'per_page' => 500,
    'has_geo' => 1,
    'extras' => 'date_upload, date_taken, geo, tags, views, url_o',
);



#
# call the API and decode the response
#

function getContent($page, $params, $cnt, $tag_counts) {

$photo_cnt=$cnt;
if($page > 0) $params['page'] = $page;


$encoded_params = array();
foreach ($params as $k => $v){
  $encoded_params[] = urlencode($k).'='.urlencode($v);
}
$url = "http://api.flickr.com/services/rest/?".implode('&', $encoded_params);
$rsp = file_get_contents($url);
$rsp_obj = unserialize($rsp);
if ($rsp_obj['stat'] == 'ok'){    
    $rows_p = array();
    $rows_u = array();
    $photo_rows = array();
    foreach($rsp_obj['photos']['photo'] as $photo) {
        $photo_rows[] = $photo;
        $photo_cnt++;
        $tags = explode(' ', trim($photo['tags']));
        foreach($tags as $t) {
            if($t != '') {
                $row_u[] = array('tag' => $t,
                                 'user' => $photo['owner']);
                $row_p[] = array('tag' => $t,
                                  'photo' => $photo['id']);
                foreach($tags as $t2) {
                    if($t != $t2) {
                        $label = "$t<>$t2";
                        $entry = false;
                        if(isset($tag_counts[$label])) {
                            $entry = $tag_counts[$label];
                        } else if(isset($tag_counts["$t2<>$t"])) {
                            $label = "$t2<>$t";
                            $entry = $tag_counts[$label];
                        }
                        if(!$entry) {
                            $entry = array("tag1" => $t,
                                           "tag2" => $t2,
                                           "count" => 1);
                        } else {
                            $entry['count']++;
                        }                    
                        $tag_counts[$label] = $entry;
                    }
                }
            }
        }
    }
    scraperwiki::save_sqlite(array('id'), $photo_rows, $table_name="photos");
    scraperwiki::save_sqlite(array(),$row_u, $table_name="tag_user");
    scraperwiki::save_sqlite(array(), $row_p, $table_name="tag_photo");
    if($page < $rsp_obj['photos']['pages']
    ) getContent($page+1, $params, $photo_cnt, $tag_counts);
    else {
    scraperwiki::save_sqlite(array('tag1','tag2'), array_values($tag_counts), $table_name="tag_tag");
    print "photos: $photo_cnt\n";
    }
}else{
    echo "Call failed: $page!";
}

}


getContent(0, $params,0, array());


?>


