<?php

# Jobs Scraper
require 'scraperwiki/simple_html_dom.php';
//$html = scraperWiki::scrape("http://www.indeed.com/jobs?q=title%3A+computational+jobs&fromage=7&from=ja&hl=en&fr=b&of=1&utm_source=jobseeker_emails&utm_medium=email&utm_campaign=job_alerts&limit=50");
//Sorted by Date, I may add the date attribute in.

//$html = scraperWiki::scrape("http://www.indeed.com/jobs?q=title%3A+computational+jobs&limit=50&fromage=7&sort=date");
//$dom = new simple_html_dom();
//$dom->load($html);
$dom = file_get_html("http://www.indeed.com/jobs?q=title%3A+computational+jobs&limit=50&fromage=7&sort=date");
foreach ($dom->find("div[@itemtype='http://schema.org/JobPosting']") as $job) {
    $title = $job->find(".jobtitle a");
    $institution= $job->find("span.company");
    $location = $job->find("span[@itemprop='addressLocality']");
    $postTime = $job->find("span.date");
    $postArr = explode ( " " , $postTime[0]->plaintext);

    $postDate = "";
    if ($postArr[1] == "days" || $postArr[1] == "day"){
        $postDate = date("Y-m-d", mktime(date("H"), date("i"), date("s") , date("m"), date("d") - $postArr[0], date("Y")));

    }else if($postArr[1] == "hours" || $postArr[1] == "hour"){
        $postDate = date("Y-m-d", mktime(date("H") - $postArr[0], date("i"), date("s") , date("m"), date("d"), date("Y")));

    }else if($postArr[1] == "minutes" || $postArr[1] == "minute"){
        $postDate = date("Y-m-d", mktime(date("H"), date("i") - $postArr[0], date("s") , date("m"), date("d"), date("Y")));

    }else{
        $postDate = "Invalid Date";
    }

    $summary = $job->find("table tbody tr td div span.summary");

    $jobRecord = array(
        'title' => $title[0]->title,
        'href' => $title[0]->href,
        'institution' => $institution[0]->plaintext,
        'location' => $location[0]->plaintext,
        'postDate'=> $postDate,
        'summary' => $summary[0]->plaintext
    );
   scraperwiki::save_sqlite(array('href'), $jobRecord);    
    
}
?>
