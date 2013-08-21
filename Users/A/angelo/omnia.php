<?php
require 'scraperwiki/simple_html_dom.php';

// Get page filtered by 7.x compatibility.
$uri = 'http://omniatv.com/community/videos';

$dom = new simple_html_dom();

print $uri;
$content = scraperwiki::scrape($uri); 
$dom->load($content);
saveProjects($dom);


function saveProjects($dom) {
    // Each project is listed in its own row. Iterate through the rows in the View to pull out the data.
    foreach($dom->find('.cMedia-ThumbList .cMedia-Title a') as $data){

        // Save this project's information to the database.
        $record = extractInfo($data->href);
        scraperwiki::save(array('page_url'), $record);
        print json_encode($record) . "\n";
    }
}

function extractInfo($data) {

    $uri2 = 'http://omniatv.com' . $data;

    $dom2 = new simple_html_dom();

    print $uri2;
    $content = scraperwiki::scrape($uri2); 
    $dom2->load($content);
    

    $record = array(
        'page url' => $data, 
      //  'git_url' => $git_url,
    );

    return $record;
}
