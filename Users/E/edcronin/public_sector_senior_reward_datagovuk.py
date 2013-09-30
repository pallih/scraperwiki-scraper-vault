import scraperwiki
import urllib2
import json
import csv
import xlrd
from string import maketrans

### Test extract of data from data.gov.uk ###

class DGUscraper(object):
    """class to scrape all data matching a tag, in a particular format from data.gov.uk"""
    
    base = "http://data.gov.uk/api/2/"
    package = "rest/package/%s"
    search = "search/package?q=%s&limit=9999"

    intab = " ./()£"
    outtab = "_______"
    trantab = maketrans(intab, outtab)
    identifier = 'XID'
    
    def __init__(self,tag,formats=('CSV',),nresources=2,mapping=None):
        self.tag = tag
        self.formats = formats
        self.nresources = nresources
        self.mapping = mapping
        if self.mapping: self.mapping[self.identifier] = self.identifier
        self.serial = 0
        self.cat = {}
        self.store = {}
        self.run()

    @staticmethod
    def _getdata(url):
        fp = urllib2.urlopen(url)
        results = json.loads(fp.read())
        fp.close()
        return results

    @staticmethod
    def _cleanCSVdata(url):
        raw = scraperwiki.scrape(url)
        reader = csv.DictReader(raw.splitlines())
        data = [x for x in reader if x.values()[0]] # exclude blanks
        del reader
        return data

    @staticmethod
    def _cleanXLSdata(url,keyline=0,datastart=1):
        data = []
        xlbin = scraperwiki.scrape(url)
        book = xlrd.open_workbook(file_contents=xlbin)
        sheet = book.sheet_by_index(0)
        keys = sheet.row_values(keyline)
        for rownumber in range(datastart, sheet.nrows):           
            values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
            row = dict(zip(keys, values))
            data.append(row)
        return data

    def mapper(self,rowdict):
        transrow = dict([(k.translate(self.trantab),v) for k,v in rowdict.items() if k])
        if self.mapping:
            # note, will discard one k,v if two ks map to same in self.mapping
            return dict([(self.mapping[k],v)for k,v in transrow.items() if k in self.mapping])
        else:
            return transrow

    def hits(self):
        return self._getdata(self.base + self.search % self.tag)

    def resources(self,pk):
        entity = self._getdata(self.base + self.package % pk)
        print entity['title'] # testing
        return [x for x in entity['resources'] if x['format'] in self.formats]

    def storedata(self,url,**kwds):
        if kwds:
            self.mapping.update(dict([(k,k) for k in kwds.keys()]))
        #try:
        if 1==1:
            rows = self._cleanCSVdata(url)
            if rows:
                #if url.upper().endswith('CSV') or url.upper().endswith('ASPX'): rows = self._cleanCSVdata(url)
                #elif url.upper().endswith('XLS'): rows = self._cleanXLSdata(url) # convert to dict lookup if more formats
                for i,row in enumerate(rows):
                    row[self.identifier] = "%s_%s" % (self.serial,i)
                    row.update(kwds)
                    row = self.mapper(row)
                    scraperwiki.sqlite.save(unique_keys=['XID'], data=row)
                #except:
                #   print "there was an exception" # handle better...
                self.serial += 1

    def run(self):
        pks = self.hits()
        print "Found %s packages for %s..." % (len(pks['results']),self.tag)
        for pk in pks['results']:
            resources = [x for x in self.resources(pk) if x['cache_url']][-self.nresources:]
            print "\t%s resources" % len(resources)
            for resource in resources:
                cache_url = resource['cache_url']
                self.storedata(cache_url,d=resource['description'],u=cache_url)

