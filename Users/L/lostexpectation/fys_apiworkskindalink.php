<?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();
$iditen = 0;



$idiarray = scraperwiki::select('id FROM reports ORDER by id DESC LIMIT 1');
print_r($idiarray);
$idi = $idiarray[0]['id'];
#print_r($idi);
#$idi = $idi[1][0];
#$idi = 0;
print "idi" . $idi;
$idistart = $idi + 1;

#https://scraperwiki.com/scrapers/singleton_council_development_applications/edit/
#for ($i = $idi; $iditen < 10; $i++ ) {  
#for ($i = 4730; $i <= 4733; $i++ ) {   
#  $existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");
 #
#if  ($existingreports != $report['id'])
   # if (sizeof($existingreports) != sizeof($report))
 #   {

#        reportupdate($id);
 #   }
 #   else
 #   {
 #      print ("Skipping already saved record " . $report['id'] . "\n");
 #   }
#}

#function reportupdate($id) {

#updating only new, easier by id number or by date?

#break;
 
#updating only new, easier by id number or by date?
for ($i = $idistart; $iditen < 30; $i++ ) {  
#for ($i = 4730; $i <= 4733; $i++ ) {   



    $data = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
      #   $data = serialize(json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i)));
  $dataprev = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
        print "\n" . "i" . $i;
$prev = $i - 1;
if(( $data['error']['message'] == "No data. There are no results to show." ) && ( $dataprev['error']['message'] == "No data. There are no results to show." ) ) { $iditen++; }
   print "\n" . "prev" . $prev;
    
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
$reporturl = "http://www.fixyourstreet.ie/reports/view/" . $id;
print $reporturl;
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
               
                    $categoryid = ltrim($categoryid, "; ");
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
                    "MediaThumb"   => $mediathumb,
                    "ReportURL"   => $reporturl

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
                 $reporturl = "";

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
                    "MediaThumb"   => $mediathumb,
                    "ReportURL"   => $reporturl
             
            );
       }
}
print "\n" . "end" . "\n" ;

}
#}
#https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals/edit/
#print_r($reports);
#if (isset($reports)){ 
#print "id" . $reports['id'];
#$existingreports = array();
#$existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $reports['id'] . "'");
#print_r($existingreports);
#    if (sizeof($existingreports) == 0)
#    {

#scraperwiki::sqliteexecute("drop table reports");
#scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string, 'reporturl' string)");


foreach ($reports as $id => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb, :reporturl)", #, :image, :address)", 
          
# $reports[] = 
array(  
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
                "mediathumb"     => $values["MediaThumb"],
                "reporturl"     => $values["ReportURL"]

            )

  );


}


#  $unique_keys = array("id");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table); #, $table
#}
#}
 #   else
 #  {
#       print ("Skipping already saved record " . $reports['id'] . "\n");
#   }
#Scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");


#if ScraperWiki::sqliteexecute("delete from reports where `title`='No data'");

ScraperWiki::sqliteexecute("delete from reports where `title`='No data'");
print "done";
scraperwiki::sqlitecommit();
#}

?><?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();
$iditen = 0;



$idiarray = scraperwiki::select('id FROM reports ORDER by id DESC LIMIT 1');
print_r($idiarray);
$idi = $idiarray[0]['id'];
#print_r($idi);
#$idi = $idi[1][0];
#$idi = 0;
print "idi" . $idi;
$idistart = $idi + 1;

#https://scraperwiki.com/scrapers/singleton_council_development_applications/edit/
#for ($i = $idi; $iditen < 10; $i++ ) {  
#for ($i = 4730; $i <= 4733; $i++ ) {   
#  $existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");
 #
#if  ($existingreports != $report['id'])
   # if (sizeof($existingreports) != sizeof($report))
 #   {

#        reportupdate($id);
 #   }
 #   else
 #   {
 #      print ("Skipping already saved record " . $report['id'] . "\n");
 #   }
#}

#function reportupdate($id) {

#updating only new, easier by id number or by date?

#break;
 
#updating only new, easier by id number or by date?
for ($i = $idistart; $iditen < 30; $i++ ) {  
#for ($i = 4730; $i <= 4733; $i++ ) {   



    $data = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
      #   $data = serialize(json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i)));
  $dataprev = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
        print "\n" . "i" . $i;
$prev = $i - 1;
if(( $data['error']['message'] == "No data. There are no results to show." ) && ( $dataprev['error']['message'] == "No data. There are no results to show." ) ) { $iditen++; }
   print "\n" . "prev" . $prev;
    
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
$reporturl = "http://www.fixyourstreet.ie/reports/view/" . $id;
print $reporturl;
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
               
                    $categoryid = ltrim($categoryid, "; ");
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
                    "MediaThumb"   => $mediathumb,
                    "ReportURL"   => $reporturl

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
                 $reporturl = "";

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
                    "MediaThumb"   => $mediathumb,
                    "ReportURL"   => $reporturl
             
            );
       }
}
print "\n" . "end" . "\n" ;

}
#}
#https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals/edit/
#print_r($reports);
#if (isset($reports)){ 
#print "id" . $reports['id'];
#$existingreports = array();
#$existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $reports['id'] . "'");
#print_r($existingreports);
#    if (sizeof($existingreports) == 0)
#    {

