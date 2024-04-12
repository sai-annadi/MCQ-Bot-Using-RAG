# MCQ-CHATBOT-USING-RAG

![image](https://github.com/sai-annadi/MCQ-CHATBOT-USING-RAG/assets/111168434/b18cd335-cae7-4256-b020-39486febbcbb)

![image](https://github.com/sai-annadi/MCQ-CHATBOT-USING-RAG/assets/111168434/f5f232a3-163e-4035-895e-9585ebbda938)


### Description:
The QuickMCQ Bot is a Flask-based application designed to facilitate the generation of multiple-choice questions (MCQs) on various topics. Leveraging a Retrieval-Augmented Generation (RAG) approach powered by the Mistral 7B v0.2 model from Hugging Face, the bot can intelligently construct questions based on user-provided topics and the desired number of MCQs. To ensure efficient access to relevant information, the bot utilizes FAISS to store vector representations of PDF files related to Java, Python, and Machine Learning, enabling quick retrieval and generation of MCQs.

The core functionality of the bot involves processing user queries, generating MCQs based on the provided topic, and retrieving answers from the stored PDFs using the FAISS vector store. Users can interact with the bot through a user-friendly web interface, entering their desired topic and the number of MCQs they require. The bot then utilizes the Hugging Face model and FAISS vector store to generate and present the MCQs to the user. This project showcases the integration of advanced natural language processing techniques with efficient data storage mechanisms to create a useful tool for generating MCQs.

![image](https://github.com/sai-annadi/MCQ-CHATBOT-USING-RAG/assets/111168434/50fa8e10-6386-4398-8bc0-7b120db5c300)

### Key Components:

1.Flask Application: The web application framework for hosting the QuickMCQ Bot, providing a user interface for interacting with the bot.

2.FAISS Vector Store: Used to store vector representations of PDF files related to Java, Python, and Machine Learning for efficient information retrieval.

3.Mistral 7B v0.2 Model: A large language model from Hugging Face, utilized for the RAG approach to generate MCQs based on user queries and stored information.

4.Retrieval QA Chain: A component that uses the Mistral model to retrieve relevant information and generate MCQs based on user inputs, including the topic and number of MCQs required.

### Features:

1.User-Friendly Interface: Allows users to easily input a topic and the number of MCQs they need.

2.Dynamic Question Generation: Utilizes the RAG approach to generate MCQs based on user queries and stored information.

3.Efficient Information Retrieval: Uses FAISS to store and retrieve vector representations of PDF files, ensuring quick and accurate retrieval of relevant information.

4.Versatile Topic Coverage: Supports a wide range of topics related to Java, Python, and Machine Learning, providing flexibility for different user needs.

### Prerequisites:
Python 3.7 or later
pip (package installer for Python)

### Installation:

1.Clone the repository:

```bash
git clone [https://github.com/your_username/MCQ-Chatbot-Using-RAG.git]
```
2.Navigate to the project directory:
```bash
cd MCQ-Chatbot-Using-RAG
```
### Usage:
1.set up a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```
2.Install the required dependencies:
```bash
pip install -r requirements.txt
```
3.Initialize the Chroma vector database by running data.py:
```bash
python dataingest.py
```
4.Start the Flask application (main bot) by running main.py:
```bash
python chatbot.py
```
5.Access the chatbot interface by opening a web browser and navigating to http://localhost:5000/. You can now interact with the chatbot by entering questions in the input field and receiving answers based on the retrieval-based approach.
