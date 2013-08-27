###############################################################################
# Basic scraper combine with http://scraperwiki.com/scrapers/tds-by-dail/edit/
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup



# check two lists for the difference

l = [["Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "Barry Andrews", "Se?n Ardagh", "Liam Aylward", "Niall Blaney", "Dan Boyle", "Johnny Brady", "Martin Brady", "James Breen", "Pat Breen", "Seamus Brennan (Deceased)", "Tommy Broughan", "John Browne", "John Bruton", "Richard Bruton", "Joan Burton", "Joe Callanan", "Ivor Callely", "Pat Carey", "John Carty", "Donie (Daniel) Cassidy", "Michael Collins", "Paul Connaughton", "Paudge Connolly", "Joe Costello", "Mary Coughlan", "Simon Coveney", "Brian Cowen", "Jerry Cowley", "Seymour Crawford", "John Cregan", "Sean Crowe", "Ciaran Cuffe", "Martin Cullen (Resigned)", "John Curran", "Noel Davern", "S?le de Valera", "John Deasy", "Jimmy Deenihan", "Noel Dempsey", "Tony Dempsey", "John Dennehy", "Jimmy Devins", "Bernard Durkan", "John Ellis", "Damien English", "Olwyn Enright", "Frank Fahey", "Martin Ferris", "Michael Finneran", "Dermot Fitzpatrick", "Sean Fleming", "Beverley Flynn", "Mildred Fox", "Pat (The Cope) Gallagher (Seat vacated 06-06-2009)", "Eamon Gilmore", "Jim Glennon", "Paul Nicholas Gogarty", "John Gormley", "Noel Grealish", "Tony Gregory (Deceased)", "Mary Hanafin", "Marian Harkin", "Mary Harney", "Sean Haughey", "Tom Hayes", "Seamus Healy", "Jackie Healy-Rae", "Joe Higgins", "Michael D. Higgins", "M?ire Hoctor", "Phil Hogan", "Brendan Howlin", "Joe Jacob", "Cecilia Keaveney", "Paul Kehoe", "Billy Kelleher", "Peter Kelly", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Tom Kitt", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Kathleen Lynch", "Miche?l Martin", "P?draic McCormack", "Charlie McCreevy", "James McDaid", "Michael McDowell", "Thomas McEllistrim", "Shane McEntee", "Dinny McGinley", "Paul McGrath", "Finian McGrath", "John McGuinness", "Paddy McHugh", "Liz McManus", "Gay Mitchell", "Olivia Mitchell", "John Anthony Moloney", "Arthur Morgan", "Donal Moynihan", "Michael Moynihan", "Breeda Moynihan-Cronin", "Michael Mulcahy", "Catherine Murphy", "Gerard Murphy", "Denis Naughten", "Dan Neville", "M. J. Nolan", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Se?n ? Feargha?l", "Aengus ? Snodaigh", "Charlie O'Connor", "Willie O'Dea", "Liz O'Donnell", "John O'Donoghue", "Denis O'Donovan", "Fergus O'Dowd", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "Tim O'Malley", "Fiona O'Malley", "Brian O'Shea", "Jan O'Sullivan", "Tom Parlon", "S?amus Pattison", "Willie Penrose", "John Perry", "Se?n Power", "Peter Power", "Ruair? Quinn", "Pat Rabbitte", "Michael Ring", "Dick Roche", "Eoin Ryan", "Sean Ryan", "Eamon Ryan", "Trevor Sargent", "Mae Sexton", "Joe Sherlock", "R?is?n Shortall", "Brendan Smith", "Michael Smith", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Liam Twomey", "Mary Upton", "Jack Wall", "Dan Wallace", "Mary Wallace", "Joe Walsh", "Ollie Wilkinson", "Michael J. Woods", "G.V. Wright"], ["Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "Chris Andrews", "Barry Andrews", "Se?n Ardagh", "Bobby Aylward", "James Bannon", "Sean Barrett", "Joe Behan", "Niall Blaney", "A?ne Brady", "Cyprian Brady", "Johnny Brady", "Pat Breen", "Seamus Brennan (Deceased)", "Tommy Broughan", "John Browne", "Richard Bruton", "Ulick Burke", "Joan Burton", "Catherine Byrne", "Thomas Byrne", "Dara Calleary", "Pat Carey", "Joe Carey", "Deirdre Clune", "Niall Collins", "Margaret Conlon", "Paul Connaughton", "Sean Connick", "Noel J Coonan", "Joe Costello", "Mary Coughlan", "Simon Coveney", "Brian Cowen", "Seymour Crawford", "Michael Creed", "John Cregan", "Lucinda Creighton", "Ciaran Cuffe", "Martin Cullen (Resigned)", "John Curran", "Michael W. D'Arcy", "John Deasy", "Jimmy Deenihan", "Noel Dempsey", "Jimmy Devins", "Timmy Dooley", "Andrew Doyle", "Bernard Durkan", "Damien English", "Olwyn Enright", "Frank Fahey", "Frank Feighan", "Martin Ferris", "Michael Finneran", "Michael Fitzpatrick", "Charles Flanagan", "Terence Flanagan", "Sean Fleming", "Beverley Flynn", "Pat (The Cope) Gallagher (Seat vacated 06-06-2009)", "Eamon Gilmore", "Paul Nicholas Gogarty", "John Gormley", "Noel Grealish", "Tony Gregory (Deceased)", "Mary Hanafin", "Mary Harney", "Sean Haughey", "Brian Hayes", "Tom Hayes", "Jackie Healy-Rae", "Michael D. Higgins", "M?ire Hoctor", "Phil Hogan", "Brendan Howlin", "Paul Kehoe", "Billy Kelleher", "Peter Kelly", "Brendan Kenneally", "Michael Kennedy", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Michael P. Kitt", "Tom Kitt", "George Lee (Resigned)", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Kathleen Lynch", "Ciar?n Lynch", "Martin Mansergh", "Miche?l Martin", "P?draic McCormack", "James McDaid", "Thomas McEllistrim", "Shane McEntee", "Dinny McGinley", "Mattie McGrath", "Michael McGrath", "Finian McGrath", "John McGuinness", "Joe McHugh", "Liz McManus", "Olivia Mitchell", "John Anthony Moloney", "Arthur Morgan", "Michael Moynihan", "Michael Mulcahy", "Denis Naughten", "Dan Neville", "M. J. Nolan", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Se?n ? Feargha?l", "Aengus ? Snodaigh", "Darragh O'Brien", "Charlie O'Connor", "Willie O'Dea", "Kieran O'Donnell", "John O'Donoghue", "Fergus O'Dowd", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "John O'Mahony", "Mary O'Rourke", "Brian O'Shea", "Maureen O'Sullivan", "Christy O'Sullivan", "Jan O'Sullivan", "Willie Penrose", "John Perry", "Se?n Power", "Peter Power", "Ruair? Quinn", "Pat Rabbitte", "James Reilly", "Michael Ring", "Dick Roche", "Eamon Ryan", "Trevor Sargent", "Eamon Scanlon", "Alan Shatter", "Tom Sheahan", "P. J. Sheehan", "Sean Sherlock", "R?is?n Shortall", "Brendan Smith", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Joanna Tuffy", "Mary Upton", "Leo Varadkar", "Jack Wall", "Mary Wallace", "Mary Alexandra White", "Michael J. Woods"], ["Theresa Ahearn", "Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "David Andrews", "Se?n Ardagh", "Liam Aylward", "Monica Barnes", "Sean Barrett", "Michael Bell", "Louis Belton", "Harry Blaney", "Andrew Boylan", "Paul Bradford", "Johnny Brady", "Martin Brady", "Matt Brennan", "Seamus Brennan (Deceased)", "Ben Briscoe", "Tommy Broughan", "John Browne", "John Browne", "John Bruton", "Richard Bruton", "Liam Burke", "Raphael P. (Ray) Burke", "Ulick Burke", "Hugh Byrne", "Ivor Callely", "Donal Carey", "Pat Carey", "Deirdre Clune", "Michael Collins", "Paul Connaughton", "Michael Joe Cosgrave", "Mary Coughlan", "Hugh Coveney", "Simon Coveney", "Brian Cowen", "Seymour Crawford", "Michael Creed", "Martin Cullen (Resigned)", "Austin Currie", "Brendan Daly", "Michael D'Arcy", "Noel Davern", "Proinsias De Rossa", "S?le de Valera", "Austin Deasy", "Jimmy Deenihan", "Noel Dempsey", "John Dennehy", "Sean (Longford-Roscommon) Doherty", "Alan Dukes", "Bernard Durkan", "John Ellis", "Tom.W Enright", "Frank Fahey", "John V. Farrelly", "Michael Ferris", "Michael Finucane", "Frances Fitzgerald", "Charles Flanagan", "Sean Fleming", "Chris Flood", "Beverley Flynn", "Denis Foley", "Mildred Fox", "Tom Gildea", "Eamon Gilmore", "John Gormley", "Tony Gregory (Deceased)", "Mary Hanafin", "Mary Harney", "Sean Haughey", "Brian Hayes", "Tom Hayes", "Seamus Healy", "Jackie Healy-Rae", "Jim Higgins", "Joe Higgins", "Michael D. Higgins", "Phil Hogan", "Brendan Howlin", "Joe Jacob", "Cecilia Keaveney", "Billy Kelleher", "Jim Kemmy", "Brendan Kenneally", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Michael P. Kitt", "Tom Kitt", "Liam Lawlor", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Miche?l Martin", "P?draic McCormack", "Charlie McCreevy", "James McDaid", "Derek McDowell", "Brendan McGahon Marian McGennis", "Dinny McGinley", "Paul McGrath", "John McGuinness", "Liz McManus", "Gay Mitchell", "Jim Mitchell", "Olivia Mitchell", "Tom Moffatt", "Robert (Bobby) Molloy", "John Anthony Moloney", "Donal Moynihan", "Michael Moynihan", "Breeda Moynihan-Cronin", "Denis Naughten", "Dan Neville", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Willie O'Dea", "Liz O'Donnell", "John O'Donoghue", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "Michael O'Kennedy", "Desmond J. O'Malley", "Mary O'Rourke", "Brian O'Shea", "Jan O'Sullivan", "Nora Owen", "S?amus Pattison", "Willie Penrose", "John Perry", "Se?n Power", "Ruair? Quinn", "Pat Rabbitte", "Albert Reynolds", "Gerry Reynolds", "Michael Ring", "Dick Roche", "Eoin Ryan", "Sean Ryan", "Trevor Sargent", "Alan Shatter", "P. J. Sheehan", "R?is?n Shortall", "Brendan Smith", "Michael Smith", "Dick Spring", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Pat Upton", "Mary Upton", "Eddie Wade", "Jack Wall", "Dan Wallace", "Mary Wallace"]]

# s1 = set([4, 6, 9])
#>>> s2 = set([1, 6, 8])
#>>> s1.difference(s2)
#http://www.devshed.com/c/a/Python/Sequences-and-Sets-in-Python/2/
# s1.symmetric_difference(s2)
#set([8, 1, 4, 9])
#>>> s1 ^ s2
#set([8, 1, 4, 9])
#>>> s1.symmetric_difference_update(s2)
#i = 0; 
#v = 1;

#for i in array:

#def list_difference(array[i], array[v]):
   # """uses list1 as the reference, returns list of items not in list2"""
  #  diff_list = []
  #  for item in array[i]:
  #      if not item in array[v]:
 #           diff_list.append(item)
 #   return diff_list

#print list_difference(array[i], array[v])  # [5, 9, 10]
#while v == 30;

# simpler using list comprehension

#diff_list = [item for item in list1 if not item in list2]
#print len(diff_list)
#l=[[1, 2], [3, 4], [4, 6], [2, 7], [3, 9]]
lf=[]
for li in l:
    for i, lfi in enumerate(lf):

        if lfi.intersection(set(li)):
            lfi=lfi.union(set(li))            
            lf[i] = lfi #You forgot to update the list
            break
    else:
        lf.append(set(li))
#print len(lf)
print lf###############################################################################
# Basic scraper combine with http://scraperwiki.com/scrapers/tds-by-dail/edit/
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup



# check two lists for the difference

l = [["Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "Barry Andrews", "Se?n Ardagh", "Liam Aylward", "Niall Blaney", "Dan Boyle", "Johnny Brady", "Martin Brady", "James Breen", "Pat Breen", "Seamus Brennan (Deceased)", "Tommy Broughan", "John Browne", "John Bruton", "Richard Bruton", "Joan Burton", "Joe Callanan", "Ivor Callely", "Pat Carey", "John Carty", "Donie (Daniel) Cassidy", "Michael Collins", "Paul Connaughton", "Paudge Connolly", "Joe Costello", "Mary Coughlan", "Simon Coveney", "Brian Cowen", "Jerry Cowley", "Seymour Crawford", "John Cregan", "Sean Crowe", "Ciaran Cuffe", "Martin Cullen (Resigned)", "John Curran", "Noel Davern", "S?le de Valera", "John Deasy", "Jimmy Deenihan", "Noel Dempsey", "Tony Dempsey", "John Dennehy", "Jimmy Devins", "Bernard Durkan", "John Ellis", "Damien English", "Olwyn Enright", "Frank Fahey", "Martin Ferris", "Michael Finneran", "Dermot Fitzpatrick", "Sean Fleming", "Beverley Flynn", "Mildred Fox", "Pat (The Cope) Gallagher (Seat vacated 06-06-2009)", "Eamon Gilmore", "Jim Glennon", "Paul Nicholas Gogarty", "John Gormley", "Noel Grealish", "Tony Gregory (Deceased)", "Mary Hanafin", "Marian Harkin", "Mary Harney", "Sean Haughey", "Tom Hayes", "Seamus Healy", "Jackie Healy-Rae", "Joe Higgins", "Michael D. Higgins", "M?ire Hoctor", "Phil Hogan", "Brendan Howlin", "Joe Jacob", "Cecilia Keaveney", "Paul Kehoe", "Billy Kelleher", "Peter Kelly", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Tom Kitt", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Kathleen Lynch", "Miche?l Martin", "P?draic McCormack", "Charlie McCreevy", "James McDaid", "Michael McDowell", "Thomas McEllistrim", "Shane McEntee", "Dinny McGinley", "Paul McGrath", "Finian McGrath", "John McGuinness", "Paddy McHugh", "Liz McManus", "Gay Mitchell", "Olivia Mitchell", "John Anthony Moloney", "Arthur Morgan", "Donal Moynihan", "Michael Moynihan", "Breeda Moynihan-Cronin", "Michael Mulcahy", "Catherine Murphy", "Gerard Murphy", "Denis Naughten", "Dan Neville", "M. J. Nolan", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Se?n ? Feargha?l", "Aengus ? Snodaigh", "Charlie O'Connor", "Willie O'Dea", "Liz O'Donnell", "John O'Donoghue", "Denis O'Donovan", "Fergus O'Dowd", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "Tim O'Malley", "Fiona O'Malley", "Brian O'Shea", "Jan O'Sullivan", "Tom Parlon", "S?amus Pattison", "Willie Penrose", "John Perry", "Se?n Power", "Peter Power", "Ruair? Quinn", "Pat Rabbitte", "Michael Ring", "Dick Roche", "Eoin Ryan", "Sean Ryan", "Eamon Ryan", "Trevor Sargent", "Mae Sexton", "Joe Sherlock", "R?is?n Shortall", "Brendan Smith", "Michael Smith", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Liam Twomey", "Mary Upton", "Jack Wall", "Dan Wallace", "Mary Wallace", "Joe Walsh", "Ollie Wilkinson", "Michael J. Woods", "G.V. Wright"], ["Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "Chris Andrews", "Barry Andrews", "Se?n Ardagh", "Bobby Aylward", "James Bannon", "Sean Barrett", "Joe Behan", "Niall Blaney", "A?ne Brady", "Cyprian Brady", "Johnny Brady", "Pat Breen", "Seamus Brennan (Deceased)", "Tommy Broughan", "John Browne", "Richard Bruton", "Ulick Burke", "Joan Burton", "Catherine Byrne", "Thomas Byrne", "Dara Calleary", "Pat Carey", "Joe Carey", "Deirdre Clune", "Niall Collins", "Margaret Conlon", "Paul Connaughton", "Sean Connick", "Noel J Coonan", "Joe Costello", "Mary Coughlan", "Simon Coveney", "Brian Cowen", "Seymour Crawford", "Michael Creed", "John Cregan", "Lucinda Creighton", "Ciaran Cuffe", "Martin Cullen (Resigned)", "John Curran", "Michael W. D'Arcy", "John Deasy", "Jimmy Deenihan", "Noel Dempsey", "Jimmy Devins", "Timmy Dooley", "Andrew Doyle", "Bernard Durkan", "Damien English", "Olwyn Enright", "Frank Fahey", "Frank Feighan", "Martin Ferris", "Michael Finneran", "Michael Fitzpatrick", "Charles Flanagan", "Terence Flanagan", "Sean Fleming", "Beverley Flynn", "Pat (The Cope) Gallagher (Seat vacated 06-06-2009)", "Eamon Gilmore", "Paul Nicholas Gogarty", "John Gormley", "Noel Grealish", "Tony Gregory (Deceased)", "Mary Hanafin", "Mary Harney", "Sean Haughey", "Brian Hayes", "Tom Hayes", "Jackie Healy-Rae", "Michael D. Higgins", "M?ire Hoctor", "Phil Hogan", "Brendan Howlin", "Paul Kehoe", "Billy Kelleher", "Peter Kelly", "Brendan Kenneally", "Michael Kennedy", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Michael P. Kitt", "Tom Kitt", "George Lee (Resigned)", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Kathleen Lynch", "Ciar?n Lynch", "Martin Mansergh", "Miche?l Martin", "P?draic McCormack", "James McDaid", "Thomas McEllistrim", "Shane McEntee", "Dinny McGinley", "Mattie McGrath", "Michael McGrath", "Finian McGrath", "John McGuinness", "Joe McHugh", "Liz McManus", "Olivia Mitchell", "John Anthony Moloney", "Arthur Morgan", "Michael Moynihan", "Michael Mulcahy", "Denis Naughten", "Dan Neville", "M. J. Nolan", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Se?n ? Feargha?l", "Aengus ? Snodaigh", "Darragh O'Brien", "Charlie O'Connor", "Willie O'Dea", "Kieran O'Donnell", "John O'Donoghue", "Fergus O'Dowd", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "John O'Mahony", "Mary O'Rourke", "Brian O'Shea", "Maureen O'Sullivan", "Christy O'Sullivan", "Jan O'Sullivan", "Willie Penrose", "John Perry", "Se?n Power", "Peter Power", "Ruair? Quinn", "Pat Rabbitte", "James Reilly", "Michael Ring", "Dick Roche", "Eamon Ryan", "Trevor Sargent", "Eamon Scanlon", "Alan Shatter", "Tom Sheahan", "P. J. Sheehan", "Sean Sherlock", "R?is?n Shortall", "Brendan Smith", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Joanna Tuffy", "Mary Upton", "Leo Varadkar", "Jack Wall", "Mary Wallace", "Mary Alexandra White", "Michael J. Woods"], ["Theresa Ahearn", "Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "David Andrews", "Se?n Ardagh", "Liam Aylward", "Monica Barnes", "Sean Barrett", "Michael Bell", "Louis Belton", "Harry Blaney", "Andrew Boylan", "Paul Bradford", "Johnny Brady", "Martin Brady", "Matt Brennan", "Seamus Brennan (Deceased)", "Ben Briscoe", "Tommy Broughan", "John Browne", "John Browne", "John Bruton", "Richard Bruton", "Liam Burke", "Raphael P. (Ray) Burke", "Ulick Burke", "Hugh Byrne", "Ivor Callely", "Donal Carey", "Pat Carey", "Deirdre Clune", "Michael Collins", "Paul Connaughton", "Michael Joe Cosgrave", "Mary Coughlan", "Hugh Coveney", "Simon Coveney", "Brian Cowen", "Seymour Crawford", "Michael Creed", "Martin Cullen (Resigned)", "Austin Currie", "Brendan Daly", "Michael D'Arcy", "Noel Davern", "Proinsias De Rossa", "S?le de Valera", "Austin Deasy", "Jimmy Deenihan", "Noel Dempsey", "John Dennehy", "Sean (Longford-Roscommon) Doherty", "Alan Dukes", "Bernard Durkan", "John Ellis", "Tom.W Enright", "Frank Fahey", "John V. Farrelly", "Michael Ferris", "Michael Finucane", "Frances Fitzgerald", "Charles Flanagan", "Sean Fleming", "Chris Flood", "Beverley Flynn", "Denis Foley", "Mildred Fox", "Tom Gildea", "Eamon Gilmore", "John Gormley", "Tony Gregory (Deceased)", "Mary Hanafin", "Mary Harney", "Sean Haughey", "Brian Hayes", "Tom Hayes", "Seamus Healy", "Jackie Healy-Rae", "Jim Higgins", "Joe Higgins", "Michael D. Higgins", "Phil Hogan", "Brendan Howlin", "Joe Jacob", "Cecilia Keaveney", "Billy Kelleher", "Jim Kemmy", "Brendan Kenneally", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Michael P. Kitt", "Tom Kitt", "Liam Lawlor", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Miche?l Martin", "P?draic McCormack", "Charlie McCreevy", "James McDaid", "Derek McDowell", "Brendan McGahon Marian McGennis", "Dinny McGinley", "Paul McGrath", "John McGuinness", "Liz McManus", "Gay Mitchell", "Jim Mitchell", "Olivia Mitchell", "Tom Moffatt", "Robert (Bobby) Molloy", "John Anthony Moloney", "Donal Moynihan", "Michael Moynihan", "Breeda Moynihan-Cronin", "Denis Naughten", "Dan Neville", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Willie O'Dea", "Liz O'Donnell", "John O'Donoghue", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "Michael O'Kennedy", "Desmond J. O'Malley", "Mary O'Rourke", "Brian O'Shea", "Jan O'Sullivan", "Nora Owen", "S?amus Pattison", "Willie Penrose", "John Perry", "Se?n Power", "Ruair? Quinn", "Pat Rabbitte", "Albert Reynolds", "Gerry Reynolds", "Michael Ring", "Dick Roche", "Eoin Ryan", "Sean Ryan", "Trevor Sargent", "Alan Shatter", "P. J. Sheehan", "R?is?n Shortall", "Brendan Smith", "Michael Smith", "Dick Spring", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Pat Upton", "Mary Upton", "Eddie Wade", "Jack Wall", "Dan Wallace", "Mary Wallace"]]

# s1 = set([4, 6, 9])
#>>> s2 = set([1, 6, 8])
#>>> s1.difference(s2)
#http://www.devshed.com/c/a/Python/Sequences-and-Sets-in-Python/2/
# s1.symmetric_difference(s2)
#set([8, 1, 4, 9])
#>>> s1 ^ s2
#set([8, 1, 4, 9])
#>>> s1.symmetric_difference_update(s2)
#i = 0; 
#v = 1;

#for i in array:

#def list_difference(array[i], array[v]):
   # """uses list1 as the reference, returns list of items not in list2"""
  #  diff_list = []
  #  for item in array[i]:
  #      if not item in array[v]:
 #           diff_list.append(item)
 #   return diff_list

#print list_difference(array[i], array[v])  # [5, 9, 10]
#while v == 30;

# simpler using list comprehension

#diff_list = [item for item in list1 if not item in list2]
#print len(diff_list)
#l=[[1, 2], [3, 4], [4, 6], [2, 7], [3, 9]]
lf=[]
for li in l:
    for i, lfi in enumerate(lf):

        if lfi.intersection(set(li)):
            lfi=lfi.union(set(li))            
            lf[i] = lfi #You forgot to update the list
            break
    else:
        lf.append(set(li))
#print len(lf)
print lf###############################################################################
# Basic scraper combine with http://scraperwiki.com/scrapers/tds-by-dail/edit/
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup



# check two lists for the difference

l = [["Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "Barry Andrews", "Se?n Ardagh", "Liam Aylward", "Niall Blaney", "Dan Boyle", "Johnny Brady", "Martin Brady", "James Breen", "Pat Breen", "Seamus Brennan (Deceased)", "Tommy Broughan", "John Browne", "John Bruton", "Richard Bruton", "Joan Burton", "Joe Callanan", "Ivor Callely", "Pat Carey", "John Carty", "Donie (Daniel) Cassidy", "Michael Collins", "Paul Connaughton", "Paudge Connolly", "Joe Costello", "Mary Coughlan", "Simon Coveney", "Brian Cowen", "Jerry Cowley", "Seymour Crawford", "John Cregan", "Sean Crowe", "Ciaran Cuffe", "Martin Cullen (Resigned)", "John Curran", "Noel Davern", "S?le de Valera", "John Deasy", "Jimmy Deenihan", "Noel Dempsey", "Tony Dempsey", "John Dennehy", "Jimmy Devins", "Bernard Durkan", "John Ellis", "Damien English", "Olwyn Enright", "Frank Fahey", "Martin Ferris", "Michael Finneran", "Dermot Fitzpatrick", "Sean Fleming", "Beverley Flynn", "Mildred Fox", "Pat (The Cope) Gallagher (Seat vacated 06-06-2009)", "Eamon Gilmore", "Jim Glennon", "Paul Nicholas Gogarty", "John Gormley", "Noel Grealish", "Tony Gregory (Deceased)", "Mary Hanafin", "Marian Harkin", "Mary Harney", "Sean Haughey", "Tom Hayes", "Seamus Healy", "Jackie Healy-Rae", "Joe Higgins", "Michael D. Higgins", "M?ire Hoctor", "Phil Hogan", "Brendan Howlin", "Joe Jacob", "Cecilia Keaveney", "Paul Kehoe", "Billy Kelleher", "Peter Kelly", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Tom Kitt", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Kathleen Lynch", "Miche?l Martin", "P?draic McCormack", "Charlie McCreevy", "James McDaid", "Michael McDowell", "Thomas McEllistrim", "Shane McEntee", "Dinny McGinley", "Paul McGrath", "Finian McGrath", "John McGuinness", "Paddy McHugh", "Liz McManus", "Gay Mitchell", "Olivia Mitchell", "John Anthony Moloney", "Arthur Morgan", "Donal Moynihan", "Michael Moynihan", "Breeda Moynihan-Cronin", "Michael Mulcahy", "Catherine Murphy", "Gerard Murphy", "Denis Naughten", "Dan Neville", "M. J. Nolan", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Se?n ? Feargha?l", "Aengus ? Snodaigh", "Charlie O'Connor", "Willie O'Dea", "Liz O'Donnell", "John O'Donoghue", "Denis O'Donovan", "Fergus O'Dowd", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "Tim O'Malley", "Fiona O'Malley", "Brian O'Shea", "Jan O'Sullivan", "Tom Parlon", "S?amus Pattison", "Willie Penrose", "John Perry", "Se?n Power", "Peter Power", "Ruair? Quinn", "Pat Rabbitte", "Michael Ring", "Dick Roche", "Eoin Ryan", "Sean Ryan", "Eamon Ryan", "Trevor Sargent", "Mae Sexton", "Joe Sherlock", "R?is?n Shortall", "Brendan Smith", "Michael Smith", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Liam Twomey", "Mary Upton", "Jack Wall", "Dan Wallace", "Mary Wallace", "Joe Walsh", "Ollie Wilkinson", "Michael J. Woods", "G.V. Wright"], ["Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "Chris Andrews", "Barry Andrews", "Se?n Ardagh", "Bobby Aylward", "James Bannon", "Sean Barrett", "Joe Behan", "Niall Blaney", "A?ne Brady", "Cyprian Brady", "Johnny Brady", "Pat Breen", "Seamus Brennan (Deceased)", "Tommy Broughan", "John Browne", "Richard Bruton", "Ulick Burke", "Joan Burton", "Catherine Byrne", "Thomas Byrne", "Dara Calleary", "Pat Carey", "Joe Carey", "Deirdre Clune", "Niall Collins", "Margaret Conlon", "Paul Connaughton", "Sean Connick", "Noel J Coonan", "Joe Costello", "Mary Coughlan", "Simon Coveney", "Brian Cowen", "Seymour Crawford", "Michael Creed", "John Cregan", "Lucinda Creighton", "Ciaran Cuffe", "Martin Cullen (Resigned)", "John Curran", "Michael W. D'Arcy", "John Deasy", "Jimmy Deenihan", "Noel Dempsey", "Jimmy Devins", "Timmy Dooley", "Andrew Doyle", "Bernard Durkan", "Damien English", "Olwyn Enright", "Frank Fahey", "Frank Feighan", "Martin Ferris", "Michael Finneran", "Michael Fitzpatrick", "Charles Flanagan", "Terence Flanagan", "Sean Fleming", "Beverley Flynn", "Pat (The Cope) Gallagher (Seat vacated 06-06-2009)", "Eamon Gilmore", "Paul Nicholas Gogarty", "John Gormley", "Noel Grealish", "Tony Gregory (Deceased)", "Mary Hanafin", "Mary Harney", "Sean Haughey", "Brian Hayes", "Tom Hayes", "Jackie Healy-Rae", "Michael D. Higgins", "M?ire Hoctor", "Phil Hogan", "Brendan Howlin", "Paul Kehoe", "Billy Kelleher", "Peter Kelly", "Brendan Kenneally", "Michael Kennedy", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Michael P. Kitt", "Tom Kitt", "George Lee (Resigned)", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Kathleen Lynch", "Ciar?n Lynch", "Martin Mansergh", "Miche?l Martin", "P?draic McCormack", "James McDaid", "Thomas McEllistrim", "Shane McEntee", "Dinny McGinley", "Mattie McGrath", "Michael McGrath", "Finian McGrath", "John McGuinness", "Joe McHugh", "Liz McManus", "Olivia Mitchell", "John Anthony Moloney", "Arthur Morgan", "Michael Moynihan", "Michael Mulcahy", "Denis Naughten", "Dan Neville", "M. J. Nolan", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Se?n ? Feargha?l", "Aengus ? Snodaigh", "Darragh O'Brien", "Charlie O'Connor", "Willie O'Dea", "Kieran O'Donnell", "John O'Donoghue", "Fergus O'Dowd", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "John O'Mahony", "Mary O'Rourke", "Brian O'Shea", "Maureen O'Sullivan", "Christy O'Sullivan", "Jan O'Sullivan", "Willie Penrose", "John Perry", "Se?n Power", "Peter Power", "Ruair? Quinn", "Pat Rabbitte", "James Reilly", "Michael Ring", "Dick Roche", "Eamon Ryan", "Trevor Sargent", "Eamon Scanlon", "Alan Shatter", "Tom Sheahan", "P. J. Sheehan", "Sean Sherlock", "R?is?n Shortall", "Brendan Smith", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Joanna Tuffy", "Mary Upton", "Leo Varadkar", "Jack Wall", "Mary Wallace", "Mary Alexandra White", "Michael J. Woods"], ["Theresa Ahearn", "Bertie Ahern", "Dermot Ahern", "Michael Ahern", "Noel Ahern", "Bernard Allen", "David Andrews", "Se?n Ardagh", "Liam Aylward", "Monica Barnes", "Sean Barrett", "Michael Bell", "Louis Belton", "Harry Blaney", "Andrew Boylan", "Paul Bradford", "Johnny Brady", "Martin Brady", "Matt Brennan", "Seamus Brennan (Deceased)", "Ben Briscoe", "Tommy Broughan", "John Browne", "John Browne", "John Bruton", "Richard Bruton", "Liam Burke", "Raphael P. (Ray) Burke", "Ulick Burke", "Hugh Byrne", "Ivor Callely", "Donal Carey", "Pat Carey", "Deirdre Clune", "Michael Collins", "Paul Connaughton", "Michael Joe Cosgrave", "Mary Coughlan", "Hugh Coveney", "Simon Coveney", "Brian Cowen", "Seymour Crawford", "Michael Creed", "Martin Cullen (Resigned)", "Austin Currie", "Brendan Daly", "Michael D'Arcy", "Noel Davern", "Proinsias De Rossa", "S?le de Valera", "Austin Deasy", "Jimmy Deenihan", "Noel Dempsey", "John Dennehy", "Sean (Longford-Roscommon) Doherty", "Alan Dukes", "Bernard Durkan", "John Ellis", "Tom.W Enright", "Frank Fahey", "John V. Farrelly", "Michael Ferris", "Michael Finucane", "Frances Fitzgerald", "Charles Flanagan", "Sean Fleming", "Chris Flood", "Beverley Flynn", "Denis Foley", "Mildred Fox", "Tom Gildea", "Eamon Gilmore", "John Gormley", "Tony Gregory (Deceased)", "Mary Hanafin", "Mary Harney", "Sean Haughey", "Brian Hayes", "Tom Hayes", "Seamus Healy", "Jackie Healy-Rae", "Jim Higgins", "Joe Higgins", "Michael D. Higgins", "Phil Hogan", "Brendan Howlin", "Joe Jacob", "Cecilia Keaveney", "Billy Kelleher", "Jim Kemmy", "Brendan Kenneally", "Enda Kenny", "Tony Killeen", "S?amus Kirk", "Michael P. Kitt", "Tom Kitt", "Liam Lawlor", "Brian Joseph Lenihan", "Conor Lenihan", "Michael Lowry", "Miche?l Martin", "P?draic McCormack", "Charlie McCreevy", "James McDaid", "Derek McDowell", "Brendan McGahon Marian McGennis", "Dinny McGinley", "Paul McGrath", "John McGuinness", "Liz McManus", "Gay Mitchell", "Jim Mitchell", "Olivia Mitchell", "Tom Moffatt", "Robert (Bobby) Molloy", "John Anthony Moloney", "Donal Moynihan", "Michael Moynihan", "Breeda Moynihan-Cronin", "Denis Naughten", "Dan Neville", "Michael Noonan", "Caoimhgh?n ? Caol?in", "?amon ? Cu?v", "Willie O'Dea", "Liz O'Donnell", "John O'Donoghue", "Noel O'Flynn", "Rory O'Hanlon", "Batt O'Keeffe", "Jim O'Keeffe", "Edward O'Keeffe", "Michael O'Kennedy", "Desmond J. O'Malley", "Mary O'Rourke", "Brian O'Shea", "Jan O'Sullivan", "Nora Owen", "S?amus Pattison", "Willie Penrose", "John Perry", "Se?n Power", "Ruair? Quinn", "Pat Rabbitte", "Albert Reynolds", "Gerry Reynolds", "Michael Ring", "Dick Roche", "Eoin Ryan", "Sean Ryan", "Trevor Sargent", "Alan Shatter", "P. J. Sheehan", "R?is?n Shortall", "Brendan Smith", "Michael Smith", "Dick Spring", "Emmet Stagg", "David Stanton", "Billy Godfrey Timmins", "Noel Treacy", "Pat Upton", "Mary Upton", "Eddie Wade", "Jack Wall", "Dan Wallace", "Mary Wallace"]]

# s1 = set([4, 6, 9])
#>>> s2 = set([1, 6, 8])
#>>> s1.difference(s2)
#http://www.devshed.com/c/a/Python/Sequences-and-Sets-in-Python/2/
# s1.symmetric_difference(s2)
#set([8, 1, 4, 9])
#>>> s1 ^ s2
#set([8, 1, 4, 9])
#>>> s1.symmetric_difference_update(s2)
#i = 0; 
#v = 1;

#for i in array:

#def list_difference(array[i], array[v]):
   # """uses list1 as the reference, returns list of items not in list2"""
  #  diff_list = []
  #  for item in array[i]:
  #      if not item in array[v]:
 #           diff_list.append(item)
 #   return diff_list

#print list_difference(array[i], array[v])  # [5, 9, 10]
#while v == 30;

# simpler using list comprehension

#diff_list = [item for item in list1 if not item in list2]
#print len(diff_list)
#l=[[1, 2], [3, 4], [4, 6], [2, 7], [3, 9]]
lf=[]
for li in l:
    for i, lfi in enumerate(lf):

        if lfi.intersection(set(li)):
            lfi=lfi.union(set(li))            
            lf[i] = lfi #You forgot to update the list
            break
    else:
        lf.append(set(li))
#print len(lf)
print lf