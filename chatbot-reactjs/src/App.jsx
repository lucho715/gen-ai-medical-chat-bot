import { useRef, useState, useEffect } from 'react';
import ChatbotIcon from "./components/ChatbotIcon"
import ChatForm from "./components/ChatForm"
import ChatMessage from "./components/ChatMessage"

const App = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [showChatbot, setShowChatbot] = useState(true);

  const chatBodyRef = useRef();

  // Replace Thinking... with response
  const updateHistory = (text, isError = false) => {
    setChatHistory(prev => [...prev.filter(msg => msg.text != "..."), {role: "model", text, isError}]);
  }

  const generateBotResponse = async (history) => {
    console.log(history)
    // Format chat with API request
    
    history = history.map(({role, text}) => ({role, parts: [{text}]}))
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        //"x-goog-api-key": import.meta.env.VITE_GOOGLE_API_KEY // Only for testing, do not pass this.
      },
      body: JSON.stringify({contents: history})
    };
    

    try {
      const response = await fetch(import.meta.env.VITE_API_URL, requestOptions);
      const data = await response.json();
      if(!response.ok) throw new Error(data.error.message || "Something is wrong");
      //console.log(data);
      //const apiResponseText = data.candidates[0].content.parts[0].text.replace(/\*\*(.*?)\*\*/g, "$1").trim(); // This is google gemini response
      const apiResponseText = data.answer
      updateHistory(apiResponseText);
    } catch (error) {
      //console.log(error);
      updateHistory(error.message, true);
    }
      
  };
  
  useEffect(() => {
    chatBodyRef.current.scrollTo({top: chatBodyRef.current.scrollHeight, behavior: "smooth"});
  }, [chatHistory]);

  return (
    <div className={`container ${showChatbot ? "show-chatbot" : ""}`}>
      <button onClick={() => setShowChatbot(prev => !prev)} id="chatbot-toggler">
        <span className="material-symbols-rounded">mode_comment</span>
        <span className="material-symbols-rounded">close</span>
      </button>

      <div className="chatbot-popup">
        
        {/* Chatbot Header */}
        <div className="chat-header">
          <div className="header-info">
            <ChatbotIcon />
            <h2 className="logo-text">Dr. Chatbot</h2>
          </div>
          <button onClick={() => setShowChatbot((prev) => !prev)}
          className="material-symbols-rounded">keyboard_arrow_down</button>
        </div>

        {/* Chatbot Body */}
        <div ref={chatBodyRef} className="chat-body">
          <div className="message bot-message">
            <ChatbotIcon />
            <p className="message-text">
              Hi there! How may I help you?
            </p>
          </div>
          {chatHistory.map((chat, index) => (
            <ChatMessage key={index} chat={chat}/>
          ))}
        </div>

        {/* Chatbot Body */}
        <div className="chat-footer">
          <ChatForm chatHistory={chatHistory} setChatHistory={setChatHistory} generateBotResponse={generateBotResponse} />
        </div>
      </div>
    </div>
  )
}

export default App