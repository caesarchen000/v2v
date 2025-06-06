import sys
import time
import threading
import json
import os
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.func.record_audio import *
from src.func.record_voice import *
from src.func.txt_to_wav import *
from src.func.use_llm import *
from src.func.wav_to_txt import *
from src.func.all_import import *
from src.func.play_audio import *

from src.server_client.bluetooth_module import *
###connection###
from src.server_client.new_client import *
from src.server_client.new_server import *
###display###
from src.server_client.screen import *
from PySide6.QtWidgets import QApplication
# from src import *


receive_or_not = False

state = "await"
received_queue = []  # 儲存多個收到的 json 訊息
flush_stdin = False  # 控制是否忽略 stdin 輸入

# === 跨平台輸入處理 ===
if platform.system() == "Windows":
    import msvcrt
else:
    import select
    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(sys.stdin.fileno())

def is_tab_pressed():
    if platform.system() == "Windows":
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            return key == '\t'
        return False
    else:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            key = sys.stdin.read(1)
            return key == '\t'
        return False

def restore_stdin():
    if platform.system() != "Windows":
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def state_monitor():
    global state, flush_stdin, receive_or_not
    while True:
        if not flush_stdin and is_tab_pressed():
            state = "sender"
            flush_stdin = True

        elif receive_or_not:
            state = "receiver"


        if state == "sender":
            print("[狀態] sender → 執行 sender_start()")
            sender_start()
            state = "await"
            flush_stdin = False

        elif state == "receiver":
            print(f"[狀態] receiver → 處理 ")
            receiver_start()
            state = "await"
            receive_or_not = False


        time.sleep(0.1)

def check_message_correctness(json_path: str) -> bool:
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    correctness = json_data.get("correctness", "none")
    if correctness == "1":
        return True
    else:
        return False
    
