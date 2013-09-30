import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("entrust_projects_html")

all = scraperwiki.sqlite.select("* from entrust_projects_html.swdata")
all_urls = [row["url"] for row in all]

done = scraperwiki.sqlite.select("URL from swdata")
done_urls = [row["URL"] for row in done]

todo_urls = set(all_urls) - set(done_urls)

for url in todo_urls:
    soup = BeautifulSoup(all["html"])

    details = soup.find("dl", "debdetails")


    dds = details.find_all("dd")

    EB_number = dds[0].get_text()
    name = dds[1].get_text()
    county = dds[2].get_text()
    address = dds[3].get_text()
    postcode = dds[4].get_text()
    project_number = dds[5].get_text()
    project_name = dds[6].get_text()
    project_description = dds[7].get_text()
    LCF_value = dds[8].get_text()
    total_vaue = dds[9].get_text()
    start_date = dds[10].get_text()
    completion_date = dds[11].get_text()
    project_postcode = dds[12].get_text()

    data = {"URL": url, "EB_number": EB_number, "Name": name, "County": county, "Address": address, "Postcode": postcode, "Project_Number": project_number, "Project_Name": project_name, "Project_Description": project_description, "LCF_Value": LCF_value, "Total_Value": total_vaue, "Start_Date": start_date, "Completion_Date": completion_date, "Project_Postcode": project_postcode }
    #print data
    scraperwiki.sqlite.save(["URL"], data)


import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("entrust_projects_html")

all = scraperwiki.sqlite.select("* from entrust_projects_html.swdata")
all_urls = [row["url"] for row in all]

done = scraperwiki.sqlite.select("URL from swdata")
done_urls = [row["URL"] for row in done]

todo_urls = set(all_urls) - set(done_urls)

for url in todo_urls:
    soup = BeautifulSoup(all["html"])

    details = soup.find("dl", "debdetails")


    dds = details.find_all("dd")

    EB_number = dds[0].get_text()
    name = dds[1].get_text()
    county = dds[2].get_text()
    address = dds[3].get_text()
    postcode = dds[4].get_text()
    project_number = dds[5].get_text()
    project_name = dds[6].get_text()
    project_description = dds[7].get_text()
    LCF_value = dds[8].get_text()
    total_vaue = dds[9].get_text()
    start_date = dds[10].get_text()
    completion_date = dds[11].get_text()
    project_postcode = dds[12].get_text()

    data = {"URL": url, "EB_number": EB_number, "Name": name, "County": county, "Address": address, "Postcode": postcode, "Project_Number": project_number, "Project_Name": project_name, "Project_Description": project_description, "LCF_Value": LCF_value, "Total_Value": total_vaue, "Start_Date": start_date, "Completion_Date": completion_date, "Project_Postcode": project_postcode }
    #print data
    scraperwiki.sqlite.save(["URL"], data)


