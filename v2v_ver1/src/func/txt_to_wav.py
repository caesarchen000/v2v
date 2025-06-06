from gtts import gTTS
from pydub import AudioSegment
import os

def txt_to_wav(input_path, output_path):
    # Read the input text file (ensure it's UTF-8 encoded)
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    if not text:
        raise ValueError("Input text file is empty.")
    # Generate speech using gTTS
    tts = gTTS(text, lang='zh')
    temp_mp3 = output_path + ".tmp.mp3"
    tts.save(temp_mp3)
    # Convert mp3 to wav using pydub
    sound = AudioSegment.from_mp3(temp_mp3)
    sound.export(output_path, format="wav")
    os.remove(temp_mp3)
    print(f"Saved WAV file: {output_path}")

# ================== 使用範例 ==================
if __name__ == "__main__":
    # 基本用法 (自動檢測編碼)
    txt_to_wav(
        input_path="/home/mason/Desktop/Make_NTU/v2v/src/func/test.txt",
        output_path="/home/mason/Desktop/Make_NTU/v2v/src/func/test.wav",
        # encoding="big5"
    )

#         FileNotFoundError: 輸入檔案不存在時拋出
#         ValueError: 無法自動檢測編碼時拋出
#     """
'''
pip install pydub
pip install gtts
'''
