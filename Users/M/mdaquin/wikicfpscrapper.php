<?php

require 'scraperwiki/simple_html_dom.php';           

function extractCatCFPList($cat, $catlink){
   for ($i = 1; $i<=20; $i++){
         if (extractCatCFPList2($cat, $catlink."&page=".$i)===false) {break;};
   }
}

function extractCatCFPList2($cat, $catlink){
   print($cat." -- ".str_replace(" ", "%20", $catlink)."\n");

   $html = scraperWiki::scrape("http://www.wikicfp.com/".str_replace(" ", "%20", $catlink));           

   $dom = new simple_html_dom();
   $dom->load($html);

   $tabletrs = $dom->find("table tr");

   $cfps = array();
   foreach ($tabletrs as $tabletr){
      $tds = $tabletr->find("td");
      if (isset($tds[0]->children[0]->tag) && strcmp($tds[0]->children[0]->tag, "a")===0){
         // print("   ".$tds[0]->children[0]->plaintext." --> ".$tds[0]->children[0]->attr['href']."\n");
         if (strcmp("About Us", $tds[0]->children[0]->plaintext)!==0 && strcmp("Creative Commons Attribution-Share Alike 3.0 License", $tds[0]->children[0]->plaintext)!==0 &&
               strcmp("first", $tds[0]->children[0]->plaintext)!==0 ) {
               $cfps[$tds[0]->children[0]->plaintext] = $tds[0]->children[0]->attr['href'];
         }
      }
   }

  if (count($cfps) === 0) {
     return false;
  }
  foreach ($cfps as $name => $link){
    extractCFP($cat, $name, $link);
  }
  $dom->__destruct();
  return true;
 }

function extractCFP($cat, $name, $link){
  print("   ".$name." -- ".$link."\n");
  if (alreadyKnown($cat, $name, $link)){
     return false;
  }
  $html = scraperWiki::scrape("http://www.wikicfp.com/".str_replace(" ", "%20", $link));           
  $dom = new simple_html_dom();
  $dom->load($html);

  $spans = $dom->find("span");

  $type = "";
  $title = "";
  $link = "";
  $id = "";
  $description = "";
  $locality = "";

  $summaries = array();
  $startdates = array();
  $enddates = array();

  $sdate = "";
  $edate = "";
  
  $deadline = "";
  $notification = "";
  $finalversion = "";

  foreach ($spans as $span){   
    // print_r($span);
    if (isset($span->attr['property'])){
     //   print("      ".$span->attr['property']."=".$span->attr['content']."\n");
        if (strcmp($span->attr['property'], "v:eventType")===0){
                $type=$span->attr['content'];
                print("      type = ".$type."\n");
        }
        if (strcmp($span->attr['property'], "dc:title")===0){
                $title=$span->attr['content'];
                print("      title = ".$title."\n");
        }
        if (strcmp($span->attr['property'], "dc:source")===0){
                $link=$span->attr['content'];
                print("      link = ".$link."\n");
        }
        if (strcmp($span->attr['property'], "dc:identifier")===0){
                $id=$span->attr['content'];
                print("      id = ".$id."\n");
        }
        if (strcmp($span->attr['property'], "dc:description")===0){
                $description=$span->attr['content'];
                print("      description = ".$description."\n");
        }
        if (strcmp($span->attr['property'], "v:locality")===0){
                $locality=$span->attr['content'];
                print("      locality = ".$locality."\n");
        }    
        if (strcmp($span->attr['property'], "v:summary")===0){
                $summaries[]=$span->attr['content'];
        }
        if (strcmp($span->attr['property'], "v:startDate")===0){
                $startdates[]=$span->attr['content'];
        }    
        if (strcmp($span->attr['property'], "v:endDate")===0){
                $enddates[]=$span->attr['content'];
        }    
    }
    $dom->__destruct();
  }
 
  foreach ($summaries as $ind=>$summary){
     if (strcmp($summary, $name) === 0){
        $sdate = $startdates[$ind];
        $edate = $enddates[$ind];  
        print("       between ".$sdate." and ".$edate."\n");
     }
     if (strcmp($summary, "Submission Deadline") === 0){
        $deadline = $startdates[$ind];
        print("       deadline = ".$deadline."\n");
     }
     if (strcmp($summary, "Notification Due") === 0){
        $notification = $startdates[$ind];
        print("       notification = ".$notification."\n");
     }
     if (strcmp($summary, "Final Version Due") === 0){
        $finalversion = $startdates[$ind];
        print("       finalversion = ".$finalversion."\n");
     }
  } 

  $record = array(
      'id' => $id, 
      'category' => $cat,
      'type' => $type,
      'title' => $title,
      'link' => $link,
      'location' => $locality,
      'description' => $description,
      'startdate' => $sdate,
      'enddate' => $edate,
      'deadline' => $deadline,
      'notification' => $notification,
      'finalversion' => $finalversion    
  );

  scraperwiki::save(array('ID', 'category'), $record);
  sleep(5);
  return true;
}

