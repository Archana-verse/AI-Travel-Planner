import React from 'react';
import { CheckCircle } from 'lucide-react';

interface HotelActionsProps {
  price: string; 
  hotelId: string;
  onSelect: (hotelId: string) => void;
  onBook: (hotelId: string) => void;
}

const HotelActions = ({ price, hotelId, onSelect }: HotelActionsProps) => {
  return (
    <div className="text-right mt-5 md:mt-0 md:ml-8">
      <div className="text-xl font-semibold text-primary mb-1">{price}</div>
      <div className="text-sm text-muted-foreground mb-4">Includes basic amenities</div>

      <button
        onClick={() => onSelect(hotelId)}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        <CheckCircle size={18} />
        <span>Select Hotel</span>
      </button>
    </div>
  );
};

export default HotelActions;
