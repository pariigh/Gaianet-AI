import requests
import random
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://pengu.gaia.domains"
MODEL = "qwen2-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
   "What's the current market sentiment for Solana?",
            "Analyze Bitcoin's price movement in the last hour",
            "Compare ETH and BTC performance today",
            "Which altcoins are showing bullish patterns?",
            "Market analysis for top 10 cryptocurrencies",
            "Technical analysis for Polkadot",
            "Price movement patterns for Avalanche",
            "Polygon's market performance analysis",
            "Latest developments affecting BNB price",
            "Cardano's market outlook",
            "What's your favorite way to engage with art?",
    "What's something you wish you could tell your future self?",
    "What's your favorite way to spend time with family?",
    "If you could have any view from your window, what would it be?",
    "What's the best thing about your personality?",
    "What's one tradition you'd like to start?",
    "What's your favorite way to travel?",
    "What's the most interesting souvenir you've brought back from a trip?",
    "If you could give one piece of advice to the world, what would it be?",
    "What's your favorite way to celebrate personal achievements?",
    "What's the most interesting thing you've learned from a stranger?",
    "What's your favorite thing to do when you're feeling creative?",
    "If you could have any historical item, what would it be?",
    "What's your favorite way to connect with nature?",
    "What's the biggest risk you've ever taken?",
    "What's your favorite kind of surprise?",
    "What would you do if you had unlimited resources for a day?",
    "What's your favorite place to read or write?",
    "What's the most unique skill you possess?",
    "What's your favorite way to give a compliment?",
    "If you could write a book, what would it be about?",
    "What's your favorite thing about your best friend?",
    "What would you do if you could fly?",
    "What's your favorite way to learn something new?",
    "What's the most beautiful thing you've ever made?",
    "What's your favorite way to celebrate a cultural event?",
    "If you could become an expert in any field overnight, what would it be?",
    "What's your favorite kind of day out?",
    "What's the most exciting thing about the future to you?",
    "What's your favorite way to remember someone special?",
    "If you could have any mythical creature as a friend, which would you choose?"
  
]

def chat_with_ai(api_key: str, question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    print("Title: GaiaAI Chatbot")
    print("Twitter: https://x.com/0xMoei")
    api_key = input("Enter your API key: ")
    run_bot(api_key)

if __name__ == "__main__":
    main()
