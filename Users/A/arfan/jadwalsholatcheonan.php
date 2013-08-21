<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.islamicfinder.org/prayer_service.php?country=south_korea&city=cheonan&state=17&zipcode=&latitude=36.8064&longitude=127.1522&timezone=9&HanfiShafi=1&pmethod=1&fajrTwilight1=10&fajrTwilight2=10&ishaTwilight=10&ishaInterval=30&dhuhrInterval=1&maghribInterval=1&dayLight=0&page_background=&table_background=&table_lines=black&text_color=green&link_color=&prayerFajr=Subuh&prayerSunrise=Fajar&prayerDhuhr=Dzuhur&prayerAsr=Ashar&prayerMaghrib=Maghrib&prayerIsha=Isya");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>