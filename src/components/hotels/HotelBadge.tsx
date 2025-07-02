
import React from 'react';
import { Star } from 'lucide-react';

interface HotelBadgeProps {
  recommended?: boolean;
  bestValue?: boolean;
}

const HotelBadge = ({ recommended, bestValue }: HotelBadgeProps) => {
  if (!recommended && !bestValue) return null;

  return (
    <div className="bg-gradient-to-r from-primary to-yellow-400 text-white px-4 py-2 text-sm font-medium flex-center">
      <Star size={16} className="mr-1" />
      {recommended ? 'Recommended' : 'Best Value'}
    </div>
  );
};

export default HotelBadge;
