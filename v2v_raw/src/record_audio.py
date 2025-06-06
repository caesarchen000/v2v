import sounddevice as sd
import soundfile as sf
import numpy as np

'''
# 基本用法（完全等同原程式行為）
record_audio()

# 高階用法（自定義參數）
record_audio(
    filename='meeting_record.wav',
    fs=48000,
    channels=1,
    max_seconds=600
)
'''

def record_audio(
    filename='output.wav',
    fs=44100,
    channels=2,
    max_seconds=300
):
    """錄音主函數，按兩次Enter鍵控制錄音起停"""
    frames = []

    def callback(indata, frames_count, time_info, status):
        """音頻輸入回調函數"""
        frames.append(indata.copy())

    def record_until_enter():
        """錄音控制核心邏輯"""
        nonlocal frames
        frames = []
        with sd.InputStream(
            samplerate=fs,
            channels=channels,
            callback=callback
        ):
            input("錄音中...再按一次 Enter 結束錄音：")
        
        audio = np.concatenate(frames, axis=0)
        sf.write(filename, audio, fs)
        print(f"錄音結束，已儲存為 {filename}")

    input("按 Enter 開始錄音：")
    record_until_enter()

