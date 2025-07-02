
import React from 'react';
import { Star } from 'lucide-react';

interface FlightBadgeProps {
  isPopular?: boolean;
  isCheapest?: boolean;
}

const FlightBadge = ({ isPopular, isCheapest }: FlightBadgeProps) => {
  if (!isPopular && !isCheapest) return null;

  return (
    <div className="bg-gradient-to-r from-primary to-yellow-400 text-white px-4 py-2 text-sm font-medium flex-center">
      <Star size={16} className="mr-1" />
      {isPopular ? 'Most Popular' : 'Best Value'}
    </div>
  );
};

export default FlightBadge;
