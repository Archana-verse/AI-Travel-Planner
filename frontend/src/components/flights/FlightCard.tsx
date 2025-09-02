import React from 'react';
import { CheckCircle, Zap } from 'lucide-react';
import FlightBadge from './FlightBadge';
import FlightTimes from './FlightTimes';
import AIRecommendation from './AIRecommendation';

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
  index,
}: FlightCardProps) => {
  const isSelected = selectedFlight === flight.id;

  return (
    <div
      className={`card-elevated overflow-hidden hover-lift transition-all duration-300 ${
        isSelected ? 'selection-ring' : ''
      } ${
        flight.aiRecommended
          ? 'bg-gradient-to-r from-[#fff7eb] dark:from-[#2a1f0f] to-white dark:to-card border-l-4 border-primary animate-glow-border'
          : ''
      }`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <FlightBadge isPopular={flight.popular} isCheapest={flight.cheapest} />

      <div className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            {/* Airline Header */}
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
              {isSelected && (
                <CheckCircle className="text-success ml-4 animate-scale-in" size={24} />
              )}
            </div>

            {/* Flight Times */}
            <FlightTimes
              departure={flight.departure}
              arrival={flight.arrival}
              departureAirport={flight.departureAirport}
              arrivalAirport={flight.arrivalAirport}
              duration={flight.duration}
              type={flight.type}
            />

            {/* AI Reasoning */}
            {flight.aiRecommended && flight.aiReasoning && (
              <AIRecommendation aiReasoning={flight.aiReasoning} />
            )}
          </div>

          {/* Actions */}
          <div className="text-right min-w-[130px]">
            <div className="text-xl font-bold text-foreground mb-1">₹{flight.price}</div>
            <div className="text-sm text-muted-foreground mb-4">per person</div>

            {isSelected ? (
              <button
                onClick={() => onBookNow(flight.id)}
                className="bg-success hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-semibold"
              >
                Continue
              </button>
            ) : (
              <button
                onClick={() => onFlightSelect(flight.id)}
                className="bg-primary hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-semibold"
              >
                Select Flight
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FlightCard;
