<?php
$result = array();
function clear_elements($str)
{
    $str = str_replace('<td align="left">','',$str);
    $str = str_replace('</td>','',$str);
    return trim($str);
}
function format_date($str)
{
    list($day,$month,$y) = explode('/',$str);
    $year = substr($y,0,4);
    $time = substr($y,5,5);
    return $year.'-'.$month.'-'.$day.' '.$time;
}
function find_program($program,$url)
{
    $content = file($url);
    $result = array();
    $i=0;
    $row=0;
    foreach($content as $c)
    {
       if(strpos($c,$program)!=0)
       {
            $row=$i;
            break;
       }
        $i++;
    }
    if($row)
    {
        $broadcast_row = $content[$row+1];
        $target_row =clear_elements($content[$row+3]);
        $broadcast_date = format_date(clear_elements($broadcast_row));
        $pid = substr($target_row,0,strpos($target_row,'&'));
        return array('program'=>$program,
                     'pid'=>$pid,
                     'broadcast_date'=>$broadcast_date,
                     'broadcast_timestamp'=> strtotime($broadcast_date));
    }
    return 'No program found';
}

$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/1/aod/default.aspx','program'=>'Ready for the Weekend');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/56/aod/default.aspx','program'=>'Graham Torrington Night Time');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/4/aod/default.aspx','program'=>'Material World');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/4/aod/default.aspx','program'=>'Farming Today');

foreach($data as $d)
{
    scraperwiki::save(array('program'), find_program($d['program'],$d['url']));  
}
?><?php
$result = array();
function clear_elements($str)
{
    $str = str_replace('<td align="left">','',$str);
    $str = str_replace('</td>','',$str);
    return trim($str);
}
function format_date($str)
{
    list($day,$month,$y) = explode('/',$str);
    $year = substr($y,0,4);
    $time = substr($y,5,5);
    return $year.'-'.$month.'-'.$day.' '.$time;
}
function find_program($program,$url)
{
    $content = file($url);
    $result = array();
    $i=0;
    $row=0;
    foreach($content as $c)
    {
       if(strpos($c,$program)!=0)
       {
            $row=$i;
            break;
       }
        $i++;
    }
    if($row)
    {
        $broadcast_row = $content[$row+1];
        $target_row =clear_elements($content[$row+3]);
        $broadcast_date = format_date(clear_elements($broadcast_row));
        $pid = substr($target_row,0,strpos($target_row,'&'));
        return array('program'=>$program,
                     'pid'=>$pid,
                     'broadcast_date'=>$broadcast_date,
                     'broadcast_timestamp'=> strtotime($broadcast_date));
    }
    return 'No program found';
}

$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/1/aod/default.aspx','program'=>'Ready for the Weekend');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/56/aod/default.aspx','program'=>'Graham Torrington Night Time');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/4/aod/default.aspx','program'=>'Material World');
$data[] = array('url'=>'http://www.iplayerconverter.co.uk/r/4/aod/default.aspx','program'=>'Farming Today');

foreach($data as $d)
{
    scraperwiki::save(array('program'), find_program($d['program'],$d['url']));  
}
?>