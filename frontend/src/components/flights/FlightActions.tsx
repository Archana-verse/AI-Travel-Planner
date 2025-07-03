import React from 'react';
import { CheckCircle } from 'lucide-react';

interface FlightActionsProps {
  flightId: string;
  price: number;
  selectedFlight: string | null;
  onFlightSelect: (flightId: string) => void;
  onBookNow: (flightId: string) => void;
}

const FlightActions = ({ 
  flightId, 
  price, 
  selectedFlight, 
  onFlightSelect, 
  onBookNow 
}: FlightActionsProps) => {
  return (
    <div className="text-right ml-8">
      <div className="text-3xl font-semibold text-primary mb-2">₹{price.toLocaleString()}</div>
      <div className="text-muted-foreground mb-6">per person</div>
      <div className="space-y-3">
        <button
          onClick={() => onFlightSelect(flightId)}
          className={`w-full px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
            selectedFlight === flightId
              ? 'bg-success text-white'
              : 'btn-primary'
          }`}
        >
          {selectedFlight === flightId ? 'Selected' : 'Select Flight'}
        </button>
        {/* Book Now button removed */}
      </div>
    </div>
  );
};

export default FlightActions;
