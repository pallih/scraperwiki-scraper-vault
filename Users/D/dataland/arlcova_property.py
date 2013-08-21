import scraperwiki
import lxml.html
import urllib
import datetime

#TODO- need to get sales codes table.

base_url = "http://arlingtonva.us/Departments/RealEstate/reassessments/scripts/"

scraperwiki.sqlite.attach("tester2") 
linkloop = scraperwiki.sqlite.select("detail_link from s_detail_link order by tmsp_queried asc")
for link in linkloop:

    detail_link = link.values()[0]
    final_url = base_url + detail_link
    html = scraperwiki.scrape(final_url)
    root = lxml.html.fromstring(html)

    # Just get html of page for now so we can practice debug later
    
    # Perform s_html record insert

    html_now = datetime.datetime.now()
    html_data = {"detail_link":detail_link, "tmsp_captured":str(html_now), "final_url":final_url, "html":html}
    scraperwiki.sqlite.save(unique_keys=["final_url"], data=html_data, table_name="s_html")
    print "finished " + detail_link

#    this_parcel_row = 0
#    
#    for count, tr in enumerate(root.cssselect('tr')):
#        row = [td.text_content() for td in tr.cssselect('td')]
#        
#        # Test row length. In some cases empty collection rows are returned
#        if len(row)>=1:
#    
#            # Determine rows that constitute address information.  These rows don't have field labels, and row location fluctuates depending
#            # on record type. Will use locations determined in 2nd pass over record to get address information.
#            if row[0] == 'Owner Name and Address:':
#                owner_data_starts = count+1
#            if row[0] == 'Tax Exempt Code:':
#                tax_exempt_row = count
#            if row [0] == 'Property Class:':
#                property_class_row = count
#        
#            # Determine if informational row present between end of sales data and view sales in this neighborhood
#            if row[0][0:11] == 'This parcel':
#                this_parcel_row = count
#            # Locate start of assessment data
#            if row[0] == 'EFFECTIVE DATE':
#                first_assessment_data_row = count+1
#            # Locate end of assessment data and start of sales data
#            if row[0] == 'SALES DATE':
#                first_sales_data_row = count+1
#                last_assessment_data_row = count-1
#            # Locate end of sales data
#            if row[0] == 'VIEW SALES IN THIS NEIGHBORHOOD':
#                if this_parcel_row > 0:
#                    last_sales_data_row = this_parcel_row-1
#                else:
#                    last_sales_data_row = count-1
#        
#            # Get other data based on stable field label characteristics of row
#            if row[0] == 'RPC:':
#                rpc_id = row[1]
#                neigh_id = row[3]
#            if row[0] == 'Address:':
#                property_address = row[1]
#                zoning = row[3]
#                lot = row [5]
#            if row[0] == 'Year Built:':
#                year_built = row[1]
#                gfa = row[3]
#            if row[0] == 'Tradename:':
#                tradename = row[1]
#            if row[0] == 'Tax Exempt Code:':
#                tax_exempt = row[1]
#            if row[0] == 'Property Class:':
#                property_class = row[1]
#                map_book_page = row[3]
#                polygon_id = row[5]
#    
#    # Execute 2nd pass over record to get information that has to be dynamically located vs. label located.
#    for count, tr in enumerate(root.cssselect('tr')):
#        row = [td.text_content() for td in tr.cssselect('td')]
#        if count == owner_data_starts:
#            owner_name_line1 = row[0]
#            legal_desc_line1 = row[1]
#        if count == (owner_data_starts+1):
#            owner_name_line2 = row[0]
#            legal_desc_line2 = row[1]
#        if count == (owner_data_starts+2):
#            own_addr_line1 = row[0]
#            legal_desc_line3 = row[1]
#        if count == (owner_data_starts+3):
#            own_addr_line2 = row[0]
#            legal_desc_line4 = row[1]
#        if count == (owner_data_starts+4):
#            legal_desc_line5 = row[1]
#        
#        # Get assessment history information
#            land_value = row[2]
#            effective_date = row[0]
#            assessment_type = row[1]
#            land_value = row[2]
#            improvement_value = row[3]
#            total_value = row[4]
#    
#            # Perform s_assess_history record insert
#    
#            assess_now = datetime.datetime.now()
#            assess_data = {"url":final_url, "tmsp_queried":str(assess_now), "rpc_id":rpc_id, "effective_date":effective_date, "assessment_type":assessment_type,
#            "land_value":land_value, "improvement_value":improvement_value, "total_value":total_value}
#            scraperwiki.sqlite.save(unique_keys=["url", "rpc_id", "effective_date"], data=assess_data, table_name="s_assess_history")
#    
#        # Get sales history information
#            sales_date = row[0]
#            sales_price = row[1]
#            sales_code = row[2]
#            grantee = row[3]
#            deed_book = row[4]
#            deed_page = row[5]
#    
#            # Perform s_assess_history record insert
#    
#            sales_now = datetime.datetime.now()
#            sales_data = {"url":final_url, "tmsp_queried":str(sales_now), "rpc_id":rpc_id, "sales_date":sales_date, "sales_price":sales_price,
#            "sales_code":sales_code, "grantee":grantee, "deed_book":deed_book, "deed_page":deed_page}
#            scraperwiki.sqlite.save(unique_keys=["url", "rpc_id", "sales_date"], data=sales_data, table_name="s_sale_history")
#    
#    # Define and set tax_exempt variable if never stepped in
#    try:
#        tax_exempt
#    except NameError:
#        tax_exempt = ''
#        
#    # Perform s_property_detail record insert
#    
#    now = datetime.datetime.now()
#    data = {"url":final_url, "tmsp_queried":str(now), "rpc_id":rpc_id, "neigh_id":neigh_id, "zoning":zoning, "lot":lot, "owner_name_line1":owner_name_line1,
#    "owner_name_line2":owner_name_line2, "legal_desc_line1":legal_desc_line1, "legal_desc_line2":legal_desc_line2, "legal_desc_line3":legal_desc_line3,
#    "legal_desc_line4":legal_desc_line4, "legal_desc_line5":legal_desc_line5, "own_addr_line1":own_addr_line1, "own_addr_line2":own_addr_line2,
#    "property_class":property_class, "map_book_page":map_book_page, "polygon_id":polygon_id, "tax_exempt_code":tax_exempt, "property_address":property_address}
    
#    scraperwiki.sqlite.save(unique_keys=["url","rpc_id"], data=data, table_name="s_property_detail")
#    print "Finished" + " " + rpc_id 
                
 

    
     
        

    

