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
MODEL = "Qwen2-0.5B-Instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
"What is decentralized artificial intelligence?",
"How does decentralized AI differ from traditional AI?",
"What are the core principles of decentralized AI?",
"What technologies enable decentralized AI systems?",
"How does blockchain integrate with decentralized AI?",
"What is the role of edge computing in decentralized AI?",
"What are the advantages of decentralized AI over centralized AI?",
"What are the limitations of decentralized AI?",
"How does decentralized AI ensure data privacy?",
"What is federated learning, and how does it relate to decentralized AI?",
"What are the key components of a decentralized AI system?",
"How do smart contracts support decentralized AI?",
"What is the role of distributed ledgers in decentralized AI?",
"How does decentralized AI handle data storage?",
"What are the challenges of scaling decentralized AI systems?",
"How does decentralized AI manage computational resources?",
"What is the role of peer-to-peer networks in decentralized AI?",
"How does decentralized AI handle data synchronization?",
"What are the security risks in decentralized AI systems?",
"How does decentralized AI ensure data integrity?",
"What are some real-world use cases of decentralized AI?",
"How is decentralized AI used in healthcare?",
"Can decentralized AI improve financial systems? How?",
"How does decentralized AI enhance supply chain management?",
"What role does decentralized AI play in IoT (Internet of Things)?",
"How is decentralized AI applied in autonomous vehicles?",
"Can decentralized AI be used for fraud detection? How?",
"How does decentralized AI support personalized marketing?",
"What are the applications of decentralized AI in gaming?",
"How can decentralized AI improve energy management systems?",
"How does decentralized AI protect user data?",
"What are the risks of data breaches in decentralized AI?",
"How does decentralized AI comply with GDPR?",
"Can decentralized AI prevent data misuse? How?",
"What encryption methods are used in decentralized AI?",
"How does decentralized AI handle data anonymization?",
"What are the ethical concerns around data ownership in decentralized AI?",
"How does decentralized AI ensure transparency in data usage?",
"Can decentralized AI prevent bias in data processing?",
"How does decentralized AI address the "black box" problem?",
"Who governs decentralized AI systems?",
"How are decisions made in decentralized AI networks?",
"What ethical frameworks apply to decentralized AI?",
"How does decentralized AI address accountability?",
"Can decentralized AI systems be biased? How?",
"How does decentralized AI handle conflicts of interest?",
"What are the risks of monopolies in decentralized AI?",
"How does decentralized AI ensure fairness in decision-making?",
"What are the ethical implications of AI autonomy in decentralized systems?",
"How does decentralized AI address the digital divide?",
"What are the biggest challenges in developing decentralized AI?",
"How does decentralized AI handle latency issues?",
"What are the energy consumption concerns in decentralized AI?",
"How does decentralized AI deal with network failures?",
"What are the scalability issues in decentralized AI?",
"How does decentralized AI handle interoperability between systems?",
"What are the risks of malicious actors in decentralized AI networks?",
"How does decentralized AI address the lack of centralized control?",
"What are the challenges of training AI models in decentralized systems?",
"How does decentralized AI handle regulatory compliance?",
"What is the future potential of decentralized AI?",
"How will decentralized AI evolve in the next decade?",
"What industries will benefit most from decentralized AI?",
"How will decentralized AI impact job markets?",
"Can decentralized AI lead to fully autonomous societies?",
"What role will decentralized AI play in smart cities?",
"How will decentralized AI influence global economies?",
"What advancements are needed to make decentralized AI mainstream?",
"How will decentralized AI impact human-AI collaboration?",
"What are the long-term risks of decentralized AI?",
"How does decentralized AI differ from centralized AI in terms of control?",
"What are the cost differences between decentralized and centralized AI?",
"How does decentralized AI improve data security compared to centralized AI?",
"What are the performance trade-offs between decentralized and centralized AI?",
"How does decentralized AI handle data ownership differently than centralized AI?",
"What are the environmental impacts of decentralized AI vs. centralized AI?",
"How does decentralized AI address bias compared to centralized AI?",
"What are the scalability differences between decentralized and centralized AI?",
"How does decentralized AI impact innovation compared to centralized AI?",
"What are the user experience differences between decentralized and centralized AI?",
"How do consensus algorithms work in decentralized AI?",
"What is the role of zero-knowledge proofs in decentralized AI?",
"How does decentralized AI handle model updates?",
"What are the challenges of training AI models on decentralized data?",
"How does decentralized AI ensure model accuracy?",
"What is the role of oracles in decentralized AI?",
"How does decentralized AI handle real-time data processing?",
"What are the trade-offs between decentralization and AI performance?",
"How does decentralized AI handle version control of models?",
"What are the challenges of debugging decentralized AI systems?",
"How can developers contribute to decentralized AI projects?",
"What are the best practices for collaborating in decentralized AI networks?",
"How does decentralized AI foster open-source innovation?",
"What are the challenges of community governance in decentralized AI?",
"How does decentralized AI incentivize participation?",
"What are the risks of fragmentation in decentralized AI communities?",
"How does decentralized AI handle intellectual property rights?",
"What are the benefits of decentralized AI for global collaboration?",
"How does decentralized AI address cultural differences in data usage?",
"What are the future opportunities for collaboration in decentralized AI?"
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
