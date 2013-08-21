<?php
######################################
# Basic PHP scraper
######################################
# Ref http://simplehtmldom.sourceforge.net/manual.htm#frag_access_special

require  'scraperwiki/simple_html_dom.php';

$pagenum=1;
for($i = 0; $i < 2; $i++)
{
    $html = scraperwiki::scrape('http://collegesearch.collegeboard.com/search/CollegeDetail.jsp?collegeId='.$pagenum.'&profileId=7');
    print $html;
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    print '<?xml version="1.0" encoding="UTF-8"?>';
        foreach($dom->find('div#profile_hdr h1') as $school_name)
        {
            # Store data in the datastore
            print "<school><schoolname>" . $school_name->plaintext . "</schoolname>";
            scraperwiki::save(array('data'), array('data' => $school_name->plaintext));
        }
        foreach($dom->find('div.profile_detail') as $program_profile)
        {
            foreach($program_profile->find('h4') as $program_category)
            {
            print "<programcat>" . $program_category->plaintext;
                foreach($program_profile->find('ul.none') as $programs)
                {
                    foreach($programs->find('li') as $program_li)
                    {
                    print "<programlist>";
                        foreach($program_li->find('a') as $program_name)
                        {
                            print "<programname>" . $program_name->plaintext . "</programname>";
                            scraperwiki::save(array('data'), array('data' => $program_name->plaintext));
                        }
                        foreach($program_li->find('em') as $degree_type)
                        {
                            print "<degreetype>" . $degree_type->plaintext . "</degreetype>";
                            scraperwiki::save(array('data'), array('data' => $degree_type->plaintext));
                        }
                    print "</programlist>";
                    }
                }
            print "</programcat>";
            }
        }
        print "</school>";


        $pagenum++;
        echo $pagenum;
}
?>