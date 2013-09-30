<?php
require 'scraperwiki/simple_html_dom.php';

// Get page filtered by 7.x compatibility.
$contents = scraperwiki::scrape("http://drupal.org/project/modules/index?project-status=0&drupal_core=7234");           

$dom = new simple_html_dom();
$dom->load($contents);

// Each project is listed in its own row. Iterate through the rows in the View to pull out the data.
foreach($dom->find('.view-project-index .views-field-title a') as $data){

    // Pull out the project's machine name from the link's href.
    $project_name = str_replace('/project/', '', $data->href);
    $drupal_code_url = "http://drupalcode.org" . $data->href . ".git";
    $git_url = "http://git.drupal.org" . $data->href . ".git";

    // Save this project's information to the database.
    $record = array(
        'project_name' => $project_name, 
        'git_url' => $git_url,
    );

    scraperwiki::save(array('project_name'), $record);

}<?php
require 'scraperwiki/simple_html_dom.php';

// Get page filtered by 7.x compatibility.
$contents = scraperwiki::scrape("http://drupal.org/project/modules/index?project-status=0&drupal_core=7234");           

$dom = new simple_html_dom();
$dom->load($contents);

// Each project is listed in its own row. Iterate through the rows in the View to pull out the data.
foreach($dom->find('.view-project-index .views-field-title a') as $data){

    // Pull out the project's machine name from the link's href.
    $project_name = str_replace('/project/', '', $data->href);
    $drupal_code_url = "http://drupalcode.org" . $data->href . ".git";
    $git_url = "http://git.drupal.org" . $data->href . ".git";

    // Save this project's information to the database.
    $record = array(
        'project_name' => $project_name, 
        'git_url' => $git_url,
    );

    scraperwiki::save(array('project_name'), $record);

}