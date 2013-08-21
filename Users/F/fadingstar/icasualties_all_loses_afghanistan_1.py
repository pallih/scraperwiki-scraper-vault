import scraperwiki           
import lxml.html

try:
    scraperwiki.sqlite.execute("""
        create table icasualities_plus
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        ) 
    """)
except:
    print "Table probably already exists."


states = ["Nationality.aspx?hndQry=US","Nationality.aspx?hndQry=Australia","Nationality.aspx?hndQry=Belgium","Nationality.aspx?hndQry=Canada","Nationality.aspx?hndQry=Czech","Nationality.aspx?hndQry=Denmark","Nationality.aspx?hndQry=Estonia","Nationality.aspx?hndQry=Finland","Nationality.aspx?hndQry=France","Nationality.aspx?hndQry=Georgia","Nationality.aspx?hndQry=Germany","Nationality.aspx?hndQry=Hungary","Nationality.aspx?hndQry=Italy","Nationality.aspx?hndQry=Jordan","Nationality.aspx?hndQry=Latvia","Nationality.aspx?hndQry=Lithuania","Nationality.aspx?hndQry=NATO","Nationality.aspx?hndQry=Netherlands","Nationality.aspx?hndQry=New Zealand","Nationality.aspx?hndQry=Norway","Nationality.aspx?hndQry=Poland","Nationality.aspx?hndQry=Portugal","Nationality.aspx?hndQry=Romania","Nationality.aspx?hndQry=South Korea","Nationality.aspx?hndQry=Spain","Nationality.aspx?hndQry=Sweden","Nationality.aspx?hndQry=Turkey","Nationality.aspx?hndQry=UK"]

for s in states:    
    html = scraperwiki.scrape("http://icasualties.org/OEF/"+s)
    root = lxml.html.fromstring(html)
    
    rows = root.cssselect("table#ctl00_ContentPlaceHolder1_GridView1 tr")  # selects all <tr> blocks within <table class="data">
    #print rows
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record = {}
            Name = table_cells[1].text_content()
            #print Name
            Date = table_cells[0].text_content()
            #print Date
            Rank = table_cells[2].text_content()
            Unit = table_cells[4].text_content()
            Age = table_cells[3].text_content()
            Branch = table_cells[5].text_content()
            State = table_cells[6].text_content()
            City = table_cells[7].text_content()
            Cause = table_cells[8].text_content()
            Place_of_Death = table_cells[9].text_content()
            Died_In = table_cells[10].text_content()
            
            scraperwiki.sqlite.save(unique_keys=["Name"], data={"Name":Name, "Date":Date, "Rank" : Rank, "Age":Age, "Unit": Unit, "Branch": Branch, "State": State, "City": City, "Cause": Cause, "Place_of_Death": Place_of_Death, "Died_In": Died_In, "Nationality": s[24:]}, table_name='icasualities_plus')