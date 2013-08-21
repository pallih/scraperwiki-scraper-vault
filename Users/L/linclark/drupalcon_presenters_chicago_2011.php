<?php

require 'scraperwiki/simple_html_dom.php';

$result = array();
$presenters_pages = array();
$dom = new simple_html_dom();
$uris = array(
    //"http://chicago2011.drupal.org/schedule",
    "http://chicago2011.drupal.org/schedule/core",
);

// Assemble the array of session presenters profile pages.
foreach ($uris as $uri) {
    $schedule_dom = file_get_html($uri);
    //$sessions = $schedule_dom->find('.type-session');
    $sessions = $schedule_dom->find('.type-coreconversation');

    foreach ($sessions as $session) {
        $title_tags = $session->find('.views-field-title');
        $title = $title_tags[0]->text();
        $presenters = $session->find('.views-field-field-presenters-uid a');
print(count($presenters));
        foreach ($presenters as $presenter) {
            $path = 'http://london2011.drupal.org' . str_replace('/user/', '/users/', $presenter->href);
            $conf_profile = 'http://chicago2011.drupal.org' . $presenter->href;
            // Only scrape pages if this presenter hasn't already been logged.
            if (!isset($result[$path])) {
                $profile_dom = file_get_html($path);
                // Add the presenter to results
                $result[$path]['conf_profile'] = $conf_profile;

                // If there is a corresponding profile from london, use that to get the d.o profile.
                if (is_object($profile_dom)) {
                    // Get Drupal.org profile.
                    $do = $profile_dom->find('.user-member .form-item a');
                    // If the Drupal.org profile exists, crawl it for more info.
                    if (isset($do[0])) {
                        $do_path = $do[0]->href;
                        $do_profile_dom = file_get_html($do_path);
                        $gender_tag = $do_profile_dom->find('dd.profile-profile_gender');
                        if (isset($gender_tag[0])) {
                            $gender = $gender_tag[0]->text();
                        }
                        else {
                            $gender = '';
                        }
                        $result[$path]['do_profile'] = $do_path;
                        $result[$path]['gender'] = $gender;
                    }
    
                    // Be a polite crawler, robots.txt says Crawl-delay: 10.
                    sleep(10);
                }
            }
            $result[$path]['session'] = $title;
      
            scraperwiki::save(array('conf_profile', 'session'), $result[$path]);
        }
    }
}
?>
