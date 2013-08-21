<?php
require 'scraperwiki/simple_html_dom.php';           


//
//Converts a string to Title Case based on one set of title case rules
// put <no_parse></no_parse> around content that you don't want to be parsed by the title case rules
//
function titleCase($string)  {
     //remove no_parse content
     $string_array = preg_split("/(<no_parse>|<\/no_parse>)+/i",$string);
     $newString = "";
     for ($k=0; $k<count($string_array); $k=$k+2){
     $string = $string_array[$k];
     //if the entire string is upper case dont perform any title case on it
     if ($string != strtoupper($string)){
 //TITLE CASE RULES:
 //1.) uppercase the first char in every word
         $new = preg_replace("/(^|\s|\'|'|\"|-){1}([a-z]){1}/ie","''.stripslashes('\\1').''.stripslashes(strtoupper('\\2')).''", $string);
         //2.) lower case words exempt from title case
         // Lowercase all articles, coordinate conjunctions ("and", "or", "nor"), and prepositions regardless of length, when they are other than the first or last word.
 // Lowercase the "to" in an infinitive." - this rule is of course aproximated since it is contex sensitive
         $matches = array();
         // perform recusive matching on the following words
         preg_match_all("/(\sof|\sa|\san|\sthe|\sbut|\sor|\snot|\syet|\sat|\son|\sin|\sover|\sabove|\sunder|\sbelow|\sbehind|\snext\sto|\sbeside|\sby|\samoung|\sbetween|\sby|\still|\ssince|\sdurring|\sfor|\sthroughout|\sto|\sand){2}/i",$new ,$matches);
 for ($i=0; $i<count($matches); $i++){
 for ($j=0; $j<count($matches[$i]); $j++){
 $new = preg_replace("/(".$matches[$i][$j]."\s)/ise","''.strtolower('\\1').''",$new);
 }
 }
 //3.) do not allow upper case appostraphies
 $new = preg_replace("/(\w'S)/ie","''.strtolower('\\1').''",$new);
 $new = preg_replace("/(\w'\w)/ie","''.strtolower('\\1').''",$new);
 $new = preg_replace("/(\W)(of|a|an|the|but|or|not|yet|at|on|in|over|above|under|below|behind|next to| beside|by|amoung|between|by|till|since|durring|for|throughout|to|and)(\W)/ise","'\\1'.strtolower('\\2').'\\3'",$new);
 //4.) capitalize first letter in the string always
         $new = preg_replace("/(^[a-z]){1}/ie","''.strtoupper('\\1').''", $new);
         //5.) replace special cases
 // you will add to this as you find case specific problems
         $new = preg_replace("/\sin-/i"," In-",$new);
         $new = preg_replace("/(\s|\"|\'){1}(ph){1}(\s|,|\.|\"|\'|:|!|\?|\*|$){1}/ie","'\\1pH\\3'",$new);
         $new = preg_replace("/^ph(\s|$)/i","pH ",$new);
         $new = preg_replace("/(\s)ph($)/i"," pH",$new);
         $new = preg_replace("/(\s|\"|\'){1}(&){1}(\s|,|\.|\"|\'|:|!|\?|\*){1}/ie","'\\1and\\3'",$new);
         $new = preg_replace("/(\s|\"|\'){1}(groundwater){1}(\s|,|\.|\"|\'|:|!|\?|\*){1}/e","'\\1Ground Water\\3'",$new);
         $new = preg_replace("/(\W|^){1}(cross){1}(\s){1}(connection){1}(\W|$){1}/ie","'\\1\\2-\\4\\5'",$new); //always hyphonate cross-connections
         $new = preg_replace("/(\s|\"|\'){1}(vs\.){1}(\s|,|\.|\"|\'|:|!|\?|\*){1}/ie","'\\1Vs.\\3'",$new);
         $new = preg_replace("/(\s|\"|\'){1}(on-off){1}(\s|,|\.|\"|\'|:|!|\?|\*){1}/ie","'\\1On-Off\\3'",$new);
         $new = preg_replace("/(\s|\"|\'){1}(on-site){1}(\s|,|\.|\"|\'|:|!|\?|\*){1}/ie","'\\1On-Site\\3'",$new);
         // special cases like Class A Fires
         $new = preg_replace("/(\s|\"|\'){1}(class\s){1}(\w){1}(\s|,|\.|\"|\'|:|!|\?|\*|$){1}/ie","'\\1\\2'.strtoupper('\\3').'\\4'",$new);
         $new = stripslashes($new);
         $string_array[$k] = $new;
         } 
        }
        for ($k=0; $k<count($string_array); $k++){
         $newString .= $string_array[$k];
        }
        return($newString); 
}

/* Start */

/* retrieve last scraped source number from datasource, initialize latest source */
$lastSource = scraperwiki::get_var('last_source');
$latestSource = $lastSource;

/* date range of scraped sources */
$firstYear = 2006;
$thisYear = strftime("%Y");

