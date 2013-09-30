<?php
/*        Met Office HadUKP (UK Precipitation Data) Scraper -- Output
 *             By Ændrew Rininsland <me at aendrew dot com> http://aendrew.com
 *             Data taken from: http://www.metoffice.gov.uk/hadobs/hadukp/data/download.html
 *
 *        This view outputs HadUKP data as a webservice in JSON, allowing users to look up preciptation data. Simple!
 * 
 *        Path arguments (region is required):
 *                   region=$REGION -- $REGION is one of:
 *                                        seep -- South East England
 *                                        swep -- South West England & Wales
 *                                        cep  -- Central England
 *                                        nwep -- North West England & Wales
 *                                        neep -- North East England
 *                                        ssp  -- South Scotland
 *                                        nsp  -- North Scotland
 *                                        esp  -- East Scotland
 *                                        nip  -- Northern Ireland
 *
 *                  date=$DATE -- date in ISO-9001 format (i.e., yyyy-mm-dd) 
 *                                Can be in a range, i.e., yyyy-mm-dd-TO-yyyy-mm-dd or comma-separated, i.e., yyyy-mm-dd,yyyy-mm-dd (TODO)
 *
 *                  callback=$CALLBACK -- JSONP callback
 */


scraperwiki::httpresponseheader('Content-Type', 'text/javascript; charset=utf-8');
if (isset($_GET['region'])) $region = $_GET['region']; else exit('Region required');
if (isset($_GET['date'])) $date = $_GET['date']; //TODO more date handling
if (isset($_GET['callback'])) $callback = $_GET['callback']; else $callback='data';

scraperwiki::attach("hadukp_webservice_scraper");


$query = '`date`, `set`, `measurement` from hadukp_webservice_scraper.swdata WHERE `set` = "' . $region . '"' . (isset($date) ? ' AND `date` = "' . $date . '"' : '') . ';';

$data = scraperwiki::select($query);


echo $callback. '(' . json_encode($data) . ');';


?>
<?php
/*        Met Office HadUKP (UK Precipitation Data) Scraper -- Output
 *             By Ændrew Rininsland <me at aendrew dot com> http://aendrew.com
 *             Data taken from: http://www.metoffice.gov.uk/hadobs/hadukp/data/download.html
 *
 *        This view outputs HadUKP data as a webservice in JSON, allowing users to look up preciptation data. Simple!
 * 
 *        Path arguments (region is required):
 *                   region=$REGION -- $REGION is one of:
 *                                        seep -- South East England
 *                                        swep -- South West England & Wales
 *                                        cep  -- Central England
 *                                        nwep -- North West England & Wales
 *                                        neep -- North East England
 *                                        ssp  -- South Scotland
 *                                        nsp  -- North Scotland
 *                                        esp  -- East Scotland
 *                                        nip  -- Northern Ireland
 *
 *                  date=$DATE -- date in ISO-9001 format (i.e., yyyy-mm-dd) 
 *                                Can be in a range, i.e., yyyy-mm-dd-TO-yyyy-mm-dd or comma-separated, i.e., yyyy-mm-dd,yyyy-mm-dd (TODO)
 *
 *                  callback=$CALLBACK -- JSONP callback
 */


scraperwiki::httpresponseheader('Content-Type', 'text/javascript; charset=utf-8');
if (isset($_GET['region'])) $region = $_GET['region']; else exit('Region required');
if (isset($_GET['date'])) $date = $_GET['date']; //TODO more date handling
if (isset($_GET['callback'])) $callback = $_GET['callback']; else $callback='data';

scraperwiki::attach("hadukp_webservice_scraper");


$query = '`date`, `set`, `measurement` from hadukp_webservice_scraper.swdata WHERE `set` = "' . $region . '"' . (isset($date) ? ' AND `date` = "' . $date . '"' : '') . ';';

$data = scraperwiki::select($query);


echo $callback. '(' . json_encode($data) . ');';


?>
