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
BASE_URL = "https://vortex.gaia.domains"
MODEL = "qwen2.5-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
"What is the primary purpose of Layer 2 solutions in Ethereum?",  
"How do Layer 2 solutions improve Ethereum's scalability?",  
"What are the main types of Layer 2 solutions available for Ethereum?",  
"How does Rollups technology work in Ethereum's Layer 2?",  
"What is the difference between Optimistic Rollups and ZK-Rollups?",  
"How does Plasma contribute to Ethereum's Layer 2 scaling?",  
"What are the security benefits of using Layer 2 solutions?",  
"How does State Channels technology function in Layer 2?",  
"What are the trade-offs between Layer 1 and Layer 2 solutions?",  
"How does Layer 2 reduce transaction fees on Ethereum?",  
"What is the role of Validium in Ethereum's Layer 2 ecosystem?",  
"How does Layer 2 enhance Ethereum's transaction throughput?",  
"What are the challenges of implementing Layer 2 solutions?",  
"How does Layer 2 interact with Ethereum's mainnet?",  
"What is the significance of fraud proofs in Optimistic Rollups?",  
"How does ZK-Rollups ensure data privacy and security?",  
"What are the advantages of using Layer 2 for decentralized applications (dApps)?",  
"How does Layer 2 impact Ethereum's decentralization?",  
"What is the role of sidechains in Ethereum's Layer 2 ecosystem?",  
"How does Layer 2 improve user experience on Ethereum?",  
"What are the key differences between Plasma and Rollups?",  
"How does Layer 2 handle smart contract execution?",  
"What is the role of off-chain computation in Layer 2?",  
"How does Layer 2 ensure data availability?",  
"What are the risks associated with Layer 2 solutions?",  
"How does Layer 2 affect Ethereum's consensus mechanism?",  
"What is the role of bridges in Layer 2 ecosystems?",  
"How does Layer 2 support cross-chain interoperability?",  
"What are the limitations of State Channels in Layer 2?",  
"How does Layer 2 handle dispute resolution in transactions?",  
"What is the role of Layer 2 in reducing Ethereum's carbon footprint?",  
"How does Layer 2 impact the finality of transactions?",  
"What are the key components of a Layer 2 solution?",  
"How does Layer 2 improve Ethereum's network congestion?",  
"What is the role of Layer 2 in enabling microtransactions?",  
"How does Layer 2 handle data storage and retrieval?",  
"What are the differences between Layer 2 and sharding?",  
"How does Layer 2 impact Ethereum's gas fees?",  
"What is the role of Layer 2 in enhancing DeFi applications?",  
"How does Layer 2 ensure compatibility with Ethereum's mainnet?",  
"What are the key players in the Layer 2 ecosystem?",  
"How does Layer 2 handle network upgrades and changes?",  
"What is the role of Layer 2 in NFT marketplaces?",  
"How does Layer 2 improve transaction confirmation times?",  
"What are the challenges of migrating dApps to Layer 2?",  
"How does Layer 2 handle scalability for gaming applications?",  
"What is the role of Layer 2 in improving Ethereum's adoption?",  
"How does Layer 2 impact the security of smart contracts?",  
"What are the differences between Layer 2 and Layer 1 smart contracts?",  
"How does Layer 2 handle cross-rollup transactions?",  
"What is the role of Layer 2 in reducing Ethereum's energy consumption?",  
"How does Layer 2 ensure trustless transactions?",  
"What are the key innovations in Layer 2 technology?",  
"How does Layer 2 handle high-frequency trading on Ethereum?",  
"What is the role of Layer 2 in enabling privacy-preserving transactions?",  
"How does Layer 2 impact the development of decentralized identity solutions?",  
"What are the differences between Layer 2 and off-chain solutions?",  
"How does Layer 2 handle oracle integration for dApps?",  
"What is the role of Layer 2 in improving Ethereum's user onboarding?",  
"How does Layer 2 impact the cost of running Ethereum nodes?",
"What are the challenges of Layer 2 adoption by developers?",  
"How does Layer 2 handle transaction batching and compression?",  
"What is the role of Layer 2 in enabling real-time applications?",  
"How does Layer 2 impact the security of cross-chain bridges?",  
"What are the differences between Layer 2 and multi-chain solutions?",  
"How does Layer 2 handle the scalability of decentralized exchanges (DEXs)?",  
"What is the role of Layer 2 in improving Ethereum's governance?",  
"How does Layer 2 impact the development of decentralized autonomous organizations (DAOs)?",  
"What are the key differences between Layer 2 and Ethereum 2.0?",  
"How does Layer 2 handle the scalability of prediction markets?",  
"What is the role of Layer 2 in enabling decentralized storage solutions?",  
"How does Layer 2 impact the scalability of social media dApps?",  
"What are the challenges of Layer 2 interoperability?",  
"How does Layer 2 handle the scalability of supply chain dApps?",  
"What is the role of Layer 2 in enabling decentralized insurance platforms?",  
"How does Layer 2 impact the scalability of lending and borrowing platforms?",  
"What are the differences between Layer 2 and hybrid scaling solutions?",  
"How does Layer 2 handle the scalability of decentralized identity systems?",  
"What is the role of Layer 2 in enabling decentralized voting systems?",  
"How does Layer 2 impact the scalability of decentralized cloud computing?",  
"What are the challenges of Layer 2 adoption by enterprises?",  
"How does Layer 2 handle the scalability of decentralized prediction platforms?",  
"What is the role of Layer 2 in enabling decentralized content creation platforms?",  
"How does Layer 2 impact the scalability of decentralized gaming economies?",  
"What are the differences between Layer 2 and centralized scaling solutions?",  
"How does Layer 2 handle the scalability of decentralized art platforms?",  
"What is the role of Layer 2 in enabling decentralized music platforms?",  
"How does Layer 2 impact the scalability of decentralized education platforms?",  
"What are the challenges of Layer 2 adoption by mainstream users?",  
"How does Layer 2 handle the scalability of decentralized healthcare platforms?",  
"What is the role of Layer 2 in enabling decentralized energy trading platforms?",  
"How does Layer 2 impact the scalability of decentralized transportation platforms?",  
"What are the differences between Layer 2 and traditional financial systems?",  
"How does Layer 2 handle the scalability of decentralized real estate platforms?",  
"What is the role of Layer 2 in enabling decentralized charity platforms?",  
"How does Layer 2 impact the scalability of decentralized governance platforms?",  
"What are the challenges of Layer 2 adoption by governments?",  
"How does Layer 2 handle the scalability of decentralized legal platforms?",  
"What is the role of Layer 2 in enabling decentralized scientific research platforms?",  
"How does Layer 2 impact the scalability of decentralized environmental platforms?",  
"What are the differences between Layer 2 and Web2 scaling solutions?",  
"How does Layer 2 handle the scalability of decentralized social impact platforms?",  
"What is the role of Layer 2 in enabling decentralized humanitarian platforms?",  
"How does Layer 2 impact the scalability of decentralized cultural platforms?",  
"What are the challenges of Layer 2 adoption by non-profit organizations?",  
"How does Layer 2 handle the scalability of decentralized innovation platforms?",  
"What is the role of Layer 2 in enabling decentralized collaboration platforms?",  
"How does Layer 2 impact the scalability of decentralized knowledge-sharing platforms?"
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
