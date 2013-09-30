import scraperwiki

scraperwiki.sqlite.attach("entrust")
scraperwiki.sqlite.attach("entrust_projects_info")

scraperwiki.sqlite.execute("drop table if exists swdata")

scraperwiki.sqlite.execute(
    """create table swdata as
          select epi.*, e.Object
          from entrust.swdata e 
          inner join entrust_projects_info.swdata epi 
          on e.URL == epi.URL
    """
)

scraperwiki.sqlite.commit()
import scraperwiki

scraperwiki.sqlite.attach("entrust")
scraperwiki.sqlite.attach("entrust_projects_info")

scraperwiki.sqlite.execute("drop table if exists swdata")

scraperwiki.sqlite.execute(
    """create table swdata as
          select epi.*, e.Object
          from entrust.swdata e 
          inner join entrust_projects_info.swdata epi 
          on e.URL == epi.URL
    """
)

scraperwiki.sqlite.commit()
