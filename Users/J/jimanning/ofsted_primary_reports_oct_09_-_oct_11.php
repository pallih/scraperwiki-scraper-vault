<?php
//gets ofsetd primary school reports Oct 09 - Oct 11

require 'scraperwiki/simple_html_dom.php';           
//scraperwiki::save_sqlite(array("a"),array("a"=>1, "bbb"=>"Hi there"));

$base_url = "http://www.ofsted.gov.uk";
$search_url = "/inspection-reports/find-inspection-report/results/type/21/range/1254351600/1317509999";

$page = 0;

//do the search

while ($page <= 1236){
    
    $raw = scraperwiki::scrape($base_url.$search_url.'&page='.$page);
    $results = str_get_html($raw);
    
    //run through the results getting the link for each school
    foreach ($results->find('ul.resultsList a') as $school_link){

        $school_url = $school_link->href;
        
        //print "school url: ".$school_url."\n";

        //go get the school page
        $raw_school = scraperwiki::scrape($base_url.$school_url);
        $school = str_get_html($raw_school);
        
        $school_name = $school->find('div#content h1', 0)->innertext ;
        $school_urn = $school->find('div#content strong', 0)->innertext;
        //$school_address = $school->find('div#content p', 1)->innertext;
        
        $report_link = $school->find('table span.html', 0)->parent()->href;

        print 'name: '.$school_name.' urn:'.$school_urn."\n";
       // print 'address: '.$school_address."\n";
       // print 'report link: '.$report_link."\n";

        //go get the actual report

        $raw_report = scraperwiki::scrape($base_url.$report_link);
        $report = str_get_html($raw_report);

        $report_meta = new table();
        foreach ($report->find('table') as $table){
            $report_meta->add_table($table);
        }

        
        //print_r ($report_meta->findAll());
        
      /*  $report_array = $report_meta->findAll();
        $report_array['name'] = $school_name;
        $report_array['address'] = $school_address;
        $report_array['schoolurl'] = $school_url;
        $report_array['reporturl'] = $report_link;
        $report_array['urn'] = $school_urn;
       */ 
        $temp = array(
            'urn'=> $school_urn,
            'reporturl'=>$report_link,
            'inspector'=>$report_meta->find('reporting inspector')
        );
        
        scraperwiki::save_sqlite(array("urn"), $temp);
        print "----------------\n";


    }

    $page++;
}


class table{
    //something to parse through any tables in the report (which _obviously_ are layed out in a squillion different ways)
    private $table_array = array();

    function get_inner_text($object){
       // print "object: ".$object."\n";
        if (is_object($object)){
            if ($object->first_child()){
                return $this->get_inner_text($object->first_child());
            }else{
                //print "returning: ".$object->innertext."\n";
                return $object->innertext;
                
            }
            
        }else{
            return $object;
        }
    }

    function add_table($table){
        //append a table to our table array
         $td = ($table->find('th', 0))?0:1; //deal with the different types of table
         foreach ($table->find('tr') as $row){
            $info_found = false;
            if ($td == 0){
                    //print $row;
                if ($row->find('th', 0) and $row->find('td', 0)){
                    $param = strtolower($this->get_inner_text($row->find('th',0)));
                    $value = $this->get_inner_text($row->find('td', 0));
                    $info_found = true;
                 }  
            }else{
                  //print $row;
                if ($row->find('td', 0) and $row->find('td', 1)){
                    $param = strtolower($this->get_inner_text($row->find('td',0)));
                    $value = $this->get_inner_text($row->find('td', 1));
                    $info_found = true;
                }
                
            }

            if ($info_found){
                 $this->table_array[$param] = $value;
            }

         }

    }

    function find($term){
        $term = strtolower($term);
        if (isset($this->table_array[$term])){
            return $this->table_array[$term];
        }else{
            return '';
        }
    }

    function findAll(){
        return $this->table_array;
    }


}

?>