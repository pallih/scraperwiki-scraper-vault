<?php
    include('scraperwiki/simple_html_dom.php');

    $opts = array(
                'http'=>array(
                    'method'=>"GET",
                    'header'=>"Accept-language: en\r\n" . "User-Agent: Mozilla/5.0 (X11; U; Linux x86_64; es-AR; rv:1.9.2.23) Gecko/20110921 Ubuntu/10.10 (maverick) Firefox/3.6.23"
                )
            );

    $context = stream_context_create($opts);

    $count = 0;

    $listStations = array();

    scraperwiki::sqliteexecute("create table data (station string, line string, closed string, type_of_closure string, current_condition string, details string, coordinates string)");

    $html = file_get_html("http://en.wikipedia.org/wiki/List_of_former_and_unopened_London_Underground_stations");

    foreach ($html -> find("a") as $as)
    {
        $ashrefs = $as -> href;

        if (strpos($ashrefs, "station") !== false && strpos($ashrefs, "St_Mary%27s_(Whitechapel_Road)_tube_station") === false && strpos($ashrefs, "Knightsbridge_tube_station") === false && strpos($ashrefs, "Green_Park_tube_station") === false && strpos($ashrefs, "Hyde_Park_Corner_tube_station") === false && strpos($ashrefs, "Hounslow_East_tube_station") === false && strpos($ashrefs, "St_John%27s_Wood_tube_station") === false && strpos($ashrefs, "Tower_Hill_tube_station") === false && strpos($ashrefs, "Park_Royal_tube_station") === false && strpos($ashrefs, "Goldhawk_Road_tube_station") === false && strpos($ashrefs, "Acton_Town_tube_station") === false && strpos($ashrefs, "Tower_Hill_tube_station") === false && strpos($ashrefs, "Gloucester_Road_tube_station") === false && strpos($ashrefs, "Embankment_tube_station") === false && strpos($ashrefs, "Kilburn_tube_station") === false && strpos($ashrefs, "Maida_Vale_tube_station") === false && strpos($ashrefs, "Marble_Arch_tube_station") === false && strpos($ashrefs, "Victoria_tube_station") === false && strpos($ashrefs, "Bank_station_(London)") === false && strpos($ashrefs, "Ealing_Broadway_station") === false && strpos($ashrefs, "Fenchurch_Street_railway_station") === false && strpos($ashrefs, "Finsbury_Park_station") === false && strpos($ashrefs, "Moorgate_station") === false && strpos($ashrefs, "Shoreditch_High_Street_railway_station") === false && strpos($ashrefs, "Stratford_station") === false && strpos($ashrefs, "List_of_former_and_unopened_London_Underground_stations") === false && strpos($ashrefs, ".jpg") === false)
        {
            $count++;

            $htmlStation = file_get_html("http://en.wikipedia.org" . $ashrefs, false, $context);

            foreach ($htmlStation -> find("span.geo") as $spans)
            {
                $spanstext = str_replace("<span class=\"geo\">", "", $spans -> outertext);
                $spanstext = str_replace("</span>", "", $spanstext);
                $spanstext = str_replace(";", ",", $spanstext);

                $spanstextParts = explode(", ", $spanstext);
                
                // $spanstext = $spanstextParts["1"] . ", " . $spanstextParts["0"];
                // $spanstext = "[" . $spanstext . "]";
                $spanstext = $spanstextParts["0"] . " " . $spanstextParts["1"];
            }

            $htmlParts = explode($ashrefs, $html);
            $htmlParts = $htmlParts[1];
            $htmlParts = explode(" </tr>", $htmlParts);
            $htmlParts = $htmlParts[0];
            $htmlParts = explode("</td>", $htmlParts);

            $htmlPartsZero = explode(">", $htmlParts[0]);
            $htmlPartsZero = explode("<", $htmlPartsZero[1]);
            $htmlPartsOne = explode("<td>", $htmlParts[1]);
            $htmlPartsTwo = explode("<td>", $htmlParts[2]);
            $htmlPartsTwo = explode("<span style=\"white-space:nowrap;\">", $htmlPartsTwo[1]);
            $htmlPartsTwo = explode("</span>", $htmlPartsTwo[1]);
            // $htmlPartsTwo = explode(">", $htmlPartsTwo[0]);
            // $htmlPartsTwo = explode("<", $htmlPartsTwo[1]);
            $htmlPartsThree = explode("<td>", $htmlParts[3]);
            $htmlPartsFour = explode("<td>", $htmlParts[4]);
            $htmlPartsFive = explode("<td>", $htmlParts[5]);
            $htmlPartsFive = explode("<sup", $htmlPartsFive[1]);

            $listStationsSearch = array_search($htmlPartsZero[0], $listStations);

            if (!$listStationsSearch)
            {
                array_push($listStations, $htmlPartsZero[0]);

                scraperwiki::sqliteexecute("insert into data values (?, ?, ?, ?, ?, ?, ?)", array(strip_tags($htmlPartsZero[0]), strip_tags($htmlPartsOne[1]), strip_tags($htmlPartsTwo[0]), strip_tags($htmlPartsThree[1]), strip_tags($htmlPartsFour[1]), str_replace("\"", "\\\"", strip_tags($htmlPartsFive[0])), strip_tags($spanstext)));
                scraperwiki::sqlitecommit();
            }
        }

        if ($count == 105)
            break;
    }
