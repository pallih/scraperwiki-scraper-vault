import scraperwiki
import datetime

scraperwiki.sqlite.attach("iati_registry_update_frequency", "src") 

sql_packagegroups = "name from src.packagegroups"

sql_packagegroup_dates = """distinct rev.date, pkggroup.name
from src.revisions rev 
inner join src.packages pkg on pkg.id=rev.package_id 
inner join src.packagegroups pkggroup on pkggroup.name=pkg.packagegroup_name 
where rev.author = 'iati-archiver' 
and pkggroup.name='%s' 
order by rev.timestamp DESC"""

for packagegroup in scraperwiki.sqlite.select(sql_packagegroups):
    
    packagegroups_date_data = scraperwiki.sqlite.select(sql_packagegroup_dates % (packagegroup['name']))

    tuples = [(datetime.datetime.strptime(packagegroups_date["date"], "%Y-%m-%d").date().year, datetime.datetime.strptime(packagegroups_date["date"], "%Y-%m-%d").date().month) for packagegroups_date in packagegroups_date_data]
    months_numbers = dict((i, tuples.count(i)) for i in tuples)

    for month, numbers in months_numbers.items():
        data = {
            'year': month[0],
            'month': month[1],
            'num_days_updates': numbers,
            'packagegroup_name': packagegroup["name"]
        }
        scraperwiki.sqlite.save(unique_keys=["packagegroup_name", "year","month"],
                data=data,
                table_name="packagegroups_dates_data")

