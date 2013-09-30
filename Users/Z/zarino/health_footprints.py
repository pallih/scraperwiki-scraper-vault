import scraperwiki
import json
import cgi, os

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

scraperwiki.sqlite.attach('un_life_expectancy_scores', 'lei')

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `trips` (`doctor_gmc` INT, `doctor_fundedby` TEXT, `hospital` TEXT, `department` TEXT, `subspecialty` TEXT, `location` TEXT, `duration` INT, `year` INT, `month` INT)')
scraperwiki.sqlite.commit()

countries = []
cc = scraperwiki.sqlite.select('country from lei.swdata order by country')
for c in cc:
    countries.append(c['country'].strip())

print """
<!doctype html>
<html>
<head>
    <title>Health Footprints</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta charset="UTF-8">
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap.min.css" rel="stylesheet">
    <style type="text/css">
        body {
            font-size: 21px;
            line-height: 30px;
            background: #f3f3f3;
        }
        h1 {
            padding: 20px 0 10px;
            border-bottom: 1px solid #ccc;
            margin-bottom: 15px;
        }
        form {
            margin-top: 15px;
        }
        form h2 {
            margin-top: 0;
            padding-top: 0;
        }
        #trips {
            display: none;
        }
        label, input, button, select, textarea {
            font-size: 16px;
            line-height: 22px;
        }
        #you, #trips {
            padding: 20px 0;
            border-top: 1px solid #ccc;
        }

        #save {
            text-align: center;
            padding: 20px;
            border-top: 1px solid #ccc;
        }
        input {
            width: 270px;
        }
        select {
            width: 284px;
        }
    </style>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
    <script type="text/javascript" src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
    <script type="text/javascript">

countries = %s;

// neat little wrapper around the ScraperWiki API
function sql_api(scrapername, sql, apikey){
    return $.ajax({
        url: "https://api.scraperwiki.com/api/1.0/datastore/sqlite",
        data: {
            format: 'jsondict',
            name: scrapername,
            query: sql
        }, 
        dataType: 'jsonp',
        timeout : 5000
    });
}
        
$(function(){
    
    $('#doctor_gmc').on('blur', function(){
        if($(this).val() != ''){
            var gmc = $(this).val();
            sql_api('health_footprints', 'select * from trips where doctor_gmc="' + gmc + '" order by rowid desc limit 1').done(function(data){
                console.log(data);
                if(data.length){
                    
                } else {
                    $('#trips h2').text('Your volunteering record is empty');
                }
                $('#trips').slideDown();
            });
        }
    });

    $('#add_trip').on('click', function(e){
        e.preventDefault();
        $(this).find('span').text('another');
        var new_trip = $('<div>');
        var trip_no = $('#trips .trip').length + 1;

        var country_select = $('<select id="country_' + trip_no + '" name="country_' + trip_no + '"></select>');
        $.each(countries, function(i, country){
            country_select.append('<option value="' + country + '">' + country + '</option>');
        });
        $('<div class="row">').append( $('<p class="span4">').append('<label for="country_' + trip_no + '">Destination</label>').append(country_select) ).append('<p class="span4"><label for="duration_' + trip_no + '">Duration (in days)</label><input type="text" id="duration_' + trip_no + '" name="duration_' + trip_no + '" />').appendTo(new_trip);

        $('<div class="row">').append('<p class="span4"><label for="year_' + trip_no + '">Year</label><input type="text" id="year_' + trip_no + '" name="year_' + trip_no + '" /></p><p class="span4"><label for="month_' + trip_no + '">Month</label><input type="text" id="month_' + trip_no + '" name="month_' + trip_no + '" /></p>').appendTo(new_trip);

        new_trip.insertBefore($(this).parent());
    });
    
});
        
    </script>
</head>
<body class="row container">
    <h1 class="span8 offset2">Health Footprints <small>by Dr Alex</small></h1>
    <p class="span8 offset2">Narrowing the global health divide by introducing a culture of &lsquo;health offsetting&rsquo; to the NHS.</p>
    <p class="span8 offset2">Tell us about yourself and your medical volunteering work, and we&rsquo;ll find out how you stand up against your department, your hospital, and the rest of the UK.</p>
    <form class="span8 offset2">
        <div id="you">
            <h2>About you</h2>
            <div class="row">
                <p class="span4">
                    <label for="doctor_gmc">GMC Number</label>
                    <input type="text" id="doctor_gmc" name="doctor_gmc" />
                </p>
                <p class="span4">
                    <label for="hospital">Hospital</label>
                    <select id="hospital" name="hospital">
                        <option value="Manchester Royal Infirmary">Manchester Royal Infirmary</option>
                        <option value="Moorfields Eye Hospital">Moorfields Eye Hospital</option>
                        <option value="Royal Liverpool University Hospital">Royal Liverpool University Hospital</option>
                    </select>
                </p>
            </div>
            <div class="row">
                <p class="span4">
                    <label for="department">Department</label>
                    <select id="department" name="department">
                        <option value="Accident and emergency">Accident and emergency</option>
                        <option value="Cardiology">Cardiology</option>
                        <option value="Ear, nose and throat">Ear, nose and throat</option>
                        <option value="Haematology">Haematology</option>
                        <option value="Ophthalmology">Ophthalmology</option>
                        <option value="Plastic surgery">Plastic surgery</option>
                        <option value="Renal">Renal</option>
                    </select>
                </p>
                <p class="span4">
                    <label for="subspecialty">Sub-specialty</label>
                    <select id="subspecialty" name="subspecialty">
                        <option value="General">General</option>
                        <option value="Cataract">Cataract</option>
                        <option value="Glaucoma">Glaucoma</option>
                        <option value="Plastics">Plastics</option>
                        <option value="Paediatrics">Paediatrics</option>
                    </select>
                </p>
            </div>
            <div>
                <p>
                    <label for="doctor_fundedby">Country that paid for your medical degree</label>
                    <select id="doctor_fundedby">""" % json.dumps(countries)

