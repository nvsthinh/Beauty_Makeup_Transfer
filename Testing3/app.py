from flask import Flask, render_template, Response, send_file
import cv2
import numpy as np
import io

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

frame = None
# Assuming 'capture' is your OpenCV video capture variable
capture = cv2.VideoCapture(2)  # You might need to adjust the argument based on your camera index

def generate_frames():
    global frame
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # _,frame1 = capture.read() # streaming frame thành Video
        # _,frame2 = capture2.read()
        # cv2.imshow('live1', frame1)
        # cv2.imshow('live2', frame2)
        # if cv2.waitKey(1) == ord('q'):
        #     cv2.imwrite("portal1.png", frame1 ) # Chụp ảnh 
        #     # cv2.imwrite("portal2.png", frame2 )
        #     break

        
@app.route('/chup_anh')
def chup_anh():
    #TODO: xu ly data va anh
    cv2.imwrite("./static/test.png", frame)
    return { "frame_path": "./static/test.png" }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_frame')
def capture_frame():
    success, frame = capture.read()
    if success:
        _, buffer = cv2.imencode('.png', frame)
        image_data = io.BytesIO(buffer)
        return send_file(image_data, mimetype='image/png', as_attachment=True, download_name='captured_frame.png')
    else:
        return 'Failed to capture frame'

if __name__ == '__main__':
    app.run(debug=True)
