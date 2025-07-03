import React, { useState } from 'react';
import { Plane } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import FlightCard from '../components/flights/FlightCard';

const Flights = () => {
  const navigate = useNavigate();
  const [selectedFlight, setSelectedFlight] = useState<string | null>(null);

  const flights = [
    {
      id: 'indigo',
      airline: 'IndiGo',
      code: '6E',
      departure: '06:30',
      arrival: '09:15',
      departureAirport: 'DEL',
      arrivalAirport: 'GOI',
      duration: '2h 45m',
      type: 'Non-stop',
      price: 8500,
      class: 'Economy',
      popular: true,
      aiRecommended: true,
      aiReasoning: {
        price: 'Competitive for a non-stop morning flight',
        duration: 'Only 2h 45m — shorter than average',
        airline: 'Known for punctuality and comfort',
        departure: 'Morning flight allows a full day at destination'
      }
    },
    {
      id: 'airindia',
      airline: 'Air India',
      code: 'AI',
      departure: '14:20',
      arrival: '17:05',
      departureAirport: 'DEL',
      arrivalAirport: 'GOI',
      duration: '2h 45m',
      type: 'Non-stop',
      price: 9200,
      class: 'Economy'
    },
    {
      id: 'spicejet',
      airline: 'SpiceJet',
      code: 'SG',
      departure: '19:45',
      arrival: '22:30',
      departureAirport: 'DEL',
      arrivalAirport: 'GOI',
      duration: '2h 45m',
      type: 'Non-stop',
      price: 7800,
      class: 'Economy',
      cheapest: true
    }
  ];

  const handleFlightSelect = (flightId: string) => {
    setSelectedFlight(flightId);
    navigate('/hotels'); // Redirect immediately after selection
  };

  const handleBookNow = (flightId: string) => {
    console.log('Booking flight:', flightId);
    navigate('/hotels');
  };

  const handleContinueWithoutFlight = () => {
    navigate('/hotels');
  };

  return (
    <div className="min-h-screen bg-pattern gradient-warm py-12 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8 animate-fade-in">
          <div className="flex-center mb-6">
            <div className="gradient-saffron p-3 rounded-2xl shadow-lg">
              <Plane className="text-white" size={32} />
            </div>
            <h1 className="text-heading ml-4 text-foreground">Available Flights</h1>
          </div>
          <p className="text-foreground mb-2 text-lg">Choose your perfect flight</p>
          <p className="text-primary italic font-medium">Yatrigan kripya dhyaan dein — sabse sahi udaan aapke liye yahan tayaar hai.</p>
        </div>

        {/* Flight List */}
        <div className="space-y-6 mb-8">
          {flights.map((flight, index) => (
            <FlightCard
              key={flight.id}
              flight={flight}
              selectedFlight={selectedFlight}
              onFlightSelect={handleFlightSelect}
              onBookNow={handleBookNow}
              index={index}
            />
          ))}
        </div>

        {/* Continue Without Flight */}
        <div className="text-center animate-fade-in">
          <button
            onClick={handleContinueWithoutFlight}
            className="px-8 py-3 border-2 border-muted text-muted-foreground rounded-xl font-medium hover:bg-muted hover:text-foreground transition-all duration-200"
          >
            Continue Without Flight Selection
          </button>
        </div>
      </div>
    </div>
  );
};

export default Flights;
