
import React from 'react';
import { Search, Brain, Plane } from 'lucide-react';

const HowRaahiWorks = () => {
  const steps = [
    {
      icon: Search,
      title: 'Tell Us Your Dream',
      description: 'Share your destination, dates, budget, and travel preferences with our smart form.'
    },
    {
      icon: Brain,
      title: 'AI Creates Your Plan',
      description: 'Our intelligent system crafts a personalized itinerary with flights, stays, and activities.'
    },
    {
      icon: Plane,
      title: 'Book & Travel Smart',
      description: 'Review, customize, and book everything seamlessly through our integrated platform.'
    }
  ];

  return (
    <div className="py-20 px-6 bg-gradient-to-b from-background to-accent/20">
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-heading mb-4">How Raahi Works</h2>
        <p className="text-body mb-16 max-w-2xl mx-auto">
          From dream to departure in three simple steps — let AI handle the complexity while you focus on the excitement.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={index} className="relative animate-fade-in" style={{ animationDelay: `${index * 0.2}s` }}>
                <div className="flex flex-col items-center">
                  <div className="w-20 h-20 gradient-saffron rounded-full flex items-center justify-center mb-6 shadow-xl">
                    <Icon className="text-white" size={32} />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold text-sm">
                    {index + 1}
                  </div>
                  <h3 className="text-subheading mb-4">{step.title}</h3>
                  <p className="text-body leading-relaxed max-w-sm">{step.description}</p>
                </div>
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-10 -right-6 w-12 h-0.5 bg-gradient-to-r from-primary to-transparent"></div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default HowRaahiWorks;
