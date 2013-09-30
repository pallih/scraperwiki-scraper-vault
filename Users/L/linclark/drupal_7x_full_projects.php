<?php
require 'scraperwiki/simple_html_dom.php';

// Get page filtered by 7.x compatibility.
$uris = array(
    'modules' => "http://drupal.org/project/modules/index?project-status=0&drupal_core=103",
    'themes' => "http://drupal.org/project/themes/index?project-status=0&drupal_core=103",
    'profiles' => "http://drupal.org/project/installation%2Bprofiles/index?project-status=0&drupal_core=103",
);

$dom = new simple_html_dom();

foreach ($uris as $uri) {
print $uri;
    $content = scraperwiki::scrape($uri); 
    $dom->load($content);
    saveProjects($dom);
}

function saveProjects($dom) {
    // Each project is listed in its own row. Iterate through the rows in the View to pull out the data.
    foreach($dom->find('.view-project-index .views-field-title a') as $data){

        // Save this project's information to the database.
        $record = extractInfo($data);
        scraperwiki::save(array('project_name'), $record);
    }
}

function extractInfo($data) {
    // Pull out the project's machine name from the link's href.
    $project_name = str_replace('/project/', '', $data->href);
    $drupal_code_url = "http://drupalcode.org" . $data->href . ".git";
    $git_url = "http://git.drupal.org" . $data->href . ".git";

    $record = array(
        'project_name' => $project_name, 
        'git_url' => $git_url,
    );

    return $record;
}
<?php
require 'scraperwiki/simple_html_dom.php';

// Get page filtered by 7.x compatibility.
$uris = array(
    'modules' => "http://drupal.org/project/modules/index?project-status=0&drupal_core=103",
    'themes' => "http://drupal.org/project/themes/index?project-status=0&drupal_core=103",
    'profiles' => "http://drupal.org/project/installation%2Bprofiles/index?project-status=0&drupal_core=103",
);

$dom = new simple_html_dom();

foreach ($uris as $uri) {
print $uri;
    $content = scraperwiki::scrape($uri); 
    $dom->load($content);
    saveProjects($dom);
}

function saveProjects($dom) {
    // Each project is listed in its own row. Iterate through the rows in the View to pull out the data.
    foreach($dom->find('.view-project-index .views-field-title a') as $data){

        // Save this project's information to the database.
        $record = extractInfo($data);
        scraperwiki::save(array('project_name'), $record);
    }
}

function extractInfo($data) {
    // Pull out the project's machine name from the link's href.
    $project_name = str_replace('/project/', '', $data->href);
    $drupal_code_url = "http://drupalcode.org" . $data->href . ".git";
    $git_url = "http://git.drupal.org" . $data->href . ".git";

    $record = array(
        'project_name' => $project_name, 
        'git_url' => $git_url,
    );

    return $record;
}
