
import React from 'react';
import { Zap } from 'lucide-react';

interface AIRecommendationProps {
  aiReasoning?: {
    price: string;
    duration: string;
    airline: string;
    departure: string;
  };
}

const AIRecommendation = ({ aiReasoning }: AIRecommendationProps) => {
  if (!aiReasoning) return null;

  return (
    <div className="bg-white/70 dark:bg-card/70 backdrop-blur-sm rounded-xl p-4 mb-4 border border-primary/20">
      <div className="flex-center mb-3">
        <Zap className="text-primary" size={16} />
        <h4 className="font-medium text-foreground ml-2">Why AI recommends this:</h4>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-foreground">
        <div><strong>Price:</strong> {aiReasoning.price}</div>
        <div><strong>Duration:</strong> {aiReasoning.duration}</div>
        <div><strong>Airline:</strong> {aiReasoning.airline}</div>
        <div><strong>Departure:</strong> {aiReasoning.departure}</div>
      </div>
    </div>
  );
};

export default AIRecommendation;
