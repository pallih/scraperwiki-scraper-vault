import scraperwiki
import csv

scraperwiki.sqlite.execute('CREATE TABLE `wards` (`ward` TEXT,`ward_id` INTEGER,`employment_-_large_employers_and_higher_managerial_occupations` REAL,`employment_-_higher_professional_occupations` REAL,`employment_-_lower_managerial_and_professional_occupations` REAL,`employment_-_intermediate_occupations` REAL,`employment_-_small_employers_and_own_account_workers` REAL,`employment_-_lower_supervisory_and_technical_occupations` REAL,`employment_-_semi-routine_occupations` REAL,`employment_-_routine_occupations` REAL,`employment_-_never_worked` REAL,`employment_-_long-term_unemployed` REAL,`employment_-_full-time_students` REAL,`employment_-_not_classifiable_for_other_reasons` REAL,`age_-_0-15` REAL,`age_-_16-24` REAL,`age_-_25-59` REAL,`age_-_60plus` REAL,`ethnicity_-_british` REAL,`ethnicity_-_irish` REAL,`ethnicity_-_other_white` REAL,`ethnicity_-_mixed_white_and_black_caribbean` REAL,`ethnicity_-_mixed_white_and_black_african` REAL,`ethnicity_-_mixed_white_and_asian` REAL,`ethnicity_-_other_mixed` REAL,`ethnicity_-_indian` REAL,`ethnicity_-_pakistani` REAL,`ethnicity_-_bangladeshi` REAL,`etnic_-_other_asian` REAL,`ethnicity_-_black_caribbean` REAL,`ethnicity_-_black_african` REAL,`ethnicity_-_other_black` REAL,`ethnic_-_chinese` REAL,`ethnicity_-_other_ethnicity_group` REAL,`cob_-_england` REAL,`cob_-_scotland` REAL,`cob_-_wales` REAL,`cob_-_n_ireland` REAL,`cob_-_rep_of_ireland` REAL,`cob_-_other_eu` REAL,`cob_-_elsewhere` REAL,`religion_-_christian` REAL,`religion_-_buddhist` REAL,`religion_-_hindu` REAL,`religion_-_jewish` REAL,`religion_-_muslim` REAL,`religion_-_sikh` REAL,`religion_-_other` REAL,`religion_-_none` REAL,`religion_-_no_stated`)')
scraperwiki.sqlite.commit()

data = scraperwiki.scrape("http://files.zarino.co.uk/scraperwiki/birmingham_ward_demographic_data.csv")

reader = csv.DictReader(data.splitlines())

for row in reader:
    row['ward_id'] = int(row['ward_id'].replace('id ', ''))
    scraperwiki.sqlite.save(['ward_id'], row, 'wards')
