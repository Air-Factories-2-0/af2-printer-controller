from flask import Flask, request, jsonify, Response , send_file
import json, threading, time, picamera, os
app=Flask(__name__)



@app.route('/', methods = ["GET"])
def action():
    action = request.args.get("action")
    if action == "snapshot":
        with picamera.PiCamera() as camera:
            #camera.resolution = (2592,1944)
            camera.contrast = 100
            camera.brightness = 70
            camera.start_preview()
            # Camera warm-up time
            time.sleep(5)
            camera.capture('_tmp/test.png')
        return send_file("_tmp/test.png", mimetype='image/png')
    else:
        return Response(json.dumps({"Error":"Action not recognized"}), 400, mimetype="application/json")


if __name__=='__main__':
    app.run(host='0.0.0.0', port=9080)
