import React from 'react';
import { Star, BadgePercent } from 'lucide-react';

interface HotelBadgeProps {
  recommended?: boolean;
  bestValue?: boolean;
}

const HotelBadge = ({ recommended, bestValue }: HotelBadgeProps) => {
  if (!recommended && !bestValue) return null;

  return (
    <div className="absolute top-3 left-3 flex gap-2 z-10">
      {recommended && (
        <span className="flex items-center gap-1 bg-primary text-white text-xs px-2 py-1 rounded-full shadow-sm">
          <Star size={12} /> Recommended
        </span>
      )}
      {bestValue && (
        <span className="flex items-center gap-1 bg-yellow-500 text-white text-xs px-2 py-1 rounded-full shadow-sm">
          <BadgePercent size={12} /> Best Value
        </span>
      )}
    </div>
  );
};

export default HotelBadge;
