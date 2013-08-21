<?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();
#scraperwiki::select("$id from reports");


#function reportupdate($id) {
#https://scraperwiki.com/scrapers/irish_president_engagements





#for ($i; $i <= 180; $i++ ) {   
#for ($i = 160; $i <= 175; $i++ ) {   
foreach($reports as $report)
/*{  $existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");

    if (sizeof($existingreports) < sizeof($report))
    {
print $report;
        scraperwiki::save(array('id'), $report);
    }
    else
    {
       print ("Skipping already saved record " . $report['id'] . "\n");
    }
*/
    $data = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
      #   $data = serialize(json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i)));
        print "\n" . "i" . $i;
        #print_r($data);
        #var_dump($data);



    $id = $i;
        #print_r($data['payload']);
        print "\n" .  "start";
        print $data['error']['message'];
 if( $data['error']['message'] == "No Error" )  {
print "no error";
    foreach($data['payload']['incidents'] as $report){

 


        print "\n" . "lll";

 $id = $i;
                $title = $report['incident']['incidenttitle'];
                $incidentdescription = $report['incident']['incidentdescription'];
                $incidentdate = $report['incident']['incidentdate'];
                $incidentmode = $report['incident']['incidentmode'];
                $incidentactive = $report['incident']['incidentactive'];
                $incidentverified = $report['incident']['incidentverified'];
                $locationid = $report['incident']['locationid'];
                $locationname = $report['incident']['locationname'];
                $locationlatitude = $report['incident']['locationlatitude'];
                $locationlongitude = $report['incident']['locationlongitude'];
                $error = $data['error']['message'];


            $catcount = count($report['categories']);
            print "\n" .  "categorycount" . $catcount;
        
            if ($catcount > 1){
                $categorytitle = "";
                $categoryid = "";
                
                for ( $b = 0; $b < $catcount;  $b++ ) {
                    print "\n" .  "bf" . $b;

                    $categorytitle .= "; " . $report['categories'][$b]['category']['title'];
                    
                    $categoryid .= "; " . $report['categories'][$b]['category']['id'];

                    print "\n" .  "categorytitlel" . $categorytitle;
               
                    $categoryod = ltrim($categoryid, "; ");
                    $categorytitle = ltrim($categorytitle, "; ");
                }


            }
            else {

                $categorytitle = $report['categories'][0]['category']['title'];
                $categoryid = $report['categories'][0]['category']['id'];
                }
                print "\n" .  "categorytitle" . $categorytitle;



 if (isset($report['media']['id'])) {


            print "mediaisset";
            $mediaid = $report['media']['id'];
            $mediatype = $report['media']['type'];
            $medialink = "http://www.fixyourstreet.ie/media/uploads/" . $report['media']['link'];
            $mediathumb = "http://www.fixyourstreet.ie/media/uploads/" . $report['media']['thumb'];

       } 

            else { 
                   
                    $mediaid = "";
                    $mediatype = "";
                    $medialink = "";
                    $mediathumb = "";

      }

               
            $reports["$id"] = array (
# "Local Authority Reference" => (string)$app->LOCAL_AUTHORITY_REFERENCE,



                    "ID"     => $id,
                    "Title"   => $title,
/*
                    "Category"   => $categorytitle,
                    "CategoryID"   => $categoryid,
                    "Incidentdescription" => $incidentdescription,
                    "Incidentdate" => $incidentdate,
                    "Incidentmode" => $incidentmode,
                    "Incidentactive" => $incidentactive,
                    "Incidentverified" => $incidentverified,
                    "Locationid" => $locationid,
                    "Locationname" => $locationname,
                    "Locationlatitude" => $locationlatitude,
                    "Locationlongitude" => $locationlongitude,
                    "Error"   => $error,
                    "MediaID"   => $mediatype,
                    "MediaType"   => $mediatype,
                    "MediaLink"   => $medialink,
                    "MediaThumb"   => $mediathumb
*/
/*
            "ID"     => $id,
                    "Title"   => $title,
                    "Category"   => $categorytitle,
                    "CategoryID"   => $categoryid,
                    "Incidentdescription" => $incidentdescription,
                    "Incidentdate" => $incidentdate,
                    "Incidentmode" => $incidentmode,
                    "Incidentactive" => $incidentactive,
                    "Incidentverified" => $incidentverified,
                    "Locationid" => $locationid,
                    "Locationname" => $locationname,
                    "Locationlatitude" => $locationlatitude,
                    "Locationlongitude" => $locationlongitude,
                    "Error"   => $error,
                    "MediaID"   => $mediatype,
                    "MediaType"   => $mediatype,
                    "MediaLink"   => $medialink,
                    "MediaThumb"   => $mediathumb
*/
            );


    }
}
    else { 
            print "kkk"; 
 foreach($data['error'] as $report){

            $error = $data['error']['message'];


$title = "No data";
                $incidentdescription = $data['error']['message'];
                $incidentdate = "";
                $incidentmode = "";
                $incidentactive = "";
                $incidentverified = "";
                $locationid = "";
                $locationname = "No data";
                $locationlatitude = "";
                $locationlongitude = "";
                $error = $data['error']['message'];
                $categorytitle = "";
                $categoryid = "";
                $mediaid = "";
                $mediatype = "";
                $medialink = "";
                $mediathumb = "";

            $reports["$id"] = array (


                    "ID"     => $id,
                    "Error"   => $error,
                    "Title"   => $title,
                    "Category"   => $categorytitle,
                    "CategoryID"   => $categoryid,
                    "Incidentdescription" => $incidentdescription,
                    "Incidentdate" => $incidentdate,
                    "Incidentmode" => $incidentmode,
                    "Incidentactive" => $incidentactive,
                    "Incidentverified" => $incidentverified,
                    "Locationid" => $locationid,
                    "Locationname" => $locationname,
                    "Locationlatitude" => $locationlatitude,
                    "Locationlongitude" => $locationlongitude,
                
                    "MediaID"   => $mediatype,
                    "MediaType"   => $mediatype,
                    "MediaLink"   => $medialink,
                    "MediaThumb"   => $mediathumb
             
            );
       }
}
print "\n" . "end" . "\n" ;

