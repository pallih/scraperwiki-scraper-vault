<?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();

#updating only new, easier by id number or by date?

for ($i = 160; $i <= 185; $i++ ) {   
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

}


#print_r($reports);


#scraperwiki::sqliteexecute("drop table reports");
scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string)");

foreach ($reports as $id => $values) {
#foreach ($reports as $key => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb)", #, :image, :address)", 
          #https://scraperwiki.com/scrapers/ie_planningalerts_corkcitytype/edit/
 $reports[] = 
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
                "mediathumb"     => $values["MediaThumb"]

            )

  );


#}
}

#  $unique_keys = array("id","title");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table);
#}

scraperwiki::sqlitecommit();
#}
?><?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();

#updating only new, easier by id number or by date?

for ($i = 160; $i <= 185; $i++ ) {   
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

}


#print_r($reports);


#scraperwiki::sqliteexecute("drop table reports");
scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string)");

foreach ($reports as $id => $values) {
#foreach ($reports as $key => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb)", #, :image, :address)", 
          #https://scraperwiki.com/scrapers/ie_planningalerts_corkcitytype/edit/
 $reports[] = 
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
                "mediathumb"     => $values["MediaThumb"]

            )

  );


#}
}

#  $unique_keys = array("id","title");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table);
#}

scraperwiki::sqlitecommit();
#}
?><?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();

#updating only new, easier by id number or by date?

for ($i = 160; $i <= 185; $i++ ) {   
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

}


#print_r($reports);


#scraperwiki::sqliteexecute("drop table reports");
scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string)");

foreach ($reports as $id => $values) {
#foreach ($reports as $key => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb)", #, :image, :address)", 
          #https://scraperwiki.com/scrapers/ie_planningalerts_corkcitytype/edit/
 $reports[] = 
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
                "mediathumb"     => $values["MediaThumb"]

            )

  );


#}
}

#  $unique_keys = array("id","title");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table);
#}

scraperwiki::sqlitecommit();
#}
?><?php
#Add API to retrieve incident with comments
#https://github.com/ushahidi/Ushahidi_Web/pull/142

$data = array();
$reports = array();

#updating only new, easier by id number or by date?

for ($i = 160; $i <= 185; $i++ ) {   
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

}


#print_r($reports);


#scraperwiki::sqliteexecute("drop table reports");
scraperwiki::sqliteexecute("create table if not exists reports ('id' string, 'title' string, 'incidentdescription' string, 'incidentdate' string, 'incidentmode' string, 'incidentactive' string, 'incidentverified' string, 'locationid' string, 'locationname' string, 'locationlatitude' string, 'locationlongitude' string, 'categorytitle' string, 'categoryid' string, 'error' string, 'mediaid' string, 'mediatype' string, 'medialink' string, 'mediathumb' string)");

foreach ($reports as $id => $values) {
#foreach ($reports as $key => $values) {
   scraperwiki::sqliteexecute("insert or replace into reports values (:id, :title, :incidentdescription, :incidentdate, :incidentmode, :incidentactive, :incidentverified, :locationid, :locationname, :locationlatitude, :locationlongitude, :categorytitle, :categoryid, :error, :mediaid, :mediatype, :medialink, :mediathumb)", #, :image, :address)", 
          #https://scraperwiki.com/scrapers/ie_planningalerts_corkcitytype/edit/
 $reports[] = 
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
                "mediathumb"     => $values["MediaThumb"]

            )

  );


#}
}

#  $unique_keys = array("id","title");
#$table = "reports";

#if (isset($reports)){ 
#scraperwiki::save_sqlite($unique_keys, $reports, $table);
#}

scraperwiki::sqlitecommit();
#}
?>