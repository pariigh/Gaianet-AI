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
"What is the primary function of the data link layer in the OSI model?",  
"How does the data link layer ensure reliable communication between devices?",  
"What are the two sublayers of the data link layer?",  
"What is the purpose of the Logical Link Control (LLC) sublayer?",  
"What is the role of the Media Access Control (MAC) sublayer?",  
"What is a MAC address and how is it used in networking?",  
"How does the data link layer handle frame synchronization?",  
"What is the difference between a switch and a hub at the data link layer?",  
"What is the purpose of error detection in the data link layer?",  
"What are common error detection methods used in the data link layer?",  
"What is the significance of the Frame Check Sequence (FCS) in a data frame?",  
"How does the data link layer handle flow control?",  
"What is the purpose of the acknowledgment (ACK) in data link layer communication?",  
"What is the difference between a unicast, multicast, and broadcast frame?",  
"How does the data link layer handle collisions in a network?",  
"What is the role of the Address Resolution Protocol (ARP) in the data link layer?",  
"What is the purpose of the Spanning Tree Protocol (STP) in the data link layer?",  
"How does the data link layer handle frame forwarding in a switched network?",  
"What is the difference between half-duplex and full-duplex communication at the data link layer?",  
"What is the purpose of the preamble in an Ethernet frame?",  
"How does the data link layer handle frame fragmentation and reassembly?",  
"What is the role of the Point-to-Point Protocol (PPP) in the data link layer?",  
"How does the data link layer handle VLAN tagging?",  
"What is the purpose of the Maximum Transmission Unit (MTU) in the data link layer?",  
"How does the data link layer handle Quality of Service (QoS) for frames?",  
"What is the role of the Ethernet protocol in the data link layer?",  
"How does the data link layer handle frame prioritization?",  
"What is the purpose of the MAC control frame in Ethernet networks?",  
"How does the data link layer handle frame buffering?",  
"What is the role of the Link Aggregation Control Protocol (LACP) in the data link layer?",  
"How does the data link layer handle frame filtering?",  
"What is the purpose of the MAC address table in a switch?",  
"How does the data link layer handle frame flooding?",  
"What is the role of the IEEE 802.1Q standard in VLANs?",  
"How does the data link layer handle frame encapsulation?",  
"What is the purpose of the MAC learning process in switches?",  
"How does the data link layer handle frame aging in switches?",  
"What is the role of the Ethernet Type field in a frame?",  
"How does the data link layer handle frame retransmission?",  
"What is the purpose of the MAC address aging timer in switches?",  
"How does the data link layer handle frame duplication?",  
"What is the role of the Ethernet frame delimiter?",  
"How does the data link layer handle frame padding?",  
"What is the purpose of the MAC address filtering feature in switches?",  
"How does the data link layer handle frame prioritization using IEEE 802.1p?",  
"What is the role of the Ethernet frame check sequence (FCS)?",  
"How does the data link layer handle frame forwarding based on MAC addresses?",  
"What is the purpose of the MAC address learning limit in switches?",  
"How does the data link layer handle frame forwarding in a VLAN environment?",  
"What is the role of the MAC address in frame addressing?",  
"How does the data link layer handle frame forwarding in a broadcast domain?",  
"What is the purpose of the MAC address table aging process?",  
"How does the data link layer handle frame forwarding in a multicast environment?",  
"What is the role of the MAC address in frame filtering?",
"How does the data link layer handle frame forwarding in a collision domain?",  
"What is the purpose of the MAC address in frame switching?",  
"How does the data link layer handle frame forwarding in a full-duplex environment?",  
"What is the role of the MAC address in frame routing?",  
"How does the data link layer handle frame forwarding in a half-duplex environment?",  
"What is the purpose of the MAC address in frame bridging?",  
"How does the data link layer handle frame forwarding in a point-to-point link?",  
"What is the role of the MAC address in frame switching in a LAN?",  
"How does the data link layer handle frame forwarding in a WAN environment?",  
"What is the purpose of the MAC address in frame switching in a WLAN?",  
"How does the data link layer handle frame forwarding in a MAN environment?",  
"What is the role of the MAC address in frame switching in a PAN?"
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
