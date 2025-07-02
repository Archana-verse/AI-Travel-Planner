
import React from 'react';
import { Link } from 'react-router-dom';
import { Plane, MapPin, MessageCircle, Calendar, Sparkles, ArrowRight } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Plane,
      title: 'Smart Flight Search',
      description: 'Find the best flights with AI-powered recommendations and real-time pricing'
    },
    {
      icon: MapPin,
      title: 'Intelligent Itineraries',
      description: 'Personalized day-by-day travel plans crafted just for your preferences'
    },
    {
      icon: MessageCircle,
      title: 'AI Travel Assistant',
      description: 'Chat with our AI for instant travel advice and 24/7 support'
    },
    {
      icon: Calendar,
      title: 'Seamless Planning',
      description: 'Complete trip planning from flights to activities in one simple form'
    }
  ];

  return (
    <div className="min-h-screen bg-pattern gradient-warm">
      {/* Hero Section */}
      <div className="text-center py-24 px-6">
        <div className="max-w-4xl mx-auto animate-fade-in">
          <div className="flex-center justify-center mb-6">
            <h1 className="text-hero">
              Namaste Yatri! 
            </h1>
            <span className="text-4xl ml-2">🙏</span>
          </div>
          <p className="text-xl text-muted-foreground mb-4 font-medium tracking-wide">
            यात्रायाः आरम्भः अत्र।
          </p>
          <p className="text-body mb-12 max-w-2xl mx-auto text-lg">
            Begin your yatra with purpose — your journey, our intelligent guidance.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <Link
              to="/plan"
              className="btn-primary flex-center text-lg group"
            >
              <Plane size={20} />
              <span>Start Planning Now</span>
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              to="/chat"
              className="btn-secondary flex-center text-lg"
            >
              <MessageCircle size={20} />
              <span>Chat with AI</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-heading mb-4">Why Choose Raahi?</h2>
            <p className="text-body max-w-2xl mx-auto">
              Experience the future of travel planning with our AI-powered platform designed for the modern Indian traveler.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="card-elevated p-8 text-center hover-lift"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="w-16 h-16 gradient-saffron rounded-2xl flex items-center justify-center mb-6 mx-auto shadow-lg">
                    <Icon className="text-white" size={28} />
                  </div>
                  <h3 className="text-subheading mb-4">{feature.title}</h3>
                  <p className="text-body leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="mx-6 mb-20">
        <div className="gradient-saffron py-20 px-8 rounded-3xl text-center text-white max-w-5xl mx-auto shadow-2xl">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-heading mb-6">Ready to explore incredible India?</h2>
            <p className="text-xl mb-8 opacity-90 leading-relaxed">
              Begin your yatra with purpose — your journey, our intelligent guidance.
            </p>
            <Link
              to="/plan"
              className="inline-flex items-center bg-white text-primary px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-gray-50 transition-all duration-200 transform hover:scale-105 shadow-xl hover:shadow-2xl gap-3"
            >
              <Sparkles size={20} />
              <span>Get Started Free</span>
              <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
