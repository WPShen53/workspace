import pandas as pd
import pymongo
import json
import pprint

dbclient = pymongo.MongoClient("mongodb://localhost:27017")
print(dbclient.list_database_names())
for db in dbclient.list_databases(): pprint.pprint(db)

coviddb = dbclient["tw_covid"]
for col in coviddb.list_collections(): pprint.pprint(col)

col_da = coviddb["daily.announcement"]
pprint.pprint(col_da.find_one())

## Insert document from json files
# with open("./data/tw20210607.json") as f:
#    file_data = json.load(f)
# col_da.insert_one(file_data)

## Delete documents
# col_da.delete_one({"date":"2020-01-01"})

## Get death trend
death = {}
records = col_da.find({"dead":{"$exists":True}}, {"_id":0, "date":1, "dead":1}).sort("date", -1)
for x in records: 
    death[x["date"]]=x["dead"]
pprint.pprint(death)
df_death = pd.DataFrame.from_dict(death, orient="index")
# df_death.index = pd.to_datetime(df_death.index)
df_death.rename(columns={0:"dead"}, inplace=True)
df_death.plot.barh()

## Find Min/Max of a date
searchDate = "2021-05-31"
val = []
records = col_da.find({"corrections.date": searchDate}, {"_id":0, "date":1, "corrections.cases.$":1}).sort("date", 1)
for _i, x in enumerate(records):
    pprint.pprint(x)
    val.append(int(x["corrections"][0]["cases"]))
print (searchDate, val)
print ("Min =", min(val), "Max=", max(val))

dbclient.close()
