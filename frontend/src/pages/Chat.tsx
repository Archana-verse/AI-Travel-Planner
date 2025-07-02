
import React, { useState } from 'react';
import { MessageCircle, Send, Bot, User, Sparkles } from 'lucide-react';

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Namaste! I\'m your AI travel assistant. How can I help you plan your perfect journey today?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user' as const,
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);

    // Simulate AI response
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        type: 'bot' as const,
        content: 'I understand you need travel assistance. Let me help you with that! Based on your requirements, I can suggest some amazing destinations and create a personalized itinerary for you.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);

    setInputMessage('');
  };

  const quickQuestions = [
    'What are the best places to visit in India during winter?',
    'How much should I budget for a 5-day trip to Kerala?',
    'What documents do I need for domestic travel?',
    'Can you suggest a romantic getaway for couples?'
  ];

  return (
    <div className="min-h-screen bg-pattern gradient-warm py-12 px-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex-center justify-center mb-4">
            <div className="gradient-saffron p-3 rounded-2xl shadow-lg">
              <MessageCircle className="text-white" size={32} />
            </div>
            <h1 className="text-heading ml-4">AI Travel Assistant</h1>
          </div>
          <p className="text-body text-lg">Ask me anything about your travel plans!</p>
        </div>

        {/* Chat Container */}
        <div className="card-elevated overflow-hidden mb-8">
          {/* Messages */}
          <div className="h-96 overflow-y-auto p-6 space-y-6 bg-gradient-to-b from-card to-accent/10">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-scale-in`}
              >
                <div className={`flex items-start space-x-3 max-w-xs lg:max-w-md ${
                  message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                }`}>
                  <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shadow-md ${
                    message.type === 'bot'
                      ? 'gradient-saffron text-white'
                      : 'bg-muted text-muted-foreground'
                  }`}>
                    {message.type === 'bot' ? <Bot size={18} /> : <User size={18} />}
                  </div>
                  <div className={`p-4 rounded-2xl shadow-sm ${
                    message.type === 'bot'
                      ? 'bg-card border border-border text-foreground'
                      : 'gradient-saffron text-white'
                  }`}>
                    <p className="text-sm leading-relaxed">{message.content}</p>
                    <p className={`text-xs mt-2 ${
                      message.type === 'bot' ? 'text-muted-foreground' : 'text-white/70'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Input Form */}
          <div className="border-t border-border p-6 bg-card">
            <form onSubmit={handleSendMessage} className="flex space-x-4">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask me about destinations, planning, or anything travel-related..."
                className="flex-1 px-4 py-3 border border-input rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all bg-background text-foreground placeholder:text-muted-foreground"
              />
              <button
                type="submit"
                className="btn-primary flex-center"
              >
                <Send size={18} />
                <span>Send</span>
              </button>
            </form>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="animate-fade-in">
          <div className="flex-center mb-6">
            <Sparkles className="text-primary mr-2" size={20} />
            <h3 className="text-subheading">Quick Questions</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => setInputMessage(question)}
                className="card-interactive p-4 text-left hover-lift"
              >
                <p className="text-body">{question}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
