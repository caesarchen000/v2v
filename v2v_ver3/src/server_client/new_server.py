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

import os
import json

def create_server_folder():
    """創建 server 主資料夾（如果不存在）"""
    try:
        os.makedirs("server", exist_ok=True)
        print(f'[System] Server 主資料夾已準備: {os.path.abspath("server")}')
    except Exception as e:
        print(f"[System] 創建 server 資料夾時發生錯誤: {str(e)}")
        raise

def create_sender_folder(json_path: str):
    """
    根據 JSON 檔案中的「來自的車牌號碼」在 server 資料夾內創建資料夾結構
    結構: server/車牌號碼/{receiver_tmp, sender_tmp}
    """
    try:
        create_server_folder()
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        license_plate = data.get("來自的車牌號碼", "unknown")
        
        if license_plate == "none":
            print(f"[Sender] 警告: 車牌號碼為 'none'，使用 'unknown' 作為資料夾名稱")
            license_plate = "unknown"
        
        # 創建主資料夾（在 server 資料夾內）
        main_folder = os.path.join("server", license_plate)
        os.makedirs(main_folder, exist_ok=True)
        print(f"[Sender] 主資料夾創建成功: {os.path.abspath(main_folder)}")
        
        # 創建子資料夾
        subfolders = ["receiver_tmp", "sender_tmp"]
        for subfolder in subfolders:
            subfolder_path = os.path.join(main_folder, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)
            print(f"[Sender] 子資料夾創建成功: {os.path.abspath(subfolder_path)}")
    
    except FileNotFoundError:
        print(f"[Sender] 錯誤: 找不到 JSON 檔案 {json_path}")
    except json.JSONDecodeError:
        print(f"[Sender] 錯誤: JSON 檔案格式不正確 {json_path}")
    except Exception as e:
        print(f"[Sender] 未預期錯誤: {str(e)}")

