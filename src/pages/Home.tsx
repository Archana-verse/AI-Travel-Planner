
import React from 'react';
import { Link } from 'react-router-dom';
import { Plane, MessageCircle, Calendar, Sparkles, ArrowRight } from 'lucide-react';
import HowRaahiWorks from '../components/home/HowRaahiWorks';
import ItineraryPreview from '../components/home/ItineraryPreview';
import FeatureHighlights from '../components/home/FeatureHighlights';

const Home = () => {
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

      {/* How Raahi Works Section */}
      <HowRaahiWorks />

      {/* Itinerary Preview Section */}
      <ItineraryPreview />

      {/* Feature Highlights Section */}
      <FeatureHighlights />

      {/* CTA Section */}
      <div className="mx-6 mb-20">
        <div className="gradient-saffron py-20 px-8 rounded-3xl text-center text-white max-w-5xl mx-auto shadow-2xl">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-heading mb-6">Ready to explore incredible India? 🇮🇳</h2>
            <p className="text-xl mb-8 opacity-90 leading-relaxed">
              Join thousands of smart travelers who trust Raahi for their perfect journeys. Your next adventure is just one click away.
            </p>
            <Link
              to="/plan"
              className="inline-flex items-center bg-white text-primary px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-gray-50 transition-all duration-200 transform hover:scale-105 shadow-xl hover:shadow-2xl gap-3"
            >
              <Sparkles size={20} />
              <span>Start Your Journey</span>
              <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
