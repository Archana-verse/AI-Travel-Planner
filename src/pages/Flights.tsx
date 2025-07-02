
import React, { useState } from 'react';
import { Plane, Clock, ArrowRight, Star, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

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
      popular: true
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
            <h1 className="text-heading ml-4">Available Flights</h1>
          </div>
          <p className="text-body mb-2 text-lg">Choose your perfect flight</p>
          <p className="text-primary italic font-medium">Yatrigan kripya dhyaan dein — sabse sahi udaan aapke liye yahan tayaar hai.</p>
        </div>

        {/* Flight List */}
        <div className="space-y-6 mb-8">
          {flights.map((flight, index) => (
            <div 
              key={flight.id} 
              className={`card-elevated overflow-hidden hover-lift ${
                selectedFlight === flight.id ? 'selection-ring' : ''
              }`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Popular/Cheapest Badge */}
              {(flight.popular || flight.cheapest) && (
                <div className="bg-gradient-to-r from-primary to-yellow-400 text-white px-4 py-2 text-sm font-medium flex-center">
                  <Star size={16} className="mr-1" />
                  {flight.popular ? 'Most Popular' : 'Best Value'}
                </div>
              )}
              
              <div className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex-center mb-4">
                      <div className="w-12 h-12 gradient-saffron rounded-xl flex items-center justify-center shadow-md">
                        <span className="font-semibold text-white">{flight.code}</span>
                      </div>
                      <div className="ml-4">
                        <h3 className="text-subheading">{flight.airline}</h3>
                        <p className="text-caption">{flight.class}</p>
                      </div>
                      {selectedFlight === flight.id && (
                        <CheckCircle className="text-success ml-4 animate-scale-in" size={24} />
                      )}
                    </div>

                    <div className="flex items-center justify-between max-w-md">
                      <div className="text-center">
                        <div className="text-2xl font-semibold text-foreground">{flight.departure}</div>
                        <div className="text-caption">{flight.departureAirport}</div>
                      </div>
                      
                      <div className="flex-1 flex items-center justify-center mx-8">
                        <div className="text-center">
                          <Plane className="text-primary mx-auto mb-1" size={20} />
                          <div className="flex-center justify-center text-caption">
                            <Clock size={14} />
                            <span>{flight.duration}</span>
                          </div>
                          <div className="text-xs text-muted-foreground">{flight.type}</div>
                        </div>
                      </div>

                      <div className="text-center">
                        <div className="text-2xl font-semibold text-foreground">{flight.arrival}</div>
                        <div className="text-caption">{flight.arrivalAirport}</div>
                      </div>
                    </div>
                  </div>

                  <div className="text-right ml-8">
                    <div className="text-3xl font-semibold text-primary mb-2">₹{flight.price.toLocaleString()}</div>
                    <div className="text-caption mb-6">per person</div>
                    
                    <div className="space-y-3">
                      <button
                        onClick={() => handleFlightSelect(flight.id)}
                        className={`w-full px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                          selectedFlight === flight.id
                            ? 'bg-success text-white'
                            : 'btn-primary'
                        }`}
                      >
                        {selectedFlight === flight.id ? 'Selected' : 'Select Flight'}
                      </button>
                      <button
                        onClick={() => handleBookNow(flight.id)}
                        className="btn-secondary w-full"
                      >
                        Book Now
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
