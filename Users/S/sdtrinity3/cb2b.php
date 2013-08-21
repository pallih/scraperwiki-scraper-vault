<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$pagenum=1;
for($i = 0; $i < 3; $i++)
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
        #    scraperwiki::save(array('data1'));

            foreach($dom->find('div.profile_detail') as $program_tree)
            {
                foreach($program_tree->find('h4') as $program_category)
                {
                    # Store data in the datastore
                    print $program_category->plaintext . "\n";
                #    scraperwiki::save(array('data2'));
                }
                foreach($program_tree->find('ul.none li a') as $program_name)
                {
                    # Store data in the datastore
                    print $program_name->plaintext . "\n";
                #    scraperwiki::save(array('data3'));
                }
                foreach($program_tree->find('ul.none li em') as $degree_type)
                {
                    # Store data in the datastore
                    print $degree_type->plaintext . "\n";
                #    scraperwiki::save(array('data2'));
                }
                scraperwiki::save(array('data'),
                array(
                    'data1' => $school_name->plaintext,
                    'data2' => $program_category->plaintext,
                    'data3' => $program_name->plaintext,
                    'data4' => $degree_type->plaintext
                    )
                );
            }
        }

        $pagenum++;
        echo $pagenum;
}
?>