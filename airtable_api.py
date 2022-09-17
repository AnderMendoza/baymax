import os
import configparser
from pyairtable import Table
from pyairtable.formulas import match

directory = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(f"{directory}/config.ini")

api_key = str(config.get("airtable", "api_key"))
base_id = str(config.get("airtable", "base_id"))
table_name = str(config.get("airtable", "table_name"))

table = Table(api_key, base_id, table_name)

def get_record_id(username:str):
    try:
        record = table.first(formula=match({"discord_id":username}), sort=["-primary_key"])
        record_id = record['id']
    except Exception as e:
        return e
    return record_id

def get_member_data(username:str):
    try:
        member = table.first(formula=match({"discord_id":username}), sort=["-primary_key"])
    except Exception as e:
        return e
    return member

def update_discord_id(discord_id:str, record_id:str):
    try:
        table.update(record_id, {"snowflake_id":discord_id})
    except Exception as e:
        return e

def delete_duplicate_records(username:str):
    try:
        matches = table.all(formula=match({"discord_id":username}), sort=["-primary_key"])
        duplicates = matches[1:]
        duplicate_ids = [duplicate['id'] for duplicate in duplicates]
        table.batch_delete(duplicate_ids)
    except Exception as e:
        return e

def delete_last_record(username:str):
    try:
        match_record = table.first(formula=match({"discord_id":username}), sort=["-primary_key"])
        match_id = match_record['id']
        table.delete(match_id)
    except Exception as e:
        return e