for country in countries:
    print """
                        <option value="%s">%s</option>""" % (country, country)
print """
                    </select>
                </p>
            </div>
        </div>
        <div id="trips">
            <h2>Your volunteering record</h2>
            <p class="well"><a class="btn" href="#" id="add_trip"><i class="icon-plus"></i> Add <span>a</span> volunteering trip</a></p>
        </div>
        <div id="save">
            <button type="submit" class="btn btn-primary">Save my details!</button>
        </div>
    </form>    
</body>
</html>
"""import scraperwiki
import json
import cgi, os

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

scraperwiki.sqlite.attach('un_life_expectancy_scores', 'lei')

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `trips` (`doctor_gmc` INT, `doctor_fundedby` TEXT, `hospital` TEXT, `department` TEXT, `subspecialty` TEXT, `location` TEXT, `duration` INT, `year` INT, `month` INT)')
scraperwiki.sqlite.commit()

countries = []
cc = scraperwiki.sqlite.select('country from lei.swdata order by country')
for c in cc:
    countries.append(c['country'].strip())

print """
<!doctype html>
<html>
<head>
    <title>Health Footprints</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta charset="UTF-8">
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap.min.css" rel="stylesheet">
    <style type="text/css">
        body {
            font-size: 21px;
            line-height: 30px;
            background: #f3f3f3;
        }
        h1 {
            padding: 20px 0 10px;
            border-bottom: 1px solid #ccc;
            margin-bottom: 15px;
        }
        form {
            margin-top: 15px;
        }
        form h2 {
            margin-top: 0;
            padding-top: 0;
        }
        #trips {
            display: none;
        }
        label, input, button, select, textarea {
            font-size: 16px;
            line-height: 22px;
        }
        #you, #trips {
            padding: 20px 0;
            border-top: 1px solid #ccc;
        }

        #save {
            text-align: center;
            padding: 20px;
            border-top: 1px solid #ccc;
        }
        input {
            width: 270px;
        }
        select {
            width: 284px;
        }
    </style>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
    <script type="text/javascript" src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
    <script type="text/javascript">

countries = %s;

// neat little wrapper around the ScraperWiki API
function sql_api(scrapername, sql, apikey){
    return $.ajax({
        url: "https://api.scraperwiki.com/api/1.0/datastore/sqlite",
        data: {
            format: 'jsondict',
            name: scrapername,
            query: sql
        }, 
        dataType: 'jsonp',
        timeout : 5000
    });
}
        
$(function(){
    
    $('#doctor_gmc').on('blur', function(){
        if($(this).val() != ''){
            var gmc = $(this).val();
            sql_api('health_footprints', 'select * from trips where doctor_gmc="' + gmc + '" order by rowid desc limit 1').done(function(data){
                console.log(data);
                if(data.length){
                    
                } else {
                    $('#trips h2').text('Your volunteering record is empty');
                }
                $('#trips').slideDown();
            });
        }
    });

    $('#add_trip').on('click', function(e){
        e.preventDefault();
        $(this).find('span').text('another');
        var new_trip = $('<div>');
        var trip_no = $('#trips .trip').length + 1;

        var country_select = $('<select id="country_' + trip_no + '" name="country_' + trip_no + '"></select>');
        $.each(countries, function(i, country){
            country_select.append('<option value="' + country + '">' + country + '</option>');
        });
        $('<div class="row">').append( $('<p class="span4">').append('<label for="country_' + trip_no + '">Destination</label>').append(country_select) ).append('<p class="span4"><label for="duration_' + trip_no + '">Duration (in days)</label><input type="text" id="duration_' + trip_no + '" name="duration_' + trip_no + '" />').appendTo(new_trip);

        $('<div class="row">').append('<p class="span4"><label for="year_' + trip_no + '">Year</label><input type="text" id="year_' + trip_no + '" name="year_' + trip_no + '" /></p><p class="span4"><label for="month_' + trip_no + '">Month</label><input type="text" id="month_' + trip_no + '" name="month_' + trip_no + '" /></p>').appendTo(new_trip);

        new_trip.insertBefore($(this).parent());
    });
    
});
        
    </script>
</head>
<body class="row container">
    <h1 class="span8 offset2">Health Footprints <small>by Dr Alex</small></h1>
    <p class="span8 offset2">Narrowing the global health divide by introducing a culture of &lsquo;health offsetting&rsquo; to the NHS.</p>
    <p class="span8 offset2">Tell us about yourself and your medical volunteering work, and we&rsquo;ll find out how you stand up against your department, your hospital, and the rest of the UK.</p>
    <form class="span8 offset2">
        <div id="you">
            <h2>About you</h2>
            <div class="row">
                <p class="span4">
                    <label for="doctor_gmc">GMC Number</label>
                    <input type="text" id="doctor_gmc" name="doctor_gmc" />
                </p>
                <p class="span4">
                    <label for="hospital">Hospital</label>
                    <select id="hospital" name="hospital">
                        <option value="Manchester Royal Infirmary">Manchester Royal Infirmary</option>
                        <option value="Moorfields Eye Hospital">Moorfields Eye Hospital</option>
                        <option value="Royal Liverpool University Hospital">Royal Liverpool University Hospital</option>
                    </select>
                </p>
            </div>
            <div class="row">
                <p class="span4">
                    <label for="department">Department</label>
                    <select id="department" name="department">
                        <option value="Accident and emergency">Accident and emergency</option>
                        <option value="Cardiology">Cardiology</option>
                        <option value="Ear, nose and throat">Ear, nose and throat</option>
                        <option value="Haematology">Haematology</option>
                        <option value="Ophthalmology">Ophthalmology</option>
                        <option value="Plastic surgery">Plastic surgery</option>
                        <option value="Renal">Renal</option>
                    </select>
                </p>
                <p class="span4">
                    <label for="subspecialty">Sub-specialty</label>
                    <select id="subspecialty" name="subspecialty">
                        <option value="General">General</option>
                        <option value="Cataract">Cataract</option>
                        <option value="Glaucoma">Glaucoma</option>
                        <option value="Plastics">Plastics</option>
                        <option value="Paediatrics">Paediatrics</option>
                    </select>
                </p>
            </div>
            <div>
                <p>
                    <label for="doctor_fundedby">Country that paid for your medical degree</label>
                    <select id="doctor_fundedby">""" % json.dumps(countries)

for country in countries:
    print """
                        <option value="%s">%s</option>""" % (country, country)
print """
                    </select>
                </p>
            </div>
        </div>
        <div id="trips">
            <h2>Your volunteering record</h2>
            <p class="well"><a class="btn" href="#" id="add_trip"><i class="icon-plus"></i> Add <span>a</span> volunteering trip</a></p>
        </div>
        <div id="save">
            <button type="submit" class="btn btn-primary">Save my details!</button>
        </div>
    </form>    
</body>
</html>
"""