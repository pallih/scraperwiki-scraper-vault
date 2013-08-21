<?php
require 'scraperwiki/simple_html_dom.php';

// Get page filtered by 7.x compatibility.
$uris = array(
    'modules' => "http://drupal.org/project/modules/index?project-status=0&drupal_core=103",
    //'themes' => "http://drupal.org/project/themes/index?project-status=0&drupal_core=103",
    //'profiles' => "http://drupal.org/project/installation%2Bprofiles/index?project-status=0&drupal_core=103",
);

$dom = new simple_html_dom();

foreach ($uris as $uri) {
    $content = scraperwiki::scrape($uri); 
    $dom->load($content);
print $uri;
    // Each project is listed in its own row. Iterate through the rows in the View to pull out the data.
    foreach($dom->find('.view-project-index .views-field-title a') as $data){
        $name = strtolower($data->text());
        if ($name[0] == 'a') {
            $project = createProject($data);
            addBranches($project);
            sleep(5);
        }
    }
}

function createProject($data) {
    // Pull out the project's machine name from the link's href.
    $project_name = str_replace('/project/', '', $data->href);
    $project_title = $data->text();
print ($project_title);
    $path = $data->href;
    $git_url = "http://git.drupal.org" . $data->href . ".git";

    $record = array(
        'project_name' => $project_name, 
        'project_title' => $project_title,
        'git_url' => $git_url,
        'path' => $path,
    );

    return $record;
}

function addBranches($project) {
    $dom = new simple_html_dom();
    $content = scraperwiki::scrape('http://drupalcode.org' . $project['path'] . '.git'); 
    $dom->load($content);
    $branches = array();

    foreach($dom->find('.tags tr a.name') as $data){
        $branch_tag = $data->text();
        $version_num = explode('-', $branch_tag);
        $core_version = explode('.', $version_num[0]);
        $proj_version = explode('.', $version_num[1]);
        if (in_array($core_version[0], array('5', '6', '7', '8'))) {
            $branches[$core_version[0]][$proj_version[0]] = $project['project_title'] . ' ' . $core_version[0] . '.x-' . $proj_version[0] . '.x';
        }
    }

    $project['uri'] = 'http://drupal.org' . $project['path'];
    $project['title'] = $project['project_title'];
    $project['parent'] = 'http://drupal.org/project/themes';
    scraperwiki::save(array('uri'), $project);
    foreach ($branches as $cv => $core_version) {
        $version = $project;
        $version['uri'] = 'http://drupal.org' . $project['path'] . '/' . $cv;
        $version['title'] = $project['project_title'] . ' ' . $cv . '.x';
        $version['parent'] = 'http://drupal.org' . $project['path'];
        scraperwiki::save(array('uri'), $version);
        foreach ($core_version as $pv => $proj_version) {
            $branch = $project;
            $branch['uri'] = 'http://drupal.org' . $project['path'] . '/' . $cv . '/' . $pv;
            $branch['title'] = $proj_version;
            $branch['parent'] = 'http://drupal.org' . $project['path'] . '/' . $cv;
            $branch['branch'] = $branch_tag;
            scraperwiki::save(array('uri'), $branch);
        }
    }
}