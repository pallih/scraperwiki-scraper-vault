# Collect Data Scraper
# This scraper collect data from different tables. Finally the different Data structures of the source tables should be cosolidates in one or two tables

import scraperwiki 

# Define Variables

#SCRAPERNAME = 'worldwide_shark_attacks'
# SCRAPERNAME = 'eu_efre_unitedkingdom_scotland'
#TABLE = 'hawaii'
# TABLE = 'EFRE_EU_UnitedKingdom_Scotland'
#NEW_TABLE_NAME = 'new hawaii'
# NEW_TABLE_NAME = 'europe_efre_payments'

# Attach future queries to the specified scraper/database so that we
# can include SCRAPERNAME.TABLE in future queries


 #scraperwiki.sqlite.attach(SCRAPERNAME);

# tables = scraperwiki.sqlite.show_tables( SCRAPERNAME )

# print tables


# Get a dictionary of the table schemas we want which contains the SQL we
# need to create a matching table.


# Select from the table which will return a list of dictionaries, which also has
# the advantage of being a shortcut for mass upload in the save command.
# results = scraperwiki.sqlite.select('* from %s.%s' % (SCRAPERNAME, TABLE) )
# scraperwiki.sqlite.save([], results, table_name=NEW_TABLE_NAME)


# Without Variables just to understand the code better - less elegant than the Sample from Ross but for understanding

# scraperwiki.sqlite.attach('eu_efre_unitedkingdom_scotland');
# tables = scraperwiki.sqlite.show_tables('eu_efre_unitedkingdom_scotland')
# print tables
# results = scraperwiki.sqlite.select('* from %s.%s' % ('eu_efre_unitedkingdom_scotland', 'EFRE_EU_UnitedKingdom_Scotland') )
# scraperwiki.sqlite.save([], results, table_name='europe_efre_payments')



# Short version
# In the select statement (Results) you can define which columns you want to retrieve from the source table
# If the scraper runs a second time, and there is no key column defined, the new seelect records will be added
# If there is no target table, it will be created automatically
# Scraper: EU_EFRE_UnitedKingdom_Scotland - Table: EFRE_EU_UnitedKingdom_Scotland
# As scrapername. use the lowercase name from the URL Link


# In case of error - has to be improved to be more failure tolerant
# check if source table exists

# Either make sure the collector deletes all tables before starting or make sure that the business keys in the tables are correct to avoid that the same record will be added multiple times. 


