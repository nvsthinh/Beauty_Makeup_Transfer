import psycopg2
import base64
from PIL import Image
import os
import io

class DatabaseManager:
    def __init__(self, file_path="./data/db_info.txt"):
        self.db_config = self.read_db_config(file_path)
        self.conn, self.status = self.connect_db()

    def read_db_config(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            return {line.split('=')[0]: line.split('=')[1].strip() for line in lines}

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                dbname=self.db_config['dbname'],
                user=self.db_config['username'],
                password=self.db_config['password'],
                host=self.db_config['hostname'],
            )
            print("connect successful")
            return conn, "Success: Connected to the database"
        except Exception as e:
            print("connect error", e)
            return None, f"Error: {e} while connecting to the database"

    def execute_query(self, query, params=None, fetch_results=True):
        try:
            with self.conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if fetch_results:
                    results = cursor.fetchall()
                    return results, "Success: Executed query"
                else:
                    self.conn.commit()
                    return None, "Success: Executed query (No results to fetch)"
        except Exception as e:
            self.conn.rollback()  # Rollback in case of error
            return None, f"Error: {e} while executing query"
        finally:
            if 'cursor' in locals():
                cursor.close()

    def save_record(self, ip_address, org_img, style_id, result):
        try:
            query = "INSERT INTO UserRecord (ipaddress, orgimage, styleid, result) VALUES (%s, %s, %s, %s)"
            params = (ip_address, org_img, style_id, result)
            self.execute_query(query, params, fetch_results=False)
            return "Success: Record inserted successfully"
        except Exception as e:
            return f"Failed to insert user record. Error: {e}"

    def show_all_tables(self):
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        return self.execute_query(query)

    def convert_image_to_base64(self, image_path):
        try:
            with Image.open(image_path) as image:
                # Chuẩn bị một buffer trong bộ nhớ
                buffered = io.BytesIO()
                # Lưu hình ảnh vào buffer ở định dạng ban đầu
                image_format = image.format  # Lấy định dạng hình ảnh (PNG, JPEG, etc.)
                image.save(buffered, format=image_format)
                # Chuyển buffer thành base64
                base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
                # Thêm header MIME phù hợp
                # return f"data:image/{image_format.lower()};base64,{base64_string}"
                return f"{base64_string}"

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
            # Use os.path.join for cross-platform compatibility
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "styles", item[1].strip())
            style_data = {
                "StyleID": item[0],
                "base64": self.convert_image_to_base64(image_path),  # Convert image to base64
                "description": item[2],
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
            SELECT I.Item, I.Description as Item_Description, P.Img, P.Link, P.Description as Product_Description
            FROM Styles S
            JOIN Style_Item SI ON S.StyleID = SI.MUSID
            JOIN Items I ON SI.MUIID  = I.ItemID
            JOIN Item_Product IP ON I.ItemID = IP.MUSIID
            JOIN Products P ON IP.PID = P.ProductID
            WHERE S.StyleID = %s
        """
        try:
            # print("Executing query:", query)  # In ra truy vấn trước khi thực thi
            results, status = self.execute_query(query, (style_id,))
            # print("Query results:", results)  # In kết quả của truy vấn

            if results is None:
                return {"key": style_id, "result": [], "status": "No results found"}

            formatted_results = [
                {
                    "Item": item[0],
                    "Item_Description": item[1],
                    # Use os.path.join for cross-platform compatibility
                    "Img": self.convert_image_to_base64(
                        os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "items", item[2].strip())),
                    "Link": item[3],
                    "Product_Description": item[4]
                }
                for item in results
            ]
            return {"key": style_id, "result": formatted_results, "status": status}
        except Exception as e:
            return {"key": style_id, "result": [], "status": f"Error: {e}"}