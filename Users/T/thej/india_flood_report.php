<?php
    
######################################
# Basic PHP scraper
######################################
print "BEGIN"."\n";
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.india-water.com/ffs/Reports/RptCurrent.asp");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
$start = false;
$i=0;
$j=1;
$k=1;
$data_store;
$final_data;
print "STARTING"."\n";
foreach($dom->find('td') as $data)
{
     //print "INSIDE1"."\n";
    if( $start == false && $data->plaintext == '1&nbsp;'){
        print "INSIDE"."\n";
        $start = true;
        //next;
     }
    if ($start == true){

        switch ($j)
        {
            case 1:
                $data_store;
                $data_store['id'] = str_replace("&nbsp;","",$data->plaintext);
                $j = $j+1;
                break;
            case 2:
                $data_store['site'] = str_replace("&nbsp;","",$data->plaintext);
                $re1='.*?';    # Non-greedy match on filler
                $re2='\\d+';    # Uninteresting: int
                $re3='.*?';    # Non-greedy match on filler
                $re4='(\\d+)';    # Integer Number 1
                $re5='(9)';    # Any Single Character 1

              if ($c=preg_match_all ("/".$re1.$re2.$re3.$re4."/is", $data, $matches))
              {
                  $int1=$matches[1][0];
                  //$c1=$matches[2][0];
                  //print "($int1) \n";
                  $data_store['url_id'] =$int1;
              }
                
                
                //scrape that exact page get flood info
                $html1 = scraperwiki::scrape("http://www.india-water.com/ffs/static_info.asp?Id=".$data_store['url_id']);
                 $data_store['url'] ="http://www.india-water.com/ffs/static_info.asp?Id=".$data_store['url_id'];
                $dom1 = new simple_html_dom();
                $dom1->load($html1);
                print $dom1;
                print "dom1";
                foreach($dom1->find('img') as $data1)
                {
                    $re1='.*?';    # Non-greedy match on filler
                    $re2='(?:[a-z][a-z]+)';    # Uninteresting: word
                    $re3='.*?';    # Non-greedy match on filler
                    $re4='(?:[a-z][a-z]+)';    # Uninteresting: word
                    $re5='.*?';    # Non-greedy match on filler
                    $re6='(?:[a-z][a-z]+)';    # Uninteresting: word
                    $re7='.*?';    # Non-greedy match on filler
                    $re8='(?:[a-z][a-z]+)';    # Uninteresting: word
                    $re9='.*?';    # Non-greedy match on filler
                    $re10='((?:[a-z][a-z]+))';    # Word 1

                   if ($c=preg_match_all ("/".$re1.$re2.$re3.$re4.$re5.$re6.$re7.$re8.$re9.$re10."/is", $data1, $matches))
                     {
                      $word1=$matches[1][0];
                      $data_store['flood_level'] = $word1;
                      print "($word1) \n";
                     }
 
                }
                
                
                $j = $j+1;
                break;
            case 3:
                $data_store['state'] = str_replace("&nbsp;","",$data->plaintext);
                $j = $j+1;
                break;
            case 4:
                $data_store['basin'] = str_replace("&nbsp;","",$data->plaintext);
                $j = 1;
                //print print_r($data_store)."\n"; 
               
                scraperwiki::save(array('id'), array('id' => $data_store['id'],'url_id' => $data_store['url_id'],'url' => $data_store['url'],'flood_level' => $data_store['flood_level'],'state' => $data_store['state'],'site' => $data_store['site'],'basin' => $data_store['basin']));
                break;

        }
        if(strpos($data_store['id'],'Inflow')){
            
            break;
        }

        
        
           
    } 
    
}

?>