for ($year = $firstYear; $year <= $thisYear; $year++ ) { 

/* scrape the page for each year to find the links to the text versions of the Registrar's Periodical */
   $url = "http://www.qp.alberta.ca/alberta_gazette.cfm?page=gazette_" . $year . "_registrar.cfm";
   $html = scraperWiki::scrape($url);
   $dom = new simple_html_dom();
   $dom->load($html);
   
   foreach ($dom->find("tr td[valign='BOTTOM'] a") as $el) {

       $link = $el->href;
       $sourceYear = substr($link,18,4);
       $sourceEdition = substr($link,28,2);
       $sourceNumber = $sourceYear . $sourceEdition + 0;

/* check if the source is the latest source scraped */          
           if ($sourceNumber > $latestSource) {
              $latestSource = $sourceNumber;
           }

/* check if source is newer than last source scraped to the datasource */
       if ($sourceNumber > $lastSource) {

           $source = "http://www.qp.alberta.ca/". $link;

          $data = scraperWiki::scrape($source);
          $lines = explode("\n", $data);

          foreach ($lines as $row) {

# find newly registered societies    
          if (preg_match("/(.*) Alberta Society Incorporated (\d+)\s([A-Z]{3})\s(\d+)\sRegistered Address:\s(.*), (.*) ALBERTA, ([A-Z][0-9][A-Z]\s[0-9][A-Z][0-9])\. No: (\d+)\.\r/",$row,$matches)) {
          $incYear = $matches[2];
          $incMonth = $matches[3];
          $incDay = $matches[4];
          $incorporationDate = $incYear . "-" . $incMonth . "-" . $incDay;
          $record = array (
              'Corporate Number' => $matches[8],
              'Organization Name' => titleCase(strtolower($matches[1])),
              'Incorporation Year' => $incYear,
              'Incorporation Date' => date_create($incorporationDate),
              'Address' => $matches[5],
              'City' => titleCase(strtolower($matches[6])),
              'Province' => "Alberta",
              'Postal Code' => $matches[7],
              'Activity' => "Incorporated",
              'Source' => $source
          );
          scraperwiki::save(array('Corporate Number','Source'), $record);
       }
    
# find revived societies

       elseif (preg_match("/(.*) Alberta Society Incorporated (\d+)\s([A-Z]{3})\s(\d+)\. Struck-Off The Alberta Register (\d+)\s([A-Z]{3})\s(\d+)\. Revived (\d+)\s([A-Z]{3})\s(\d+)\. No: (\d+)\.\r/",$row,$matches)) {
          $incYear = $matches[2];
          $incMonth = $matches[3];
          $incDay = $matches[4];
          $struckYear = $matches[5];
          $struckMonth = $matches[6];
          $struckDay = $matches[7];
          $revivedYear = $matches[8];
          $revivedMonth = $matches[9];
          $revivedDay = $matches[10];
          $incorporationDate = $incYear . "-" . $incMonth . "-" . $incDay;
          $struckDate = $struckYear . "-" . $struckMonth . "-" . $struckDay;
          $revivedDate = $revivedYear . "-" . $revivedMonth . "-" . $revivedDay;
          $record = array (
              'Corporate Number' => $matches[11],
              'Organization Name' => titleCase(strtolower($matches[1])),
              'Incorporation Year' => $incYear,
              'Incorporation Date' => date_create($incorporationDate),
              'Struck Date' => date_create($struckDate),
              'Revived Date' => date_create($revivedDate),
              'Activity' => "Revived",
              'Source' => $source
          );
          scraperwiki::save(array('Corporate Number','Source'), $record);
       }

#find name changes

       elseif (preg_match("/(.*) Alberta Society Incorporated (\d+)\s([A-Z]{3})\s(\d+)\. New Name: (.*) Effective Date: (\d+)\s([A-Z]{3})\s(\d+)\. No: (\d+)\.\r/",$row,$matches)) {
          $incYear = $matches[2];
          $incMonth = $matches[3];
          $incDay = $matches[4];
          $effectiveYear = $matches[6];
          $effectiveMonth = $matches[7];
          $effectiveDay = $matches[8];
          $incorporationDate = $incYear . "-" . $incMonth . "-" . $incDay;
          $effectiveDate = $effectiveYear . "-" . $effectiveMonth . "-" . $effectiveDay;
          $record = array (
              'Corporate Number' => $matches[9],
              'Organization Name' => titleCase(strtolower($matches[5])),
              'Old Name' => titleCase(strtolower($matches[1])),
              'Incorporation Year' => $incYear,
              'Incorporation Date' => date_create($incorporationDate),
              'Effective Date' => date_create($effectiveDate),
              'Activity' => "Name Change",
              'Source' => $source
          );
          scraperwiki::save(array('Corporate Number','Source'), $record);
       }
     }

   }

 }

}
/* set source number of latest source scraped */
scraperwiki::save_var('last_source', $latestSource); 
?>