def sender_pipeline():
    sender_pipeline_part1() # create txt file

    ###    display txt on main screen      ###
    with open('sender_tmp/sender.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
        # send to server
        send_txt_to_server_and_store_json(CAR_ID, message=content,mode='sender_tmp/sender.txt') # send the message to the server

    sender_check=check_message_correctness(json_path='sender_tmp/sender.json')
    while sender_check!=True:
        sender_resend_pipeline()
        sender_check=check_message_correctness(json_path='sender_tmp/sender.json')

    # the message format should be correct now
    tell_server_correctness(CAR_ID, mode="sender_tmp/sender.json", message="json_correct", content="json_correct")

    txt_to_wav(input_path='sender_tmp/sender_notyet_confirm.txt', output_path='sender_tmp/let_sender_confirm.wav')

    sender_pipeline_part2()
    with open('sender_tmp/sender_final_confirm.txt', 'r', encoding='utf-8') as f:
        filecontent = f.read()
        # send to server the final confirm
        tell_server_correctness(CAR_ID,mode="sender_tmp/sender_final_confirm.txt" , message="final_confirm",content=filecontent)

    ## receive 輸入正確 or 不正確

def sender_pipeline_part1():
    # detect user's voice
    record_audio(filename='sender_tmp/sender.wav', fs=44100, channels=2, max_seconds=300)  # record audio

    # convert voice to text
    wav_to_txt(input_path='sender_tmp/sender.wav', output_path='sender_tmp/sender.txt')

def sender_resend_pipeline():
    # tell sender not clear
    txt_to_wav(input_path='src/basic_text/resend_1.txt', output_path='sender_tmp/resend_1.wav')
    
    ###  play audio and display resend_1.txt###
    play_audio('sender_tmp/resend_1.wav')
    with open('sender_tmp/resend_1.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
    sender_pipeline_part1() # create txt file

    with open('sender_tmp/sender.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
        # send to server
        send_txt_to_server_and_store_json(CAR_ID,content,mode='sender_tmp/sender.txt') # send the message to the server


def sender_pipeline_part2():
    # play the audio
    with open('src/basic_text/send_check.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
        play_audio('sender_tmp/sender_notyet_confirm.wav')
    # play the audio
    play_audio('sender_tmp/let_sender_confirm.wav')

    # wait for sender to confirm
    record_audio(filename='sender_tmp/sender_final_confirm.wav', fs=44100, channels=2, max_seconds=300)  # record audio

    # convert voice to text
    wav_to_txt(input_path='sender_tmp/sender_final_confirm.wav', output_path='sender_tmp/sender_final_confirm.txt')



###receive handle###
def handle_incoming(data_pack):
    global receive_or_not
    receive_or_not = True

    aim = data_pack['aim']
    data = data_pack['data']
    mode = data_pack['mode']
    print(f"[Main got message] {data}")

    if aim == 'tell send' :
        if data =="1":
            window.mainScreen_display("輸入正確 --> 傳送")
            txt_to_wav(input_path='src/basic_text/correct_and_send.txt', output_path='sender_tmp/correct_and_send.wav')
            play_audio('sender_tmp/correct_and_send.wav')
    else:
        if aim == 'txt to json' or 'json to txt' or 'tell correctness':
            filepath=mode 
        elif aim == 'transport':
            filepath=mode #!!!may occur error but not used now!!!
            
        # 指定儲存的目錄和檔案名稱

        filepath = os.path.join(filepath)
        
        if aim == 'txt to json':
            # 將 json_data 寫入檔案
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        elif aim == 'json to txt' or 'tell correctness':
            # 將 json_data 寫入檔案
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data)
        ### there should call a function to do sth
        elif aim == 'transport' and mode == 'receiver_tmp/received.txt':
            # 將 received.txt 寫入檔案
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data)
        elif aim == 'transport' and mode == 'sender_tmp/received.txt':
            # 將 received.txt 寫入檔案
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data)
                txt_to_wav(input_path='sender_tmp/received.txt', output_path='sender_tmp/received.wav')
                # play the audio
                window.mainScreen_display(f"收到來自{data_pack['from_car_id']}的訊息")
                play_audio('sender_tmp/received.wav')


def receiver_pipeline():
    # convert text to voice
    txt_to_wav(input_path='receiver_tmp/received.txt', output_path='receiver_tmp/received.wav')
    # play the audio
    play_audio('receiver_tmp/received.wav')
    # wait for receiver to confirm
    receiver_pipeline_part1() # output a receiver.txt file

    ###    display txt on main screen      ###
    with open('receiver_tmp/receiver.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
        # send to server
        send_txt_to_server_and_store_json(CAR_ID, message=content, mode='receiver_tmp/receiver.txt') # send the message to the server

    receiver_check = check_message_correctness(json_path='receiver_tmp/receiver.json')
    while receiver_check != True:
        receiver_resend_pipeline()
        receiver_check = check_message_correctness(json_path='receiver_tmp/receiver.json')
    # the message format should be correct now
    tell_server_correctness(CAR_ID, mode="receiver_tmp/receiver.json", message="json_correct", content="json_correct")

    txt_to_wav(input_path='receiver_tmp/receiver_notyet_confirm.txt', output_path='receiver_tmp/let_receiver_confirm.wav')

    receiver_pipeline_part2()
    with open('receiver_tmp/receiver_final_confirm.txt', 'r', encoding='utf-8') as f:
        filecontent = f.read()
        # send to server the final confirm
        tell_server_correctness(CAR_ID, mode="receiver_tmp/receiver_final_confirm.txt", message="final_confirm", content=filecontent)
    
    # receive 輸入正確 or 不正確

def receiver_resend_pipeline():
    # tell receiver not clear
    txt_to_wav(input_path='src/basic_text/resend_1.txt', output_path='receiver_tmp/resend_1.wav')
    
    ###  play audio and display resend_1.txt###
    play_audio('receiver_tmp/resend_1.wav')
    with open('receiver_tmp/resend_1.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
    receiver_pipeline_part1() # create txt file

    with open('receiver_tmp/receiver.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
        # send to server
        send_txt_to_server_and_store_json(CAR_ID, content, mode='receiver_tmp/receiver.txt') # send the message to the server



def receiver_pipeline_part1():
    # detect user's voice
    record_audio(filename='receiver_tmp/receiver.wav', fs=44100, channels=2, max_seconds=300)  # record audio

    # convert voice to text
    wav_to_txt(input_path='receiver_tmp/receiver.wav', output_path='receiver_tmp/receiver.txt')

def receiver_pipeline_part2():
    # play the audio
    with open('src/basic_text/send_check.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        window.mainScreen_display(content)
        play_audio('receiver_tmp/receiver_notyet_confirm.wav')
    # play the audio
    play_audio('receiver_tmp/let_receiver_confirm.wav')

    # wait for receiver to confirm
    record_audio(filename='receiver_tmp/receiver_final_confirm.wav', fs=44100, channels=2, max_seconds=300)  # record audio

    # convert voice to text
    wav_to_txt(input_path='receiver_tmp/receiver_final_confirm.wav', output_path='receiver_tmp/receiver_final_confirm.txt')

def sender_start():
    sender_pipeline()

    sio.wait()

def receiver_start():
    # record from which car ID
    receiver_check=receiver_pipeline()
    while receiver_check!=True:
        receiver_check=receiver_pipeline()
    with open('receiver_tmp/received.json', 'r', encoding='utf-8') as f:
        received_json_data = json.load(f)
        from_car_ID=received_json_data.get("來自的車牌號碼", "none")
        with open('receiver_tmp/receiver.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            send_to(from_car_ID, json_data) # send the message to the sender
    sio.wait()

if __name__== "__main__":
    ##set CarID
    carID = input('your car ID: ')
    set_car_id(carID)
    ##設定receiver function註冊
    set_on_message_callback(handle_incoming)
    ##接上server
    connect_with_retry()

    ###   display   ###
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    threading.Thread(target=state_monitor, daemon=True).start()
    threading.Thread(target=sio.wait, daemon=True).start()

    # # try:
    # sio.wait() # --> let window cant pop out
    # #關螢幕等於關機
    sys.exit(app.exec())