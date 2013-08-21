<?php
$page = array(
 "http://drupal.org/search/site/commerce?f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=1&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=2&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=3&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=4&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=5&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=6&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=7&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=8&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=9&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=10&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=11&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule",
 "http://drupal.org/search/site/commerce?page=12&f[0]=drupal_core%3A103&f[1]=bs_project_sandbox%3A0&f[2]=ss_meta_type%3Amodule"
);       
require 'scraperwiki/simple_html_dom.php';

// To change schema:
// - Clear data
// - Run
if (!scraperwiki::table_info('swdata')) {
scraperwiki::sqliteexecute("create table swdata (`name` string, `url` string, `author` string, `maintenance` string, `dev_status` string, `rec_release_version` string, `rec_release_type` string, `rec_release_timestamp` datetime, `downloads` int, `installs` int, `bugs` int, `total_bugs` int, `age_years` float, `mbug_rate` float, `created` datetime, `modified` datetime, `last_commit` datetime)");
scraperwiki::sqlitecommit();
}



$now = time();
$i=0;
foreach ($page as $id=>$url) {
  $html = scraperWiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);
  // Grab urls for each module
  foreach($dom->find("dt[@class='title'] a") as $data){
    $i++;
    if (stristr($data->href,"commerce_")) {
      // Load Module Data
      $html2 = scraperWiki::scrape($data->href);
      $dom2 = new simple_html_dom();
      $dom2->load($html2);
      // author
      foreach($dom2->find("div[@class='submitted'] a") as $data2){
        $author = $data2->plaintext;
        break;
      }

      // created
      $created= NULL;
      foreach($dom2->find("div[@class='submitted'] em") as $data2){
        $created = str_ireplace(' at ', ' ', $data2->plaintext);
        if (!empty($created)) {
          $created = date_create($created);
        }

        break;
      }

      // description
      $first = true;
      foreach($dom2->find("div[@class='node-content'] p") as $data2){
        if ($first) {
          // get sentences
          $sentences = preg_split('/(?<=[.!?]|[.!?][\'"])\s+/', $data2->plaintext, -1, PREG_SPLIT_NO_EMPTY);
          $desc = $sentences[0];
          $first = false;
        }
      }
      // module stats
      $maintenance_status = "";
      $dev_status = "";
      $installs = 0;
      $downloads = 0;
      $lastmodified = "";
      foreach($dom2->find("div[@class='project-info'] ul li") as $data2){
        if (stristr($data2->plaintext,"Maintenance")) {
          $maintenance_status = substr($data2->plaintext,20);
        }
        if (stristr($data2->plaintext,"Development")) {
          $dev_status = substr($data2->plaintext,20);
        }
        if (stristr($data2->plaintext,"Reported")) {
          $array = explode(" ",$data2->plaintext);
          $installs = intval(str_replace(",","",$array[2]));
        }
        if (stristr($data2->plaintext,"Downloads")) {
          $array = explode(" ",$data2->plaintext);
          $downloads = intval(str_replace(",","",$array[1]));
        }
        if (stristr($data2->plaintext,"Last")) {
          $lastmodified = date_create(substr($data2->plaintext,15));
        }
      }

      // Stable releases
      $rec_release = array('version' => '', 'type' => '', 'timestamp' => '');      
      foreach($dom2->find("div.download-table-ok tr.views-row-first") as $data2){
        foreach ($data2->find('td.views-field-version a') as $release_data) {
          $rec_release['version'] = $release_data->plaintext;
          // resolve type of release
          //7.x-1.0-beta4
          $version_parts = explode('-', $rec_release['version']);
          if (!empty($version_parts)) {
            $rec_release['type'] = 'unknown';
            $version_parts_count = count($version_parts);
            if (count($version_parts) > 2) {
              $last_version_part = $version_parts[$version_parts_count - 1];
              foreach (array('beta', 'alpha', 'rc') as $version_type) {
                if (stripos($last_version_part, $version_type) !== FALSE) {
                  $rec_release['type'] = $version_type;
                  break;
                }
              }
            }
            else {
             $rec_release['type'] = 'stable';
            }
          }

          break;
        }
        foreach ($data2->find('td.views-field-file-timestamp') as $release_data) {
          $rec_release['timestamp'] = date_create($release_data->plaintext);
          break;
        }

        break;
      }

      // Issues
      $open_bugs = 0;
      $total_bugs = 0;
      foreach($dom2->find("div.issue-cockpit-bug div.issue-cockpit-totals a") as $data2){
        if (empty($open_bugs) && stristr($data2->plaintext, "open")) {
          $open_bugs = intval(str_ireplace(' open', '', $data2->plaintext));
          continue;
        }
        elseif (empty($total_bugs) && stristr($data2->plaintext, "total")) {
          $total_bugs = intval(str_ireplace(' total', '', $data2->plaintext));
        }
      }

      // Commit stats
      // ex: "last: 9 weeks ago, first: 1 year ago"
      $last_commit = NULL;
      foreach($dom2->find("div.vc-commit-times") as $data2) {
        $commits = preg_split('@\,\s*@', $data2->plaintext, 2);
        foreach ($commits as $commit_i => $commit) {
          if (stripos($commit, 'last') !== FALSE) {
            $last_commit = preg_replace('@^.*\:\s*@', '', $commit);
            if (!empty($last_commit)) {
              $last_commit = date_create($last_commit);
            }
            break;
          }
        }

        break;
      }

      // Analysis
      $total_opp_days = 0;
      $age = 0;
      if (!empty($created) && is_object($created)) {
        $age = $now - $created->format('U');
        $age_days = $age / 86400;
        $total_opp_days = $downloads * $age_days;
      }

      // Failure rate: bugs / opp-days
      $bug_rate = 0;
      if (!empty($total_opp_days)) {
       $bug_rate = $total_bugs / $total_opp_days;
      }
        
      // Build data record
      $uniquekeys = array("name","url");
      $data = array(
        "name" => $data->plaintext,
        "url" => $data->href,
        "author" => $author,
        "maintenance" => $maintenance_status,
        "dev_status" => $dev_status,
        "rec_release_version" => $rec_release['version'],
        "rec_release_type" => $rec_release['type'],
        "rec_release_timestamp" => $rec_release['timestamp'],
        "downloads" => $downloads,
        "installs" => $installs,
        "bugs" => $open_bugs,
        "total_bugs" => $total_bugs,
        "age_years" => round($age / 86400 / 365.25, 2),
        "mbug_rate" => round($bug_rate * 1000, 2),
        "created" => $created,
        "modified" => $lastmodified,
        "last_commit" => $last_commit,
      );
      scraperwiki::save($uniquekeys,$data);
    }
  }

}
?>