?><?php
    include('scraperwiki/simple_html_dom.php');

    $opts = array(
                'http'=>array(
                    'method'=>"GET",
                    'header'=>"Accept-language: en\r\n" . "User-Agent: Mozilla/5.0 (X11; U; Linux x86_64; es-AR; rv:1.9.2.23) Gecko/20110921 Ubuntu/10.10 (maverick) Firefox/3.6.23"
                )
            );

    $context = stream_context_create($opts);

    $count = 0;

    $listStations = array();

    scraperwiki::sqliteexecute("create table data (station string, line string, closed string, type_of_closure string, current_condition string, details string, coordinates string)");

    $html = file_get_html("http://en.wikipedia.org/wiki/List_of_former_and_unopened_London_Underground_stations");

    foreach ($html -> find("a") as $as)
    {
        $ashrefs = $as -> href;

        if (strpos($ashrefs, "station") !== false && strpos($ashrefs, "St_Mary%27s_(Whitechapel_Road)_tube_station") === false && strpos($ashrefs, "Knightsbridge_tube_station") === false && strpos($ashrefs, "Green_Park_tube_station") === false && strpos($ashrefs, "Hyde_Park_Corner_tube_station") === false && strpos($ashrefs, "Hounslow_East_tube_station") === false && strpos($ashrefs, "St_John%27s_Wood_tube_station") === false && strpos($ashrefs, "Tower_Hill_tube_station") === false && strpos($ashrefs, "Park_Royal_tube_station") === false && strpos($ashrefs, "Goldhawk_Road_tube_station") === false && strpos($ashrefs, "Acton_Town_tube_station") === false && strpos($ashrefs, "Tower_Hill_tube_station") === false && strpos($ashrefs, "Gloucester_Road_tube_station") === false && strpos($ashrefs, "Embankment_tube_station") === false && strpos($ashrefs, "Kilburn_tube_station") === false && strpos($ashrefs, "Maida_Vale_tube_station") === false && strpos($ashrefs, "Marble_Arch_tube_station") === false && strpos($ashrefs, "Victoria_tube_station") === false && strpos($ashrefs, "Bank_station_(London)") === false && strpos($ashrefs, "Ealing_Broadway_station") === false && strpos($ashrefs, "Fenchurch_Street_railway_station") === false && strpos($ashrefs, "Finsbury_Park_station") === false && strpos($ashrefs, "Moorgate_station") === false && strpos($ashrefs, "Shoreditch_High_Street_railway_station") === false && strpos($ashrefs, "Stratford_station") === false && strpos($ashrefs, "List_of_former_and_unopened_London_Underground_stations") === false && strpos($ashrefs, ".jpg") === false)
        {
            $count++;

            $htmlStation = file_get_html("http://en.wikipedia.org" . $ashrefs, false, $context);

            foreach ($htmlStation -> find("span.geo") as $spans)
            {
                $spanstext = str_replace("<span class=\"geo\">", "", $spans -> outertext);
                $spanstext = str_replace("</span>", "", $spanstext);
                $spanstext = str_replace(";", ",", $spanstext);

                $spanstextParts = explode(", ", $spanstext);
                
                // $spanstext = $spanstextParts["1"] . ", " . $spanstextParts["0"];
                // $spanstext = "[" . $spanstext . "]";
                $spanstext = $spanstextParts["0"] . " " . $spanstextParts["1"];
            }

            $htmlParts = explode($ashrefs, $html);
            $htmlParts = $htmlParts[1];
            $htmlParts = explode(" </tr>", $htmlParts);
            $htmlParts = $htmlParts[0];
            $htmlParts = explode("</td>", $htmlParts);

            $htmlPartsZero = explode(">", $htmlParts[0]);
            $htmlPartsZero = explode("<", $htmlPartsZero[1]);
            $htmlPartsOne = explode("<td>", $htmlParts[1]);
            $htmlPartsTwo = explode("<td>", $htmlParts[2]);
            $htmlPartsTwo = explode("<span style=\"white-space:nowrap;\">", $htmlPartsTwo[1]);
            $htmlPartsTwo = explode("</span>", $htmlPartsTwo[1]);
            // $htmlPartsTwo = explode(">", $htmlPartsTwo[0]);
            // $htmlPartsTwo = explode("<", $htmlPartsTwo[1]);
            $htmlPartsThree = explode("<td>", $htmlParts[3]);
            $htmlPartsFour = explode("<td>", $htmlParts[4]);
            $htmlPartsFive = explode("<td>", $htmlParts[5]);
            $htmlPartsFive = explode("<sup", $htmlPartsFive[1]);

            $listStationsSearch = array_search($htmlPartsZero[0], $listStations);

            if (!$listStationsSearch)
            {
                array_push($listStations, $htmlPartsZero[0]);

                scraperwiki::sqliteexecute("insert into data values (?, ?, ?, ?, ?, ?, ?)", array(strip_tags($htmlPartsZero[0]), strip_tags($htmlPartsOne[1]), strip_tags($htmlPartsTwo[0]), strip_tags($htmlPartsThree[1]), strip_tags($htmlPartsFour[1]), str_replace("\"", "\\\"", strip_tags($htmlPartsFive[0])), strip_tags($spanstext)));
                scraperwiki::sqlitecommit();
            }
        }

        if ($count == 105)
            break;
    }
?>