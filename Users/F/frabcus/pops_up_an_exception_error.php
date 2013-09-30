<?php

function print_date($when) {
    print $when->format(DATE_ISO8601) . "\n"; 
}

$when = date_create('21 June 2010'); print_date($when); # 2010-06-21T00:00:00+0100
$when = date_create('10-Jul-1899'); print_date($when);  # 1899-07-10T00:00:00+0100
$when = date_create('01/01/01'); print_date($when);     # 2001-01-01T00:00:00+0100

print get_class(date_create('21 June 2010')) . "\n"; # DateTime




$when = date_create('Tue 27 Sep 2011 00:25:48 BST'); print_date($when); # 2011-09-27T00:25:48+0100
$when = date_create('3/2/1999'); print_date($when); # 1999-03-02T00:00:00+0000


print getlocale()

<?php

function print_date($when) {
    print $when->format(DATE_ISO8601) . "\n"; 
}

$when = date_create('21 June 2010'); print_date($when); # 2010-06-21T00:00:00+0100
$when = date_create('10-Jul-1899'); print_date($when);  # 1899-07-10T00:00:00+0100
$when = date_create('01/01/01'); print_date($when);     # 2001-01-01T00:00:00+0100

print get_class(date_create('21 June 2010')) . "\n"; # DateTime




$when = date_create('Tue 27 Sep 2011 00:25:48 BST'); print_date($when); # 2011-09-27T00:25:48+0100
$when = date_create('3/2/1999'); print_date($when); # 1999-03-02T00:00:00+0000


print getlocale()

