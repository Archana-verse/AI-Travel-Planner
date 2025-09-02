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
    <div className="flex items-center justify-between flex-wrap gap-4 mt-5">
      <button
        onClick={() => onSelect(hotelId)}
        className="btn-primary flex items-center gap-2 px-4 py-2"
      >
        <CheckCircle size={18} />
        <span>Select Hotel</span>
      </button>

      <div className="text-right">
        <div className="text-xl font-semibold text-primary">{price}</div>
        <div className="text-sm text-muted-foreground">Includes basic amenities</div>
      </div>
    </div>
  );
};

export default HotelActions;
