import React from 'react';
import { Calendar, MapPin, Plane, Hotel, Download, RefreshCw, Copy, Clock, IndianRupee, CheckCircle } from 'lucide-react';

const Itinerary = () => {
  const tripSummary = {
    flight: {
      airline: 'IndiGo',
      route: 'Delhi → Kolkata',
      departure: '08:30 AM',
      arrival: '11:15 AM',
      price: '₹4,890',
      date: 'June 27, 2025'
    },
    hotel: {
      name: 'Rukmini Guest House',
      location: 'Park Street, Kolkata',
      checkIn: 'June 27, 2025',
      checkOut: 'June 30, 2025',
      price: '₹2,400/night',
      rating: '4.2'
    }
  };

  const itinerary = [
    {
      day: 1,
      date: 'June 27, 2025',
      title: 'Arrival in Kolkata',
      activities: [
        { time: '11:15 AM', icon: '✈️', activity: 'Arrive at Netaji Subhas Chandra Bose Airport' },
        { time: '12:30 PM', icon: '🏨', activity: 'Check-in at Rukmini Guest House' },
        { time: '2:00 PM', icon: '🏛️', activity: 'Visit Victoria Memorial (2 hours)' },
        { time: '7:30 PM', icon: '🍽️', activity: 'Dinner at Peter Cat – Chelo Kebabs' }
      ]
    },
    {
      day: 2,
      date: 'June 28, 2025',
      title: 'Historical Kolkata',
      activities: [
        { time: '9:00 AM', icon: '🌉', activity: 'Visit Howrah Bridge (1 hr)' },
        { time: '11:00 AM', icon: '🌼', activity: 'Explore Flower Market (1 hr)' },
        { time: '2:00 PM', icon: '🏛️', activity: 'Indian Museum (3 hrs)' },
        { time: '7:00 PM', icon: '🍛', activity: 'Dinner at 6 Ballygunge Place (Bengali cuisine)' }
      ]
    },
    {
      day: 3,
      date: 'June 29, 2025',
      title: 'Cultural Exploration',
      activities: [
        { time: '9:00 AM', icon: '🕌', activity: 'Kalighat Kali Temple (1.5 hrs)' },
        { time: '11:30 AM', icon: '🏛️', activity: 'Dakshineswar Kali Temple (2 hrs)' },
        { time: '3:00 PM', icon: '📚', activity: 'College Street Book Market (2 hrs)' },
        { time: '7:30 PM', icon: '🍤', activity: 'Dinner at Oh! Calcutta (Bengali seafood)' }
      ]
    }
  ];

  const handleDownloadPDF = () => {
    console.log('Downloading PDF...');
  };

  const handleRegenerateItinerary = () => {
    console.log('Regenerating itinerary...');
  };

  const handleCopyToClipboard = () => {
    console.log('Copying to clipboard...');
  };

  return (
    <div className="min-h-screen bg-pattern gradient-warm py-12 px-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-hero mb-4 bg-gradient-to-r from-primary to-yellow-500 bg-clip-text text-transparent">
            Your Perfect Itinerary
          </h1>
          <p className="text-body text-lg">
            AI-generated travel plan for your journey to Kolkata
          </p>
        </div>

        {/* Trip Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Flight Summary */}
          <div className="card-elevated p-6 animate-scale-in">
            <div className="flex-center mb-4">
              <div className="gradient-saffron p-3 rounded-xl shadow-md">
                <Plane className="text-white" size={24} />
              </div>
              <div className="ml-4">
                <h3 className="text-subheading">Flight Details</h3>
                <p className="text-caption">{tripSummary.flight.airline}</p>
              </div>
            </div>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Route:</span>
                <span className="font-medium text-foreground">{tripSummary.flight.route}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Departure:</span>
                <span className="font-medium text-foreground">{tripSummary.flight.departure}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Arrival:</span>
                <span className="font-medium text-foreground">{tripSummary.flight.arrival}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Price:</span>
                <span className="font-semibold text-primary">{tripSummary.flight.price}</span>
              </div>
            </div>
            <button
              className="btn-primary w-full mt-6"
              style={{ fontSize: '1rem', padding: '0.75rem 0' }}
              onClick={() => {/* Add booking logic here */}}
            >
              BOOK NOW
            </button>
          </div>

          {/* Hotel Summary */}
          <div className="card-elevated p-6 animate-scale-in" style={{ animationDelay: '0.1s' }}>
            <div className="flex-center mb-4">
              <div className="gradient-saffron p-3 rounded-xl shadow-md">
                <Hotel className="text-white" size={24} />
              </div>
              <div className="ml-4">
                <h3 className="text-subheading">Hotel Details</h3>
                <div className="flex-center">
                  <span className="text-caption mr-2">Rating:</span>
                  <span className="text-yellow-500">⭐</span>
                  <span className="text-caption ml-1">{tripSummary.hotel.rating}</span>
                </div>
              </div>
            </div>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Hotel:</span>
                <span className="font-medium text-foreground">{tripSummary.hotel.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Location:</span>
                <span className="font-medium text-foreground">{tripSummary.hotel.location}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Check-in:</span>
                <span className="font-medium text-foreground">{tripSummary.hotel.checkIn}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Price:</span>
                <span className="font-semibold text-primary">{tripSummary.hotel.price}</span>
              </div>
            </div>
            <button
              className="btn-primary w-full mt-6"
              style={{ fontSize: '1rem', padding: '0.75rem 0' }}
              onClick={() => {/* Add booking logic here */}}
            >
              BOOK NOW
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-12 animate-fade-in">
          <button
            onClick={handleDownloadPDF}
            className="btn-primary flex-center"
          >
            <Download size={18} />
            <span>Download PDF</span>
          </button>
          <button
            onClick={handleRegenerateItinerary}
            className="btn-secondary flex-center"
          >
            <RefreshCw size={18} />
            <span>Regenerate</span>
          </button>
          <button
            onClick={handleCopyToClipboard}
            className="flex-center border-2 border-muted text-muted-foreground px-6 py-3 rounded-xl font-medium hover:bg-muted hover:text-foreground transition-all duration-200"
          >
            <Copy size={18} />
            <span>Copy to Clipboard</span>
          </button>
        </div>

        {/* Itinerary Cards */}
        <div className="space-y-8">
          {itinerary.map((day, dayIndex) => (
            <div 
              key={day.day} 
              className="card-elevated p-8 animate-scale-in"
              style={{ animationDelay: `${dayIndex * 0.1}s` }}
            >
              <div className="flex-center mb-6">
                <div className="gradient-saffron text-white w-12 h-12 rounded-2xl flex items-center justify-center font-semibold text-lg shadow-lg">
                  {day.day}
                </div>
                <div className="ml-4">
                  <h2 className="text-subheading">
                    Day {day.day}: {day.title}
                  </h2>
                  <div className="flex-center text-caption">
                    <Calendar size={16} className="text-primary" />
                    <span className="ml-1">{day.date}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                {day.activities.map((activity, index) => (
                  <div 
                    key={index} 
                    className="flex items-start space-x-4 p-4 rounded-xl bg-accent/50 hover:bg-accent transition-colors duration-200"
                  >
                    <div className="flex-center min-w-fit">
                      <Clock size={16} className="text-primary" />
                      <span className="text-sm font-medium text-muted-foreground ml-2">{activity.time}</span>
                    </div>
                    <div className="text-2xl">{activity.icon}</div>
                    <div className="flex-1">
                      <p className="text-foreground font-medium leading-relaxed">{activity.activity}</p>
                    </div>
                    <CheckCircle size={20} className="text-muted-foreground hover:text-success cursor-pointer transition-colors" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Total Cost Summary */}
        <div className="mt-12 card-elevated p-8 bg-gradient-to-r from-accent/30 to-primary/5 animate-fade-in">
          <div className="flex items-center justify-between">
            <div className="flex-center">
              <div className="gradient-saffron p-3 rounded-xl shadow-lg">
                <IndianRupee className="text-white" size={24} />
              </div>
              <h3 className="text-subheading ml-4">Estimated Total Cost</h3>
            </div>
            <div className="text-4xl font-semibold bg-gradient-to-r from-primary to-yellow-500 bg-clip-text text-transparent">
              ₹12,090
            </div>
          </div>
          <p className="text-caption mt-4 leading-relaxed">
            *Includes flights, accommodation, and estimated meal costs. Actual costs may vary based on your preferences and seasonal pricing.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Itinerary;
