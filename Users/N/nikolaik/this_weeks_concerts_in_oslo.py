#Ref:
# - dateutil: http://labix.org/python-dateutil#head-1443e0f14ad5dff07efd465e080d1110920673d8
# - jinja2: http://jinja.pocoo.org/docs/
# - moment.js: http://momentjs.com/docs/#/displaying/calendar-time/
# - datatables: http://www.datatables.net/blog/Twitter_Bootstrap_2
import scraperwiki

from jinja2 import Template

from datetime import *
from dateutil.relativedelta import *
import calendar

sourcescraper = 'concerts_in_oslo_w_metadata'

scraperwiki.sqlite.attach("concerts_in_oslo_w_metadata")

TODAY= date.today()
next_sunday = TODAY+relativedelta(weekday=calendar.SUNDAY)
if next_sunday == TODAY:
    next_sunday += relativedelta(days=7)

sql_one_week = "* from `concerts_in_oslo` where start_datetime < '%s' and start_datetime > date('now') order by start_datetime" % next_sunday
events = scraperwiki.sqlite.select(sql_one_week)
template = Template('''
<thead>
    <tr>
        <th>Name</th>
        <th>When</th>
        <th>Where</th>
        <th>Description</th>
    </tr>
</thead>
{% for event in events %}
    <tr>
        <td class="span4"><a href="{{ event.url }}">{{ event.name }}</a></td>
        <td><i class="icon-time"></i> <span class="event-start-datetime">{{ event.start_datetime }}</span></td>
        <td><i class="icon-map-marker"></i> {{ event.venue }}</td>
        <td class="span5">{{ event.description }}</td>
    </tr>
{% endfor %}
''')
output_table_rows = template.render(events=events)

print """<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">
        <link href="//netdna.bootstrapcdn.com/font-awesome/3.0.2/css/font-awesome.css" rel="stylesheet">
        <link href="//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/css/jquery.dataTables.css" rel="stylesheet">

        <style>
            table.table thead .sorting,
            table.table thead .sorting_asc,
            table.table thead .sorting_desc,
            table.table thead .sorting_asc_disabled,
            table.table thead .sorting_desc_disabled {
                cursor: pointer;
                *cursor: hand;
            }
             
            table.table thead .sorting { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_both.png') no-repeat center right; }
            table.table thead .sorting_asc { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_asc.png') no-repeat center right; }
            table.table thead .sorting_desc { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_desc.png') no-repeat center right; }
             
            table.table thead .sorting_asc_disabled { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_asc_disabled.png') no-repeat center right; }
            table.table thead .sorting_desc_disabled { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_desc_disabled.png') no-repeat center right; }
        </style>
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->
    
        <header>
        </header>
        <section class="container-fluid">
            <div class="span12">
                <h2>This weeks concerts in Oslo</h2>
                <table cellpadding="0" cellspacing="0" border="0" class="this-weeks-concerts table table-striped table-bordered">
                    %s
                </table>
            </div>

        </section
        <footer>
        </footer>

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.9.0.min.js"><\/script>')</script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/moment.js/2.0.0/moment.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/jquery.dataTables.min.js"></script>


        <script>
            $(document).ready(function() {
                $(".event-start-datetime").each(function( index ) {
                    /* 2013-03-27T00:00:00 */
                    var m = moment($(this).text(), "YYYY-MM-DDT HH:mm:ss");
                    $(this).html(m.calendar());
                });
                $(".this-weeks-concerts").dataTable({
                    "sDom": "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>",
                    "aaSorting": []
                });
                $.extend( $.fn.dataTableExt.oStdClasses, {
                    "sWrapper": "dataTables_wrapper form-inline"
                } );
            });
        </script>
    </body>
</html>
""" % output_table_rows#Ref:
# - dateutil: http://labix.org/python-dateutil#head-1443e0f14ad5dff07efd465e080d1110920673d8
# - jinja2: http://jinja.pocoo.org/docs/
# - moment.js: http://momentjs.com/docs/#/displaying/calendar-time/
# - datatables: http://www.datatables.net/blog/Twitter_Bootstrap_2
import scraperwiki

from jinja2 import Template

from datetime import *
from dateutil.relativedelta import *
import calendar

sourcescraper = 'concerts_in_oslo_w_metadata'

scraperwiki.sqlite.attach("concerts_in_oslo_w_metadata")

TODAY= date.today()
next_sunday = TODAY+relativedelta(weekday=calendar.SUNDAY)
if next_sunday == TODAY:
    next_sunday += relativedelta(days=7)

sql_one_week = "* from `concerts_in_oslo` where start_datetime < '%s' and start_datetime > date('now') order by start_datetime" % next_sunday
events = scraperwiki.sqlite.select(sql_one_week)
template = Template('''
<thead>
    <tr>
        <th>Name</th>
        <th>When</th>
        <th>Where</th>
        <th>Description</th>
    </tr>
</thead>
{% for event in events %}
    <tr>
        <td class="span4"><a href="{{ event.url }}">{{ event.name }}</a></td>
        <td><i class="icon-time"></i> <span class="event-start-datetime">{{ event.start_datetime }}</span></td>
        <td><i class="icon-map-marker"></i> {{ event.venue }}</td>
        <td class="span5">{{ event.description }}</td>
    </tr>
{% endfor %}
''')
output_table_rows = template.render(events=events)

print """<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">
        <link href="//netdna.bootstrapcdn.com/font-awesome/3.0.2/css/font-awesome.css" rel="stylesheet">
        <link href="//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/css/jquery.dataTables.css" rel="stylesheet">

        <style>
            table.table thead .sorting,
            table.table thead .sorting_asc,
            table.table thead .sorting_desc,
            table.table thead .sorting_asc_disabled,
            table.table thead .sorting_desc_disabled {
                cursor: pointer;
                *cursor: hand;
            }
             
            table.table thead .sorting { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_both.png') no-repeat center right; }
            table.table thead .sorting_asc { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_asc.png') no-repeat center right; }
            table.table thead .sorting_desc { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_desc.png') no-repeat center right; }
             
            table.table thead .sorting_asc_disabled { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_asc_disabled.png') no-repeat center right; }
            table.table thead .sorting_desc_disabled { background: url('//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/images/sort_desc_disabled.png') no-repeat center right; }
        </style>
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->
    
        <header>
        </header>
        <section class="container-fluid">
            <div class="span12">
                <h2>This weeks concerts in Oslo</h2>
                <table cellpadding="0" cellspacing="0" border="0" class="this-weeks-concerts table table-striped table-bordered">
                    %s
                </table>
            </div>

        </section
        <footer>
        </footer>

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.9.0.min.js"><\/script>')</script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/moment.js/2.0.0/moment.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/datatables/1.9.4/jquery.dataTables.min.js"></script>


        <script>
            $(document).ready(function() {
                $(".event-start-datetime").each(function( index ) {
                    /* 2013-03-27T00:00:00 */
                    var m = moment($(this).text(), "YYYY-MM-DDT HH:mm:ss");
                    $(this).html(m.calendar());
                });
                $(".this-weeks-concerts").dataTable({
                    "sDom": "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>",
                    "aaSorting": []
                });
                $.extend( $.fn.dataTableExt.oStdClasses, {
                    "sWrapper": "dataTables_wrapper form-inline"
                } );
            });
        </script>
    </body>
</html>
""" % output_table_rows