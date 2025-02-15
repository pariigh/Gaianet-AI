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
"What is a cryptocurrency?",
"How does blockchain work?",
"What is the difference between a coin and a token?",
"How does cryptocurrency mining work?",
"What is a digital wallet, and how does it work?",
"What is the difference between a hot wallet and a cold wallet?",
"What is the difference between a hard fork and a soft fork?",
"What does decentralization mean in cryptocurrencies?",
"What is a smart contract, and how does it work?",
"What is the difference between Bitcoin and Ethereum?",
"What is hash rate, and why is it important?",
"What is a 51% attack, and how does it work?",
"How does the Proof of Work (PoW) consensus algorithm work?",
"How does the Proof of Stake (PoS) consensus algorithm work?",
"What is the difference between PoW and PoS?",
"What is scalability in cryptocurrencies?",
"What is Layer 2 in blockchain?",
"What is the difference between a public and private blockchain?",
"What is a double-spending attack, and how is it prevented?",
"What is a private key, and why is it important?",
"What is a cryptocurrency exchange?",
"What is the difference between a centralized and decentralized exchange?",
"What is market capitalization in crypto?",
"What is a stablecoin, and how does it maintain its value?",
"What is a bull market and a bear market in crypto?"
"What is HODL in cryptocurrency slang?",
"What is a crypto wallet address?",
"What is a limit order and a market order in crypto trading?",
"What is liquidity in cryptocurrency markets?",
"What is a crypto index fund?",
"What is Ethereum, and how is it different from Bitcoin?",
"What is Ripple (XRP), and what is its use case?",
"What is Cardano, and how does it work?",
"What is Polkadot, and what problem does it solve?",
"What is Chainlink, and how does it work?",
"What is Solana, and why is it popular?",
"What is Binance Coin (BNB), and what is its purpose?",
"What is Dogecoin, and why did it gain popularity?",
"What is Shiba Inu, and how is it related to Dogecoin?",
"What is Avalanche, and how does it work?",
"What is Know Your Customer (KYC) in crypto exchanges?",
"What is Anti-Money Laundering (AML) in cryptocurrency?",
"How do governments regulate cryptocurrencies?",
"What is a crypto tax, and how does it work?",
"What is the difference between a security token and a utility token?",
"What is the SEC's role in regulating cryptocurrencies?",
"What are the risks of investing in unregulated crypto projects?",
"What is a crypto license, and why is it important?",
"How do countries like China and the US differ in crypto regulations?",
"What is the future of cryptocurrency regulations worldwide?",
"What is a decentralized autonomous organization (DAO)?",
"What is the role of nodes in a blockchain network?",
"What is sharding, and how does it improve scalability?",
"What is a sidechain, and how does it work?",
"What is cross-chain interoperability, and why is it important?",
"What is a zero-knowledge proof, and how does it enhance privacy?",
"What is the Lightning Network, and how does it solve Bitcoin’s scalability issues?",
"What is a decentralized application (dApp)?",
"What is gas in Ethereum, and how is it calculated?",
"What is a crypto market cycle, and how does it work?",
"What is a whale in the crypto market?",
"What is a pump-and-dump scheme in crypto?",
"What is the fear and greed index in cryptocurrency?",
"What is the role of institutional investors in crypto markets?",
"What is a crypto ETF, and why is it significant?",
"What is the impact of macroeconomic factors on cryptocurrency prices?",
"What is the role of social media in crypto price movements?",
"What is a crypto bubble, and how can it be identified?",
"What is the role of influencers in the crypto space?",
"What is a privacy coin, and how does it work?",
"What is Monero, and how does it ensure privacy?",
"What is Zcash, and how does it use zk-SNARKs?",
"What is the difference between privacy and anonymity in crypto?",
"What is a mixing service, and how does it work?",
"What is the role of Tor in cryptocurrency transactions?",
"What is a stealth address, and how does it enhance privacy?",
"What is the difference between transparent and shielded transactions in Zcash?",
"What is the impact of privacy coins on regulatory compliance?",
"What is CoinJoin, and how does it improve Bitcoin privacy?",
"What is a non-fungible token (NFT)?",
"How do NFTs differ from cryptocurrencies?",
"What is the role of NFTs in the art world?",
"What is the metaverse, and how does it relate to crypto?",
"What is the difference between fungible and non-fungible tokens?",
"What is the role of blockchain in the metaverse?",
"What is Play-to-Earn (P2E) in crypto gaming?",
"What is Decentraland, and how does it work?",
"What is the environmental impact of NFTs?",
"What is the future of NFTs in the gaming industry?",
"What is a rug pull in crypto, and how can it be avoided?",
"What is the environmental impact of Bitcoin mining?",
"What is the risk of losing access to a crypto wallet?",
"What is the role of hackers in the crypto space?",
"What is the risk of investing in meme coins?",
"What is the impact of quantum computing on cryptocurrencies?",
"What is the risk of regulatory bans on cryptocurrencies?",
"What is the role of scams in the crypto industry?",
"What is the risk of centralization in blockchain networks?",
"What is the future of crypto adoption amid global challenges?"
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
