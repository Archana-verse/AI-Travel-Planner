
import React from 'react';
import { Plane, Clock } from 'lucide-react';

interface FlightTimesProps {
  departure: string;
  arrival: string;
  departureAirport: string;
  arrivalAirport: string;
  duration: string;
  type: string;
}

const FlightTimes = ({ 
  departure, 
  arrival, 
  departureAirport, 
  arrivalAirport, 
  duration, 
  type 
}: FlightTimesProps) => {
  return (
    <div className="flex items-center justify-between max-w-md mb-6">
      <div className="text-center">
        <div className="text-2xl font-semibold text-foreground">{departure}</div>
        <div className="text-muted-foreground">{departureAirport}</div>
      </div>
      
      <div className="flex-1 flex items-center justify-center mx-8">
        <div className="text-center">
          <Plane className="text-primary mx-auto mb-1" size={20} />
          <div className="flex-center justify-center text-muted-foreground">
            <Clock size={14} />
            <span>{duration}</span>
          </div>
          <div className="text-xs text-muted-foreground">{type}</div>
        </div>
      </div>

      <div className="text-center">
        <div className="text-2xl font-semibold text-foreground">{arrival}</div>
        <div className="text-muted-foreground">{arrivalAirport}</div>
      </div>
    </div>
  );
};

export default FlightTimes;
