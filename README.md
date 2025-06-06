# V2V: Voice-to-Vehicle Communication System

This project explores a Voice-to-Vehicle (V2V) communication prototype using Python. The goal is to enable vehicles to semantically interpret and exchange voice commands — supporting scenarios like requesting lane changes, emergency signals, or coordinated driving.

## 📁 Project Versions

Each version is organized into its own Git branch to reflect development progression:


| Version Name           | Description                                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------------- |
| `raw`                  | Raw prototype with basic modules for recording and message transmission                            |
| `ver1`, `ver2`, `ver3` | Structured versions with growing modularity, but still under development and debugging             |
| `final_version`        | Cleaned and fully functional version for demonstration, with all core features working as expected |

> Each version reflects incremental improvements in usability, modularity, and robustness.

## 🧩 Core Features

- 🎙️ Voice input recording and audio-to-text conversion
- 🧠 Semantic intent parsing using LLM
- 📡 Message transmission between vehicles (via socket or simulated)
- 📋 On-screen confirmation and logging of commands
- 🔄 Re-send and error-handling mechanism for reliability

## 📦 Project Structure (typical in `final` branch)

```bash
v2v_final_version/
├── main.py                   # Entry point script
├── jobs.md                   # Job/task documentation
├── README.md                 # Project readme
├── test.py                   # General testing script
├── receiver_tmp/             # Temporary storage for received messages
│   ├── received.json
│   └── received.txt
├── sender_tmp/               # Temporary storage for sent messages
│   ├── check.txt
│   ├── error_message.txt
│   ├── my_check.txt
│   ├── sender.json
│   └── sender.txt
├── src/
│   ├── main_controller.py    # Orchestrates overall logic
│   ├── basic_text/           # Pre-defined message templates
│   │   ├── correct_and_send.txt
│   │   ├── resend_1.txt
│   │   ├── resend_2.txt
│   │   └── send_check.txt
│   ├── func/                 # Voice processing, LLM API, audio
│   │   ├── all_import.py
│   │   ├── api.py
│   │   ├── play_audio.py
│   │   ├── record_audio.py
│   │   ├── record_voice.py
│   │   ├── test.txt
│   │   ├── txt_to_wav.py
│   │   ├── use_llm.py
│   │   └── wav_to_txt.py
│   ├── others/               # Tests, additional utilities
│   │   ├── test_llm.py
│   │   └── use_llm_test.txt
│   └── server_client/        # TCP communication modules
│       ├── bluetooth_module.py
│       ├── client.py
│       ├── communication_history.json
│       ├── new_client.py
│       ├── new_server.py
│       ├── screen.py
│       ├── server.py
│       ├── test_clientimport.py
│       └── test_screenimport.py
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/caesarchen000/v2v.git
cd v2v/v2v_final_version/
```

### 2. Run the System

You can run any of the following main scripts depending on your desired setup:

```bash
python main.py
# or
python main2.py
# or
python main_ok_with_holding.py
```

1. 🔧 Notes

* 🖥️ The system requires a **microphone** and **speaker** for real-time voice interaction.
* 📡 Ensure **port availability** if you're testing client-server communication locally (via `server.py` / `client.py`).
* 🔑 For LLM features (e.g., OpenAI integration), you may need to add your **API key** in `use_llm.py`.

## 🧠 Future Plans

* 🚗 Integration with **vehicle simulators** or real car hardware
* 🧠 Enhanced **NLP error detection** and robustness
* 📱 Development of a **web or mobile UI**
* 📊 Collection of voice-command data for **fine-tuning intent recognition**
