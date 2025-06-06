import makeNTU.v2v.src.server_client.new_client as new_client
import json
import os
new_client.set_car_id(input('your car ID: '))

def handle_incoming(data):
    print(f"[Main got message] {data}")
    # 指定儲存的目錄和檔案名稱
    directory = "receiver_tmp"
    filename = "received.json"
    filepath = os.path.join(directory, filename)
    os.makedirs(directory)
    
    # 將 json_data 寫入檔案
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    ### there should call a function to do sth
##設定receiver function註冊
new_client.set_on_message_callback(handle_incoming)
##接上server
new_client.connect_with_retry()

new_client.sio.wait()