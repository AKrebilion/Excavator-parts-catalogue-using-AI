from flask import Flask, make_response, request, jsonify
import cv2
import base64
import numpy as np
from brain import *

app = Flask(__name__)
@app.route("/excavator",methods=["POST"])
def Proctoring():
    if request.headers["Content-Type"] == "application/octet-stream":
        try:
            video_data=request.data
            
            with open('received_video.mp4', 'wb') as file:
                file.write(video_data)

            Resp = ProcessRequest('received_video.mp4')
            
            if Resp["status"] == 200:
                # Save the result as JSON
                with open('result.json', 'w') as json_file:
                    json.dump(Resp, json_file,indent=4)
                return make_response(jsonify({"message":"Excavator parts detected"}),200)
            else:
                return make_response(jsonify({"message":"No video found"}),202)
        except Exception as e:
            return make_response(jsonify({"StatusCode":500,"Error":str(e)}),200)
    else:
        return make_response(jsonify({"StatusCode":415, "Error":"Wrong Content-Type"}), 200)
        