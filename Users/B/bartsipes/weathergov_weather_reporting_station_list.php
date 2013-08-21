<?php
    require 'scraperwiki/simple_html_dom.php';           
    $x = scraperWiki::scrape('http://www.weather.gov/xml/current_obs/index.xml');
   
    if( !empty( $x ) ) {
        $x = simplexml_load_string( $x );
        if( $x && $x->station ) {
            $d = array();

            foreach( $x->station as $s ) {
            #for($i = 0; $i < 100; $i++) {
            #    $s = $x->station[$i];
                $d['code'] = (string)($s->station_id);
                $d['state'] = (string)($s->state);
                $d['name'] = (string)($s->station_name);
                $d['latitude'] = (float)($s->latitude);
                $d['longitude'] = (float)($s->longitude);

                $html = scraperWiki::scrape("http://www.weather.gov/data/obhistory/" . $d['code']. ".html");
                $dom = new simple_html_dom();
                $dom->load($html);
                
                $curDate = getdate();
                foreach($dom->find("table[cellpadding=2]>tbody>tr") as $tr) {
                    $tds = $tr->find("td");
                    
                    if (sizeof($tds) == 17) {
                        $record = array();
    
                        $record['code'] = (string)($d['code']);
                        $record['state'] = (string)($d['state']);
                        $record['name'] = (string)($d['name']);
                        $record['latitude'] = (float)($d['latitude']);
                        $record['longitude'] = (float)($d['longitude']);
    
                        $record['datetime'] = (string)($curDate['year'] . "-". $curDate['mon'] . "-" . $tds[0]->plaintext . " " . $tds[1]->plaintext);
                        $record['wind'] = (string)($tds[2]->plaintext);
                        $record['visibility'] = (string)($tds[3]->plaintext);
                        $record['air_temp'] = (string)($tds[6]->plaintext);
                        $record['dewpoint'] = (string)($tds[7]->plaintext);
                        $record['rel_humidity'] = (string)($tds[10]->plaintext);
                        $record['windchill'] = (string)($tds[11]->plaintext);
                        $record['pressure_altimiter'] = (string)($tds[12]->plaintext);
                        $record['pressure_sea_level'] = (string)($tds[13]->plaintext);
                        $record['precip_last_one_hours'] = (string)($tds[14]->plaintext);
                        $record['precip_last_three_hours'] = (string)($tds[15]->plaintext);
                        $record['precip_last_six_hours'] = (string)($tds[16]->plaintext);

                        scraperwiki::save( array( 'code', 'datetime' ), $record );
                    }
                }
            }
        }
    }
?>
