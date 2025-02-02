📌 Telegram Fact-Checking Bot

🔹 Overview

This is a Telegram bot that performs fact-checking using:

Google Fact Check API

FAISS and Sentence Transformers (DPR Model) for knowledge base search.

The bot helps verify claims by fetching fact-checking reports and searching a pre-defined knowledge base.

🔹 Features

✅ Fetches verified fact-checking reports from Google Fact Check API.
✅ Searches a knowledge base using FAISS & DPR model.
✅ Handles Telegram bot commands for easy access.

🔹 Installation & Setup

1️⃣ Install Dependencies

Run the following command to install required Python packages:

pip install faiss-cpu sentence-transformers pyTelegramBotAPI requests

2️⃣ Set Up API Keys

Replace the placeholders in GOOGLE_FACT_CHECK_API_KEY and TELEGRAM_BOT_TOKEN with your actual API keys:

GOOGLE_FACT_CHECK_API_KEY = "your_google_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

3️⃣ Run the Bot

Execute the script to start the Telegram bot:

python bot.py

🔹 How to Use

✅ Commands:

/fact_check <claim> → Checks a claim against verified sources.

/knowledge_base <claim> → Searches the internal knowledge base for relevant facts.

✅ Example Usage:

Send the command:

/fact_check The Earth is flat

The bot will reply with fact-checking results or related knowledge base facts.

🔹 Deployment (Optional)

To deploy the bot on a server (e.g., AWS, Google Cloud, or Heroku), make sure:

Your Python script runs continuously (bot.polling() keeps the bot active).

Use screen or nohup to keep it running after logout:

nohup python bot.py &

🔹 Dependencies

Python 3.7+

FAISS (faiss-cpu)

Sentence Transformers (sentence-transformers)

PyTelegramBotAPI (pyTelegramBotAPI)

Requests (requests)

🔹 Notes

The knowledge base is currently hardcoded; you can expand it dynamically.

Ensure your API keys are valid before running the bot.

🚀 Now your bot is ready to fact-check claims on Telegram!
