
import React from 'react';
import { Sparkles } from 'lucide-react';
import PlanForm from '../components/plan/PlanForm';

const Plan = () => {
  return (
    <div className="min-h-screen bg-pattern gradient-warm py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-hero mb-4">
            Plan Your Perfect Journey
          </h1>
          <p className="text-body mb-4 max-w-2xl mx-auto">
            Begin your yatra with purpose — your journey, our intelligent guidance.
          </p>
          <p className="flex-center justify-center text-primary font-medium">
            <span>Tell us about your dream trip and let our AI create magic</span>
            <Sparkles size={20} />
          </p>
        </div>

        <PlanForm />
      </div>
    </div>
  );
};

export default Plan;


