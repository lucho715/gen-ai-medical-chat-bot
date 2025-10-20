# Introduction
This project shows the creation of a AI chatbot with the following characteristics:
1. It reads PDFs to gather information for the AI. This can be extended to look for other file formats (think of company sharepoint)
2. It converts the texts in the document into chunks.
3. The chunks are embedded with a model. This project uses all-MiniLM-L6-v2 for the semantic search and sentence similarity.
4. The embeddings are stored in a vector database. This project stores onto Pinecone cloud vector database, but others can be used, such as Chroma, QDrant, etc, or locally with FAISS
5. Prompts are created to direct the model.
6. Prompts and embeddings are passed to an AI model for further processing. This project uses OpenAI ChatGTP, but other can be used, such as Google Gemini, Meta Llama, or locally with GGUF (ex: Llama-3.2-3B-Instruct-Q2_K.gguf for low resources)
7. AI models returns a response.
8. Flask is used to create backend rest APIs.
9. A chatbot is created with nodejs, vite, and react.
10. The chabot receives the user message and invokes Flash rest APIs.

# Notes
1. Using langchain 0.3.27 as 1.0.0+ breaks langchain.chains packages

# Run Project Requirements
1. conda (optional but recommended). Example: ```wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh```
2. pyhon 3.10
3. nodejs (https://nodejs.org/en/download) 

# Run Project
1. git clone https://github.com/lucho715/gen-ai-medical-chat-bot
2. Go to folder: gen-ai-medical-chat-bot
3. Create conda environment with python 3.10 ```conda create -n gen-ai-medical-chat-bot```
4. Activate conda environment ```conda activate gen-ai-medical-chat-bot```
5. Download required packages ```pip install -r requirements.txt```
6. Supply your API_KEYs. This projects use PINECONE_API_KEY and OPENAI_API_KEY.
7. Change directory to ```chatbot-reactjs``` and edit .env to add your get route rest api configured in flask (example: running locally is http://localhost:8081/get)
8. In directory ```chatbot-reactjs``` run: ```npm install``` and then: ```npm run build```
8. Run: ```python app.py```
9. Browser: ```http://localhost:8081``` 

# Run on a domain using a reverse proxy (Optional)
1. Edit vite.config.js to use a base url path, example: ```base: '/gen-ai-medical-chat-bot/',```
2. This project use Caddy. Edit ```/etc/caddy/Caddyfile``` add reverse proxy ```handle_path /gen-ai-medical-chat-bot/* { reverse_proxy 127.0.0.1:8081 }```
3. In browser, navigate to: ```https://yourdomain.com/gen-ai-medical-chat-bot/``` (last forward slash is import or add redirection in caddy file)