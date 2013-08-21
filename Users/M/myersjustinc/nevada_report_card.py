import lxml.html
import requests
import scraperwiki

DISTRICTS = {
    "Churchill": "01",
    "Clark": "02",
    "Douglas": "03",
    "Elko": "04",
    "Esmeralda": "05",
    "Eureka": "06",
    "Humboldt": "07",
    "Lander": "08",
    "Lincoln": "09",
    "Lyon": "10",
    "Mineral": "11",
    "Nye": "12",
    "Carson City": "13",
    "Pershing": "14",
    "State Public Schools": "18",
    "Storey": "15",
    "Washoe": "16",
    "White Pine": "17",
}

YEARS = {
    "2010-2011": "10-11",
    "2009-2010": "09-10",
    "2008-2009": "08-09",
    "2007-2008": "07-08",
    "2006-2007": "06-07",
    "2005-2006": "05-06",
    "2004-2005": "04-05",
    "2003-2004": "03-04",
}

FILENAMES = {
    "Demographic Profile": {
        "Ethnicity": "ethnicity",
        "Gender": "gender",
        "Special Populations": "splpopulations",
    },
    "Fiscal Information": {
        "Per Pupil Expenditures": "perpupilexpenditure",
        "Remedial Education Funding": "remedialedufunding",
        "Professional Development Funding": "professionaldevfunding",
        "Sources of Funding": "fundssource",
        "Legislative Appropriations": "appropriations",
    },
    "Technology": {
        "Technology": "technologydetails",
    },
    "Students": {
        "Average Daily Attendance": "studavgattendance",
        "Student/Teacher Ratio": "studteacherratio",
        "Average Class Size": "avgclasssize",
        "Retention by Grade": "retebygrade",
        "Credit Deficient": "creditdeficit",
        "Transiency": "transiency",
        "Discipline": "discipline",
        "Graduation Completion Indicators": "graduation",
        "Graduation Rates": "graduationrates",
        "Dropout Rates": "dropoutrates",
        "Proficiency Failures": "proficiencyfailures",
        "Remedial NSHE": "remedialuccsn",
    },
    "Career and Technical Education": {
        "CTE ADA": "CTEstudavgattendance",
        "CTE Completion": "CTEgraduation",
    },
    "Parents": {
        "Conference Attendance": "parentsconferenceatended",
    },
    "Personnel": {
        "Teachers": "seccoresubject",
        "Paraprofessionals": "paraprofessionals",
        "Substitute Teachers": "longshorttermsubstitutes",
        "Staffing": "PersonnelStaffing",
    },
    "Adequate Yearly Progress": {
        "District AYP Status": "ayp_status",
        "School AYP Status": "schoolayp_statuslist",
    },
    "Special Programs": {
        "Special Programs": "specialprograms"
    },
}

class DataSet(object):
    URL_TEMPLATE = "http://www.nevadareportcard.com/profile/%(filename)s.aspx?levelid=D&entityid=%(district)s&yearid=%(year)s"
    
    def __init__(self, district, year, filename):
        self.district = district
        self.year = year
        self.filename = filename
        self.html = ''
    
    def get_html(self):
        r = requests.get(URL_TEMPLATE % {
            "district": self.district,
            "filename": self.filename,
            "year": self.year,
        })
        self.html = r.text
    
    def get_data(self):
        document = lxml.html.fromstring(self.html)
        table = document.cssselect("table table table")
        
        header_rows = table.cssselect(".heading3")
        measures = []
        if len(header_rows) == 2:
            if len(header_rows[1]) == len(table.cssselect(".heading4")[0]) - 1:
                for cell in header_rows[0]:
                    cell_text = cell.text.strip()
                    measures.append(cell_text)
        else:
            if len(header_rows[0]) == len(table.cssselect(".heading4")[0]) - 1:
                for cell in header_rows[0]:
                    cell_text = cell.text.strip()
                    measures.append(cell_text)
            else:
                print "Row headers don't match up"
        
        
    
    
