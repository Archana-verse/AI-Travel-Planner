
import React from 'react';
import { CheckCircle, Zap } from 'lucide-react';
import FlightBadge from './FlightBadge';
import FlightTimes from './FlightTimes';
import AIRecommendation from './AIRecommendation';
import FlightActions from './FlightActions';

interface FlightCardProps {
  flight: {
    id: string;
    airline: string;
    code: string;
    departure: string;
    arrival: string;
    departureAirport: string;
    arrivalAirport: string;
    duration: string;
    type: string;
    price: number;
    class: string;
    popular?: boolean;
    cheapest?: boolean;
    aiRecommended?: boolean;
    aiReasoning?: {
      price: string;
      duration: string;
      airline: string;
      departure: string;
    };
  };
  selectedFlight: string | null;
  onFlightSelect: (flightId: string) => void;
  onBookNow: (flightId: string) => void;
  index: number;
}

const FlightCard = ({ 
  flight, 
  selectedFlight, 
  onFlightSelect, 
  onBookNow, 
  index 
}: FlightCardProps) => {
  return (
    <div 
      className={`card-elevated overflow-hidden hover-lift ${
        selectedFlight === flight.id ? 'selection-ring' : ''
      } ${flight.aiRecommended ? 'bg-gradient-to-r from-[#fff7eb] dark:from-[#2a1f0f] to-white dark:to-card border-l-4 border-primary' : ''}`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <FlightBadge isPopular={flight.popular} isCheapest={flight.cheapest} />
      
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex-center mb-4">
              <div className="w-12 h-12 gradient-saffron rounded-xl flex items-center justify-center shadow-md">
                <span className="font-semibold text-white">{flight.code}</span>
              </div>
              <div className="ml-4">
                <div className="flex-center">
                  <h3 className="text-subheading text-foreground">{flight.airline}</h3>
                  {flight.aiRecommended && (
                    <div className="ml-3 flex-center bg-gradient-to-r from-primary to-yellow-400 text-white px-3 py-1 rounded-full text-xs font-medium">
                      <Zap size={12} className="mr-1" />
                      AI Recommended
                    </div>
                  )}
                </div>
                <p className="text-muted-foreground">{flight.class}</p>
              </div>
              {selectedFlight === flight.id && (
                <CheckCircle className="text-success ml-4 animate-scale-in" size={24} />
              )}
            </div>

            <FlightTimes
              departure={flight.departure}
              arrival={flight.arrival}
              departureAirport={flight.departureAirport}
              arrivalAirport={flight.arrivalAirport}
              duration={flight.duration}
              type={flight.type}
            />

            {flight.aiRecommended && (
              <AIRecommendation aiReasoning={flight.aiReasoning} />
            )}
          </div>

          <FlightActions
            flightId={flight.id}
            price={flight.price}
            selectedFlight={selectedFlight}
            onFlightSelect={onFlightSelect}
            onBookNow={onBookNow}
          />
        </div>
      </div>
    </div>
  );
};

export default FlightCard;
