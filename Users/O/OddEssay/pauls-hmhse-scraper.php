<?php

require  'scraperwiki/simple_html_dom.php';

$frontPage = scraperwiki::scrape('http://www.european-football-statistics.co.uk/englandcontent.htm');

$frontDom = new simple_html_dom();
$frontDom->load($frontPage);


function clubURL($url)
{
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
       
    $dom->load($html);
        
        
        $clubName = trim(str_replace('&nbsp;','',$dom->find('table',0)->find('tr',2)->plaintext));
        $formatClubName = trim(preg_replace('/\s+/',' ',$clubName));

        $_GLOBAL['clubs'][] = $formatClubName;
        echo 'running '.$formatClubName."\n";
        foreach($dom->find('table',2)->find('tr') as $row)
        {
            if( is_numeric( $row->find( 'td' , 0 )->plaintext ) )
            {
                $year = trim($row->find('td',0)->plaintext);
                $position = trim(str_replace('&nbsp;','',$row->find('td',1)->plaintext) );
                if(trim($position) == 'Champion') { $position = 1; }
                $leagueLevel = trim($row->find('td',2)->plaintext);
                $overallPosition = trim($row->find('td',3)->plaintext);
                $avgAttendance = trim(str_replace('.','',$row->find('td',4)->plaintext));
                $totalAttendance = trim(str_replace('.','',$row->find('td',12)->plaintext));
        
            
                $dataset = array
                (
                    'club' => $formatClubName,
                    'year' => $year,
                    'finishedPosition' => $position,
                    'league' => $leagueLevel,
                    'overallPosition' => $overallPosition,
                    'avgAttendance' => $avgAttendance,
                    'totalAttendance' => $totalAttendance
                );
                scraperwiki::save(array('club','year'),$dataset);
          
            }            
        }
    /*
     * The next to lines stop a memory leak in Simple XML as per http://simplehtmldom.sourceforge.net/manual_faq.htm#memory_leak
     */
    $dom->clear();
    unset($dom);
}

foreach($frontDom->find('a') as $link)
{

    if( strpos($link->href,'attnclub') !== FALSE )
    {
        clubURL('http://www.european-football-statistics.co.uk/'.$link->href);       
    }
}  

scraperwiki::save_metadata('Clubs',implode(',',$_GLOBAL['clubs']));

?>
