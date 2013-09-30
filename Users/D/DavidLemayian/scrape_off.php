<?php
    $time_start = microtime(true);

    set_time_limit(0);
    ini_set('memory_limit', '-1');
    
    $outh_token = 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ';
    $list_id = '50be8a06e4b009725341ae0c';
    $cat_id = '4cae28ecbf23941eb1190695';
    
    $url = 'https://api.foursquare.com/v2/lists/50be8a06e4b009725341ae0c?oauth_token=CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ';
    $url2 = 'https://api.foursquare.com/v2/venues/VENUE_ID/flag';
    
    $result = file_get_contents($url);
    
    $obj = json_decode($result);

    foreach ($obj->{'response'}->{'list'}->{'listItems'}->{'items'} as $list_item){
        $url2 = 'https://api.foursquare.com/v2/venues/'.$list_item->{'id'}.'/flag';
        $data2 = array('problem' => 'mislocated', 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');
        $options = array('http' => array('method'  => 'POST','content' => http_build_query($data2)));
        $context  = stream_context_create($options);
        $result2 = file_get_contents($url2, false, $context);
        
        
        $url3 = 'https://api.foursquare.com/v2/lists/50be8a06e4b009725341ae0c/deleteitem';
        $data3 = array('itemId' => $list_item->{'id'}, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');
        $options = array('http' => array('method'  => 'POST','content' => http_build_query($data3)));
        $context  = stream_context_create($options);
        $result3 = file_get_contents($url3, false, $context);
        
        //echo $list_item->{'id'}.'<br/>';
    }
                    
                    /*
                    $data1 = array('name' => $reg_name, 'primaryCategoryId' => $cat_id, 'description' => $reg_desc, 'll' => $reg_ll, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                    $options = array('http' => array('method'  => 'POST','content' => http_build_query($data1)));
                    $context  = stream_context_create($options);

                    
                    
                    var_dump($result);
                    $obj = json_decode($result);
                    echo '<br/><br/>';
                    //Add to list
                    $data2 = array('venueId' => $obj->{'response'}->{'venue'}->{'id'}, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                    $options = array('http' => array('method'  => 'POST','content' => http_build_query($data2)));
                    $context  = stream_context_create($options);

                    $result = file_get_contents($url2, false, $context);
                    var_dump($result);
                }
                }
            }
            
            $row++;
        }
        fclose($handle);
    }*/
    
    echo "<br/><br/>Rows: ".$row;
    $time_end = microtime(true);
    $time = $time_end -$time_start;

    echo "<br/>Time: ".$time." seconds</p>";
?><?php
    $time_start = microtime(true);

    set_time_limit(0);
    ini_set('memory_limit', '-1');
    
    $outh_token = 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ';
    $list_id = '50be8a06e4b009725341ae0c';
    $cat_id = '4cae28ecbf23941eb1190695';
    
    $url = 'https://api.foursquare.com/v2/lists/50be8a06e4b009725341ae0c?oauth_token=CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ';
    $url2 = 'https://api.foursquare.com/v2/venues/VENUE_ID/flag';
    
    $result = file_get_contents($url);
    
    $obj = json_decode($result);

    foreach ($obj->{'response'}->{'list'}->{'listItems'}->{'items'} as $list_item){
        $url2 = 'https://api.foursquare.com/v2/venues/'.$list_item->{'id'}.'/flag';
        $data2 = array('problem' => 'mislocated', 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');
        $options = array('http' => array('method'  => 'POST','content' => http_build_query($data2)));
        $context  = stream_context_create($options);
        $result2 = file_get_contents($url2, false, $context);
        
        
        $url3 = 'https://api.foursquare.com/v2/lists/50be8a06e4b009725341ae0c/deleteitem';
        $data3 = array('itemId' => $list_item->{'id'}, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');
        $options = array('http' => array('method'  => 'POST','content' => http_build_query($data3)));
        $context  = stream_context_create($options);
        $result3 = file_get_contents($url3, false, $context);
        
        //echo $list_item->{'id'}.'<br/>';
    }
                    
                    /*
                    $data1 = array('name' => $reg_name, 'primaryCategoryId' => $cat_id, 'description' => $reg_desc, 'll' => $reg_ll, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                    $options = array('http' => array('method'  => 'POST','content' => http_build_query($data1)));
                    $context  = stream_context_create($options);

                    
                    
                    var_dump($result);
                    $obj = json_decode($result);
                    echo '<br/><br/>';
                    //Add to list
                    $data2 = array('venueId' => $obj->{'response'}->{'venue'}->{'id'}, 'oauth_token' => 'CWSGAOBXSZ3MMJ0HYY0YA4HKSOIHFTJDFPRWN31LCV2H1TPJ');

                    $options = array('http' => array('method'  => 'POST','content' => http_build_query($data2)));
                    $context  = stream_context_create($options);

                    $result = file_get_contents($url2, false, $context);
                    var_dump($result);
                }
                }
            }
            
            $row++;
        }
        fclose($handle);
    }*/
    
    echo "<br/><br/>Rows: ".$row;
    $time_end = microtime(true);
    $time = $time_end -$time_start;

    echo "<br/>Time: ".$time." seconds</p>";
?>