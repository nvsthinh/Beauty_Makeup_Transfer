import psycopg2

class DatabaseManager:
    def __init__(self, file_path="db_info.txt"):
        self.db_config = self.read_db_config(file_path)
        self.conn = self.connect_db()

    def read_db_config(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            return {line.split('=')[0]: line.split('=')[1].strip() for line in lines}

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                host=self.db_config["hostname"],
                database=self.db_config["dbname"],
                user=self.db_config["username"],
                password=self.db_config["password"]
            )
            print(f"Database {self.db_config['dbname']} connected successfully ")
            return conn
        except Exception as e:
            print(f"Failed to connect to the database. Error: {e}")

    def execute_query(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                results = cursor.fetchall()
                return results
        except Exception as e:
            print(f"Something went wrong. Error: {e}")
            return None
        finally:
            cursor.close()

    def show_all_tables(self):
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        return self.execute_query(query)

    def group_style(self, group_style:str):
        query = "SELECT * FROM Styles WHERE GroupType = %s"
        return self.execute_query(query, (group_style,))

    def get_metadata(self, style_id:int):
        query = """
            SELECT I.Item, I.Description as Item_Description, P.Link, P.Description as Product_Description
            FROM Styles S
            JOIN Style_Item SI ON S.StyleID = SI.MUSID
            JOIN Items I ON SI.MUIID = I.ItemID
            JOIN Item_Product IP ON I.ItemID = IP.MUSIID
            JOIN Products P ON IP.PID = P.ProductID
            WHERE S.StyleID = %s
        """
        return self.execute_query(query, (style_id,))
if __name__ == '__main__':
    db = DatabaseManager() #connect luôn với database
    num_table = db.show_all_tables()
    print(num_table)
    group_style = db.group_style("Work Style")
    print(group_style)
    get_meta = db.get_metadata(1)
    print(get_meta)
