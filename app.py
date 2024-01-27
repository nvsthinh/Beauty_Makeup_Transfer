import cv2
import json
import base64

from flask import Flask, render_template, Response, request, jsonify
from user_handling import apply_beautygan_filter

app = Flask(__name__)

# 1_Take IP
txtPath = "./user_ip.txt"
imgPath = "./static/test.png"


def loadUserInfo():
    global userInfo
    file = open(txtPath, "r")
    userInfo = file.read()
    userInfo = userInfo.replace("'", '"')
    file.close()
    userInfo = json.loads(userInfo)


def takeIp():
    loadUserInfo()
    return userInfo["ip"]


def addImgInputPath():
    loadUserInfo()
    userInfo["inputImgPath"] = imgPath
    userInfoText = str(userInfo)
    userInfoText = userInfoText.replace("'", '"')
    # print(userInfoText)
    with open(txtPath, "w") as file:
        file.write(userInfoText)


# 2_Connect_to_webcam_then_push it to web
def generate_frames():
    capture = cv2.VideoCapture(0)
    global frame
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode(".jpg", frame)

        # Yield the frame in the response
        yield (
            b"--frame/r/n"
            b"Content-Type: image/jpeg/r/n/r/n" + buffer.tobytes() + b"/r/n"
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chup_anh")
def chup_anh():
    # TODO: xu ly data va anh
    cv2.imwrite(imgPath, frame)
    return {
        "frame_path": "/home/lequocviet/For_Studying/Project/DPL302m/Testing/Testing4/static/test.png"
    }


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/user_ip")
def userip():
    imgPath = "./static/test.png"
    my_string = takeIp()
    image = cv2.imread(imgPath)
    # Convert the image to base64
    _, img_encoded = cv2.imencode(".png", image)
    img_base64 = base64.b64encode(img_encoded.tobytes()).decode("utf-8")

    # Render the template and pass the variables to it
    return render_template("index2.html", my_string=my_string, img_base64=img_base64)


@app.route("/image", methods=["GET"])
def imageHandler():
    try:
        # Specify the image paths
        origin_img_path = "./static/test.png"
        style_img_path = "./static/img2.png"

        # Read images from the paths
        origin_img = cv2.imread(origin_img_path)
        style_img = cv2.imread(style_img_path)

        # Check if images are loaded successfully
        if origin_img is None or style_img is None:
            raise ValueError("Failed to load one or both of the images.")

        # Encode images to base64
        _, origin_img_encoded = cv2.imencode(".png", origin_img)
        _, style_img_encoded = cv2.imencode(".png", style_img)

        # Check if encoding is successful
        if origin_img_encoded is None or style_img_encoded is None:
            raise ValueError("Failed to encode one or both of the images.")

        origin_base64 = base64.b64encode(origin_img_encoded.tobytes()).decode("utf-8")
        style_base64 = base64.b64encode(style_img_encoded.tobytes()).decode("utf-8")
        print("avatar " + origin_base64)

        # Apply beautygan_filter function
        output_img = apply_beautygan_filter(origin_img, style_img)

        # Check if the output image is valid
        if output_img is None:
            raise ValueError("Failed to generate the result image.")

        # Encode the result image to base64
        # _, output_img_encoded = cv2.imencode(".png", output_img)
        print(apply_beautygan_filter(origin_img, style_img))

        # if output_img_encoded is None:
        #     raise ValueError("Failed to encode the result image.")

        # output_base64 = base64.b64encode(output_img_encoded.tobytes()).decode("utf-8")

        return jsonify(
            {
                # "origin_image": origin_base64,
                # "style_image": style_base64,
                "result_image": output_img,
            }
        )
        return jsonify({"msg": "done"})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
