from scraperwiki.sqlite import save,execute,commit

save([],[{"a":"bb"},{"g":"aoeu"},{"a":"hurc"}])
execute("UPDATE `swdata` SET g=? WHERE a=?",["eo","bb"])
commit()from scraperwiki.sqlite import save,execute,commit

save([],[{"a":"bb"},{"g":"aoeu"},{"a":"hurc"}])
execute("UPDATE `swdata` SET g=? WHERE a=?",["eo","bb"])
commit()