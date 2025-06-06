# input: str(input path, wav file)
# output: str(output path, txt file)

#def wav_to_txt(input_path: str) -> str:

  import os
  import whisper
  
  # ====== 重要資訊 ======
  # Whisper 本地端模型無明確檔案大小限制，但單一音檔建議不要超過1小時或500MB，
  # 避免記憶體爆炸或處理過慢。實務上，音檔長度 5~30 分鐘、檔案大小 <200MB 效果最佳。
  # 若音檔過大，建議先用 ffmpeg 或 pydub 分段處理。
  # =====================
  
  os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
  # 設定檔案路徑
  input_path = r"C:\Users\User\OneDrive\Desktop\MakeNTU\input\test.wav" # change path
  output_path = r"C:\Users\User\OneDrive\Desktop\MakeNTU\output\test.txt" # change path
  
  # 建議：檢查檔案大小（建議單檔不超過200MB）
  max_size_mb = 200
  file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
  if file_size_mb > max_size_mb:
      raise ValueError(f"音檔過大（{file_size_mb:.1f} MB），建議先分段處理。")
  
  # 載入 Whisper 模型
  model = whisper.load_model("base")  # 可選 tiny, base, small, medium, large
  
  # 語音辨識，指定語言為中文，並用 initial_prompt 強化中文語境
  result = model.transcribe(
      input_path,
      language="zh",
      initial_prompt="以下是普通話的句子。"
  )
  
  # 儲存辨識結果為文字檔
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(result["text"])

  print(f"轉錄完成，結果已存入 {output_path}")