function alreadyKnown($cat, $name, $link){
  $data = scraperwiki::sqliteexecute(           
      "select distinct id from swdata where title='".str_replace("'", "", $name)."' and category='".$cat."'");
  if (count($data->data) === 0) return false;
  echo "already known : ".$name." in ".$cat."\n";
  return true;
}


// get the list of categories and links
$html = scraperWiki::scrape("http://www.wikicfp.com/cfp/allcat");           

$dom = new simple_html_dom();
$dom->load($html);

$tabletrs = $dom->find("table tr");

  // only getting the first column... need more...


$categories = array();
foreach ($tabletrs as $tabletr){
   $tds = $tabletr->find("td");
   if (isset($tds[0]->children[0]->tag) && strcmp($tds[0]->children[0]->tag, "a")===0){
      // print($tds[0]->children[0]->plaintext." --> ".$tds[0]->children[0]->attr['href']."\n");
      if (strcmp("About Us", $tds[0]->children[0]->plaintext)!==0 && strcmp("Creative Commons Attribution-Share Alike 3.0 License", $tds[0]->children[0]->plaintext)!==0) {
        $categories[$tds[0]->children[0]->plaintext] = $tds[0]->children[0]->attr['href'];
      }
   }
   if (isset($tds[2]->children[0]->tag) && strcmp($tds[2]->children[0]->tag, "a")===0){
     // print($tds[2]->children[0]->plaintext." --> ".$tds[2]->children[0]->attr['href']."\n");
      if (strcmp("About Us", $tds[2]->children[0]->plaintext)!==0 && strcmp("Creative Commons Attribution-Share Alike 3.0 License", $tds[2]->children[0]->plaintext)!==0) {
        $categories[$tds[2]->children[0]->plaintext] = $tds[2]->children[0]->attr['href'];
      }
   }
   if (isset($tds[4]->children[0]->tag) && strcmp($tds[4]->children[0]->tag, "a")===0){
      // print($tds[4]->children[0]->plaintext." --> ".$tds[4]->children[0]->attr['href']."\n");
      if (strcmp("About Us", $tds[4]->children[0]->plaintext)!==0 && strcmp("Creative Commons Attribution-Share Alike 3.0 License", $tds[4]->children[0]->plaintext)!==0) {
        $categories[$tds[4]->children[0]->plaintext] = $tds[4]->children[0]->attr['href'];
      }
   }
}

// otherwise, get stuck at artificial intelligence
$categories = array_reverse($categories);
$s = rand(1,350);
$r = rand(1,10);
$ind = 1;
print ("I will only try to update every ".$r." categories starting from ".$s."\n");
foreach ($categories as $cat => $catlink){ 
   if ($ind >= $s && $ind % $r === 0) {
       extractCatCFPList($cat, $catlink); 
   }
   $ind++;
}
// if we reach the end, we re-start at the beginning of the list
foreach ($categories as $cat => $catlink){ 
   if ($ind % $r === 0) {
       extractCatCFPList($cat, $catlink); 
   }
   $ind++;
}

?>
