// code to be ported to scraperlibs once complete
$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"; 
$apilimit = 500; 

function getKeys($name)
{
    global $apiurl; 
    $url = "{$apiurl}getkeys?&name={$name}"; 
    $handle = fopen($url, "r"); 
    $ljson = stream_get_contents($handle); 
    fclose($handle);
    return json_decode($ljson); 
}

function generateData($urlbase, $limit, $offset)
{
    global $apilimit; 
    $count = 0;
    $loffset = 0;
    $result = array(); 
    while (true)
    {
        $llimit = ($limit == -1 ? $apilimit : min($apilimit, $limit-$count)); 
            
        $url = "{$urlbase}&limit={$llimit}&offset=".($offset+$loffset); 
        $handle = fopen($url, "r"); 
        $ljson = stream_get_contents($handle); 
        fclose($handle);
        $lresult = json_decode($ljson); 
        $count += count($lresult); 
        $result = array_merge($result, $lresult); 
        if (count($lresult) < $llimit)  // run out of records
            break; 
            
        if (($limit != -1) and ($count >= $limit))    // exceeded the limit
            break; 

        $loffset += $llimit; 
    }
    return $result; 
}

function getData($name, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdata?name={$name}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByDate($name, $start_date, $end_date, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabydate?name={$name}&start_date={$start_date}&end_date={$end_date}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByLocation($name, $lat, $lng, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabylocation?name={$name}&lat={$lat}&lng={$lng}"; 
    return generateData($urlbase, $limit, $offset); 
}
    
function search($name, $filterdict, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $filter = ""; 
    foreach ($filterdict as $key => $value)
    {
        if ($filter)
            $filter .= "|";
        $filter .= urlencode($key).",".urlencode($value); 
    }
    $urlbase = "{$apiurl}search?name={$name}&filter={$filter}"; 
    return generateData($urlbase, $limit, $offset); 
}


function Test()
{
    global $apilimit; 
    $apilimit = 50; // make tests easier to stress
    
    $name1 = "uk-offshore-oil-wells"; 
    $name2 = "uk-lottery-grants"; 
    print_r(getKeys($name1)); 

    print_r(getData($name1, 110)); 
    print_r(getDataByDate($name2, $start_date="2009-01-01", $end_date="2009-01-12")); 
    
    print_r(getDataByLocation($name1, $lat=59.033358, $lng=1.0486569, $limit=60)); 
    $filterdict = array('Distributing_Body' => 'UK Sport', "Region" => "London"); 
    print_r(search($name2, $filterdict, $offset=5, $limit=17)); 
}

//Test(); 

// code to be ported to scraperlibs once complete
$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"; 
$apilimit = 500; 

function getKeys($name)
{
    global $apiurl; 
    $url = "{$apiurl}getkeys?&name={$name}"; 
    $handle = fopen($url, "r"); 
    $ljson = stream_get_contents($handle); 
    fclose($handle);
    return json_decode($ljson); 
}

function generateData($urlbase, $limit, $offset)
{
    global $apilimit; 
    $count = 0;
    $loffset = 0;
    $result = array(); 
    while (true)
    {
        $llimit = ($limit == -1 ? $apilimit : min($apilimit, $limit-$count)); 
            
        $url = "{$urlbase}&limit={$llimit}&offset=".($offset+$loffset); 
        $handle = fopen($url, "r"); 
        $ljson = stream_get_contents($handle); 
        fclose($handle);
        $lresult = json_decode($ljson); 
        $count += count($lresult); 
        $result = array_merge($result, $lresult); 
        if (count($lresult) < $llimit)  // run out of records
            break; 
            
        if (($limit != -1) and ($count >= $limit))    // exceeded the limit
            break; 

        $loffset += $llimit; 
    }
    return $result; 
}

function getData($name, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdata?name={$name}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByDate($name, $start_date, $end_date, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabydate?name={$name}&start_date={$start_date}&end_date={$end_date}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByLocation($name, $lat, $lng, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabylocation?name={$name}&lat={$lat}&lng={$lng}"; 
    return generateData($urlbase, $limit, $offset); 
}
    
function search($name, $filterdict, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $filter = ""; 
    foreach ($filterdict as $key => $value)
    {
        if ($filter)
            $filter .= "|";
        $filter .= urlencode($key).",".urlencode($value); 
    }
    $urlbase = "{$apiurl}search?name={$name}&filter={$filter}"; 
    return generateData($urlbase, $limit, $offset); 
}


function Test()
{
    global $apilimit; 
    $apilimit = 50; // make tests easier to stress
    
    $name1 = "uk-offshore-oil-wells"; 
    $name2 = "uk-lottery-grants"; 
    print_r(getKeys($name1)); 

    print_r(getData($name1, 110)); 
    print_r(getDataByDate($name2, $start_date="2009-01-01", $end_date="2009-01-12")); 
    
    print_r(getDataByLocation($name1, $lat=59.033358, $lng=1.0486569, $limit=60)); 
    $filterdict = array('Distributing_Body' => 'UK Sport', "Region" => "London"); 
    print_r(search($name2, $filterdict, $offset=5, $limit=17)); 
}

//Test(); 

// code to be ported to scraperlibs once complete
$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"; 
$apilimit = 500; 

function getKeys($name)
{
    global $apiurl; 
    $url = "{$apiurl}getkeys?&name={$name}"; 
    $handle = fopen($url, "r"); 
    $ljson = stream_get_contents($handle); 
    fclose($handle);
    return json_decode($ljson); 
}

function generateData($urlbase, $limit, $offset)
{
    global $apilimit; 
    $count = 0;
    $loffset = 0;
    $result = array(); 
    while (true)
    {
        $llimit = ($limit == -1 ? $apilimit : min($apilimit, $limit-$count)); 
            
        $url = "{$urlbase}&limit={$llimit}&offset=".($offset+$loffset); 
        $handle = fopen($url, "r"); 
        $ljson = stream_get_contents($handle); 
        fclose($handle);
        $lresult = json_decode($ljson); 
        $count += count($lresult); 
        $result = array_merge($result, $lresult); 
        if (count($lresult) < $llimit)  // run out of records
            break; 
            
        if (($limit != -1) and ($count >= $limit))    // exceeded the limit
            break; 

        $loffset += $llimit; 
    }
    return $result; 
}

function getData($name, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdata?name={$name}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByDate($name, $start_date, $end_date, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabydate?name={$name}&start_date={$start_date}&end_date={$end_date}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByLocation($name, $lat, $lng, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabylocation?name={$name}&lat={$lat}&lng={$lng}"; 
    return generateData($urlbase, $limit, $offset); 
}
    
function search($name, $filterdict, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $filter = ""; 
    foreach ($filterdict as $key => $value)
    {
        if ($filter)
            $filter .= "|";
        $filter .= urlencode($key).",".urlencode($value); 
    }
    $urlbase = "{$apiurl}search?name={$name}&filter={$filter}"; 
    return generateData($urlbase, $limit, $offset); 
}


function Test()
{
    global $apilimit; 
    $apilimit = 50; // make tests easier to stress
    
    $name1 = "uk-offshore-oil-wells"; 
    $name2 = "uk-lottery-grants"; 
    print_r(getKeys($name1)); 

    print_r(getData($name1, 110)); 
    print_r(getDataByDate($name2, $start_date="2009-01-01", $end_date="2009-01-12")); 
    
    print_r(getDataByLocation($name1, $lat=59.033358, $lng=1.0486569, $limit=60)); 
    $filterdict = array('Distributing_Body' => 'UK Sport', "Region" => "London"); 
    print_r(search($name2, $filterdict, $offset=5, $limit=17)); 
}

//Test(); 

// code to be ported to scraperlibs once complete
$apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"; 
$apilimit = 500; 

function getKeys($name)
{
    global $apiurl; 
    $url = "{$apiurl}getkeys?&name={$name}"; 
    $handle = fopen($url, "r"); 
    $ljson = stream_get_contents($handle); 
    fclose($handle);
    return json_decode($ljson); 
}

function generateData($urlbase, $limit, $offset)
{
    global $apilimit; 
    $count = 0;
    $loffset = 0;
    $result = array(); 
    while (true)
    {
        $llimit = ($limit == -1 ? $apilimit : min($apilimit, $limit-$count)); 
            
        $url = "{$urlbase}&limit={$llimit}&offset=".($offset+$loffset); 
        $handle = fopen($url, "r"); 
        $ljson = stream_get_contents($handle); 
        fclose($handle);
        $lresult = json_decode($ljson); 
        $count += count($lresult); 
        $result = array_merge($result, $lresult); 
        if (count($lresult) < $llimit)  // run out of records
            break; 
            
        if (($limit != -1) and ($count >= $limit))    // exceeded the limit
            break; 

        $loffset += $llimit; 
    }
    return $result; 
}

function getData($name, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdata?name={$name}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByDate($name, $start_date, $end_date, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabydate?name={$name}&start_date={$start_date}&end_date={$end_date}"; 
    return generateData($urlbase, $limit, $offset); 
}

function getDataByLocation($name, $lat, $lng, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $urlbase = "{$apiurl}getdatabylocation?name={$name}&lat={$lat}&lng={$lng}"; 
    return generateData($urlbase, $limit, $offset); 
}
    
function search($name, $filterdict, $limit= -1, $offset= 0)
{
    global $apiurl; 
    $filter = ""; 
    foreach ($filterdict as $key => $value)
    {
        if ($filter)
            $filter .= "|";
        $filter .= urlencode($key).",".urlencode($value); 
    }
    $urlbase = "{$apiurl}search?name={$name}&filter={$filter}"; 
    return generateData($urlbase, $limit, $offset); 
}


function Test()
{
    global $apilimit; 
    $apilimit = 50; // make tests easier to stress
    
    $name1 = "uk-offshore-oil-wells"; 
    $name2 = "uk-lottery-grants"; 
    print_r(getKeys($name1)); 

    print_r(getData($name1, 110)); 
    print_r(getDataByDate($name2, $start_date="2009-01-01", $end_date="2009-01-12")); 
    
    print_r(getDataByLocation($name1, $lat=59.033358, $lng=1.0486569, $limit=60)); 
    $filterdict = array('Distributing_Body' => 'UK Sport', "Region" => "London"); 
    print_r(search($name2, $filterdict, $offset=5, $limit=17)); 
}

//Test(); 