def create_client_folder(json_path: str):
    """
    根據 JSON 檔案中的「傳給的車牌號碼」在 server 資料夾內創建資料夾結構
    結構: server/車牌號碼/{receiver_tmp, sender_tmp}
    """
    try:
        create_server_folder()
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        license_plate = data.get("傳給的車牌號碼", "unknown")
        
        if license_plate == "none":
            print(f"[Client] 警告: 車牌號碼為 'none'，使用 'unknown' 作為資料夾名稱")
            license_plate = "unknown"
        
        # 創建主資料夾（在 server 資料夾內）
        main_folder = os.path.join("server", license_plate)
        os.makedirs(main_folder, exist_ok=True)
        print(f"[Client] 主資料夾創建成功: {os.path.abspath(main_folder)}")
        
        # 創建子資料夾
        subfolders = ["receiver_tmp", "sender_tmp"]  # 注意: 這裡使用 receiver_tmp 保持一致性
        for subfolder in subfolders:
            subfolder_path = os.path.join(main_folder, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)
            print(f"[Client] 子資料夾創建成功: {os.path.abspath(subfolder_path)}")
    
    except FileNotFoundError:
        print(f"[Client] 錯誤: 找不到 JSON 檔案 {json_path}")
    except json.JSONDecodeError:
        print(f"[Client] 錯誤: JSON 檔案格式不正確 {json_path}")
    except Exception as e:
        print(f"[Client] 未預期錯誤: {str(e)}")

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
    aim = data.get('aim')
    payload = data.get('payload')      # 要發的內容
    mode = data.get('mode')
    if aim == 'tell correctness':
        # tell sender or receiver the correctness of the message
        # payload is a str, like "json_correct"
        reply = payload
        if reply == "json_correct":
            print("[Correctness] json_correct")
            open_path="../../server_storage/"+target_id+mode
            with open(open_path, 'r', encoding='utf-8') as f:
                content=json.load(f)
                if mode == "sender_tmp/sender.json":
                    sender_notyet_confirm_message=json_to_txt_pipeline(content)
                    # save txt file in sender_tmp folder
                    with open('../../server_storage/'+target_id+'sender_tmp/sender.txt', 'w', encoding='utf-8') as f:
                        f.write(sender_notyet_confirm_message)
                    # and send txt back to sender
                    data_pack={"aim": "tell correctness", "mode": "sender_tmp/sender_notyey_confirm", "data": sender_notyet_confirm_message}
                    socketio.emit('message', data_pack, room=target_id)
                    print("send sender_notyet_confirm.txt back to sender")
                elif mode == "receiver_tmp/receiver.json":
                    receiver_notyet_confirm_message=json_to_txt_pipeline(content)
                    # save txt file in receiver_tmp folder
                    with open('../../server_storage/'+target_id+'receiver_tmp/receiver.txt', 'w', encoding='utf-8') as f:
                        f.write(receiver_notyet_confirm_message)
                    # and send txt back to receiver
                    data_pack={"aim": "tell correctness", "mode": "receiver_tmp/receiver_notyet_confirm", "data": receiver_notyet_confirm_message}
                    socketio.emit('message', data_pack, room=target_id)
                    print("send receiver_notyet_confirm.txt back to receiver")


        elif reply == "final_confirm":
            content=data.get('content')
            print("[Correctness] final_confirm")
            open_path="../../server_storage/"+target_id+mode
            with open(open_path, 'r', encoding='utf-8') as f:
                content=f.read()
                if mode == "sender_tmp/sender_final_confirm.txt":
                    sender_final_confirm_result=confirm_pipeline(content)
                    if sender_final_confirm_result == "1":
                        # send message to receiver
                        with open('../../server_storage/'+target_id+'sender_tmp/sender_notyet_confirm.txt', 'r', encoding='utf-8') as f:
                            content=f.read()
                            # save txt file in sender_tmp folder
                            with open('../../server_storage/'+target_id+'sender_tmp/sender.json', 'r', encoding='utf-8') as f2:
                                json_message=json.load(f2)
                                receiver_id=json_message.get("傳給的車牌號碼")
                                sender_id=json_message.get("來自的車牌號碼")
                                data_pack_for_sender={"aim": "tell send", "mode": "1", "data": content}
                                target_sid=car_sessions.get(sender_id)
                                if target_sid:
                                    socketio.emit('message', data_pack_for_sender, room=target_sid)
                                    print("send sender_final_confirm.txt back to sender")
                                # and send txt back to sender
                                # write received.txt in server_storage/receiver_tmp folder
                                with open('../../server_storage/'+receiver_id+'receiver_tmp/received.txt', 'w', encoding='utf-8') as f3:
                                    f3.write(content)
                                with open('../../server_storage/'+receiver_id+'receiver_tmp/received.json', 'w', encoding='utf-8') as f4:
                                    json.dump(json_message, f4, ensure_ascii=False, indent=4)
                                    # and send txt back to receiver
                                data_pack={"aim": 'transport', "mode": "receiver_tmp/received.txt", "data": content}
                                target_sid=car_sessions.get(receiver_id)
                                if target_sid:
                                    socketio.emit('message', data_pack, room=target_sid)
                                    print("send received.txt back to receiver")
                    # tell sender everything is ok and message been forwarded to receiver

                    else:
                        pass
                elif mode == "receiver_tmp/receiver_final_confirm.txt":
                    receiver_final_confirm_result=confirm_pipeline(content)
                    if receiver_final_confirm_result == "1":
                        # send message to sender
                        with open('../../server_storage/'+target_id+'sender_tmp/sender.json','r', encoding='utf-8') as f:
                            json_message=json.read(f)
                            # save txt file in sender_tmp folder
                            sender_id=json_message.get("來自的車牌號碼")
                            receiver_id=json_message.get("傳給的車牌號碼")
                            with open('../../server_storage/'+receiver_id+'receiver_tmp/receiver_notyet_confirm.txt', 'r', encoding='utf-8') as f2:
                                content=f2.read()
                                # and send txt back to receiver
                                data_pack_for_receiver={"aim": "tell send", "mode": "1", "data": content}
                                target_sid=car_sessions.get(receiver_id)
                                if target_sid:
                                    socketio.emit('message', data_pack_for_receiver, room=target_sid)
                                    print("send receiver_final_confirm.txt back to receiver")
                                # write received.txt in server_storage/receiver_tmp folder
                                with open('../../server_storage/'+sender_id+'sender_tmp/received.txt', 'w', encoding='utf-8') as f3:
                                    f3.write(content)
                                with open('../../server_storage/'+sender_id+'sender_tmp/received.json', 'w', encoding='utf-8') as f4:
                                    json.dump(json_message, f4, ensure_ascii=False, indent=4)
                                    # and send txt back to receiver 
                                data_pack={"aim": 'transport', "mode": "sender_tmp/received.txt", "data": content}
                                target_sid=car_sessions.get(sender_id)
                                if target_sid:
                                    socketio.emit('message', data_pack, room=target_sid)
                                    print("send received.txt back to sender")

                    # tell sender everything is ok and message been forwarded to receiver

                    else:
                        pass
                
    else:
        if aim == 'txt to json':
            ##call sth for txt to json 
            #payload is txt str
            reply=txt_to_json_pipeline(payload)
            mode=mode.split(".")[0]+".json"
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
                create_client_folder(reply) # create folder for receiver
                # save reply to file
                filepath = os.path.join("") ### please change to the correct path
                # save reply as a json file in filepath
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(reply, f, ensure_ascii=False, indent=4)
                socketio.emit('message', data_pack, room=target_sid)
                print(f"[Forwarded] to {target_id}")
            else:
                print(f"[Warning] Target {target_id} not connected.")
        else:
            print("[Error] Message missing 'target_id' or 'reply'.")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)