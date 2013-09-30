<?php

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://events.fai.org/calendar?id=61");
print $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('tr.rowfront0,tr.rowfront1') as $event) {

         scraperwiki::save(array('event'), array(
                            'event' => "http://events.fai.org".$event ->children(1)->children(0)->children(0)->href,
                            'startdate' => preg_replace('/to<br \/>\d+ \w+/i','',$event ->children(0)->innertext),
                            'enddate' => preg_replace('/.*to<br \/>/i','',$event ->children(0)->innertext),
                            'title' => $event ->children(1)->children(0)->plaintext,
                            'location'=> preg_replace('/.*<br \/>(.*)<br \/>&nbsp;/i','$1',$event ->children(1)->innertext)
                           )
                          );

}
 
?><?php

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://events.fai.org/calendar?id=61");
print $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('tr.rowfront0,tr.rowfront1') as $event) {

         scraperwiki::save(array('event'), array(
                            'event' => "http://events.fai.org".$event ->children(1)->children(0)->children(0)->href,
                            'startdate' => preg_replace('/to<br \/>\d+ \w+/i','',$event ->children(0)->innertext),
                            'enddate' => preg_replace('/.*to<br \/>/i','',$event ->children(0)->innertext),
                            'title' => $event ->children(1)->children(0)->plaintext,
                            'location'=> preg_replace('/.*<br \/>(.*)<br \/>&nbsp;/i','$1',$event ->children(1)->innertext)
                           )
                          );

}
 
?>