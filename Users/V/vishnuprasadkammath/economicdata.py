import scraperwiki
import requests
import lxml.html
import getpass
import json
import datetime


PATHS = {
    'login': 'http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/CensusDataOnline_Login.aspx'}
    #'home': 'https://nhseportfolios.org/Auth/SitePages/Trainee/Default.aspx'}
    




def signIn(username, password):
    raw = requests.get(PATHS['login'])
    session_left_slice = raw.headers['set-cookie'].find('=') + 1
    session_right_slice = raw.headers['set-cookie'].find(';')
    session_id = raw.headers['set-cookie'][session_left_slice:session_right_slice]
    html = lxml.html.fromstring(raw.text)
    db_viewstate = html.cssselect("input#__DATABASE_VIEWSTATE").value
    print db_viewstate
    ev_validation = html.cssselect("input#__EVENTVALIDATION").value
    # Create the form payload
    username_key = 'txtUserID'
    password_key = 'txtPassword'
    login_button = 'btnSubmit'
    form_payload = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        
        '__VIEWSTATE': db_viewstate,
        '__EVENTVALIDATION': ev_validation,
        username_key: username,
        password_key: password,}
    session = requests.session()
    session.post(PATHS['login'], data = form_payload)
    return session
print "Enter user credentials"
username1, password1= 'vpkv123','Mylord@123'
print "Validating user credentials"
session = signIn(username1,password1)
print "Getting DOPS assessments"
print "Finished"

