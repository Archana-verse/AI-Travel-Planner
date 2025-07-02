
import React, { useState } from 'react';
import { Plane, Clock, ArrowRight, Star, CheckCircle, Zap } from 'lucide-react';
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
            <div 
              key={flight.id} 
              className={`card-elevated overflow-hidden hover-lift ${
                selectedFlight === flight.id ? 'selection-ring' : ''
              } ${flight.aiRecommended ? 'bg-gradient-to-r from-[#fff7eb] dark:from-[#2a1f0f] to-white dark:to-card border-l-4 border-primary' : ''}`}
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

                    <div className="flex items-center justify-between max-w-md mb-6">
                      <div className="text-center">
                        <div className="text-2xl font-semibold text-foreground">{flight.departure}</div>
                        <div className="text-muted-foreground">{flight.departureAirport}</div>
                      </div>
                      
                      <div className="flex-1 flex items-center justify-center mx-8">
                        <div className="text-center">
                          <Plane className="text-primary mx-auto mb-1" size={20} />
                          <div className="flex-center justify-center text-muted-foreground">
                            <Clock size={14} />
                            <span>{flight.duration}</span>
                          </div>
                          <div className="text-xs text-muted-foreground">{flight.type}</div>
                        </div>
                      </div>

                      <div className="text-center">
                        <div className="text-2xl font-semibold text-foreground">{flight.arrival}</div>
                        <div className="text-muted-foreground">{flight.arrivalAirport}</div>
                      </div>
                    </div>

                    {/* AI Recommendation Block */}
                    {flight.aiRecommended && flight.aiReasoning && (
                      <div className="bg-white/70 dark:bg-card/70 backdrop-blur-sm rounded-xl p-4 mb-4 border border-primary/20">
                        <div className="flex-center mb-3">
                          <Zap className="text-primary" size={16} />
                          <h4 className="font-medium text-foreground ml-2">Why AI recommends this:</h4>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-foreground">
                          <div><strong>Price:</strong> {flight.aiReasoning.price}</div>
                          <div><strong>Duration:</strong> {flight.aiReasoning.duration}</div>
                          <div><strong>Airline:</strong> {flight.aiReasoning.airline}</div>
                          <div><strong>Departure:</strong> {flight.aiReasoning.departure}</div>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="text-right ml-8">
                    <div className="text-3xl font-semibold text-primary mb-2">₹{flight.price.toLocaleString()}</div>
                    <div className="text-muted-foreground mb-6">per person</div>
                    
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
