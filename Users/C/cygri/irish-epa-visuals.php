<?php
    scraperwiki::attach('ireland-epa-enforcement-files', 'enf');            
    $enforcements = scraperwiki::select("* from enf.swdata");
//    $enforcements = scraperwiki::getData('ireland-epa-enforcement-files');
    $enforcement_regnos = array();
    foreach ($enforcements as $row) {
        if (preg_match('/-/', $row['reg'])) continue;
        $enforcement_regnos[] = 'P' . str_pad($row['reg'], 4, '0', STR_PAD_LEFT) . '-01';
    }

    $by_year = array();
    $by_county = array();
    $by_class = array();
    $enforcements_by_class = array();
    scraperwiki::attach('irish-epa-licenses', 'lic');
    $licenses = scraperwiki::select("* from lic.swdata");
//    $licenses = scraperwiki::getData('irish-epa-licenses');
    foreach ($licenses as $c => $row) {
        // skip re-applications
        if (!preg_match('/-01$/', $row['regno'])) continue;
        $year = substr($row['application_date'], 0, 4);
        if (empty($by_year[$year])) $by_year[$year] = 0;
        $by_year[$year] += 1;
        if (!empty($row['county'])) {
            $county = $row['county'];
            if (empty($by_county[$county])) $by_county[$county] = 0;
            $by_county[$county] += 1;
        }
        $class = $row['activity_class_name'];
        if (empty($by_class[$class])) $by_class[$class] = 0;
        $by_class[$class] += 1;
        if (in_array($row['regno'], $enforcement_regnos)) {
            if (empty($enforcements_by_class[$class])) {
                $enforcements_by_class[$class] = 0;
            }
            $enforcements_by_class[$class] += 1;
        }
    }
    ksort($by_year);
    ksort($by_county);
    ksort($by_class);
    ksort($enforcements_by_class);
?>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
google.setOnLoadCallback(makechart);

function makechart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Year');
    data.addColumn('number', 'Applications');
    data.addRows([
<?php
    $i = 0;
    foreach ($by_year as $k => $value) {
        echo "        ['$k', $value],\n";
        $i += 1;
    }
?>
    ]);
    var chart = new google.visualization.BarChart(document.getElementById('by_year'));
    chart.draw(data, {width: 800, height: 300, title: 'IPPC license applications by year'});

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'County');
    data.addColumn('number', 'Applications');
    data.addRows([
<?php 
    $i = 0; 
    foreach ($by_county as $k => $value) {
        echo "        ['$k', $value],\n";
        $i += 1; 
    }
?>
    ]);
    var chart = new google.visualization.BarChart(document.getElementById('by_county'));
    chart.draw(data, {width: 800, height: 500, title: 'IPPC license applications by county'});

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Activity class');
    data.addColumn('number', 'Applications');
    data.addColumn('number', 'Enforcements');
    data.addRows([
<?php
    $i = 0;
    foreach ($by_class as $k => $value) {
        $enf = isset($enforcements_by_class[$k]) ? $enforcements_by_class[$k] : 0;
        echo "        ['$k', $value, $enf],\n";
        $i += 1;
    }
?>
    ]);
    var chart = new google.visualization.BarChart(document.getElementById('by_class'));
    chart.draw(data, {width: 800, height: 300, title: 'IPPC license applications by class of activity'});
}
</script>

<div id="by_year"></div>
<div id="by_county"></div>
<div id="by_class"></div>