#}
#}

#print_r($reports);


#scraperwiki::sqliteexecute("drop table reports");
#scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string)");

/*
foreach ($reports as $id => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb)", #, :image, :address)", 
          
# $reports[] = array(  
                "title"     => $values["Title"],
                "id"    => $id,                
                "incidentdescription" => $values["Incidentdescription"],
                "incidentdate" => $values["Incidentdate"],
                "incidentmode" => $values["Incidentmode"],
                "incidentactive" => $values["Incidentactive"],
                "incidentverified" => $values["Incidentverified"],
                "locationid" => $values["Locationid"],
                "locationname" => $values["Locationname"],
                "locationlatitude" => $values["Locationlatitude"],
                "locationlongitude" => $values["Locationlongitude"],
                "categorytitle"     => $values["Category"],
                "categoryid"     => $values["CategoryID"],
                "error"     => $values["Error"],
                "mediaid"     => $values["MediaID"],
                "mediatype"     => $values["MediaType"],
                "medialink"     => $values["MediaLink"],
                "mediathumb"     => $values["MediaThumb"]

            )
   );


}

*/
#  $unique_keys = array("id");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table); #, $table
#}

/*https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals
https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals/edit/
*/

/*view-source:https://scraperwiki.com/editor/raw/318p_4_dept_websites_ho
def ScrapeRaw():
    scraperwiki.sqlite.execute("create table if not exists htmlcache (url text)")
    urlbatch = scraperwiki.sqlite.execute("select xllinks.url, xllinks.sheetname, xllinks.i from xllinks left join htmlcache on htmlcache.url = xllinks.url where htmlcache.url is null limit 20")
    ldata = [ ]
    for url, sheetname, i in urlbatch["data"]:
        page_req=requests.get(url)
        page_raw=page_req.content
        data = {'url':url, 'sheetname':sheetname, 'i':i, 'status':page_req.status_code}
        data['html']=unicode(page_raw, 'iso-8859-1')
        if re.search('charset=utf-8"', page_raw):
            try:
                data['html']=unicode(page_raw, 'utf-8')
            except UnicodeDecodeError, e:
                print "unicode failure", url
        ldata.append(data)
    scraperwiki.sqlite.save(["url"], ldata, "htmlcache")
    return len(ldata)
*/
#php version of this https://scraperwiki.com/scrapers/ratemyplace_food_safety_inspections/
/* ScraperWikiselect("id, date from swdata").each { |i| old[i["id"]] = i["date"]}

    puts scraped.to_yaml

    scraped.flatten.each do |i|
      if old.has_key?(i[:id].to_s) === FALSE
        get_inspection_detail(i)
        puts "Adding new inspection for #{i[:name]}"
      elsif old[i[:id]] != i[:date].to_s
        get_inspection_detail(i)
        puts "Updating inspection for #{i[:name]}"
      end
    end

  end 
*/
/*
old = new();
foreach ($i; ($old[$i["id"]] = $i["id"];) $i++; ) {
scraperwiki::select("$id from swdata"); 
}
#https://scraperwiki.com/scrapers/ratemyplace_food_safety_inspections/


   // puts scraped.to_yaml

    foreach($id; as id;) {
      if ($old((string)$i[$id]) === FALSE) {
       get_extras($i);
}
        print "Adding new inspection for" . $i[$incidenttitle];

#$iid =(string)$i[$id] 
      elseif( $old[$i[$id]] != (string)$i[$id]; ) {

       get_extras($i);
}
        print "Updating inspection for" . $i[$incidenttitle];
    

}
*/
#https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals/edit/
    #$existingRecords = scraperwiki::sqliteexecute("select * from swdata where `council_reference`='" . $record['council_reference'] . "'");
    #if (sizeof($existingRecords) == 0)
    #{
     #   scraperwiki::save(array('council_reference'), $record);
    #}
    #else
    #{
    #    print ("Skipping already saved record " . $record['council_reference'] . "\n");
    #}
  
}