this_mapping = {'Any_notes':'EXCLUDE','Contact_E-mail':'EXCLUDE','Contact_Phone':'EXCLUDE',
'E-mail':'EXCLUDE','Full_Name':'EXCLUDE','Full_Name_with_Title':'EXCLUDE',
'Gross_Budget_Responsibility_11_12___m_':'EXCLUDE','Invoice_Currency_Unit':'EXCLUDE',
'Name':'EXCLUDE','Notes':'EXCLUDE','Phone':'EXCLUDE','Post_Holder':'EXCLUDE',
'Reporting_Senior_Post':'EXCLUDE','Reports_To':'EXCLUDE','Reports_to_Senior_Post':'EXCLUDE',
'Supplier':'EXCLUDE','Surname':'EXCLUDE','Service_area':'EXCLUDE',
'Unique_reference_identifier_of_SCS_post_to_whom_these_staff_report':'EXCLUDE','Unique_Reporting_Identifier':'EXCLUDE',
'VAT_Registration_Number':'EXCLUDE','Fees_for_2010-09':'EXCLUDE',
'Parent_Department':'EXCLUDE','Parent_Dept':'EXCLUDE','Reporting_post_reference':'EXCLUDE',
'Reporting_SCS_post_reference':'EXCLUDE','Department_Family':'EXCLUDE','Actual_pay_floor':'EXCLUDE',
'Actual_Pay_Floor____':'EXCLUDE','Actual_pay_ceiling':'EXCLUDE','Actual_Pay_Ceiling____':'EXCLUDE',
'Post_ref':'EXCLUDE','Post_Unique_Reference':'EXCLUDE','No_of_posts':'EXCLUDE','Non-executive_Member':'EXCLUDE',
'Expense_Type':'EXCLUDE','Expenses_paid_in_month_of_Oct_2011____':'EXCLUDE',
'Expenses_paid_in_month_of_Sept_2011____':'EXCLUDE','Fees_for_2010-11':'EXCLUDE',
'Total_Remuneration_including_Pensioncontributions':'EXCLUDE','ID_Number':'ID','Reference':'ID',
'Unique_reference_identifier':'ID','Organisation':'ORG','Body':'ORG','Body_Name':'ORG','Entity':'ORG',
'Service_Area':'DIVISION','Unit':'DIVISION','Basic_Pay':'BASIC_SALARY','FTE_Salary':'BASIC_SALARY',
'Job_Title':'JOB_TITLE','Job_Title_':'JOB_TITLE','Generic_Job_Title':'JOB_TITLE','Post':'JOB_TITLE',
'Post_name':'JOB_TITLE','Grade':'LEVEL','Job_Function':'FUNCTION','Job_Role_Code':'FUNCTION',
'Profession':'FUNCTION','Professional_Occupational_Group':'FUNCTION','Job_Team_Function':'FUNCTION',
'Date':'EDATE','Reporting_Month':'EDATE','FTE_pay_floor':'PAY_FLOOR','FTE_pay_floor_':'PAY_FLOOR',
'Data_Standard_FTE_Pay_Floor':'PAY_FLOOR','Pay_Floor':'PAY_FLOOR','Payscale_Min':'PAY_FLOOR',
'Payscale_minimum':'PAY_FLOOR','Payscale_Minimum____':'PAY_FLOOR','FTE_pay_ceiling':'PAY_CEILING',
'FTE_pay_ceiling_':'PAY_CEILING','Data_Standard_FTE_Pay_Ceiling':'PAY_CEILING','Pay_ceiling':'PAY_CEILING',
'Payscale_Max':'PAY_CEILING','Payscale_maximum':'PAY_CEILING','Payscale_Maximum____':'PAY_CEILING',
'Salary_Band':'PAY_BAND','Salary_group':'PAY_BAND',
'Pension_Contributions__Based_on_Common_Ratefrom_Actuary_':'PENSION_CONTRIB',
'Salary_Cost_of_Reports__':'SALARY_OF_REPORTS','Salary_Cost_of_Reports____':'SALARY_OF_REPORTS',
'FTE':'FTE','FTE_':'FTE','FTE__':'FTE','_FTE':'FTE','WTE':'FTE','No__FTE_Employees':'N_FTE',
'Number_of_Posts_in_FTE':'N_FTE','Number_of_such_posts_in_FTE':'N_FTE','_Amount_':'AMOUNT',
'Amount':'AMOUNT','FTE_hours':'HOURS','FTE_of_minimum_contract':'HOURS',
'FTE_of_Minimum_Contracted_Hours':'HOURS','ExpenseAllowances':'EXPENSES',
'Salary_including_fees_and_allowances':'TOTAL_PAY','Total_Pay____':'TOTAL_PAY',
'Total_Remuneration_excluding_Pensioncontributions':'TOTAL_PAY'}

