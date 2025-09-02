import React from 'react';
import { Zap } from 'lucide-react';

interface AIReasoning {
  rating: string;
  location: string;
  amenities: string;
  value: string;
}

interface HotelAIRecommendationProps {
  aiReasoning?: AIReasoning;
}

const HotelAIRecommendation = ({ aiReasoning }: HotelAIRecommendationProps) => {
  if (!aiReasoning) return null;

  return (
    <div className="bg-white/70 dark:bg-card/70 backdrop-blur-sm rounded-xl p-4 mb-4 border border-primary/20">
      <div className="flex items-center mb-3">
        <Zap className="text-primary" size={16} />
        <h4 className="font-medium text-foreground ml-2">Why AI recommends this:</h4>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-foreground">
        <div><strong>Rating:</strong> {aiReasoning.rating}</div>
        <div><strong>Location:</strong> {aiReasoning.location}</div>
        <div><strong>Amenities:</strong> {aiReasoning.amenities}</div>
        <div><strong>Value:</strong> {aiReasoning.value}</div>
      </div>
    </div>
  );
};

export default HotelAIRecommendation;