# DateAndTime    RecNo    AmountApproved    Receiver    Year    AmountPaid    Subject
scraperwiki.sqlite.attach('eu_efre_unitedkingdom_scotland');
results = scraperwiki.sqlite.select('"United Kingdom" as Country, "Scotland" as State, DateAndTime, RecNo, AmountApproved, Receiver, Year, AmountPaid, Subject, "EFRE" as EuFondsConcerned, "good" as quality_coll from eu_efre_unitedkingdom_scotland.EFRE_EU_UnitedKingdom_Scotland' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")


#EFRE_Germany_Hessen.EFRE_EU_GERMANY_HESSEN
#DateAndTime    RecNo    AmountApproved    Receiver    Year    AmountPaid    Subject
scraperwiki.sqlite.attach('efre_germany_hessen');
results = scraperwiki.sqlite.select('"Germany" as Country, "Hessen" as State, DateAndTime, RecNo, AmountApproved, Receiver, Year, AmountPaid, Subject, "EFRE" as EuFondsConcerned, "good" as quality_coll  from efre_germany_hessen.EFRE_EU_GERMANY_HESSEN' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")


# Germany, eu_efre_germany_nordrhein-westfalen 
# DateAndTime    RecNo    AmountApproved    Receiver    Year    AmountPaid    Subject
scraperwiki.sqlite.attach('eu_efre_germany_nordrheinwestfalen');
results = scraperwiki.sqlite.select('"Germany" as Country, "NRW" as State, DateAndTime, RecNo, AmountApproved, Receiver, Year, AmountPaid, Subject, "EFRE" as EuFondsConcerned, "good" as quality_coll  from eu_efre_germany_nordrheinwestfalen.NORDRHEIN_WESTFALEN' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")


# data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'Year' :Year , 'AmountApproved' : AmountApproved, 'AmountPaid' : 0, 'DateAndTime' : today.isoformat()})


# Germany Baden-Wuerttemberg
# eu_efre_germany_badenwuerttemberg.EFRE_EU_GERMANY_BADEN_WUERTTEMBERG
scraperwiki.sqlite.attach('eu_efre_germany_badenwuerttemberg');
results = scraperwiki.sqlite.select('"Germany" as Country, "Baden-Wuerttemberg" as State, DateAndTime, RecNo, AmountApproved, Receiver, Year, AmountPaid, Subject, "EFRE" as EuFondsConcerned, "good" as quality_coll from eu_efre_germany_badenwuerttemberg.EFRE_EU_GERMANY_BADEN_WUERTTEMBERG' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")



# eu_efre_germany_rheinland-pfalz.RHEINLAND_PFALZ
# Possibly the dash makes a problem
scraperwiki.sqlite.attach('eu_efre_germany_rheinlandpfalz');
results = scraperwiki.sqlite.select('"Germany" as Country, "Rheinland-Pfalz" as State, DateAndTime, RecNo, AmountApproved, Receiver, Year, AmountPaid, Subject, "EFRE" as EuFondsConcerned, "good" as quality_coll from eu_efre_germany_rheinlandpfalz.EFRE_EU_GERMANY_RHEINLAND_PFALZ' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")


# France Midi_Pyrenees
# eu_efre_france_midipyrenees.EFRE_EU_FRANCE_MIDIPYRENEES
# data={ 'RecNo' : RecNo , 'Receiver' : Receiver, 'Subject' : Subject, 'ProjectAmount' : ProjectAmount , 'Year' : Year  , 'AmountApproved' : AmountApproved , 'EuFondsConcerned' : EuFondsConcerned , 'ProjectPlace' : ProjectPlace , 'NameBeneficary' : NameBeneficary , 'RegionCode' : RegionCode , 'SpenderBudgetName' : SpenderBudgetName , 'ProjectCategory' : ProjectCategory , 'DateAndTime' : today.isoformat()})
scraperwiki.sqlite.attach('eu_efre_france_midipyrenees');
results = scraperwiki.sqlite.select('"France" as Country, "Midi-Pyrenees" as State, DateAndTime, RecNo, ProjectAmount as AmountApproved, NameBeneficary as Receiver, Year, AmountApproved as AmountPaid, Subject, EuFondsConcerned, "good" as quality_coll  from eu_efre_france_midipyrenees.EFRE_EU_FRANCE_MIDIPYRENEES' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")


# Spain Islas Canarias
# eu_efre_eu_efre_spain_islascanarias.EFRE_EU_SPAIN_ISLAS_CANARIAS
#EFRE_EU_SPAIN_ISLAS_CANARIAS [2497 rows] CREATE TABLE `EFRE_EU_SPAIN_ISLAS_CANARIAS` (`Amount` text, `seqmin` integer, `DateAndTime` text, `Country` text, `seqmax` integer, `PrId` integer, `State` text, `Year` text, `Receiver` text, `SeqRespCol` text, `AmountPaid` text, `Subject` text)
scraperwiki.sqlite.attach('eu_efre_spain_islascanarias');
results = scraperwiki.sqlite.select('Country, State, DateAndTime, PrId as RecNo, Amount as AmountApproved, Receiver as Receiver, Year, AmountPaid, Subject, "EFRE" as EuFondsConcerned, "PartiallyWrong" as quality_coll from eu_efre_spain_islascanarias.EFRE_EU_SPAIN_ISLAS_CANARIAS' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")


# Spain Andalucia
# eu_efre_spain_andalucia.EFRE_EU_SPAIN_ANDALUCIA
# EFRE_EU_SPAIN_ANDALUCIA [10864 rows] CREATE TABLE `EFRE_EU_SPAIN_ANDALUCIA` (`Amount` text, `seqmin` integer, `DateAndTime` text, `Country` text, `seqmax` integer, `PrId` integer, `State` text, `Year` text, `Receiver` text, `SeqRespCol` text, `AmountPaid` text, `Subject` text)
scraperwiki.sqlite.attach('eu_efre_spain_andalucia');
results = scraperwiki.sqlite.select('Country, State, DateAndTime, PrId as RecNo, Amount as AmountApproved, Receiver as Receiver, Year, AmountPaid, Subject, "EFRE" as EuFondsConcerned, "PartiallyWrong" as quality_coll from eu_efre_spain_andalucia.EFRE_EU_SPAIN_ANDALUCIA' )
scraperwiki.sqlite.save([], results, table_name="EU_EFRE_CollectedPayments_MultipleStatesAndCountries")

