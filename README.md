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

# Run Project
1. Run: ```python app.py```
2. Browser: ```http://localhost:8081``` 