#scraperwiki::sqlitecommit();
#$i = $id;
?><?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();
#scraperwiki::select("$id from reports");


#function reportupdate($id) {
#https://scraperwiki.com/scrapers/irish_president_engagements





#for ($i; $i <= 180; $i++ ) {   
#for ($i = 160; $i <= 175; $i++ ) {   
foreach($reports as $report)
/*{  $existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");

    if (sizeof($existingreports) < sizeof($report))
    {
print $report;
        scraperwiki::save(array('id'), $report);
    }
    else
    {
       print ("Skipping already saved record " . $report['id'] . "\n");
    }
*/
    $data = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
      #   $data = serialize(json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i)));
        print "\n" . "i" . $i;
        #print_r($data);
        #var_dump($data);



    $id = $i;
        #print_r($data['payload']);
        print "\n" .  "start";
        print $data['error']['message'];
 if( $data['error']['message'] == "No Error" )  {
print "no error";
    foreach($data['payload']['incidents'] as $report){

 


        print "\n" . "lll";

 $id = $i;
                $title = $report['incident']['incidenttitle'];
                $incidentdescription = $report['incident']['incidentdescription'];
                $incidentdate = $report['incident']['incidentdate'];
                $incidentmode = $report['incident']['incidentmode'];
                $incidentactive = $report['incident']['incidentactive'];
                $incidentverified = $report['incident']['incidentverified'];
                $locationid = $report['incident']['locationid'];
                $locationname = $report['incident']['locationname'];
                $locationlatitude = $report['incident']['locationlatitude'];
                $locationlongitude = $report['incident']['locationlongitude'];
                $error = $data['error']['message'];


            $catcount = count($report['categories']);
            print "\n" .  "categorycount" . $catcount;
        
            if ($catcount > 1){
                $categorytitle = "";
                $categoryid = "";
                
                for ( $b = 0; $b < $catcount;  $b++ ) {
                    print "\n" .  "bf" . $b;

                    $categorytitle .= "; " . $report['categories'][$b]['category']['title'];
                    
                    $categoryid .= "; " . $report['categories'][$b]['category']['id'];

                    print "\n" .  "categorytitlel" . $categorytitle;
               
                    $categoryod = ltrim($categoryid, "; ");
                    $categorytitle = ltrim($categorytitle, "; ");
                }


            }
            else {

                $categorytitle = $report['categories'][0]['category']['title'];
                $categoryid = $report['categories'][0]['category']['id'];
                }
                print "\n" .  "categorytitle" . $categorytitle;



 if (isset($report['media']['id'])) {


            print "mediaisset";
            $mediaid = $report['media']['id'];
            $mediatype = $report['media']['type'];
            $medialink = "http://www.fixyourstreet.ie/media/uploads/" . $report['media']['link'];
            $mediathumb = "http://www.fixyourstreet.ie/media/uploads/" . $report['media']['thumb'];

       } 

            else { 
                   
                    $mediaid = "";
                    $mediatype = "";
                    $medialink = "";
                    $mediathumb = "";

      }

               
            $reports["$id"] = array (
# "Local Authority Reference" => (string)$app->LOCAL_AUTHORITY_REFERENCE,



                    "ID"     => $id,
                    "Title"   => $title,
/*
                    "Category"   => $categorytitle,
                    "CategoryID"   => $categoryid,
                    "Incidentdescription" => $incidentdescription,
                    "Incidentdate" => $incidentdate,
                    "Incidentmode" => $incidentmode,
                    "Incidentactive" => $incidentactive,
                    "Incidentverified" => $incidentverified,
                    "Locationid" => $locationid,
                    "Locationname" => $locationname,
                    "Locationlatitude" => $locationlatitude,
                    "Locationlongitude" => $locationlongitude,
                    "Error"   => $error,
                    "MediaID"   => $mediatype,
                    "MediaType"   => $mediatype,
                    "MediaLink"   => $medialink,
                    "MediaThumb"   => $mediathumb
*/
/*
            "ID"     => $id,
                    "Title"   => $title,
                    "Category"   => $categorytitle,
                    "CategoryID"   => $categoryid,
                    "Incidentdescription" => $incidentdescription,
                    "Incidentdate" => $incidentdate,
                    "Incidentmode" => $incidentmode,
                    "Incidentactive" => $incidentactive,
                    "Incidentverified" => $incidentverified,
                    "Locationid" => $locationid,
                    "Locationname" => $locationname,
                    "Locationlatitude" => $locationlatitude,
                    "Locationlongitude" => $locationlongitude,
                    "Error"   => $error,
                    "MediaID"   => $mediatype,
                    "MediaType"   => $mediatype,
                    "MediaLink"   => $medialink,
                    "MediaThumb"   => $mediathumb
*/
            );


    }
}
    else { 
            print "kkk"; 
 foreach($data['error'] as $report){

            $error = $data['error']['message'];


$title = "No data";
                $incidentdescription = $data['error']['message'];
                $incidentdate = "";
                $incidentmode = "";
                $incidentactive = "";
                $incidentverified = "";
                $locationid = "";
                $locationname = "No data";
                $locationlatitude = "";
                $locationlongitude = "";
                $error = $data['error']['message'];
                $categorytitle = "";
                $categoryid = "";
                $mediaid = "";
                $mediatype = "";
                $medialink = "";
                $mediathumb = "";

            $reports["$id"] = array (


                    "ID"     => $id,
                    "Error"   => $error,
                    "Title"   => $title,
                    "Category"   => $categorytitle,
                    "CategoryID"   => $categoryid,
                    "Incidentdescription" => $incidentdescription,
                    "Incidentdate" => $incidentdate,
                    "Incidentmode" => $incidentmode,
                    "Incidentactive" => $incidentactive,
                    "Incidentverified" => $incidentverified,
                    "Locationid" => $locationid,
                    "Locationname" => $locationname,
                    "Locationlatitude" => $locationlatitude,
                    "Locationlongitude" => $locationlongitude,
                
                    "MediaID"   => $mediatype,
                    "MediaType"   => $mediatype,
                    "MediaLink"   => $medialink,
                    "MediaThumb"   => $mediathumb
             
            );
       }
}
print "\n" . "end" . "\n" ;

