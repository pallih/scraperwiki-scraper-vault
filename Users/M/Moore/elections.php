<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.ark.ac.uk/elections/");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$array_data_hd = array();
$array_headings = array();

$ar_regex = array(
                'party_header' => '/(<font color="#ffffff" face="Verdana, Arial, Helvetica, sans-serif" size="1">)([\w&;]*)(<\/font>)/',
                'get_year' => '/([\d]{4})/',
                'get_row_name' => '/$([\w\s]*)([(]{1})/'
            );
$b_heading = false;
$yr = -1;
$row_title = '';

foreach($dom->find('tr') as $data)
{
    # Store data in the datastore
    if(count($data->children) > 4){
        foreach($data->children() as $td){
            //print "matching {$td->innertext}" . preg_match($ar_regex['party_header'],$td->innertext) . "\n";
            //print $td->innertext. "\n";
        
            if(preg_match($ar_regex['party_header'],$td->innertext) ==1 ){ //heading with parties
                
                $sttmp = trim($td->plaintext);

                if($sttmp !== ''){
                    $array_headings[$sttmp] = array();
                }
        
            }else if($b_heading){
                if($i_row == 0 && $i_col == 0){
                     $mtch = preg_match_all($ar_regex['get_year'], $td->plaintext, $matches, PREG_SET_ORDER);
                    if($mtch > 0){
                       $yr = $matches[1];
                    }

                }else if($i_col = 0){
                    
                    $mtch = preg_match_all($ar_regex['get_row_name'], $td->plaintext, $matches, PREG_SET_ORDER);
                    if($mtch > 0){
                          $row_title = $matches[0];    
                    }
                }

                  
                    
                $i_col++;
            }
            
        }
            if(count($array_headings)>0 && $b_heading==false){
                $b_heading = true;
                $i_row = 0;
            }else if($b_heading == true && $i_row <2){
                $i_row++;
            }else if($b_heading == true && $i_row == 2){
                $i_row = 0;
                $array_data_hd[$yr] = $array_headings;
                $array_headings = array();
            }
            $i_col=0;
    }
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

var_dump($array_headings);

?>