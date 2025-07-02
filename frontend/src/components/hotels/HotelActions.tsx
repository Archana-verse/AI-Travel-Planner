
import React from 'react';
import { CheckCircle } from 'lucide-react';

interface HotelActionsProps {
  price: number;
  hotelId: string;
  onSelect: (hotelId: string) => void;
  onBook: (hotelId: string) => void;
}

const HotelActions = ({ price, hotelId, onSelect, onBook }: HotelActionsProps) => {
  return (
    <div className="text-right mt-6 lg:mt-0 lg:ml-8">
      <div className="text-3xl font-semibold text-primary mb-1">₹{price.toLocaleString()}</div>
      <div className="text-muted-foreground mb-6">per night</div>
      
      <div className="space-y-3">
        <button
          onClick={() => onSelect(hotelId)}
          className="btn-primary w-full flex-center"
        >
          <CheckCircle size={18} />
          <span>Select Hotel</span>
        </button>
        <button
          onClick={() => onBook(hotelId)}
          className="btn-secondary w-full"
        >
          Book Hotel
        </button>
      </div>
    </div>
  );
};

export default HotelActions;
