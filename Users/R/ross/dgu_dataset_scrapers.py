import scraperwiki

# Don't forget to run this scraper if you add a new one to the list

scraperwiki.sqlite.save(['name'], {'name': 'dfid_energy_and_water', 'type': 'simple'}, "data")
scraperwiki.sqlite.save(['name'], {'name': 'dgu_city_hackney_pct_spend', 'type': 'simple'}, "data") 
scraperwiki.sqlite.save(['name'], {'name': 'dgu_derbyshire_ft_transparency', 'type': 'simple'}, "data") 
scraperwiki.sqlite.save(['name'], {'name': 'dgu_treasury_gpc', 'type': 'simple'}, "data") 
scraperwiki.sqlite.save(['name'], {'name': 'dgu_cafcass_spend', 'type': 'simple'}, "data") 
scraperwiki.sqlite.save(['name'], {'name': 'dgu_central_manchester_nhs_ft_spending', 'type': 'simple'}, "data") 
scraperwiki.sqlite.save(['name'], {'name': 'dgu_fireservicecollege_spending', 'type': 'simple'}, "data") 

