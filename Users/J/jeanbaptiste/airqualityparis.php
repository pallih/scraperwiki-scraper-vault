<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://calendrier.voyages-sncf.com/resultat/OUTWARD_DATE/20-08-2012/TRAVEL_TYPE/AS/DISPLAY_NIGHT_TRAINS/on/DESTINATION_RR/FRPAR/ORIGIN_RR/FRXUY/DISTRIBUTED_COUNTRY/FR/NB_PASSENGERS/1/PASSENGER_1_AGE/26/PASSENGER_1_FID_PROG/default/OUTWARD_TIME/12/COMFORT_CLASS/2/INWARD_TIME/7/RANGE_AGE/ADULT/PASSENGER_1_CARD/YOUNG/REFERRER/bandeauflexibilite/DIRECT_TRAIN/true/aller#http://calendrier.voyages-sncf.com:80/resultat/ORIGIN_RR/FRXUY/DESTINATION_RR/FRPAR/NB_PASSENGERS/1/TRAVEL_TYPE/AS/DISTRIBUTED_COUNTRY/FR/COMFORT_CLASS/2/OUTWARD_DATE/20-08-2012/OUTWARD_TIME/12/INWARD_TIME/7/RANGE_AGE/STANDARD/DIRECT_TRAIN/true/PASSENGER_1_CARD/YOUNG/INITIAL_OUTWARD_BEST_PRICE/51.0/DISPLAY_NIGHT_TRAINS/on/PASSENGER_1_AGE/26/SHIFT_O/0/DISPLAYED_BEST_PRICE/63.0/CALENDAR_SELECTED_DATE_O/19-08-2012/aller");
$html = str_get_html($html_content);
$cpt = 0;

foreach ($html->find("div a span (text)") as $el) {

$save = array('Value'=>$el->innertext);
        
scraperwiki::save(array('Value'), $save);
 
}

?>
<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://calendrier.voyages-sncf.com/resultat/OUTWARD_DATE/20-08-2012/TRAVEL_TYPE/AS/DISPLAY_NIGHT_TRAINS/on/DESTINATION_RR/FRPAR/ORIGIN_RR/FRXUY/DISTRIBUTED_COUNTRY/FR/NB_PASSENGERS/1/PASSENGER_1_AGE/26/PASSENGER_1_FID_PROG/default/OUTWARD_TIME/12/COMFORT_CLASS/2/INWARD_TIME/7/RANGE_AGE/ADULT/PASSENGER_1_CARD/YOUNG/REFERRER/bandeauflexibilite/DIRECT_TRAIN/true/aller#http://calendrier.voyages-sncf.com:80/resultat/ORIGIN_RR/FRXUY/DESTINATION_RR/FRPAR/NB_PASSENGERS/1/TRAVEL_TYPE/AS/DISTRIBUTED_COUNTRY/FR/COMFORT_CLASS/2/OUTWARD_DATE/20-08-2012/OUTWARD_TIME/12/INWARD_TIME/7/RANGE_AGE/STANDARD/DIRECT_TRAIN/true/PASSENGER_1_CARD/YOUNG/INITIAL_OUTWARD_BEST_PRICE/51.0/DISPLAY_NIGHT_TRAINS/on/PASSENGER_1_AGE/26/SHIFT_O/0/DISPLAYED_BEST_PRICE/63.0/CALENDAR_SELECTED_DATE_O/19-08-2012/aller");
$html = str_get_html($html_content);
$cpt = 0;

foreach ($html->find("div a span (text)") as $el) {

$save = array('Value'=>$el->innertext);
        
scraperwiki::save(array('Value'), $save);
 
}

?>