scraped = DGUscraper("salaries",nresources=1,mapping=this_mapping)


        




import scraperwiki
import urllib2
import json
import csv
import xlrd
from string import maketrans

### Test extract of data from data.gov.uk ###

class DGUscraper(object):
    """class to scrape all data matching a tag, in a particular format from data.gov.uk"""
    
    base = "http://data.gov.uk/api/2/"
    package = "rest/package/%s"
    search = "search/package?q=%s&limit=9999"

    intab = " ./()£"
    outtab = "_______"
    trantab = maketrans(intab, outtab)
    identifier = 'XID'
    
    def __init__(self,tag,formats=('CSV',),nresources=2,mapping=None):
        self.tag = tag
        self.formats = formats
        self.nresources = nresources
        self.mapping = mapping
        if self.mapping: self.mapping[self.identifier] = self.identifier
        self.serial = 0
        self.cat = {}
        self.store = {}
        self.run()

    @staticmethod
    def _getdata(url):
        fp = urllib2.urlopen(url)
        results = json.loads(fp.read())
        fp.close()
        return results

    @staticmethod
    def _cleanCSVdata(url):
        raw = scraperwiki.scrape(url)
        reader = csv.DictReader(raw.splitlines())
        data = [x for x in reader if x.values()[0]] # exclude blanks
        del reader
        return data

    @staticmethod
    def _cleanXLSdata(url,keyline=0,datastart=1):
        data = []
        xlbin = scraperwiki.scrape(url)
        book = xlrd.open_workbook(file_contents=xlbin)
        sheet = book.sheet_by_index(0)
        keys = sheet.row_values(keyline)
        for rownumber in range(datastart, sheet.nrows):           
            values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
            row = dict(zip(keys, values))
            data.append(row)
        return data

    def mapper(self,rowdict):
        transrow = dict([(k.translate(self.trantab),v) for k,v in rowdict.items() if k])
        if self.mapping:
            # note, will discard one k,v if two ks map to same in self.mapping
            return dict([(self.mapping[k],v)for k,v in transrow.items() if k in self.mapping])
        else:
            return transrow

    def hits(self):
        return self._getdata(self.base + self.search % self.tag)

    def resources(self,pk):
        entity = self._getdata(self.base + self.package % pk)
        print entity['title'] # testing
        return [x for x in entity['resources'] if x['format'] in self.formats]

    def storedata(self,url,**kwds):
        if kwds:
            self.mapping.update(dict([(k,k) for k in kwds.keys()]))
        #try:
        if 1==1:
            rows = self._cleanCSVdata(url)
            if rows:
                #if url.upper().endswith('CSV') or url.upper().endswith('ASPX'): rows = self._cleanCSVdata(url)
                #elif url.upper().endswith('XLS'): rows = self._cleanXLSdata(url) # convert to dict lookup if more formats
                for i,row in enumerate(rows):
                    row[self.identifier] = "%s_%s" % (self.serial,i)
                    row.update(kwds)
                    row = self.mapper(row)
                    scraperwiki.sqlite.save(unique_keys=['XID'], data=row)
                #except:
                #   print "there was an exception" # handle better...
                self.serial += 1

    def run(self):
        pks = self.hits()
        print "Found %s packages for %s..." % (len(pks['results']),self.tag)
        for pk in pks['results']:
            resources = [x for x in self.resources(pk) if x['cache_url']][-self.nresources:]
            print "\t%s resources" % len(resources)
            for resource in resources:
                cache_url = resource['cache_url']
                self.storedata(cache_url,d=resource['description'],u=cache_url)

