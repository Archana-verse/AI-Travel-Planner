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
    <div className="bg-muted/40 dark:bg-muted/30 border border-primary/20 rounded-lg p-3 mt-4">
      <div className="flex items-center mb-2">
        <Zap size={16} className="text-primary mr-2" />
        <span className="text-sm font-medium text-foreground">AI-picked highlights:</span>
      </div>

      <div className="flex flex-wrap gap-2 text-sm text-muted-foreground">
        <span className="bg-muted px-2 py-1 rounded-full">{aiReasoning.rating}</span>
        <span className="bg-muted px-2 py-1 rounded-full">{aiReasoning.location}</span>
        <span className="bg-muted px-2 py-1 rounded-full">{aiReasoning.amenities}</span>
        <span className="bg-muted px-2 py-1 rounded-full">{aiReasoning.value}</span>
      </div>
    </div>
  );
};

export default HotelAIRecommendation;
