<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://scoopeo.com/membre/vincentdidier/hp");
//print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('h3') as $data)
{
    foreach($data->children as $child)
    {
        if($child->tag == 'a')
        {
            
           scraperwiki::save(
                                array('table_cell','table'), 
                                array(
                                        'table_cell' => $child->plaintext,
                                        'table' => $child->getAttribute('href')
                                      )
                            );

            //scraperwiki::save(array('data'), array('data' => $child->getAttribute('href')));
        }
    }
   
}

?>