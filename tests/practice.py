import pandas as pd
import sqlite3

import referencenotes.constants as k

con = sqlite3.connect(k.PATH)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print(tables)

tables = {
            'items': ['itemID'],
            'itemDataValues': ['valueID', 'value'], # Where names are
            'itemData': ['itemID', 'fieldID', 'valueID'], # valueID is info, fieldID is what info
            'creators': ['creatorID', 'firstName', 'lastName'], # Authors
            'collections': ['collectionID', 'collectionName'], # my collections
            'itemCreators': ['itemID', 'creatorID'], # tie item to author
          }

for table in tables:
    tab = table[0]
    print(tab)
    df = pd.read_sql_query(f"SELECT * from {tab}", con)
    print(df)

df = pd.read_sql_query(f"SELECT * from fields", con)
for index, row in df.iterrows():
    print(f"{row['fieldID']}: {row['fieldName']}")

con.close()
