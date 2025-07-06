import React, { useEffect, useState } from 'react';
import {
  Calendar, Plane, Download, RefreshCw, Copy,
  Clock, IndianRupee, CheckCircle
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';

// ✅ Airline → Official Booking URL mapping
const airlineBookingUrls: Record<string, string> = {
  'IndiGo': 'https://www.goindigo.in/',
  'Air India': 'https://www.airindia.com/',
  'Vistara': 'https://www.airvistara.com/',
  'SpiceJet': 'https://book.spicejet.com/',
  'Go First': 'https://www.flygofirst.com/',
  'Akasa Air': 'https://www.akasaair.com/',
  'Alliance Air': 'https://www.allianceair.in/',
  'AirAsia India': 'https://www.airasia.co.in/',
  'Star Air': 'https://www.starair.in/',
};

const Itinerary = () => {
  const navigate = useNavigate();
  const [flight, setFlight] = useState<any | null>(null);

  useEffect(() => {
    const savedFlight = localStorage.getItem('selectedFlight');
    if (savedFlight) {
      setFlight(JSON.parse(savedFlight));
    }
  }, []);

  const itinerary = [
    {
      day: 1,
      date: 'June 27, 2025',
      title: 'Arrival in Destination',
      activities: [
        { time: '11:15 AM', icon: '✈️', activity: 'Arrive at airport' },
        { time: '12:30 PM', icon: '🏨', activity: 'Check-in at hotel' },
        { time: '2:00 PM', icon: '🏛️', activity: 'Visit historical place' },
        { time: '7:30 PM', icon: '🍽️', activity: 'Dinner at local restaurant' }
      ]
    },
    {
      day: 2,
      date: 'June 28, 2025',
      title: 'Exploration Day',
      activities: [
        { time: '9:00 AM', icon: '🌉', activity: 'Visit major attraction' },
        { time: '11:00 AM', icon: '🌼', activity: 'Explore markets' },
        { time: '2:00 PM', icon: '🏛️', activity: 'Museum tour' },
        { time: '7:00 PM', icon: '🍛', activity: 'Dinner at cultural restaurant' }
      ]
    }
  ];

  const handleDownloadPDF = () => console.log('Downloading PDF...');
  const handleRegenerateItinerary = () => navigate('/plan');
  const handleCopyToClipboard = () => console.log('Copied to clipboard');

  const handleBookFlight = () => {
    if (!flight) return;
    const airline = flight.airline?.trim();
    const redirectUrl = airlineBookingUrls[airline];

    if (redirectUrl) {
      window.open(redirectUrl, '_blank');
    } else {
      alert(`Booking link for airline "${airline}" not available.`);
    }
  };

  return (
    <div className="min-h-screen bg-pattern gradient-warm py-12 px-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-hero mb-4 bg-gradient-to-r from-primary to-yellow-500 bg-clip-text text-transparent">
            Your Perfect Itinerary
          </h1>
          <p className="text-body text-lg">AI-generated travel plan for your journey</p>
        </div>

        {/* Flight Summary Card */}
        <div className="card-elevated p-6 animate-scale-in mb-8">
          <div className="flex-center mb-4">
            <div className="gradient-saffron p-3 rounded-xl shadow-md">
              <Plane className="text-white" size={24} />
            </div>
            <div className="ml-4">
              <h3 className="text-subheading">Flight Details</h3>
              <p className="text-caption">{flight?.airline || 'No flight selected'}</p>
            </div>
          </div>
          {flight ? (
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Route:</span>
                <span className="font-medium text-foreground">
                  {flight.departureAirport} → {flight.arrivalAirport}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Departure:</span>
                <span className="font-medium text-foreground">{flight.departure}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Arrival:</span>
                <span className="font-medium text-foreground">{flight.arrival}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Price:</span>
                <span className="font-semibold text-primary">₹{flight.price}</span>
              </div>
            </div>
          ) : (
            <p className="text-muted-foreground">No flight selected</p>
          )}
          <button
            className="btn-primary w-full mt-6"
            style={{ fontSize: '1rem', padding: '0.75rem 0' }}
            onClick={handleBookFlight}
          >
            BOOK NOW
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-12 animate-fade-in">
          <button onClick={handleDownloadPDF} className="btn-primary flex-center">
            <Download size={18} />
            <span>Download PDF</span>
          </button>
          <button onClick={handleRegenerateItinerary} className="btn-secondary flex-center">
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

        {/* Total Cost */}
        <div className="mt-12 card-elevated p-8 bg-gradient-to-r from-accent/30 to-primary/5 animate-fade-in">
          <div className="flex items-center justify-between">
            <div className="flex-center">
              <div className="gradient-saffron p-3 rounded-xl shadow-lg">
                <IndianRupee className="text-white" size={24} />
              </div>
              <h3 className="text-subheading ml-4">Estimated Total Cost</h3>
            </div>
            <div className="text-4xl font-semibold bg-gradient-to-r from-primary to-yellow-500 bg-clip-text text-transparent">
              ₹12,000
            </div>
          </div>
          <p className="text-caption mt-4 leading-relaxed">
            *Includes flights, accommodation, and estimated meal costs. Actual costs may vary.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Itinerary;
