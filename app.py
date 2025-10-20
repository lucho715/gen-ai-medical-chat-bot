from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from src.helper import download_embeddings
from pinecone import Pinecone as pc
from langchain_openai import OpenAI
from langchain_pinecone import Pinecone
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import *
from dotenv import load_dotenv
import os

embeddings = download_embeddings()

load_dotenv()
pc = pc(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("lucho715")

docsearch = Pinecone.from_existing_index(index_name="lucho715", embedding=embeddings)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI(model="gpt-4o-mini", temperature=0.3)
prompt = ChatPromptTemplate.from_template(prompt_template)
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

app = Flask(__name__,
            # 1. Define the folder for static files (CSS, JS, images)
            static_folder='chatbot-reactjs/dist', 
            # 2. Define the URL path for static files
            static_url_path='')

# This allows your React app (on a different port) to make requests to Flask.
# Temp for dev
CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index.html')
    #return render_template('index.html') #not using template folder, instead look for flask folder


@app.route("/get", methods=['GET', 'POST'])
def chat():
    # request.get_json() parses the incoming JSON payload from your React app.
    # It is coming with a history for context awareness, but for this examples it is only processing the last user question
    data = request.get_json()
    print(f"Data received: {data}")
    user_message = data['contents'][-1]['parts'][0]['text']
    print(f"Received message: {user_message}")

    # From HTML
    #msg = request.form["msg"]
    #input = msg
    #print(input)

    response = rag_chain.invoke({"input": user_message})
    answer = response["answer"]
    print(f"Response: {response['answer']}")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
