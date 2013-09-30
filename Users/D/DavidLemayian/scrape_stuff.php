<?php
    $time_start = microtime(true);

    set_time_limit(0);
    ini_set('memory_limit', '-1');
    
    $outh_token = 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ';
    $list_id = '50bebb85e4b098cd643a8b43';
    $cat_id = '4cae28ecbf23941eb1190695';
    
    $url = 'https://api.foursquare.com/v2/venues/add';
    $url2 = 'https://api.foursquare.com/v2/lists/'.$list_id.'/additem';
    
    function http_post ($url, $data)
{
    $data_url = http_build_query ($data);
    $data_len = strlen ($data_url);

    return array ('content'=>file_get_contents ($url, false, stream_context_create (array ('http'=>array ('method'=>'POST'
            , 'header'=>"Connection: close\r\nContent-Length: $data_len\r\n"
            , 'content'=>$data_url
            ))))
        , 'headers'=>$http_response_header
        );
}
    
    $row = 1;
    if (($handle = fopen("http://davidlemayian.github.com/fs/uasin-gishu.csv", "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            
            if ($row == 1){
                //Skip
            } else { 
                if ($row > 0 && $row < 250){
                $lon = $data[1];
                if($lon==0){
                    //No geo location.
                } else {
                    $reg_county = addslashes(ucwords(strtolower($data[2])));
                    $reg_const = addslashes(ucwords(strtolower($data[4])));
                    $reg_ward = addslashes(ucwords(strtolower($data[5])));
                    $reg_name1 = addslashes(ucwords(strtolower($data[0])));
                    $reg_name = "IEBC Registration Centre - ".$reg_name1;
                    $reg_desc = "IEBC Registration Centre - ".$reg_name1.". County: ".$reg_county.", Constitutency: ".$reg_const.", Ward: ".$reg_ward.". Brought to you by Nimeregister! http://nimeregister.com";
                    $reg_ll = $data[3].",".$data[1];
                    
                    $data1 = array('name' => $reg_name, 'primaryCategoryId' => $cat_id, 'description' => $reg_desc, 'll' => $reg_ll, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                    $options = array('http' => array('method'  => 'POST','content' => http_build_query($data1)));
                    $context  = stream_context_create($options);

                    //$result = file_get_contents($url, false, $context);
                    $result = http_post ($url, $data1);
                    
                    echo $row." - ";
                    //if ($row == 499){
                        var_dump($result);
                    //}
                    
                    if ($result['content'] == 'bool(false)'){
                        //Nothing to add to list.
                    } else {
                        $obj = json_decode($result['content']);
                        //echo '<br/><br/>';
                        //Add to list
                        $data2 = array('venueId' => $obj->{'response'}->{'venue'}->{'id'}, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                        $options = array('http' => array('method'  => 'POST','content' => http_build_query($data2)));
                        $context  = stream_context_create($options);

                        //$result = file_get_contents($url2, false, $context);
                        $result = http_post ($url, $data2);
                        var_dump($result);
                    }
                    
                }
                }
            }
            
            $row++;
        }
        fclose($handle);
    }
    
    echo "<br/><br/>Rows: ".$row;
    $time_end = microtime(true);
    $time = $time_end -$time_start;

    echo "<br/>Time: ".$time." seconds</p>";
?><?php
    $time_start = microtime(true);

    set_time_limit(0);
    ini_set('memory_limit', '-1');
    
    $outh_token = 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ';
    $list_id = '50bebb85e4b098cd643a8b43';
    $cat_id = '4cae28ecbf23941eb1190695';
    
    $url = 'https://api.foursquare.com/v2/venues/add';
    $url2 = 'https://api.foursquare.com/v2/lists/'.$list_id.'/additem';
    
    function http_post ($url, $data)
{
    $data_url = http_build_query ($data);
    $data_len = strlen ($data_url);

    return array ('content'=>file_get_contents ($url, false, stream_context_create (array ('http'=>array ('method'=>'POST'
            , 'header'=>"Connection: close\r\nContent-Length: $data_len\r\n"
            , 'content'=>$data_url
            ))))
        , 'headers'=>$http_response_header
        );
}
    
    $row = 1;
    if (($handle = fopen("http://davidlemayian.github.com/fs/uasin-gishu.csv", "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            
            if ($row == 1){
                //Skip
            } else { 
                if ($row > 0 && $row < 250){
                $lon = $data[1];
                if($lon==0){
                    //No geo location.
                } else {
                    $reg_county = addslashes(ucwords(strtolower($data[2])));
                    $reg_const = addslashes(ucwords(strtolower($data[4])));
                    $reg_ward = addslashes(ucwords(strtolower($data[5])));
                    $reg_name1 = addslashes(ucwords(strtolower($data[0])));
                    $reg_name = "IEBC Registration Centre - ".$reg_name1;
                    $reg_desc = "IEBC Registration Centre - ".$reg_name1.". County: ".$reg_county.", Constitutency: ".$reg_const.", Ward: ".$reg_ward.". Brought to you by Nimeregister! http://nimeregister.com";
                    $reg_ll = $data[3].",".$data[1];
                    
                    $data1 = array('name' => $reg_name, 'primaryCategoryId' => $cat_id, 'description' => $reg_desc, 'll' => $reg_ll, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                    $options = array('http' => array('method'  => 'POST','content' => http_build_query($data1)));
                    $context  = stream_context_create($options);

                    //$result = file_get_contents($url, false, $context);
                    $result = http_post ($url, $data1);
                    
                    echo $row." - ";
                    //if ($row == 499){
                        var_dump($result);
                    //}
                    
                    if ($result['content'] == 'bool(false)'){
                        //Nothing to add to list.
                    } else {
                        $obj = json_decode($result['content']);
                        //echo '<br/><br/>';
                        //Add to list
                        $data2 = array('venueId' => $obj->{'response'}->{'venue'}->{'id'}, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                        $options = array('http' => array('method'  => 'POST','content' => http_build_query($data2)));
                        $context  = stream_context_create($options);

                        //$result = file_get_contents($url2, false, $context);
                        $result = http_post ($url, $data2);
                        var_dump($result);
                    }
                    
                }
                }
            }
            
            $row++;
        }
        fclose($handle);
    }
    
    echo "<br/><br/>Rows: ".$row;
    $time_end = microtime(true);
    $time = $time_end -$time_start;

    echo "<br/>Time: ".$time." seconds</p>";
?>