#}
#}

#print_r($reports);


#scraperwiki::sqliteexecute("drop table reports");
#scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string)");

/*
foreach ($reports as $id => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb)", #, :image, :address)", 
          
# $reports[] = array(  
                "title"     => $values["Title"],
                "id"    => $id,                
                "incidentdescription" => $values["Incidentdescription"],
                "incidentdate" => $values["Incidentdate"],
                "incidentmode" => $values["Incidentmode"],
                "incidentactive" => $values["Incidentactive"],
                "incidentverified" => $values["Incidentverified"],
                "locationid" => $values["Locationid"],
                "locationname" => $values["Locationname"],
                "locationlatitude" => $values["Locationlatitude"],
                "locationlongitude" => $values["Locationlongitude"],
                "categorytitle"     => $values["Category"],
                "categoryid"     => $values["CategoryID"],
                "error"     => $values["Error"],
                "mediaid"     => $values["MediaID"],
                "mediatype"     => $values["MediaType"],
                "medialink"     => $values["MediaLink"],
                "mediathumb"     => $values["MediaThumb"]

            )
   );


}

*/
#  $unique_keys = array("id");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table); #, $table
#}

/*https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals
https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals/edit/
*/

/*view-source:https://scraperwiki.com/editor/raw/318p_4_dept_websites_ho
def ScrapeRaw():
    scraperwiki.sqlite.execute("create table if not exists htmlcache (url text)")
    urlbatch = scraperwiki.sqlite.execute("select xllinks.url, xllinks.sheetname, xllinks.i from xllinks left join htmlcache on htmlcache.url = xllinks.url where htmlcache.url is null limit 20")
    ldata = [ ]
    for url, sheetname, i in urlbatch["data"]:
        page_req=requests.get(url)
        page_raw=page_req.content
        data = {'url':url, 'sheetname':sheetname, 'i':i, 'status':page_req.status_code}
        data['html']=unicode(page_raw, 'iso-8859-1')
        if re.search('charset=utf-8"', page_raw):
            try:
                data['html']=unicode(page_raw, 'utf-8')
            except UnicodeDecodeError, e:
                print "unicode failure", url
        ldata.append(data)
    scraperwiki.sqlite.save(["url"], ldata, "htmlcache")
    return len(ldata)
*/
#php version of this https://scraperwiki.com/scrapers/ratemyplace_food_safety_inspections/
/* ScraperWikiselect("id, date from swdata").each { |i| old[i["id"]] = i["date"]}

    puts scraped.to_yaml

    scraped.flatten.each do |i|
      if old.has_key?(i[:id].to_s) === FALSE
        get_inspection_detail(i)
        puts "Adding new inspection for #{i[:name]}"
      elsif old[i[:id]] != i[:date].to_s
        get_inspection_detail(i)
        puts "Updating inspection for #{i[:name]}"
      end
    end

  end 
*/
/*
old = new();
foreach ($i; ($old[$i["id"]] = $i["id"];) $i++; ) {
scraperwiki::select("$id from swdata"); 
}
#https://scraperwiki.com/scrapers/ratemyplace_food_safety_inspections/


   // puts scraped.to_yaml

    foreach($id; as id;) {
      if ($old((string)$i[$id]) === FALSE) {
       get_extras($i);
}
        print "Adding new inspection for" . $i[$incidenttitle];

#$iid =(string)$i[$id] 
      elseif( $old[$i[$id]] != (string)$i[$id]; ) {

       get_extras($i);
}
        print "Updating inspection for" . $i[$incidenttitle];
    

}
*/
#https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals/edit/
    #$existingRecords = scraperwiki::sqliteexecute("select * from swdata where `council_reference`='" . $record['council_reference'] . "'");
    #if (sizeof($existingRecords) == 0)
    #{
     #   scraperwiki::save(array('council_reference'), $record);
    #}
    #else
    #{
    #    print ("Skipping already saved record " . $record['council_reference'] . "\n");
    #}
  
}

#scraperwiki::sqlitecommit();
#$i = $id;
?>