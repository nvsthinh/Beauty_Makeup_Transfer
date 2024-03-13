import pyodbc
import base64
from PIL import Image
import os
from pathlib import Path
class DatabaseManager:
    def __init__(self, file_path="./data/db_info.txt"):
        self.db_config = self.read_db_config(file_path)
        self.conn,self.status = self.connect_db()

    def read_db_config(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            return {line.split('=')[0]: line.split('=')[1].strip() for line in lines}

    def connect_db(self):
        try:
            conn = pyodbc.connect(f"DRIVER={{SQL Server}};Server={self.db_config['hostname']};Database={self.db_config['dbname']};UID={self.db_config['username']};PWD={self.db_config['password']}")
            return conn,"Success: Connected to the database"
        except Exception as e:
            return None,f"Error: {e} while connecting to the database"

    def execute_query(self, query, params=None, fetch_results=True):
        try:
            with self.conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if fetch_results:
                    results = cursor.fetchall()
                    return results, f"Success: Executed query"
                else:
                    return None, f"Success: Executed query (No results to fetch)"
        except Exception as e:
            error_message = f"Error: {e} while executing query"
            return None, error_message
        finally:
            cursor.close()

    def save_record(self, ip_address, org_img, style_id, result):
        try:
            query = "INSERT INTO UserRecord (ipaddress, orgimage, styleid, result) VALUES (%s, %s, %s, %s)"
            params = (ip_address, org_img, style_id, result)
            self.execute_query(query, params, fetch_results=False)
            self.conn.commit()
            return "Success: Record inserted successfully"
        except Exception as e:
            error_message = f"Failed to insert user record. Error: {e}"
            self.conn.rollback()
            return error_message

    def show_all_tables(self):
        query = "SELECT name FROM sys.tables"
        return self.execute_query(query)
    def convert_image_to_base64(self, image_path):
        try:
            with Image.open(image_path,"r") as image:
                image_bytes = image.tobytes()
                base64_string = base64.b64encode(image_bytes).decode("utf-8")
                return base64_string
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found: {image_path}")
        except (IOError, OSError) as e:
            raise IOError(f"Error processing image file: {e}")

    def group_style(self):
        query = "SELECT * FROM Styles"
        results, status = self.execute_query(query)
        # Group results by key
        grouped_results = {}
        for item in results:
            key = item[3]  # Assuming 'key' field is stored in the 4th column
            style_data = {
                "StyleID": item[0],
                "Img": self.convert_image_to_base64(os.path.join(os.path.dirname(os.path.abspath(__file__)),"images\\styles\\",item[1].strip())),  # Convert image to base64
                "Style Description": item[2],
            }

            if key not in grouped_results:
                grouped_results[key] = []
            grouped_results[key].append(style_data)

        # Prepare final JSON structure
        final_results = [
            {"key": key, "data": styles} for key, styles in grouped_results.items()
        ]

        return {"result": final_results, "status": status}


    def get_metadata(self, style_id: int):
        query = """
            SELECT I.Item, I.Description as Item_Description, P.Img ,P.Link, P.Description as Product_Description
            FROM Styles S
            JOIN Style_Item SI ON S.StyleID = SI.MUSID
            JOIN Items I ON SI.MUIID = I.ItemID
            JOIN Item_Product IP ON I.ItemID = IP.MUSIID
            JOIN Products P ON IP.PID = P.ProductID
            WHERE S.StyleID = ?
        """
        results, status = self.execute_query(query, (style_id,))
        formatted_results = [
            {
                "Item": item[0],
                "Item_Description": item[1],
                "Img": self.convert_image_to_base64(os.path.join(os.path.dirname(os.path.abspath(__file__)),"images\\items\\",item[2].strip())),
                "Link": item[3],
                "Product_Description": item[4]
            }
            for item in results
        ]

        return {"key": style_id, "result": formatted_results, "status": status}