#scraperwiki::sqliteexecute("drop table reports");
#scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string, 'reporturl' string)");


foreach ($reports as $id => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb, :reporturl)", #, :image, :address)", 
          
# $reports[] = 
array(  
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
                "mediathumb"     => $values["MediaThumb"],
                "reporturl"     => $values["ReportURL"]

            )

  );


}


#  $unique_keys = array("id");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table); #, $table
#}
#}
 #   else
 #  {
#       print ("Skipping already saved record " . $reports['id'] . "\n");
#   }
#Scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");


#if ScraperWiki::sqliteexecute("delete from reports where `title`='No data'");

ScraperWiki::sqliteexecute("delete from reports where `title`='No data'");
print "done";
scraperwiki::sqlitecommit();
#}

?><?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();
$iditen = 0;



$idiarray = scraperwiki::select('id FROM reports ORDER by id DESC LIMIT 1');
print_r($idiarray);
$idi = $idiarray[0]['id'];
#print_r($idi);
#$idi = $idi[1][0];
#$idi = 0;
print "idi" . $idi;
$idistart = $idi + 1;

#https://scraperwiki.com/scrapers/singleton_council_development_applications/edit/
#for ($i = $idi; $iditen < 10; $i++ ) {  
#for ($i = 4730; $i <= 4733; $i++ ) {   
#  $existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");
 #
#if  ($existingreports != $report['id'])
   # if (sizeof($existingreports) != sizeof($report))
 #   {

#        reportupdate($id);
 #   }
 #   else
 #   {
 #      print ("Skipping already saved record " . $report['id'] . "\n");
 #   }
#}

#function reportupdate($id) {

#updating only new, easier by id number or by date?

#break;
 
#updating only new, easier by id number or by date?
for ($i = $idistart; $iditen < 30; $i++ ) {  
#for ($i = 4730; $i <= 4733; $i++ ) {   



    $data = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
      #   $data = serialize(json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i)));
  $dataprev = json_decode(file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i), true);
        print "\n" . "i" . $i;
$prev = $i - 1;
if(( $data['error']['message'] == "No data. There are no results to show." ) && ( $dataprev['error']['message'] == "No data. There are no results to show." ) ) { $iditen++; }
   print "\n" . "prev" . $prev;
    
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
$reporturl = "http://www.fixyourstreet.ie/reports/view/" . $id;
print $reporturl;
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
               
                    $categoryid = ltrim($categoryid, "; ");
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
                    "MediaThumb"   => $mediathumb,
                    "ReportURL"   => $reporturl

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
                 $reporturl = "";

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
                    "MediaThumb"   => $mediathumb,
                    "ReportURL"   => $reporturl
             
            );
       }
}
print "\n" . "end" . "\n" ;

}
#}
#https://scraperwiki.com/scrapers/campbelltown_city_council_development_proposals/edit/
#print_r($reports);
#if (isset($reports)){ 
#print "id" . $reports['id'];
#$existingreports = array();
#$existingreports = scraperwiki::sqliteexecute("select * from reports where `id`='" . $reports['id'] . "'");
#print_r($existingreports);
#    if (sizeof($existingreports) == 0)
#    {

#scraperwiki::sqliteexecute("drop table reports");
#scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string, 'reporturl' string)");


foreach ($reports as $id => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb, :reporturl)", #, :image, :address)", 
          
# $reports[] = 
array(  
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
                "mediathumb"     => $values["MediaThumb"],
                "reporturl"     => $values["ReportURL"]

            )

  );


}


#  $unique_keys = array("id");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table); #, $table
#}
#}
 #   else
 #  {
#       print ("Skipping already saved record " . $reports['id'] . "\n");
#   }
#Scraperwiki::sqliteexecute("select * from reports where `id`='" . $report['id'] . "'");


#if ScraperWiki::sqliteexecute("delete from reports where `title`='No data'");

ScraperWiki::sqliteexecute("delete from reports where `title`='No data'");
print "done";
scraperwiki::sqlitecommit();
#}

?>