from flask import Flask, render_template, jsonify, request
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

app = Flask(__name__)

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


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=['GET', 'POST'])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print(response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
