<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?tm=0");          

$dom = new simple_html_dom();

$dom->load($html);

//HOW MANY PAGES OF JOBS ARE THERE?
$current_page_info = $dom->find('div.searchSummary',0)->plaintext;
$regex_pattern = "/Jobs ([0-9]+)-([0-9]+) of ([0-9]+)/";
preg_match_all($regex_pattern,$current_page_info,$matches);

//IF WE KNOW HOW MANY JOBS, WE CAN WORK OUT NUMBER OF PAGES
//AND LOOP THROUGH THEM
if(isset($matches[3])) {
    $number_of_jobs = intval($matches[3][0]);
    $number_of_pages = ceil($number_of_jobs/25);

    //FOR EACH PAGE OF JOBS
    for($i=1; $i<=$number_of_pages;$i++) {
        scrape_job_page($i);
    }
}

function scrape_job_page($page) {
    $page_html = scraperWiki::scrape("https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?tm=0&pg=".$page);
    $dom = new simple_html_dom();
    $dom->load($page_html);
    foreach($dom->find("table tr") as $data){
        $tds = $data->find("td");
        if(count($tds)==5){
            $id_hyperlink = $tds[0]->find('a[name]',0);
            $id = intval($id_hyperlink->name);

            $more_info_hyperlink = $tds[2]->find('a',0)->href;        
            print($more_info_hyperlink);
            $record = array(
                'id' => $id,
                'posted_date' => date_create($tds[0]->plaintext),
                'job_title' => trim($tds[2]->plaintext),
                'company' => trim($tds[3]->plaintext),
                'location' => trim($tds[4]->plaintext),
                'url' => $more_info_hyperlink
            );
            

            

            //print json_encode($record) . "\n";
            scraperwiki::save(array('id'), $record);  
        }
    }
    $dom->__destruct();
}


?>
<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?tm=0");          

$dom = new simple_html_dom();

$dom->load($html);

//HOW MANY PAGES OF JOBS ARE THERE?
$current_page_info = $dom->find('div.searchSummary',0)->plaintext;
$regex_pattern = "/Jobs ([0-9]+)-([0-9]+) of ([0-9]+)/";
preg_match_all($regex_pattern,$current_page_info,$matches);

//IF WE KNOW HOW MANY JOBS, WE CAN WORK OUT NUMBER OF PAGES
//AND LOOP THROUGH THEM
if(isset($matches[3])) {
    $number_of_jobs = intval($matches[3][0]);
    $number_of_pages = ceil($number_of_jobs/25);

    //FOR EACH PAGE OF JOBS
    for($i=1; $i<=$number_of_pages;$i++) {
        scrape_job_page($i);
    }
}

function scrape_job_page($page) {
    $page_html = scraperWiki::scrape("https://jobsearch.direct.gov.uk/JobSearch/PowerSearch.aspx?tm=0&pg=".$page);
    $dom = new simple_html_dom();
    $dom->load($page_html);
    foreach($dom->find("table tr") as $data){
        $tds = $data->find("td");
        if(count($tds)==5){
            $id_hyperlink = $tds[0]->find('a[name]',0);
            $id = intval($id_hyperlink->name);

            $more_info_hyperlink = $tds[2]->find('a',0)->href;        
            print($more_info_hyperlink);
            $record = array(
                'id' => $id,
                'posted_date' => date_create($tds[0]->plaintext),
                'job_title' => trim($tds[2]->plaintext),
                'company' => trim($tds[3]->plaintext),
                'location' => trim($tds[4]->plaintext),
                'url' => $more_info_hyperlink
            );
            

            

            //print json_encode($record) . "\n";
            scraperwiki::save(array('id'), $record);  
        }
    }
    $dom->__destruct();
}


?>
