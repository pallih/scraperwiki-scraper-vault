<?php 
scraperwiki::attach("usa_unemployment_history");

global $checkboxDefault;
$checkboxDefault = 'On';

$graphWidth = 800;
$graphHeight = 600;

$chartTypes = array(
    'Pie' => 'Pie',
    'Bar' => 'Bar',
    'Area' => 'Area',
    'Column' => 'Column',
    'Line' => 'Line',
    'Table' => 'Table',
);

$axisPos = array(
    'Pie' => null,
    'Bar' => 'hAxis',
    'Area' => 'vAxis',
    'Column' => 'vAxis',
    'Line' => 'vAxis',
    'Table' => 'vAxis'
);

$whereFields = array(
    'monthyear' => 'Month / Year',
    'race' => 'Race',
    'age' => 'Age',
    'sex' => 'Sex'
);
$selectFields = array(
    'total_employed_in_labor_force' => 'Total Employed In Labor Force',
    'total_unemployed_in_labor_force' => 'Total Unemployed In Labor Force',
    'total_civilian_labor_force' => 'Total Civilian Labor Force',
    'not_in_labor_force' => 'Not In Labor Force',
    'percent_unemployed_in_labor_force' => 'Percent Unemployed In Labor Force',
    'percent_employed_in_labor_force' => 'Percent Employed In Labor Force',
    'civilian_noninstitional_population' => 'Civilian Non-Institutional Population',
    'percent_of_population_in_labor_force' => 'Percent Of Population In Labor Force'
);

$selectData = array();
$chartWhere = array();
$where = array();
$whereVals = array();

if (! array_key_exists('chart-type', $_GET))
    $_GET['chart-type'] = '';

if ($_GET['chart-type'] == 'Table')
    $chartType = $_GET['chart-type'];
else
    $chartType = $_GET['chart-type'] . "Chart";

foreach ($whereFields as $field => $value) {
    if (! array_key_exists($field, $_GET))
        $_GET[$field] = '';
    if (! array_key_exists('group' . $field, $_GET))
        $_GET['group' . $field] = '';
}
foreach ($selectFields as $field => $value) {
    if (! array_key_exists($field, $_GET))
        $_GET[$field] = '';
}

foreach ($whereFields as $key => $value) {
    $selectData[$key] = scraperwiki::sqliteexecute("SELECT DISTINCT `{$key}` from `unemployment_data` WHERE {$key} != ''");

    if ($key == 'monthyear') {
        $data = $selectData[$key];
        foreach ($data->data as $k => $v) {
            $dt = new DateTime($v[0]);
            $data->data[$k][0] = $dt->format('F Y');
        }
    }

    if ($_GET[$key] !== '') {
        $chartWhere[] = $key;
        $where[] = " `{$key}` = ?";
        $whereVals[] = $_GET[$key];
    }
}

$columns = array();
foreach ($selectFields as $key => $value) {
    if (array_key_exists($key, $_GET) && $_GET[$key] == $checkboxDefault)
        $columns[] = $key;
}

if (count($columns) == 0) $columns[] = "*";

