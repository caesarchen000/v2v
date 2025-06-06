from text_to_speech_module import speak_text

# 支援的語音指令對應內部動作
COMMAND_MAP = {
    "剎車": "brake",
    "停旁邊": "stop",
    "超車": "overtake"
}

def handle_command(text: str) -> str:
    """解析語音文字並執行對應動作"""
    for keyword, action in COMMAND_MAP.items():
        if keyword in text:
            speak_text(f"已收到指令：{keyword}，即將執行 {action}")
            return action
    speak_text("無法辨識指令，請再說一次")
    return "unknown"

# 範例：
# handle_command("我要剎車")