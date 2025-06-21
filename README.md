# 💅 TwiNailz.AI

> An AI-powered Telegram bot for nail art enthusiasts and professionals

---

## 🌟 Features

- 🧠 **AI Brain**: Intelligent nail art recommendations and advice
- 📊 **Trend Analysis**: Real-time nail art trend tracking and insights
- 🎨 **Enhanced Features**: Advanced nail art suggestions and tutorials
- 👥 **Multiple Personalities**: Different AI personas for varied interaction styles
- 💾 **Database Integration**: Persistent storage for user preferences and history
- 🔧 **Telegram Integration**: Seamless bot experience with rich messaging features

---

## 🚀 Technologies

- **Python 3.x** - Core development language
- **Telegram Bot API** - Bot platform integration
- **Async/Await** - High-performance asynchronous operations
- **AI/ML Libraries** - Intelligent recommendation engine
- **Database** - User data and preferences storage

---

## 🛠 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/TwiNailz-AI.git
   cd TwiNailz-AI
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

Create a `.env` file in the project root with the following content (replace values as needed):

```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=twinailz_data.db
NAIL_TRENDS_API=simple_trends
GOOGLE_TRENDS_ENABLED=false
DEBUG_MODE=true
CACHE_ENABLED=true
MAX_USERS=1000
RATE_LIMIT=30
```

**Required:**
- `TELEGRAM_BOT_TOKEN` — Your Telegram bot token from BotFather
- `OPENAI_API_KEY` — Your OpenAI API key

**Optional:**
- `DATABASE_URL` — Path to your SQLite database file (default: `twinailz_data.db`)
- `NAIL_TRENDS_API` — Nail trends API to use (default: `simple_trends`)
- `GOOGLE_TRENDS_ENABLED` — Enable Google Trends integration (`true`/`false`)
- `DEBUG_MODE` — Enable debug logging (`true`/`false`)
- `CACHE_ENABLED` — Enable caching (`true`/`false`)
- `MAX_USERS` — Maximum number of users (default: `1000`)
- `RATE_LIMIT` — Rate limit per user (default: `30`)

---

## ▶️ Running the Bot

Start the bot with:

```bash
python src/main_bot.py
```

---

## 💡 Usage

- Interact with your bot on Telegram after starting it.
- Try commands like `/start`, `/help`, or explore the AI-powered features.
- [Add more usage instructions or command list here if needed]

---

## 📊 Project Status

🔧 Currently under development and code optimization.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[Specify your license here, e.g., MIT]

---

## 📝 Notes

- Make sure your `.env` file is **never committed** to version control!
- For production, set `DEBUG_MODE=false`.
