<?php

    $x = scraperWiki::scrape('http://www.weather.gov/xml/current_obs/index.xml');
    if( !empty( $x ) ) {
        $x = simplexml_load_string( $x );
        if( $x && $x->station ) {
            foreach( $x->station as $s ) {
                $d = array();
                $d['code'] = (string)$s->station_id;
                $d['state'] = (string)$s->state;
                $d['name'] = (string)$s->station_name;
                $d['latitude'] = (float)$s->latitude;
                $d['longitude'] = (float)$s->longitude;
                $d['urlhtml'] = (string)$s->html_url;
                $d['urlrss'] = (string)$s->rss_url;
                $d['urlxml'] = (string)$s->xml_url;
                scraperwiki::save( array( 'code' ), $d );
            }
        }
    }

?>
<?php

    $x = scraperWiki::scrape('http://www.weather.gov/xml/current_obs/index.xml');
    if( !empty( $x ) ) {
        $x = simplexml_load_string( $x );
        if( $x && $x->station ) {
            foreach( $x->station as $s ) {
                $d = array();
                $d['code'] = (string)$s->station_id;
                $d['state'] = (string)$s->state;
                $d['name'] = (string)$s->station_name;
                $d['latitude'] = (float)$s->latitude;
                $d['longitude'] = (float)$s->longitude;
                $d['urlhtml'] = (string)$s->html_url;
                $d['urlrss'] = (string)$s->rss_url;
                $d['urlxml'] = (string)$s->xml_url;
                scraperwiki::save( array( 'code' ), $d );
            }
        }
    }

?>
