# server.py
from flask import Flask, request
from flask_socketio import SocketIO, emit

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
    print(f"[Received Message] {data}")

    target_id = data.get('target_id')  # 想發給誰
    payload = data.get('payload')      # 要發的內容

    if target_id and payload:
        target_sid = car_sessions.get(target_id)
        if target_sid:
            socketio.emit('message', payload, room=target_sid)
            print(f"[Forwarded] to {target_id}")
        else:
            print(f"[Warning] Target {target_id} not connected.")
    else:
        print("[Error] Message missing 'target_id' or 'payload'.")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
