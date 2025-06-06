# server.py
from flask import Flask, request
from flask_socketio import SocketIO, emit
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.func.all_import import *
from src.func.use_llm import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 連線車輛記錄： car_id -> session_id
car_sessions = {}

@socketio.on('register')
def handle_register(car_id):
    print(f"[Register] Car ID: {car_id} -> SID: {request.sid}")
    car_sessions[car_id] = request.sid

@socketio.on('disconnect')
def handle_disconnect():
    print(f"[Disconnected] {request.sid}")
    for car_id, sid in list(car_sessions.items()):
        if sid == request.sid:
            del car_sessions[car_id]
            break

@socketio.on('message')
def handle_message(data):
    """
    data is 協定 with client send_to()
    data is a dict = {
        "target_id": target_id: str,
        "payload": message: any
    }
    """
    print(f"[Received Message] {data}")

    target_id = data.get('target_id')  # 想發給誰
    payload = data.get('payload')      # 要發的內容
    aim = data.get('aim')
    mode = data.get('mode')

    if aim == 'txt to json':
        ##call sth for txt to json 
        #payload is txt str
        reply=txt_to_json_pipeline(payload)
        #payload should change to json at here

    elif aim == 'json to txt':
        ##call sth for json to txt
        #payload is json dict
        reply=json_to_txt_pipeline(payload)
        #payload should change to txt(str) here
    elif aim == 'confirm':
        reply=confirm_pipeline(payload)
    elif aim == 'transport':
        reply=payload
    
    data_pack = {"aim": aim,"mode": mode, "data": reply} #package aim in data to receive so that we know receiver or sender

    if target_id and data_pack:
        target_sid = car_sessions.get(target_id)
        if target_sid:
            socketio.emit('message', data_pack, room=target_sid)
            print(f"[Forwarded] to {target_id}")
        else:
            print(f"[Warning] Target {target_id} not connected.")
    else:
        print("[Error] Message missing 'target_id' or 'reply'.")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)