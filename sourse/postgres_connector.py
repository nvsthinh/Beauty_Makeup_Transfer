# sourse/postgres_connector.py
import psycopg2

def read_database_config(file_path="database_init.txt"):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return {line.split('=')[0]: line.split('=')[1].strip() for line in lines}

database_config = read_database_config()

try:
    conn = psycopg2.connect(
        host=database_config["hostname"],
        database=database_config["dbname"],
        user=database_config["username"],
        password=database_config["password"]
    )
    print(f"Successfully connected to the database with name: {database_config["dbname"]}")
except Exception as e:
    print(f"Failed to connect to the database. Error: {e}")

cur = conn.cursor()
def save_user_record_to_db(user_id: str):
    user_record = user_records[user_id]
    cur.execute(
        "INSERT INTO user_records (user_id, ip_address, org_img, style_id, result) VALUES (%s, %s, %s, %s, %s)",
        (user_id, user_record["ip_address"], user_record["org_img"], user_record.get("style_id"), user_record.get("result"))
    )
    conn.commit()

def get_user_record_from_db(user_id: str):
    cur.execute("SELECT * FROM user_records WHERE user_id = %s", (user_id,))
    db_record = cur.fetchone()
    return {"ip_address": db_record[2], "org_img": db_record[3], "style_id": db_record[4], "result": db_record[5]}