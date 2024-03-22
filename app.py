import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from data.util import DatabaseManager
from model import apply_beautygan_filter
import tempfile
import os
import socket
import uvicorn
from data import  util

class ImageProcessingApp:
    def __init__(self):
        self.app = FastAPI()
        self.db_manager = DatabaseManager()

        # Enable CORS for all routes
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # @self.app.get("/image")
        # def read_image():
        #     try:
        #         origin_img_path = "./images/users_input/1.png"
        #         style_img_path = "./images/styles/1.png"
        #
        #         output_img = apply_beautygan_filter(origin_img_path, style_img_path)
        #
        #         if output_img is None:
        #             raise HTTPException(status_code=500, detail="Failed to generate the result image.")
        #
        #         return {"result_image": output_img}
        #
        #     except Exception as e:
        #         raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/image")
        def create_image(data: dict):
            origin_img_base64 = data.get("origin_img_base64", "")
            style_img_base64 = data.get("style_img_base64", "")

            try:
                # Xử lý origin_img_base64
                if origin_img_base64.startswith("data:image/png;base64,"):
                    origin_img_base64 = origin_img_base64.split(",")[1]  # Loại bỏ tiền tố

                origin_img_data = base64.b64decode(origin_img_base64)

                # Xử lý style_img_base64
                if style_img_base64.startswith("data:image/png;base64,"):
                    style_img_base64 = style_img_base64.split(",")[1]  # Loại bỏ tiền tố

                style_img_data = base64.b64decode(style_img_base64)

                origin_img_path = self.get_temp_file_path(".png")
                style_img_path = self.get_temp_file_path(".png")

                with open(origin_img_path, "wb") as origin_file:
                    origin_file.write(origin_img_data)

                with open(style_img_path, "wb") as style_file:
                    style_file.write(style_img_data)

                result_data = apply_beautygan_filter(origin_img_path, style_img_path)

                return {"result_data": result_data}

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            # finally:
            #
            #     if origin_img_path and os.path.exists(origin_img_path):
            #         os.remove(origin_img_path)
            #
            #     if style_img_path and os.path.exists(style_img_path):
            #         os.remove(style_img_path)

        @self.app.get("/test")
        def read_test():
            return {"msg": "test successful"}

        @self.app.get("/group_style")
        def group_style():
            return self.db_manager.group_style()

        @self.app.get("/get_metadata")
        def get_metadata(style_id: int):
            return self.db_manager.get_metadata(style_id)

        @self.app.get("/check_connection")
        def check_connection():
            return {"status": self.db_manager.status}
    def run(self):
        # host = socket.gethostbyname(socket.gethostname())
        host = "192.168.0.100"
        port = 5000
        uvicorn.run(self.app, host=host, port=port)

    def get_temp_file_path(self, suffix: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            return temp_file.name

    def cleanup_temp_files(self, *file_paths: str) -> None:
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    app = ImageProcessingApp()
    app.run()
