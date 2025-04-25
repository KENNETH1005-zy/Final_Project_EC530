# Final_Project_EC530

**Document Analyzer for Teachers**  
A Python/Redis/SQLite application that uses an LLM to automatically generate teaching materials (summaries, key points, quizzes), provide feedback, and assign grades to arbitrary text documents.

---

## 🔧 Features

- **LLM-powered analysis** via OpenAI’s GPT models  
- **Redis pub/sub** for decoupled, asynchronous messaging  
- **SQLite storage** with JSON-serialization of complex fields  
- **CLI entry point** for easy integration and automation  
- **Subscriber** script to receive & display results in real time  
- **Monitor** script to inspect active channels & subscriber counts  
- **Robust error handling** with logging to `error_log.txt`  
- **Schema-conflict resolution** (overwrite, rename, abort)

---

## 🛠️ Requirements

- Python 3.8+  
- Redis server (local or Docker)  
- An OpenAI API key  
- `pip` for installing dependencies  

---

## 🚀 Getting Started

1. **Clone the repo**  
   ```bash
   git clone https://github.com/KENNETH1005-zy/Final_Project_EC530.git
   cd Final_Project_EC530
2. **Create & activate a virtual environment**
   python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate.bat      # Windows
3. **Install dependencies**
   pip install -r requirements.txt
4. **Configure your API key**
   Copy your key into a file named .env at the project root:
   OPENAI_API_KEY=sk-…
5. **Start Redis**
   •	macOS (Homebrew):
   brew install redis
brew services start redis
	•	Linux:
sudo apt update && sudo apt install redis-server
sudo systemctl enable --now redis
	•	Windows: see https://redis.io
6. **Prepare a sample document**
   echo "This is a test document for analysis." > sample_doc.txt


