<?php

require 'scraperwiki/simple_html_dom.php';

$DEBUG = false;

$init = count(scraperwiki::show_tables())==0;

$lastbrandmodelcrawl = scraperwiki::get_var('lastcrawl');

if(time() > $lastbrandmodelcrawl+3600*24*7) {
  //Find the brands/Makers
  $allbrands = scraperWiki::scrape("http://www.flickr.com/cameras/brands/");     
  $allbrands_dom = new simple_html_dom();
  $allbrands_dom->load($allbrands);
  $brands_node = $allbrands_dom->find("td.clTxt h4 a");
    
  if(!$init) {
    $known_brands = scraperwiki::select("count(url) as cnt from brands");
  }
  if($init || $known_brands[0]['cnt'] != count($brands_node)) {
    foreach($brands_node as $data){
      $record = array(
                      'name' => $data->plaintext,
                      'url' => $data->href
                      );
      if($DEBUG) { print_r($record); }
      else {scraperwiki::save_sqlite(array('url'), $record, $table_name="brands");}
    }
  }
  $lastbrandmodelcrawl = scraperwiki::save_var('lastcrawl', time());
 }
    
//Crawl each brand page to find the camera models
// find the brand that we haven't processed at all (i.e. the ones with no entry in the cameras table)
$missingbrands = scraperwiki::select("brands.url as url from brands left outer join cameras on cameras.brand_url=brands.url group by brands.url having count(brands.url) = 1");
//then add the ones we already looked at.  
$knownbrands = scraperwiki::select("distinct brand_url as url from cameras");
//this is done to crawl first the cameras that might have been missed by a too long execution time.
$missingbrands = array_merge($missingbrands, $knownbrands);
foreach($missingbrands as $br) {
  $brandpage = scraperWiki::scrape("http://www.flickr.com/".$br['url']);     
  $cameras_dom = new simple_html_dom();
  $cameras_dom->load($brandpage);
  foreach($cameras_dom->find("div#models td.cfM a") as $realdata){     
    if(!$init) {
      $countCam = scraperwiki::select("count(url) as cnt from cameras where url='".$realdata->href."'");
    }
    //there is no point in inserting if we already know about this camera. In particular, we do not want to overwrite the initial count.
    if($init || intval($countCam[0]['cnt']) == 0) {
      $record = array(
                      'name' => $realdata->plaintext,
                      'url' => $realdata->href,
                      'brand_url' => $br['url'],
                      'record_date' => date("Y-m-d")
                      );
      //and the camera type
      $type = $realdata->parent()->next_sibling()->next_sibling()->next_sibling()->next_sibling(); 
        //sometimes on flickr, this column is missing and we end up grabing some count instead of the actual camera type.
        if(!preg_match('/[a-zA-Z]/',$type->plaintext)) {
          $record['camera_type'] = "Unknown"; 
        } else {
          $record['camera_type'] = $type->plaintext;
        }
      //we store the camera but not all the details yet
      if($DEBUG) { print_r($record);}
      else { scraperwiki::save_sqlite(array('url'), $record, $table_name="cameras"); }
    }
    if(!$init) {
      $countStat = scraperwiki::select("count(camera_url) as cnt from camera_stats where date='".date("Y-m-d")."' and camera_url='".$realdata->href."'");
    }
    if($init || intval($countStat[0]['cnt']) == 0) {
        $statrecord = array(
                            'camera_url'=>$realdata->href,
                            'date' => date("Y-m-d")
                            );
        $inituse = $realdata->parent()->next_sibling();
        $statrecord['photo_count'] = intval(preg_replace('/,/','',$inituse->plaintext));
        $avgusers = $inituse->next_sibling();
        $statrecord['daily_users'] = intval(preg_replace('/,/','',$avgusers->plaintext));
        if($DEBUG) { print_r($statrecord);}
        //TODO: do not store if the numbers didn't change since last record
        else { scraperwiki::save_sqlite(array('camera_url','date'), $statrecord, $table_name="camera_stats"); }
    }
  }
}



//Now, fetch the camera details if we have time. Just fetch for the ones without existing metadata
$cameras = scraperwiki::select("name, url, brand_url, record_date from cameras  where megapixels is null or camera_type is null");
foreach($cameras as $cam) {

  $detailspage = scraperWiki::scrape("http://www.flickr.com/".$cam['url']);     
  $det_dom = new simple_html_dom();
  $det_dom->load($detailspage);

  $detail_record = array(
                         'name' => $cam['name'],
                         'url' => $cam['url'],
                         'brand_url' => $cam['brand_url'],
                         'record_date' =>$cam['record_date']);
  //store all details about the cameras
  foreach($det_dom->find("div#cfMoSpecs td") as $detail) {
    $header = $detail->prev_sibling()->plaintext;
    $header = strtolower(preg_replace('/ /','_',$header));
    $header = preg_replace('/:/','',$header);
    $detail_record[$header] = preg_replace('/\s*$/','',preg_replace('/ˆ\s*/','',$detail->plaintext));
  }
 
  if($DEBUG) {print_r($datail_record);}
  else if($detail_record['camera_type']){
    scraperwiki::save_sqlite(array('url'), $detail_record, $table_name="cameras");
  }    
}

?>