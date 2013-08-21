<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$arr_urls = array();
$arr_urls['north_belfast'] = 'http://www.ark.ac.uk/elections/anb.htm';
$arr_urls['west_belfast']='http://www.ark.ac.uk/elections/awb.htm';
$arr_urls['south_belfast']='http://www.ark.ac.uk/elections/asb.htm';
$arr_urls['east_belfast']='http://www.ark.ac.uk/elections/aeb.htm';

$arr_results=array();

$current_area ='';

    foreach($arr_urls as $key=>$url){
        
        $html = scraperwiki::scrape($url);
        
        $dom = new simple_html_dom();
        $dom->load($html);

        $current_area = $key;

        $arr_results[$key] = scrape_result($dom);

    }

    foreach($arr_results as $key=>$res){

        foreach($res as $k=>$r){
            #print "\nrecord\n";
            #print_r($r);
            #print "\n";
            
            if($k != 'summary'){

                $r['area'] = $key;
                $r['type'] = 'result';
                scraperwiki::save( array('party','name'), $r ); 

            }else{
                $r['area'] = $key;
                $r['type'] = 'summary';
                scraperwiki::save( array('area','type'), $r ); 
            }
            //scraperwiki::save( array_keys($r),$r );
            //print_r($r);
           
        }

    }

function scrape_result($dom){

    # Use the PHP Simple HTML DOM Parser to extract <td> tags

    
    foreach($dom->find('p[style]') as $data)
    {
        # Store data in the datastore
        
        return disect_p($data);

    }
    
    $st = 'p strong';
    
    if($alt_p = $dom->find($st)){
        #return $alt_p->parent();
        return disect_p($alt_p[0]->parent());
    }

}

    function disect_p($data){

        $tmp = explode('<br>',trim($data->innertext));

        $i_cnt = count($tmp)-1;
        while($tmp[$i_cnt] == ''){
            $i_cnt--;
        }     

        $array_values = array();

        $sum = break_sum($tmp[$i_cnt]);

        for($i=0;$i<$i_cnt;$i++){
            #print "monkey = {$tmp[$i]}";
            if($tmp_can = break_candidate($tmp[$i])){
                $st_key = $tmp_can['name'] . '_' . $tmp_can['party'];
                $array_values[$st_key] = do_stats(array('votes'=>$tmp_can['vals']),$sum);
                $array_values[$st_key]['party'] =  $tmp_can['party'];
                $array_values[$st_key]['name'] =  $tmp_can['name'];
            }
        }

        $array_values['MNV'] = get_novote($sum);

        $array_values['summary'] = $sum;        

        return $array_values;
    }

    function break_sum($stin){
        
         $array_results = explode(';',$stin);

        $array_values = array();

        foreach($array_results as $value){

            $tmp_vals = explode(':',trim($value));
           
            $act_vals = explode(' ',trim($tmp_vals[1]));

            $array_values[$tmp_vals[0]] = str_replace(',','',$act_vals[0]);
            
        }
        return $array_values;
    }

    function break_candidate($details){

        $reg_ex = '/(^([\w\s&;])+)([(]{1}[\w&;\s]*[)]{1})([\s]+[\d,]*[\s])/';

        $arr_rep = array('<strong>','</strong>','@','*');

        $details = trim(str_replace($arr_rep,'',$details));

        print 'details : ' . $details . "\n";

        $mtch = preg_match_all($reg_ex, $details, $matches, PREG_SET_ORDER);
        if($mtch !== false && $mtch>0){
            print "matched : \n";
            print_r($matches);
            print "\n";

            return array( 'name'=>trim($matches[0][1]), 'vals'=>str_replace(',','',trim($matches[0][4])), 'party'=>trim($matches[0][3]) );
        }else{
            print "failed candidate $details\n"  ;
        }
    }

        function do_stats($cand, $summary){
            
            if(isset($cand['votes'])){
                
                $cand['real_perc'] = ($cand['votes']/$summary['Electorate'])*100;
                $cand['norm_perc'] = ($cand['votes']/$summary['Valid Votes'])*100;

                //$cand['no_vote_perc'] = ($cand['votes']/($summary['Electorate']-$summary['Total Poll']))*100;
            
            }
            
            return $cand;
        }

            function get_novote($sum){
                global $current_area;
                $no_vote = $sum['Electorate'] - $sum['Total Poll'];
                    
                $nv = array();
                
                $nv['votes']= $no_vote;
                $nv['real_perc'] = ($nv['votes']/$sum['Electorate'])*100;
                $nv['norm_perc'] = ($nv['votes']/$sum['Valid Votes'])*100;
                $nv['party'] = '(MVN)';
                $nv['name'] = 'Mr. N. Vote _ ' . $current_area;

                return $nv;
                
            }

?>

