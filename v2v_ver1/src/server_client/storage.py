import os
import json

def create_server_folder():
    """創建 server 主資料夾（如果不存在）"""
    try:
        os.makedirs("server", exist_ok=True)
        print(f'[System] Server 主資料夾已準備: {os.path.abspath("server")}') # change path(not yet)
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
