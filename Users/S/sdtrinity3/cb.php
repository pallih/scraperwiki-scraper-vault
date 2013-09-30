<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$pagenum=1;
for($i = 0; $i < 2; $i++)
{
    $html = scraperwiki::scrape('http://collegesearch.collegeboard.com/search/CollegeDetail.jsp?collegeId='.$pagenum.'&profileId=7');
    print $html;
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    
        foreach($dom->find('div#profile_hdr h1') as $school_name)
        {
            # Store data in the datastore
            print $school_name->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $school_name->plaintext));
        }
        foreach($dom->find('div.profile_detail h4') as $program_category)
        {
            # Store data in the datastore
            print $program_category->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $program_category->plaintext));
        }
        foreach($dom->find('div.profile_detail ul.none li a') as $program_name)
        {
            # Store data in the datastore
            print $program_name->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $program_name->plaintext));
        }
        foreach($dom->find('div.profile_detail ul.none li em') as $degree_type)
        {
            # Store data in the datastore
            print $degree_type->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $degree_type->plaintext));
        }
        $pagenum++;
        echo $pagenum;
}
?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$pagenum=1;
for($i = 0; $i < 2; $i++)
{
    $html = scraperwiki::scrape('http://collegesearch.collegeboard.com/search/CollegeDetail.jsp?collegeId='.$pagenum.'&profileId=7');
    print $html;
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    
        foreach($dom->find('div#profile_hdr h1') as $school_name)
        {
            # Store data in the datastore
            print $school_name->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $school_name->plaintext));
        }
        foreach($dom->find('div.profile_detail h4') as $program_category)
        {
            # Store data in the datastore
            print $program_category->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $program_category->plaintext));
        }
        foreach($dom->find('div.profile_detail ul.none li a') as $program_name)
        {
            # Store data in the datastore
            print $program_name->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $program_name->plaintext));
        }
        foreach($dom->find('div.profile_detail ul.none li em') as $degree_type)
        {
            # Store data in the datastore
            print $degree_type->plaintext . "\n";
            scraperwiki::save(array('data'), array('data' => $degree_type->plaintext));
        }
        $pagenum++;
        echo $pagenum;
}
?>