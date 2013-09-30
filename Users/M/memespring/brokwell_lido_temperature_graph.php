<?php

scraperwiki::attach("brockwell_lido_temperature");
$data = scraperwiki::select("* from swdata order by datetime desc");

foreach($data as $p){
    if(!empty($p['rows'])){
        $points[] = '[' . ( strtotime($p['date_time']) * 1000 ) . ', ' . $p['rows'] . ']';
    }
}

$flot_data = '[' . join(',', $points) . ']';

?><!DOCTYPE html>
<html>
    <head>
        <title>Rows in ScraperWiki datastore</title>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
        <script type="text/javascript" src="https://media.scraperwiki.com/js/jquery.flot.js"></script>
        <script type="text/javascript">
        $(function(){
            $.plot($('#graph'), [{
                data: <?php echo $flot_data; ?>,
                bars: { show: true, lineWidth: 10 },
                label:"Rows of data"
            }],{
                yaxis: { 
                    label:"rows"
                },
                xaxis: { 
                    mode: "time",
                    timeformat: "%d/%m"
                }
            });
        });
        </script>
    </head>
    <body>
        <div id="graph" style="width:800px;height:600px"></div>
    </body>
</html>
<?php

scraperwiki::attach("brockwell_lido_temperature");
$data = scraperwiki::select("* from swdata order by datetime desc");

foreach($data as $p){
    if(!empty($p['rows'])){
        $points[] = '[' . ( strtotime($p['date_time']) * 1000 ) . ', ' . $p['rows'] . ']';
    }
}

$flot_data = '[' . join(',', $points) . ']';

?><!DOCTYPE html>
<html>
    <head>
        <title>Rows in ScraperWiki datastore</title>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
        <script type="text/javascript" src="https://media.scraperwiki.com/js/jquery.flot.js"></script>
        <script type="text/javascript">
        $(function(){
            $.plot($('#graph'), [{
                data: <?php echo $flot_data; ?>,
                bars: { show: true, lineWidth: 10 },
                label:"Rows of data"
            }],{
                yaxis: { 
                    label:"rows"
                },
                xaxis: { 
                    mode: "time",
                    timeformat: "%d/%m"
                }
            });
        });
        </script>
    </head>
    <body>
        <div id="graph" style="width:800px;height:600px"></div>
    </body>
</html>
