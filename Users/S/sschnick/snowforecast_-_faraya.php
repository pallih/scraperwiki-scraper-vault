<?php

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();

//Change that to get another resort
$resort_name = 'Kicking-Horse';

//Load the url
$url = 'http://www.snow-forecast.com/resorts/'.$resort_name.'/6day/top';
$html = scraperWiki::scrape($url);  


//Load the html
$dom->load($html);   

//Get the 2nd table with class forecasts, the one with the one the matters
$table= $dom->find('table[class=forecasts]', 1);

//Initiate results array
$forecast = array();

//Row counter
$r = 0;

//Circle through the rows
foreach($table->find('tr') as $row)
{
    //Date row
    if($r == 1)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['when'] = trim(str_replace(array("\n", chr(13), '-'), '', $column->plaintext));
            
            //Determine the date
            $today_day   = date('j');
            $today_month = date('n');
            $when_comp = explode(' ', $forecast[$c]['when'], 3);
            $when_day = $when_comp[1];
            
            if($when_day < $today_day)
            {
                $when_month = date('n') + 1;
            }
            else
            {
                $when_month = date('n');
            }
            
            if($when_month < $today_month)
            {
                $when_year = date('Y') + 1;
            }
            else
            {
                $when_year = date('Y');
            }
            
            switch(trim($when_comp[2]))
            {
                case 'morning':
                    $when_hour = 9;
                    break;
                case 'afternoon':
                    $when_hour = 14;
                    break;
                case 'night':
                    $when_hour = 21;
                    break;
            }
            
            $forecast[$c]['timestamp'] = mktime($when_hour, 0, 0, $when_month, $when_day, $when_year);
            
            
            
            $c++;
            $column->__destruct();
        }
        
    }

    //Forecast row
    if($r == 4)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['forecast'] = trim($column->plaintext);
            $c++;
            $column->__destruct();            
        }
    }

    //Snow row
    if($r == 5)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['snow'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Rain row
    if($r == 6)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['rain'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Max temprature row
    if($r == 7)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['t_max'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Min temprature row
    if($r == 8)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['t_min'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Win Chill temprature row
    if($r == 9)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['t_wchill'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    $r++;
}

//Circle through our forecast table and save in db
foreach($forecast as $one)
{
    scraperwiki::save(array('timestamp'),$one);
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();

//Change that to get another resort
$resort_name = 'Kicking-Horse';

//Load the url
$url = 'http://www.snow-forecast.com/resorts/'.$resort_name.'/6day/top';
$html = scraperWiki::scrape($url);  


//Load the html
$dom->load($html);   

//Get the 2nd table with class forecasts, the one with the one the matters
$table= $dom->find('table[class=forecasts]', 1);

//Initiate results array
$forecast = array();

//Row counter
$r = 0;

//Circle through the rows
foreach($table->find('tr') as $row)
{
    //Date row
    if($r == 1)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['when'] = trim(str_replace(array("\n", chr(13), '-'), '', $column->plaintext));
            
            //Determine the date
            $today_day   = date('j');
            $today_month = date('n');
            $when_comp = explode(' ', $forecast[$c]['when'], 3);
            $when_day = $when_comp[1];
            
            if($when_day < $today_day)
            {
                $when_month = date('n') + 1;
            }
            else
            {
                $when_month = date('n');
            }
            
            if($when_month < $today_month)
            {
                $when_year = date('Y') + 1;
            }
            else
            {
                $when_year = date('Y');
            }
            
            switch(trim($when_comp[2]))
            {
                case 'morning':
                    $when_hour = 9;
                    break;
                case 'afternoon':
                    $when_hour = 14;
                    break;
                case 'night':
                    $when_hour = 21;
                    break;
            }
            
            $forecast[$c]['timestamp'] = mktime($when_hour, 0, 0, $when_month, $when_day, $when_year);
            
            
            
            $c++;
            $column->__destruct();
        }
        
    }

    //Forecast row
    if($r == 4)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['forecast'] = trim($column->plaintext);
            $c++;
            $column->__destruct();            
        }
    }

    //Snow row
    if($r == 5)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['snow'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Rain row
    if($r == 6)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['rain'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Max temprature row
    if($r == 7)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['t_max'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Min temprature row
    if($r == 8)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['t_min'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    //Win Chill temprature row
    if($r == 9)
    {
        //Column counter, every column is one forecast
        $c = 0;
        foreach($row->find('td') as $column)
        {
            $forecast[$c]['t_wchill'] = trim($column->plaintext);
            $c++;
            $column->__destruct();
        }
    }

    $r++;
}

//Circle through our forecast table and save in db
foreach($forecast as $one)
{
    scraperwiki::save(array('timestamp'),$one);
}

?>
