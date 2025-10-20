from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from src.helper import download_embeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import Pinecone
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from src.prompt import *
from dotenv import load_dotenv
import os
load_dotenv()

embeddings = download_embeddings()
docsearch = Pinecone.from_existing_index(index_name=os.getenv("PINECONE_INDEX_NAME"), embedding=embeddings)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":5})

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Rephrasing the question from the history
# Example: 1st Q: What is allergies? 2nd Q: How can I treat it? Rephrasing: How can I treat alleargies?
rephrase_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the last question. Just return the query, nothing else.")
])
# If there is no chat_history, then the input is just passed directly to the retriever. 
# If there is chat_history, then the prompt and LLM will be used to generate a search query. 
# That search query is then passed to the retriever.
history_aware_retriever = create_history_aware_retriever(llm, retriever, rephrase_prompt)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    Context: {context}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

# Create chains
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


app = Flask(__name__,
            # vibe dist folder
            static_folder='chatbot-reactjs/dist', 
            static_url_path='')

# This allows your React app (on a different port) to make requests to Flask.
CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index.html')
    # v1: From templates folder
    # return render_template('index.html')


@app.route("/get", methods=['GET', 'POST'])
def chat():
    # request.get_json() parses the incoming JSON payload from your React app.
    data = request.get_json()

    # Hold chat history
    chat_history_list = data.get('contents', [])

    # Get last question
    current_question = chat_history_list[-1]['parts'][0]['text'] 
    
    # Convert the history (all BUT the last message) into a list of Message objects
    chat_history_messages = []
    for message in chat_history_list[:-1]:
        if message['role'] == 'user':
            chat_history_messages.append(HumanMessage(content=message['parts'][0]['text']))
        else:
            chat_history_messages.append(AIMessage(content=message['parts'][0]['text']))

    print(f"Current Question: {current_question}")
    print(f"History: {chat_history_messages}")

    # Invoke chain
    response = rag_chain.invoke({
            "input": current_question,
            "chat_history": chat_history_messages
        })
    answer = response["answer"]
    print(f"Response: {response['answer']}")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
