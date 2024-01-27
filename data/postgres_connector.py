import psycopg2
import api
def read_db_config(file_path="db_info.txt"):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return {line.split('=')[0]: line.split('=')[1].strip() for line in lines}


def connect_db(db_config):
    try:
        conn = psycopg2.connect(
            host=db_config["hostname"],
            database=db_config["dbname"],
            user=db_config["username"],
            password=db_config["password"]
        )
        print(f"Successfully connected to the database with name: {db_config["dbname"]}")
        return conn
    except Exception as e:
        print(f"Failed to connect to the database. Error: {e}")

def save_record(cur,user_records):
    try:
        cur.execute(
            "INSERT INTO user_records (user_id, ip_address, org_img, style_id, result) VALUES (%s, %s, %s, %s, %s)",
            (user_id, user_record["ip_address"], user_record["org_img"], user_record.get("style_id"), user_record.get("result"))
        )
        print(f"Successfully inserted")
        cur.commit()
    except Exception as e:
        print(f"Failed to insert the record. Error: {e}")
        cur.rollback()
        cur.close()

def get_user(user_id: str):
    cur.execute("SELECT * FROM user_records WHERE user_id = %s", (user_id,))
    db_record = cur.fetchone()
    return {"ip_address": db_record[2], "org_img": db_record[3], "style_id": db_record[4], "result": db_record[5]}
def show_all_tables(cursor):

    # Lấy tất cả các bảng trong schema 'public'
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

    # Sử dụng fetchall() để lấy danh sách tên bảng
    tables = cursor.fetchall()

    #close
    cursor.close()

    # Trả về số lượng bảng
    return tables
def group_style(cursor,groupStyle:str):
    try:
        # Thực hiện truy vấn với tham số
        cursor.execute('SELECT * FROM Styles WHERE GroupType = %s', (groupStyle,))

        # Lấy tất cả kết quả
        results = cursor.fetchall()
        for row in results:
            print(row[3])
        # Kiểm tra xem có kết quả hay không
        if not results:
            return "Không tìm thấy kết quả cho {}".format(groupStyle)
        else:
            return results
    except Exception as e:
        return f"Something went wrong. Error: {e}"
    finally:
        #close cursor
        cursor.close()

if __name__ == "__main__":
    db_config = read_db_config()
    conn = connect_db(db_config)
    cur1 = conn.cursor() #tạo cursor 1
    print(show_all_tables(cur1))
    cur2 = conn.cursor() #tạo cursor 2
    print(group_style(cur2,"Work Style"))

    # user_records = api.get_user_record()  #return dict
    # save_record(user_records)
    conn.close()