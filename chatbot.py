from flask import Flask, request, jsonify, render_template_string
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

app = Flask(__name__)

HUGGINGFACEHUB_API_TOKEN = "YOUR_API_TOKEN"
DB_FAISS_PATH = "./vectorstore/db_faiss"

def set_custom_prompt():
    template = """
    You are a Large Language Model (LLM) designed as a Quick MCQ AI ChatBot. Use the following pieces of information to construct meaningful responses to the user's questions. 
    If you encounter a question for which you lack information, respond with 'I don't know the answer' rather than generating a speculative response.
    For Each MCQ question should be concise and spaced appropriately.After Each MCQ Question takes new line for each options and correct Answer.
    Use Maximum complete sentences and keep the answer concise yet thorough.
    Context: {context}
    Question: {question}
    Only return responses that directly address the user's question and provide valuable information. 
    Omit extraneous details or speculative content.
    Helpful answer:"""
    return PromptTemplate(template=template, input_variables=["context", "question"])

def load_model():
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        repo_id=repo_id,
        temperature=0.5
    )
    return llm

def create_retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_type="similarity",search_kwargs={"k": 2}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain

def create_retrieval_qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings,allow_dangerous_deserialization=True)

    llm = load_model()
    qa_prompt = set_custom_prompt()
    qa = create_retrieval_qa_chain(llm=llm, prompt=qa_prompt, db=db)

    return qa

QA_CHAIN = create_retrieval_qa_bot()


@app.route('/')
def home():
    return render_template_string("""
    <!doctype html>
    <html>
    <head>
        <title>QA Bot</title>
        <style>
            body{
                background-color: #17202A;
                color: white;
                font-family: Verdana, Geneva, Tahoma, sans-serif;
            }
            .heading{
                background-color:#283747;
                margin-top: -49px;
                margin-left: -5px;
                margin-right: -5px;
                text-align: center;
                margin-bottom: -129px !important;
            }
            .qa{
                font-size: 50px;
                font-weight: 500;
            }
            .clr{
                background-color:#78281F;
                color:white;
                float: right;
                border: 10px solid #78281F;
                border-radius: 8px;
                margin-top: -102px;
                margin-right: 88px;
                font-size: 15px;
                cursor:pointer
                
            }
            .clr:hover
            {
                background-color: #EC7063;
                border-radius: 8px;
                border:10px solid #EC7063;
                cursor:pointer
            }
            #chatbox {
                height: 455px;
                overflow-y: scroll;
                padding: 10px;
                margin-bottom: 10px;
                margin-left: 75px;
                margin-right: 75px;
                color: white;
                font-size: 15px;
                margin-top:20px;
            }

            #userInput {
                width: 80%;
                padding: 10px;
                box-sizing: border-box;
                margin-left: 75px;
                margin-right: 75px;
                background-color: #344950;
                color:white;
                font-size: 15px;
                margin-top: 30px;
                margin-bottom:15px
            }
            .submit{
                background-color:#78281F;
                color:white;
                float: right;
                border: 12px solid #78281F;
                border-radius: 8px;
                margin-top: -60px;
                margin-right: 210px;
                font-size: 17px;
                cursor:pointer
            }
            .submit:hover
            {
                background-color: #EC7063;
                border-radius: 8px;
                border:12px solid #EC7063;
                cursor:pointer
            }

            .javabot{
                border:1px solid white;
                margin-left: 100px;
                margin-right: 100px;
                margin-bottom:-50px;
                margin-top:35px;
            }
            #topic{
                width: 30%;
                padding: 10px;
                box-sizing: border-box;
                margin-left: 135px;
                margin-right: 75px;
                background-color: #344950;
                color:white;
                font-size: 15px;
                margin-top: 118px;
                margin-bottom:-27px
            }
            #num_mcq{
                width: 30%;
                padding: 10px;
                box-sizing: border-box;
                margin-left: 5px;
                margin-right: 75px;
                background-color: #344950;
                color:white;
                font-size: 15px;
                margin-top: 30px;
                margin-bottom:15px
            
            }
            .chats{
                                  
            }
        </style>
    </head>
    <body>
        <div class="heading"> 
            <p class="qa" >Quick MCQ Bot </p><button class="clr"  onclick="clearHistory()">CLEAR HISTORY</button> 
            </div>
        <div class="chats">
        <input type="text" id="topic" placeholder="Enter the topic..." required/>
        <input type="number" id="num_mcq" placeholder="Enter the number of MCQs..." required/>
        <button class="submit" onclick="sendQuestion(event)">SUBMIT</button>
        </div>
        <div class="javabot">
        <div id="chatbox">
        </div>
        </div>
         <script>
            function sendQuestion(event) {
                event.preventDefault(); // Prevent default form submission behavior
                var topic = document.getElementById('topic').value;
                var num_mcq = document.getElementById('num_mcq').value;
                var chatbox = document.getElementById('chatbox');
                document.getElementById('topic').value = ''; // Clear the input after sending
                document.getElementById('num_mcq').value = ''; // Clear the input after sending
                var question = "prepare a " + num_mcq + " MCQs on " + topic;
                chatbox.innerHTML += "<div style='margin-top: 5px;'>User: " + question + "</div>";

                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({query: question})
                })
                .then(response => response.json())
                .then(data => {
                    var mcqs = data.answer.split(/\d+\./).filter(Boolean);
                    mcqs.forEach(mcq => {
                        mcq = mcq.trim(); // Trim the string to remove leading and trailing whitespace
                        var parts = mcq.split(/a\)|b\)|c\)|d\)|Answer:\s*/).map(part => part.trim()).filter(Boolean); // Split on 'Answer:' followed by any whitespace, trim each part, and filter out empty strings
                        if (parts.length >= 6) {
                            for (var i = 0; i < parts.length - 1; i = i + 6) {                           
                                var formattedMCQ = "<div style='margin-top: 5px;'>" + parts[i].trim() + "<br>";
                                formattedMCQ += "A) " + parts[i + 1].trim() + "<br>";
                                formattedMCQ += "B) " + parts[i + 2].trim() + "<br>";
                                formattedMCQ += "C) " + parts[i + 3].trim() + "<br>";
                                formattedMCQ += "D) " + parts[i + 4].trim() + "<br>";
                                formattedMCQ += "Answer: " + parts[i + 5].trim() + "</div>";

                                // Append the formatted MCQ to the chatbox
                                chatbox.innerHTML += "<div style='margin-top: 5px;'>" + formattedMCQ + "</div>";
                            } 
                        } else {
                            console.error('Invalid MCQ format:', mcq);
                        }
                    });
                    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
                })
                .catch((error) => {
                    console.error('Error:', error);
                    chatbox.innerHTML += "<div style='margin-top: 5px;'>Error: " + error + "</div>";
                });
            }

            function clearHistory() {
            var chatbox = document.getElementById('chatbox');
            chatbox.innerHTML = ''; // clear the chatbox
        }
        </script>

    </body>
    </html>
    
    """)

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    if not query:
        return jsonify({"error": "No query provided"}), 400
    try:
        response = QA_CHAIN({"query": query})
        return jsonify({"answer": response['result'] if 'result' in response else "No answer found"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()


