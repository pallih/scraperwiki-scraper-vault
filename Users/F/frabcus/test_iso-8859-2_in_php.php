<?php
require  'scraperwiki/simple_html_dom.php';

$url = "http://volby.cz/pls/kv2010/kv1111?xjazyk=CZ&xid=0&xdz=4&xnumnuts=1100&xobec=554782&xstat=0&xvyber=0";
$html = scraperwiki::scrape($url);

//scraperwiki::save(array('data'), array('data' => $html));
//exit(20);

//$html = iconv("ISO-8859-2", "UTF-8", $html);

print $html;

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('<div class="tabulka1"> tr') as $tr)
{
   # foreach($data->children as $td)
   # {
        if(count($tr->children)==5)
        {
        print $tr. "\n";
        
        scraperwiki::save(
                                array('cell1','cell2','cell3','cell4'), 
                                array(
                                        'cell1' => $tr->children(0)->plaintext,
                                        'cell2' =>$tr->children(1)->plaintext,
                                        'cell3' =>$tr->children(2)->plaintext,
                                         'cell4' => $tr->children(3)->plaintext,
                                        'cell4' => $tr->children(4)->plaintext
                                 )
                            );
        }
  #  }
}

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

#foreach($dom->find('td') as $data)
#{
#    scraperwiki::save(array('data'), array('data' => $data->plaintext));
#}


# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?>