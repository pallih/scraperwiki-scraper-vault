<?php

    require 'scraperwiki/simple_html_dom.php';

    $url = 'http://fantasy.premierleague.com/web/api/elements/';
    

    $upper_limit = 650;
    $lower_limit = 1;

    $ppgmin = 3;
    $sdmax = 5;

    for($id = $lower_limit; $id <= $upper_limit; $id++)
    {
        $html = scraperwiki::scrape($url.$id);
    
        $dom = new simple_html_dom();
        $dom->load($html);

        $player_data = json_decode($dom);

        if($player_data->id)
        {
            $player_info = array(
                        'total_points' => strval($player_data->total_points),
                        'id' => strval($player_data->id),
                        'last_name' => strval($player_data->web_name),
                        'position' => strval($player_data->type_name),
                        'team' => strval($player_data->team_name),
                        'cost' => strval($player_data->now_cost),
                        'form' => strval($player_data->form),
                        'ppg' => strval($player_data->points_per_game)
                        #'esp' => strval($player_data->
            );
            $ppg = strval($player_data->points_per_game);

            $stdev = 0;
            $game = 1;
            foreach($player_data->fixture_history->all as $gw)
            {
                $points = strval($gw[18]);
                $gameweek = strval($gw[1]);
                #$player_info['game' . $game] = $points;
            
                $vari = $points - $ppg;
                $dev = pow($vari, 2);
    
                #print($vari . "\t");

                $stdev += $dev;
                $game++;

            }
            $stdev = sqrt($stdev / ($game));
            $player_info['stdev'] = $stdev;
            #print("\nStandard Deviation: " . $stdev . "\n");
            #print("Gameweeks Played: " . $gameweek . "\n");            

            
            switch($player_info['position'])
            {
                case 'Goalkeeper':
                    #print("Door Blocker\n");
                    scraperwiki::save_sqlite(array('id'),$player_info,'goalkeepers');
                    break;
                case 'Defender':
                    scraperwiki::save_sqlite(array('id'),$player_info,'defenders');
                    break;
                case 'Midfielder':
                    scraperwiki::save_sqlite(array('id'),$player_info,'midfielders');
                    break;
                case 'Forward':
                    scraperwiki::save_sqlite(array('id'),$player_info,'forwards');
                    break;
            }
            // Save to a db that contains all players.
            scraperwiki::save_sqlite(array('id'),$player_info,'all');
            if($stdev <= $sdmax && $ppg >= $ppgmin)
            {
                scraperwiki::save_sqlite(array('id'),$player_info,'topdogs');                
            }
            


        }

    }

?>