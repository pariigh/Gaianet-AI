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
"What is blockchain technology?",  
"How does blockchain ensure decentralization?",  
"What are the key features of a decentralized system?",  
"What is the difference between centralized and decentralized networks?",  
"How does blockchain achieve consensus without a central authority?",  
"What are the main types of blockchain consensus mechanisms?",  
"What is Proof of Work (PoW) and how does it work?",  
"What is Proof of Stake (PoS) and how does it differ from PoW?",  
"What are smart contracts and how do they function on a blockchain?",  
"What is a distributed ledger and how is it used in blockchain?",  
"What are the advantages of decentralization in blockchain?",  
"What are the challenges of implementing decentralized systems?",  
"How does blockchain ensure data immutability?",  
"What is a blockchain node and what role does it play?",  
"What is the role of miners in a blockchain network?",  
"What is a 51% attack and how does it threaten decentralization?",  
"What is the difference between public, private, and consortium blockchains?",  
"How does blockchain technology enhance transparency?",  
"What is the role of cryptography in blockchain security?",  
"What are the limitations of blockchain technology?",  
"How does blockchain handle scalability issues?",  
"What is the difference between on-chain and off-chain transactions?",  
"What is a fork in blockchain and how does it occur?",  
"What is a hard fork and how does it differ from a soft fork?",  
"What is a decentralized application (dApp)?",  
"How do decentralized exchanges (DEXs) work?",  
"What is the role of tokens in a blockchain ecosystem?",  
"What is the difference between a coin and a token?",  
"What is the significance of private and public keys in blockchain?",  
"How does blockchain ensure privacy and anonymity?",  
"What is zero-knowledge proof and how is it used in blockchain?",  
"What is the role of oracles in blockchain systems?",  
"What is the difference between permissioned and permissionless blockchains?",  
"What is the role of governance in decentralized networks?",  
"How does blockchain technology impact traditional financial systems?",  
"What is decentralized finance (DeFi) and how does it work?",  
"What are the risks associated with DeFi platforms?",  
"What is a stablecoin and how does it maintain its value?",  
"What is the role of blockchain in supply chain management?",  
"How does blockchain improve data security?",  
"What is the difference between blockchain and traditional databases?",  
"What is the role of hashing in blockchain technology?",  
"What is a Merkle tree and how is it used in blockchain?",  
"What is the significance of the genesis block in a blockchain?",  
"How does blockchain technology support digital identity?",  
"What is the role of blockchain in voting systems?",  
"How does blockchain impact the healthcare industry?",  
"What is the role of blockchain in the Internet of Things (IoT)?",  
"What is a blockchain wallet and how does it work?",  
"What is the difference between hot wallets and cold wallets?",  
"What is the role of blockchain in intellectual property protection?",  
"How does blockchain technology support cross-border payments?",  
"What is the role of blockchain in reducing fraud?",  
"How does blockchain impact the real estate industry?",  
"What is the role of blockchain in energy trading?",  
"How does blockchain support peer-to-peer transactions?",  
"What is the role of blockchain in digital advertising?",  
"How does blockchain impact the gaming industry?",  
"What is the role of blockchain in content creation and distribution?",  
"What is the difference between blockchain and distributed ledger technology (DLT)?",  
"How does blockchain technology support charity and donations?",
"What is the role of blockchain in education and credential verification?",  
"How does blockchain impact the insurance industry?",  
"What is the role of blockchain in combating counterfeit goods?",  
"How does blockchain support data integrity?",  
"What is the role of blockchain in the music industry?",  
"How does blockchain impact the art and collectibles market?",  
"What is the role of blockchain in identity verification?",  
"How does blockchain support decentralized storage solutions?",  
"What is the role of blockchain in the legal industry?",  
"How does blockchain impact the logistics and transportation industry?",  
"What is the role of blockchain in digital voting systems?",  
"How does blockchain support transparency in charitable organizations?",  
"What is the role of blockchain in the pharmaceutical industry?",  
"How does blockchain impact the food supply chain?",  
"What is the role of blockchain in carbon credit trading?",  
"How does blockchain support renewable energy initiatives?",  
"What is the role of blockchain in the automotive industry?",  
"How does blockchain impact the aviation industry?",  
"What is the role of blockchain in the entertainment industry?",  
"How does blockchain support crowdfunding platforms?",  
"What is the role of blockchain in the telecommunications industry?",  
"How does blockchain impact the retail industry?",  
"What is the role of blockchain in the tourism industry?",  
"How does blockchain support anti-money laundering (AML) efforts?",  
"What is the role of blockchain in the fashion industry?",  
"How does blockchain impact the agriculture industry?",  
"What is the role of blockchain in the sports industry?",  
"How does blockchain support disaster relief efforts?",  
"What is the role of blockchain in the publishing industry?",  
"How does blockchain impact the nonprofit sector?",  
"What is the role of blockchain in the cybersecurity industry?",  
"How does blockchain support digital rights management?",  
"What is the role of blockchain in the e-commerce industry?",  
"How does blockchain impact the media and journalism industry?",  
"What is the role of blockchain in the gambling industry?",  
"How does blockchain support decentralized autonomous organizations (DAOs)?",  
"What is the role of blockchain in the pet industry?",  
"How does blockchain impact the luxury goods market?",  
"What is the role of blockchain in the toy industry?",  
"How does blockchain support the sharing economy?",  
"What is the role of blockchain in the event management industry?",  
"How does blockchain impact the subscription-based business model?",  
"What is the role of blockchain in the digital transformation of industries?"
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
