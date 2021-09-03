import sqlite3
import os
from typing import List, Dict, Union
import pandas as pd

import referencenotes.constants as k

reference_folder = 'references'
try:
    os.mkdir(reference_folder)
except FileExistsError:
    pass

con = sqlite3.connect(k.PATH)
cur = con.cursor()

def get_rows_from_table(table: str, col_name: str, value: Union[str, int]):
    if isinstance(value, str):
        cur.execute(f"SELECT * FROM {table} WHERE {col_name} = '{value}'")
    else:
        cur.execute(f"SELECT * FROM {table} WHERE {col_name} = {value}")
    cols = list(map(lambda x: x[0], cur.description))
    val_id = cur.fetchall()
    return [{cols[i]: val_id[j][i] for i in range(len(cols))} 
            for j in range(len(val_id))]

def get_row_from_table(table: str, col_name: str, value: Union[str, int]):
    if isinstance(value, str):
        cur.execute(f"SELECT * FROM {table} WHERE {col_name} = '{value}'")
    else:
        cur.execute(f"SELECT * FROM {table} WHERE {col_name} = {value}")
    cols = list(map(lambda x: x[0], cur.description))
    val_id = cur.fetchall()
    return {cols[i]: val_id[0][i] for i in range(len(cols))}

def create_template_data(value: str) -> Dict[str, Union[str, List[str]]]:
    """Creates data for template by coagulating data from value.

    Args:  
        value (str):  
            Some value to be searched for in itemDataValues table.

    Returns: 
        template (Dict[str, Union[str, List[str]]]):  
            Dictionary with {  
            'Title': str,  
            'Author': [authors],  
            'collection': str,  
            (and if available)  
            'Date of Publication': str,  
            'Journal': str,  
            'doi': str  
            }
    """
    template = {}
    itemDict = get_row_from_table('itemDataValues', 'value', value)
    itemData = get_row_from_table('itemData', 'valueID', itemDict['valueID'])
    itemCreators = get_rows_from_table('itemCreators', 'itemID', itemData['itemID'])
    creators = [get_row_from_table('creators', 'creatorID', 
            itemCreators[i]['creatorID']) for i in 
            range(len(itemCreators))]
    template['Authors'] = [[creator['firstName'], creator['lastName']] for creator
            in creators]
    collectionItem = get_row_from_table('collectionItems', 'itemID', 
            itemData['itemID'])
    collection = get_row_from_table('collections', 'collectionID', 
            collectionItem['collectionID'])
    template['collection'] = collection['collectionName']
    fieldIDs = get_rows_from_table('itemData', 'itemID', itemData['itemID'])
    try:
        dateID = [fields['valueID'] for fields in fieldIDs 
                  if fields['fieldID'] == k.DATE][0]
        date = get_row_from_table('itemDataValues', 'valueID', dateID)
        template['Date of Publication'] = date['value']
    except IndexError:
        pass
    try:
        pubID = [fields['valueID'] for fields in fieldIDs 
                if fields['fieldID'] == k.PUBLISHER][0]
        pub = get_row_from_table('itemDataValues', 'valueID', pubID)
        template['Journal'] = pub['value']
    except IndexError:
        pass
    try:
        doiID = [fields['valueID'] for fields in fieldIDs 
                if fields['fieldID'] == k.DOI][0]
        doi = get_row_from_table('itemDataValues', 'valueID', doiID)
        template['doi'] = doi['value']
    except IndexError:
        pass
    try:
        doiID = [fields['valueID'] for fields in fieldIDs 
                if fields['fieldID'] == k.TITLE][0]
        doi = get_row_from_table('itemDataValues', 'valueID', doiID)
        template['Title'] = doi['value']
    except IndexError:
        pass
    
    return template

def create_template_md(template, lines):
    """Creates template md file"""
    save_folder = os.path.join(reference_folder, template['collection'])
    try:
        os.mkdir(save_folder)
    except FileExistsError:
        pass
    # Use first author last name + 
    name = template['Authors'][0][1] + "".join(template['Title'].split()[:3])
    name = os.path.join(save_folder, name + '.md')
    with open(name, 'a') as f:
        for line in lines:
            for key in template:
                if key == line:
                    if key == 'Title':
                        f.write(f"#{template[key]}\n")
                    else:
                        f.write(f"##{key}")
                        if key == 'Authors':
                            for author in template[key]:
                                f.write(f"{author[0]} {author[1]}\n")
                        else:
                            f.write(f"{template[key]}\n")
                else:
                    f.write(line + '\n')

value = 'On Splitting Training and Validation Set: A Comparative Study of Cross-Validation, Bootstrap and Systematic Sampling for Estimating the Generalization Performance of Supervised Learning'
template = create_template_data(value)
create_template_md(template, k.MD_lines)
