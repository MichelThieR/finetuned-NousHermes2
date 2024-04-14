import { useState } from 'react'
import './App.css'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.css'
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react'

function App() {
  const [typing, setTyping] = useState(false);
  const [messages, setMessages] = useState([
    {
      message: "Hello, how can I help today?",
      sender: "NousHermes",
      direction: "incoming"
    }
  ])
  
  const handleSend = async (message) => {
    const newMessage = {
      message: message,
      sender: "user",
      direction: "outgoing"
    }
    const newMessages = [...messages, newMessage]; // all the old messages, + the new message
    // update our messages state
    setMessages(newMessages);

    // set a typing indicator
    setTyping(true);
    // process message to nous hermes (send it over and see the response)
    await processMessageToNousHermes(newMessage);
  }

  async function processMessageToNousHermes(userPrompt) {
    const apiPrompt = {
      prompt: userPrompt.message
    }

    await fetch("http://127.0.0.1:5000", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(apiPrompt)
    }).then((data) => {
      return data.json();
    }).then((data) =>{
      const newMessage = {
        message: data.response,
        sender: "NousHermes",
        direction: "incoming"
      };
      const newMessages = [...messages, userPrompt, newMessage];
      // update our message state
      setMessages(newMessages);
      // set typing to false
      setTyping(false);
    });
  }

  return (
    <div className='my-chat-container'>
      <div style={{position: "relative", height:"400px", width: "750px"}}>
        <MainContainer >
          <ChatContainer >
            <MessageList
              scrollBehavior='smooth'
              typingIndicator={typing ? <TypingIndicator content="NousHermes is typing" />: null}
            >
              {messages.map((message, i) => {
                return <Message key={i} model={message} />
              })}
            </MessageList>
            <MessageInput placeholder='Ask away' onSend={handleSend} attachButton={false} />
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  )
}

export default App
