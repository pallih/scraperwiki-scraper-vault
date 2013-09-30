<?php

# Blank PHP
print "yo";

#$html = scraperWiki::scrape("http://www.gcis.gov.za/content/resourcecentre/directory/lists/ministers");

require 'scraperwiki/simple_html_dom.php';
function scrape_ministers ($id, $type){

  $html = scraperWiki::scrape("http://apps.gcis.gov.za/gcis/InternetIncludes/gcis_list.jsp?id=$id&amp;heading=$type");

  $dom = new simple_html_dom();
  $dom->load($html);
  foreach($dom->find("tr") as $data){
       $tds = $data->find("td");
       if(count($tds)==2){
           if ($tds[0]->plaintext == "Minister:")
              $minister = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Portfolio:")
              $portfolio = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Tel no:")
              $tel_no = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Fax no:")
              $fax_no = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Mail address:"){
               $record = array(
                 'minister' => $minister,
                 'portfolio' => $portfolio,
                 'tel_no' => $tel_no,
                 'fax_no' => $fax_no,
                 'mail address' => $tds[1]->plaintext);
               scraperwiki::save(array('minister'), $record);
               #print json_encode($record) . "\n";
             }
       }
  }
}

scrape_ministers(1, "Ministers");
scrape_ministers(2, "Deputy%20Ministers");


# a2a_config.linkname='Ministers | Government Communication and Information System (GCIS)'; a2a_config.linkurl='http://www.gcis.gov.za/content/resourcecentre/directory/lists/ministers'; a2a.init('page', {target: '#da2a_1'});

#print $html . "\n"; 

print "bye";
?>
<?php

# Blank PHP
print "yo";

#$html = scraperWiki::scrape("http://www.gcis.gov.za/content/resourcecentre/directory/lists/ministers");

require 'scraperwiki/simple_html_dom.php';
function scrape_ministers ($id, $type){

  $html = scraperWiki::scrape("http://apps.gcis.gov.za/gcis/InternetIncludes/gcis_list.jsp?id=$id&amp;heading=$type");

  $dom = new simple_html_dom();
  $dom->load($html);
  foreach($dom->find("tr") as $data){
       $tds = $data->find("td");
       if(count($tds)==2){
           if ($tds[0]->plaintext == "Minister:")
              $minister = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Portfolio:")
              $portfolio = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Tel no:")
              $tel_no = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Fax no:")
              $fax_no = $tds[1]->plaintext;
           elseif ($tds[0]->plaintext == "Mail address:"){
               $record = array(
                 'minister' => $minister,
                 'portfolio' => $portfolio,
                 'tel_no' => $tel_no,
                 'fax_no' => $fax_no,
                 'mail address' => $tds[1]->plaintext);
               scraperwiki::save(array('minister'), $record);
               #print json_encode($record) . "\n";
             }
       }
  }
}

scrape_ministers(1, "Ministers");
scrape_ministers(2, "Deputy%20Ministers");


# a2a_config.linkname='Ministers | Government Communication and Information System (GCIS)'; a2a_config.linkurl='http://www.gcis.gov.za/content/resourcecentre/directory/lists/ministers'; a2a.init('page', {target: '#da2a_1'});

#print $html . "\n"; 

print "bye";
?>