this_mapping = {'Any_notes':'EXCLUDE','Contact_E-mail':'EXCLUDE','Contact_Phone':'EXCLUDE',
'E-mail':'EXCLUDE','Full_Name':'EXCLUDE','Full_Name_with_Title':'EXCLUDE',
'Gross_Budget_Responsibility_11_12___m_':'EXCLUDE','Invoice_Currency_Unit':'EXCLUDE',
'Name':'EXCLUDE','Notes':'EXCLUDE','Phone':'EXCLUDE','Post_Holder':'EXCLUDE',
'Reporting_Senior_Post':'EXCLUDE','Reports_To':'EXCLUDE','Reports_to_Senior_Post':'EXCLUDE',
'Supplier':'EXCLUDE','Surname':'EXCLUDE','Service_area':'EXCLUDE',
'Unique_reference_identifier_of_SCS_post_to_whom_these_staff_report':'EXCLUDE','Unique_Reporting_Identifier':'EXCLUDE',
'VAT_Registration_Number':'EXCLUDE','Fees_for_2010-09':'EXCLUDE',
'Parent_Department':'EXCLUDE','Parent_Dept':'EXCLUDE','Reporting_post_reference':'EXCLUDE',
'Reporting_SCS_post_reference':'EXCLUDE','Department_Family':'EXCLUDE','Actual_pay_floor':'EXCLUDE',
'Actual_Pay_Floor____':'EXCLUDE','Actual_pay_ceiling':'EXCLUDE','Actual_Pay_Ceiling____':'EXCLUDE',
'Post_ref':'EXCLUDE','Post_Unique_Reference':'EXCLUDE','No_of_posts':'EXCLUDE','Non-executive_Member':'EXCLUDE',
'Expense_Type':'EXCLUDE','Expenses_paid_in_month_of_Oct_2011____':'EXCLUDE',
'Expenses_paid_in_month_of_Sept_2011____':'EXCLUDE','Fees_for_2010-11':'EXCLUDE',
'Total_Remuneration_including_Pensioncontributions':'EXCLUDE','ID_Number':'ID','Reference':'ID',
'Unique_reference_identifier':'ID','Organisation':'ORG','Body':'ORG','Body_Name':'ORG','Entity':'ORG',
'Service_Area':'DIVISION','Unit':'DIVISION','Basic_Pay':'BASIC_SALARY','FTE_Salary':'BASIC_SALARY',
'Job_Title':'JOB_TITLE','Job_Title_':'JOB_TITLE','Generic_Job_Title':'JOB_TITLE','Post':'JOB_TITLE',
'Post_name':'JOB_TITLE','Grade':'LEVEL','Job_Function':'FUNCTION','Job_Role_Code':'FUNCTION',
'Profession':'FUNCTION','Professional_Occupational_Group':'FUNCTION','Job_Team_Function':'FUNCTION',
'Date':'EDATE','Reporting_Month':'EDATE','FTE_pay_floor':'PAY_FLOOR','FTE_pay_floor_':'PAY_FLOOR',
'Data_Standard_FTE_Pay_Floor':'PAY_FLOOR','Pay_Floor':'PAY_FLOOR','Payscale_Min':'PAY_FLOOR',
'Payscale_minimum':'PAY_FLOOR','Payscale_Minimum____':'PAY_FLOOR','FTE_pay_ceiling':'PAY_CEILING',
'FTE_pay_ceiling_':'PAY_CEILING','Data_Standard_FTE_Pay_Ceiling':'PAY_CEILING','Pay_ceiling':'PAY_CEILING',
'Payscale_Max':'PAY_CEILING','Payscale_maximum':'PAY_CEILING','Payscale_Maximum____':'PAY_CEILING',
'Salary_Band':'PAY_BAND','Salary_group':'PAY_BAND',
'Pension_Contributions__Based_on_Common_Ratefrom_Actuary_':'PENSION_CONTRIB',
'Salary_Cost_of_Reports__':'SALARY_OF_REPORTS','Salary_Cost_of_Reports____':'SALARY_OF_REPORTS',
'FTE':'FTE','FTE_':'FTE','FTE__':'FTE','_FTE':'FTE','WTE':'FTE','No__FTE_Employees':'N_FTE',
'Number_of_Posts_in_FTE':'N_FTE','Number_of_such_posts_in_FTE':'N_FTE','_Amount_':'AMOUNT',
'Amount':'AMOUNT','FTE_hours':'HOURS','FTE_of_minimum_contract':'HOURS',
'FTE_of_Minimum_Contracted_Hours':'HOURS','ExpenseAllowances':'EXPENSES',
'Salary_including_fees_and_allowances':'TOTAL_PAY','Total_Pay____':'TOTAL_PAY',
'Total_Remuneration_excluding_Pensioncontributions':'TOTAL_PAY'}

scraped = DGUscraper("salaries",nresources=1,mapping=this_mapping)


        




