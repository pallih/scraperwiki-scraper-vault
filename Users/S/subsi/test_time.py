# Blank Python

from datetime import datetime, timedelta

print """<html>
<head>
    <title>now</title>
</head>
<body>
    <h3>time</h3>
    <div id="article" class="content">
        <p>%s</p>
    </div>
</body>
</html>
""" % (datetime.utcnow()+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')# Blank Python

from datetime import datetime, timedelta

print """<html>
<head>
    <title>now</title>
</head>
<body>
    <h3>time</h3>
    <div id="article" class="content">
        <p>%s</p>
    </div>
</body>
</html>
""" % (datetime.utcnow()+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')