
import React from 'react';
import { MessageCircle, Search, Shield, Zap, Globe, Heart } from 'lucide-react';

const FeatureHighlights = () => {
  const features = [
    {
      icon: MessageCircle,
      title: 'AI Chat Assistant',
      description: 'Get instant travel advice, booking help, and destination insights from our intelligent travel companion.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Search,
      title: 'Live Flight & Hotel Search',
      description: 'Access real-time pricing from 500+ airlines and 2M+ properties with smart filtering and price alerts.',
      color: 'from-primary to-orange-400'
    },
    {
      icon: Shield,
      title: 'Secure & Trusted Booking',
      description: 'Bank-level security with instant confirmations and 24/7 customer support for all your reservations.',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: Zap,
      title: 'Lightning-Fast Planning',
      description: 'Complete itineraries generated in under 30 seconds, optimized for your time, budget, and preferences.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: Globe,
      title: 'India-First Experience',
      description: 'Designed for Indian travelers with local insights, festival calendars, and regional cuisine recommendations.',
      color: 'from-amber-500 to-red-500'
    },
    {
      icon: Heart,
      title: 'Personalized Recommendations',
      description: 'Machine learning adapts to your travel style, dietary needs, and cultural preferences for better suggestions.',
      color: 'from-rose-500 to-pink-500'
    }
  ];

  return (
    <div className="py-20 px-6 bg-gradient-to-b from-accent/20 to-background">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-heading mb-4">Powerful Features for Modern Travelers</h2>
          <p className="text-body max-w-3xl mx-auto">
            Every feature is crafted to make your travel planning effortless, intelligent, and uniquely yours.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="group card-elevated p-8 hover-lift"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className={`w-14 h-14 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center mb-6 shadow-lg group-hover:scale-110 transition-transform duration-200`}>
                  <Icon className="text-white" size={24} />
                </div>
                <h3 className="text-lg font-semibold mb-3 text-foreground">{feature.title}</h3>
                <p className="text-body leading-relaxed">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default FeatureHighlights;