?>
<!DOCTYPE html>
<html>
    <head>
        <title>USA Unemployment Viewer</title>
        <link href='https://fonts.googleapis.com/css?family=Kaushan+Script|Galdeano' rel='stylesheet' type='text/css'>
        <style type="text/css">
            <!-- 
                body {
                height: 1000px;
                /* begin funky bg noize. For some great info: http://snook.ca/archives/html_and_css/multiple-bg-css-gradients */
                background-image: -webkit-gradient(linear, 0 top,  0 bottom, from(#fff), to(#666));
                background-image: -moz-linear-gradient(rgba(255,255,255,0), rgba(0,0,0,0));
                background-repeat: repeat-x;
                color: black;
                font-family: 'Galdeano', sans-serif;
                }       
                h1#title {font-size: 3em;}
                h1#title a {color: #ccc; text-decoration: none;}
                .center { width: 925px; margin-left: auto; margin-right: auto; }
                form { overflow: hidden; }
                form div { display: block; }
                #fields-to-graph label { width: 230px; display: inline-block; }
                #limit-data label, #group-data label { width: 100px; display: inline-block; }
                #fields-to-graph, #limit-data, #group-data { float: left; margin-right: 2em; }
                #chart_div { margin-left: auto; margin-right: auto; width: <?php echo $graphWidth; ?>px; margin-top: 1em; }
            -->
        </style>
    <script>
    function drawChart() {
    <?php
    if (count($where) > 0 || $columns[0] != '*'):
        $dataColumns = $columns;
        $scraperWikiSelectColumns = array_map(function($v) { return "SUM({$v} * 1000) AS $v"; }, $columns);
 
        $group = array();
        $stringColumns = array();
        foreach ($whereFields as $key => $value) {
            if (array_key_exists('group' . $key, $_GET) && $_GET['group' . $key] == $checkboxDefault) {
                $stringColumns[] = $group[] = $key;
                $columns[] = $key;
            }
        }

        $scraperWikiSelectColumns = array_merge($scraperWikiSelectColumns, $stringColumns);

        $select = implode(", ", $scraperWikiSelectColumns) . " FROM `unemployment_data`";
        $select .= " WHERE 1 = 1";
        if (count($where) > 0) {
            $select .= " AND " . implode(" AND ", $where);
        }

        if (count($group) > 0) {
            $select .= " GROUP BY " . implode(", ", $group);
            $select .= " ORDER BY " . implode(" ASC, ", $group);
        }

        echo "/* $select */";

        $data = scraperwiki::select($select, $whereVals);

        $outputData = array();
        foreach ($data as $key => $value) {
            $od = array();
            foreach ($stringColumns as $column) {
                if ($column == 'monthyear' && preg_match('/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$/', $value[$column])) {
                    $dt = new DateTime($value[$column]);
                    $value[$column] = $dt->format('F Y');
                }
                $od[] = $value[$column];
            }
            foreach ($dataColumns as $column)
                $od[] = preg_replace('/,/', '', $value[$column]) + 0;
            $outputData[] = $od; 
        }

        $chartTitle = 'US Unemployment Information';
        if (count($group) > 0) {
            $chartTitle .= ', by ' . implode(", ", array_map(function($a) { global $whereFields; return $whereFields[$a]; }, $group));
        }
        if (count($where) > 0) {
            $chartTitle .= " for " . implode(", ", array_map(function($a) { global $whereFields; return $whereFields[$a] . " = " . $_GET[$a]; }, $chartWhere));
        }

    ?>
                var data = new google.visualization.DataTable();
                <?php foreach ($stringColumns as $column): ?>
                data.addColumn('string', '<?php echo htmlentities($whereFields[$column], ENT_QUOTES, 'UTF-8') ?>');
                <?php endforeach; ?>
                <?php foreach ($dataColumns as $column): ?>
                data.addColumn('number', '<?php echo htmlentities($selectFields[$column], ENT_QUOTES, 'UTF-8') ?>');
                <?php endforeach; ?>
                data.addRows(<?php echo json_encode($outputData); ?>);
                
                var options = {
                    'title':'<?php echo htmlentities($chartTitle, ENT_QUOTES, 'UTF-8') ?>',
                    'width': <?php echo $graphWidth ?>,
                    'height': <?php echo $graphHeight ?>,
                    '<?php echo $axisPos[$_GET['chart-type']] ?>': { 'title': 'Values' }
                };
                
                var chart = new google.visualization.<?php echo $chartType ?>(document.getElementById('chart_div'));
                var formatter = new google.visualization.NumberFormat({negativeColor: 'red', negativeParens: true, pattern:'#,###' });
                <?php $column = count($stringColumns); ?>
                <?php foreach ($dataColumns as $c): ?>
                formatter.format(data, <?php echo $column++ ?>);
                <?php endforeach; ?>
                chart.draw(data, options);
    <?php endif; ?>
            }
        </script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load('visualization', '1.0', {'packages':['corechart', 'table']});
            google.setOnLoadCallback(drawChart);
        </script>
    </head>
    <body>
        <h1 class="center" id="title">USA Unemployment Viewer, by <a href="http://www.dp.cx/blog">Glen Solsberry</a></h1>
        <h2 class="center" id="data-source">Data Sourced From The <a href="http://www.bls.gov/web/empsit/cpseea13.htm">US Bureau of Labor Statistics</a></h2>
        <form class="center" method="get" action="">
            <div id="fields-to-graph">
                <h3>Choose some fields to graph</h3>
                <?php foreach ($selectFields as $key => $value): ?>
                <?php generateSelectField($key, $value, $_GET[$key]); ?>
                <?php endforeach; ?>
            </div>
            <div id="limit-data">
                <h3>Limit your data to the following values</h3>
                <?php foreach ($whereFields as $key => $value): ?>
                <?php generateWhereField($key, $value, $selectData[$key]->data, $_GET[$key]); ?>
                <?php endforeach; ?>
            </div>
            <div id="group-data">
                <h3>Group your data</h3>
                <?php foreach ($whereFields as $key => $value): ?>
                <?php generateSelectField('group' . $key, $value, $_GET['group' . $key]); ?>
                <?php endforeach; ?>
            </div>
            <div id="chart-type">
                <h3>Chart Type</h3>
                <?php generateWhereField('chart-type', null, $chartTypes, $_GET['chart-type'], false); ?>
            </div>
    
            <input type="submit" />
        </form>

        <div id="chart_div"></div>

    </body>
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-64589-12']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</html>

<?php

function generateWhereField($fieldname, $fieldoutput, $values, $selectedVal, $showLabel = true) {
    echo <<<FIELD
    <div id="field{$fieldname}">
FIELD;

    if ($showLabel) {
        echo <<<FIELD
    <label for="{$fieldname}">{$fieldoutput}</label>
FIELD;
    }

    echo <<<FIELD
    <select name="{$fieldname}" id="{$fieldname}">
        <option value="">Choose One...</option>
FIELD;
    
    foreach ($values as $key) {
        
        if ((is_array($key) && $key[0] == $selectedVal) || $key == $selectedVal) {
            $selected = ' selected="selected"';
        } else {
            $selected = '';
        }
        
        $key = htmlentities(is_array($key) ? $key[0] : $key, ENT_QUOTES, 'UTF-8');
        echo "<option value=\"{$key}\"$selected>{$key}</option>";
    }

    echo <<<FIELD
    </select>
    </div>
FIELD;
}

function generateSelectField($fieldname, $fieldoutput, $selected) {
    global $checkboxDefault;    

    if ($selected == $checkboxDefault) $checked = ' checked="checked"';
    else $checked = '';

    echo <<<FIELD
    <div id="field{$fieldname}">
    <label for="{$fieldname}">{$fieldoutput}</label>
    <input type="checkbox" name="{$fieldname}" id="{$fieldname}" value="{$checkboxDefault}"{$checked}>
    </div>
FIELD;
}
