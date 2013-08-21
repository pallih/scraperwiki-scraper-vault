<?php

scraperwiki::attach("github_users_each_year");
$data = scraperwiki::select("* from swdata order by `when` desc");

foreach($data as $p){
    $points_new[] = '[' . ( strtotime($p['when']) * 1000 ) . ', ' . $p['new_users'] .']';
    $points_total[] = '[' . ( strtotime($p['when']) * 1000 ) . ', ' . $p['total_users'] .']';
}

$flot_data_new = '[' . join(',', $points_new) . ']';
print_r($flow_data_new);

$flot_data_total = '[' . join(',', $points_total) . ']';

?><!DOCTYPE html>
<html>
    <head>
        <title>Users on GitHub</title>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
        <script type="text/javascript" src="https://media.scraperwiki.com/js/jquery.flot.js"></script>
        <script type="text/javascript">
        $(function(){
            $.plot($('#graph_new'), [{
                data: <?php echo $flot_data_new; ?>,
                bars: { show: true, lineWidth: 10 },
                label:"New users"
            }],{
                yaxis: { 
                    label:"rows"
                },
                xaxis: { 
                    mode: "time",
                    timeformat: "%b %y",
                    tickSize: [2, "month"],
                    monthNames: ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
                }
            });

            $.plot($('#graph_total'), [{
                data: <?php echo $flot_data_total; ?>,
                bars: { show: true, lineWidth: 10 },
                label:"Total users"
            }],{
                yaxis: { 
                    label:"rows"
                },
                xaxis: { 
                    mode: "time",
                    timeformat: "%b %y",
                    tickSize: [2, "month"],
                    monthNames: ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
                }
            });
        });
        </script>
    </head>
    <body>
        <h1>Github signed up users over time</h1>
        <p>See <a href="https://scraperwiki.com/scrapers/github_users_each_year/">Github users each month</a> for the scraper that gathers this data by searching Github.com, and to download it or make SQL queries on it.</p>
        <div id="graph_total" style="width:1000px;height:400px"></div>
        <div id="graph_new" style="width:1000px;height:400px"></div>
    </body>
</html>
