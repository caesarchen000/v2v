import pyttsx3
# 語速 (rate) 與音量 (volume) 可依需求調整。

# 初始化語音引擎
engine = pyttsx3.init()

# 設定為台灣中文語音
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ZH-TW_HANHAN_11.0')

# 語速與音量設定
engine.setProperty('rate', 150)    # 語速，預設約200
engine.setProperty('volume', 0.9)  # 音量，0.0~1.0

# 讀取文字檔案（請確保檔案為 UTF-8 編碼）
input_path = r"C:\Users\User\OneDrive\Desktop\MakeNTU\input\test.txt"
with open(input_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 輸出語音檔案
output_path = r"C:\Users\User\OneDrive\Desktop\MakeNTU\output\test.wav"
engine.save_to_file(text, output_path)
engine.runAndWait()
