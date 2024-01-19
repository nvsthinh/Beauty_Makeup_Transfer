# backend/user_handling.py
from backend.postgres_connector import save_user_record_to_db, get_user_record_from_db

user_records = {}

def add_user_record(user_id: str, ip_address: str, org_img: str):
    user_records[user_id] = {"ip_address": ip_address, "org_img": org_img}

def choose_style(user_id: str, style_id: str):
    user_records[user_id]["style_id"] = style_id
    save_user_record_to_db(user_id)

def show_result(user_id: str):
    user_record = get_user_record_from_db(user_id)
    return {"user_id": user_id, "result": user_record["result"]}