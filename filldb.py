import sqlite3
import json
import csv

con = sqlite3.connect("data.db")
cur = con.cursor()

# with open("regions.json", "r") as json_file:
#     regs = json.load(json_file)
#     for rec in regs['records']:
#
#         cur.execute("INSERT into regions values(:ID, :CODE_FNS, :SUBJECT)", rec['data'])
#         con.commit()

with open("pkk_cadastral_rayons.csv", newline="") as csvfile:
    districts = csv.DictReader(csvfile, delimiter=";")
    for rec in districts:
        cn = rec['attrs_cn'].split(':')[0]
        # print(f"INSERT into districts values({int(rec['id'])}, {rec['attrs_cn']}, {rec['attrs_name']}, {cn})")
        cur.execute(f"INSERT into districts values({int(rec['id'])}, '{rec['attrs_cn']}', '{rec['attrs_name']}', '{cn}')")
        con.commit()
        
con.close()

