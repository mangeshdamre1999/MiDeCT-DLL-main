import os
import sys
import subprocess

# Function to install required packages
def install_packages():
    required_packages = ["faiss-cpu", "sentence-transformers", "pyTelegramBotAPI", "numpy", "requests"]
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))  # Check if package is installed
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install dependencies before importing modules
install_packages()

import requests
import json
import telebot
import faiss
from sentence_transformers import SentenceTransformer, util

# Set your API Keys (Replace with your actual keys)
GOOGLE_FACT_CHECK_API_KEY = "AIzaSyAYlncuOAOVn0Cuw0CMWqVVHI7_vc7MAzc"
TELEGRAM_BOT_TOKEN = "7241148778:AAFMMeq-CiCgRzep2kc-dJKuBeLBztABHXE"

# Initialize Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Load SentenceTransformer model for DPR
model = SentenceTransformer('facebook-dpr-ctx_encoder-single-nq-base')

# Sample knowledge base (replace with your actual data)
knowledge_base = [
    {"text": "The Earth is round.", "source": "Scientific consensus"},
    {"text": "COVID-19 vaccines are safe and effective.", "source": "CDC"},
    {"text": "The sun is a star.", "source": "Basic astronomy"},
    # Add more facts to your knowledge base
]

# Create FAISS index
knowledge_base_embeddings = model.encode([fact['text'] for fact in knowledge_base])
index = faiss.IndexFlatL2(knowledge_base_embeddings.shape[1])
index.add(knowledge_base_embeddings)

def google_fact_check(claim):
    """Fetch fact-checking reports from Google Fact Check API"""
    url = f'https://factchecktools.googleapis.com/v1alpha1/claims:search?query={claim}&key={GOOGLE_FACT_CHECK_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "claims" in data:
            return data["claims"]
    return []

def search_knowledge_base(claim, top_k=3):
    """Search knowledge base using FAISS and DPR."""
    claim_embedding = model.encode(claim)
    D, I = index.search(claim_embedding.reshape(1, -1), top_k)

    # Only return results if the match is strong (filter out weak matches)
    results = []
    for i in range(len(I[0])):
        if D[0][i] < 50:  # Adjust threshold for better filtering
            results.append(knowledge_base[I[0][i]])

    return results

def fact_check_pipeline(claim):
    """Complete Fact-Checking Pipeline."""
    result_text = f"\n🔍 Checking claim: {claim}\n"

    # Step 1: Google Fact Check API
    fact_check_results = google_fact_check(claim)
    if fact_check_results:
        result_text += "✅ Found Verified Fact Check:\n"
        for i, result in enumerate(fact_check_results, 1):
            textual_rating = result.get("textualRating", "No rating available")
            claim_review = result.get("claimReview", [])
            review_url = claim_review[0]["url"] if claim_review else "No URL available"
            result_text += f"{i}. {textual_rating} - {review_url}\n"
        return result_text  # ✅ Return immediately if verified fact check exists

    # Step 2: Search Knowledge Base (FAISS & DPR)
    knowledge_base_results = search_knowledge_base(claim)

    # Only show knowledge base results if there's a strong match
    if knowledge_base_results:
        result_text += "🔎 Found relevant facts in knowledge base:\n"
        for i, result in enumerate(knowledge_base_results, 1):
            result_text += f"{i}. {result['text']} (Source: {result['source']})\n"
        return result_text  # ✅ Return only if there's a match

    # If neither Google Fact Check nor Knowledge Base has relevant data, show this:
    return "⚠ No verified fact checks or relevant knowledge base results found."

@bot.message_handler(commands=['fact_check'])
def handle_fact_check(message):
    """Handles the /fact_check command"""
    claim = message.text.replace('/fact_check ', '')
    result = fact_check_pipeline(claim)
    bot.reply_to(message, result)

@bot.message_handler(commands=['knowledge_base'])
def handle_knowledge_base_command(message):
    """Handles the /knowledge_base command"""
    claim = message.text.replace('/knowledge_base ', '')
    knowledge_base_results = search_knowledge_base(claim)
    if knowledge_base_results:
        response = "🔎 Found relevant facts in knowledge base:\n"
        for i, result in enumerate(knowledge_base_results, 1):
            response += f"{i}. {result['text']} (Source: {result['source']})\n"
    else:
        response = "⚠ No relevant facts found in knowledge base."
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handles all text messages"""
    claim = message.text
    result = fact_check_pipeline(claim)
    bot.reply_to(message, result)

if __name__ == "__main__":
    print("🤖 Telegram Bot is running...")
    bot.polling()
