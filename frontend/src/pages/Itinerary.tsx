import React, { useEffect, useState } from 'react';
import {
  Plane, Calendar, Clock, Download, RefreshCw, Copy,
  CheckCircle, IndianRupee
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import html2pdf from 'html2pdf.js'; 

const Itinerary = () => {
  const navigate = useNavigate();
  const [flight, setFlight] = useState<any | null>(null);
  const [hotel, setHotel] = useState<any | null>(null);
  const [itinerary, setItinerary] = useState<any[] | null>(null);

  useEffect(() => {
    const savedFlight = localStorage.getItem('selectedFlight');
    const savedItinerary = localStorage.getItem('itinerary');
    const formDataRaw = localStorage.getItem('formData');

    if (savedFlight) setFlight(JSON.parse(savedFlight));
    if (savedItinerary) {
      const itineraryData = JSON.parse(savedItinerary);
      if (itineraryData.hotel) setHotel(itineraryData.hotel);
    }

    if (formDataRaw) {
      const formData = JSON.parse(formDataRaw);
      const payload = {
        to: formData.to,
        departureDate: formData.departureDate,
        returnDate: formData.returnDate,
        interests: formData.interests || [],
        travelers: formData.travelers,
        diet: formData.diet,
      };

      fetch('http://127.0.0.1:8000/api/itinerary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) setItinerary(data);
          else setItinerary([]);
        })
        .catch(err => {
          console.error("❌ Error:", err);
          setItinerary([]);
        });
    }
  }, []);

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
    'Air India Express': 'https://www.airindiaexpress.com/',
  };

  const handleBookFlight = () => {
    if (!flight) return;
    const airline = flight.airline?.trim();
    const redirectUrl = airlineBookingUrls[airline];
    if (redirectUrl) {
      window.open(redirectUrl, '_blank');
    } else {
      alert(`Booking link not available for "${airline}"`);
    }
  };

  const handleBookHotel = () => {
    const hotelName = hotel?.name?.trim();
    const bookingLink =
      hotel?.link ||
      hotel?.booking_url ||
      hotel?.url ||
      (hotelName
        ? `https://www.booking.com/searchresults.html?ss=${encodeURIComponent(hotelName)}`
        : null);

    if (bookingLink && bookingLink.startsWith('http')) {
      window.open(bookingLink, '_blank');
    } else {
      alert("⚠ Valid hotel booking link not found.");
    }
  };

  // ✅ NEW: fallback to formData if hotel check-in/out missing
  const formDataRaw = localStorage.getItem('formData');
  let fallbackCheckIn = '';
  let fallbackCheckOut = '';

  if (formDataRaw) {
    const formData = JSON.parse(formDataRaw);
    fallbackCheckIn = formData.departureDate;
    fallbackCheckOut = formData.returnDate;
  }

  const checkIn = hotel?.checkIn || fallbackCheckIn;
  const checkOut = hotel?.checkOut || fallbackCheckOut;

  const getNights = () => {
    const inDate = new Date(checkIn);
    const outDate = new Date(checkOut);
    const diffTime = outDate.getTime() - inDate.getTime();
    return Math.max(Math.ceil(diffTime / (1000 * 60 * 60 * 24)), 1);
  };

  const nights = getNights();
  const hotelPerNight = hotel?.price ?? hotel?.pricePerNight ?? hotel?.cost ?? 1000;
  const hotelTotal = hotelPerNight * nights;
  const totalCost = (flight?.price ?? 0) + hotelTotal + 1500;

  if (itinerary === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#fef9f4] dark:bg-neutral-900">
        <div className="w-12 h-12 border-4 border-orange-400 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fef9f4] dark:bg-neutral-900 py-12 px-6 text-black dark:text-white">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-[#ff8c00] mb-2">Your Perfect Itinerary</h1>
          <p className="text-gray-600 dark:text-gray-300 text-lg">
            AI-generated travel plan for your journey to {hotel?.city || flight?.arrivalAirport}
          </p>
        </div>

        {/* Flight + Hotel Section */}
        <div className="flex flex-col lg:flex-row justify-between gap-6 mb-10">
          {/* Flight Card */}
          <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl shadow-md flex-1 border border-gray-200 dark:border-gray-700">
            <h3 className="font-semibold text-lg mb-3 flex items-center gap-2">
              <Plane size={20} className="text-orange-500" /> Flight Details
            </h3>
            {flight ? (
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span>Route:</span> <span>{flight.departureAirport} → {flight.arrivalAirport}</span></div>
                <div className="flex justify-between"><span>Departure:</span> <span>{flight.departure}</span></div>
                <div className="flex justify-between"><span>Arrival:</span> <span>{flight.arrival}</span></div>
                <div className="flex justify-between font-semibold text-orange-600"><span>Price:</span> <span>₹{flight.price.toLocaleString()}</span></div>
              </div>
            ) : <p>No flight selected</p>}
            <button className="btn-primary w-full mt-4" onClick={handleBookFlight}>BOOK NOW</button>
          </div>

          {/* Hotel Card */}
          <div className="bg-white dark:bg-neutral-800 p-6 rounded-xl shadow-md flex-1 border border-gray-200 dark:border-gray-700">
            <h3 className="font-semibold text-lg mb-3">Hotel Details</h3>
            {hotel ? (
              <div className="text-sm space-y-1">
                <div className="font-semibold">{hotel.name}</div>
                <div className="text-gray-500 dark:text-gray-300">{hotel.address}</div>
                <div className="flex justify-between"><span>Check-in:</span><span>{checkIn}</span></div>
                <div className="flex justify-between"><span>Check-out:</span><span>{checkOut}</span></div>
                <div className="flex justify-between font-semibold text-orange-600">
                  <span>Total Price ({nights} night{nights > 1 ? 's' : ''}):</span>
                  <span>₹{hotelTotal.toLocaleString()}</span>
                </div>
                <button className="btn-primary w-full mt-4" onClick={handleBookHotel}>BOOK NOW</button>
              </div>
            ) : <p>No hotel selected</p>}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          <button
            className="btn-primary flex items-center gap-2"
            onClick={() => {
              const element = document.querySelector('.max-w-5xl');
              if (!element) return;
              html2pdf().set({
                margin: 0.5,
                filename: 'itinerary.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
              }).from(element).save();
            }}
          >
            <Download size={18} />Download PDF
          </button>

          <button className="btn-secondary flex items-center gap-2" onClick={() => navigate('/plan')}>
            <RefreshCw size={18} />Regenerate
          </button>

          <button className="flex items-center gap-2 border px-4 py-2 rounded-xl hover:bg-gray-100 dark:hover:bg-neutral-700">
            <Copy size={18} />Copy to Clipboard
          </button>
        </div>

        {/* Day-wise Itinerary */}
        <div className="space-y-8">
          {itinerary.map((day, index) => (
            <div key={day.day} className="bg-white dark:bg-neutral-800 p-6 rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold">{day.day}</div>
                <div className="ml-4">
                  <h3 className="font-semibold text-lg">Day {day.day}: {day.title}</h3>
                  <div className="text-sm text-gray-500 dark:text-gray-300 flex items-center gap-1">
                    <Calendar size={14} /> {day.date}
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                {day.activities.map((activity: any, i: number) => (
                  <div key={i} className="flex items-start gap-4 bg-gray-50 dark:bg-neutral-700 p-4 rounded-lg">
                    <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-300 min-w-[120px]">
                      <Clock size={16} /> {activity.time}
                    </div>
                    <div className="text-2xl">{activity.icon}</div>
                    <div className="flex-1 text-gray-800 dark:text-white font-medium">{activity.activity}</div>
                    <CheckCircle size={20} className="text-gray-400 hover:text-green-500 cursor-pointer" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Estimated Total */}
        <div className="mt-12 p-6 rounded-xl bg-gradient-to-r from-orange-100 to-yellow-50 dark:from-orange-900 dark:to-yellow-800 border dark:border-yellow-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <IndianRupee size={28} className="text-orange-600" />
              <h3 className="text-lg font-semibold">Estimated Total Cost</h3>
            </div>
            <div className="text-3xl font-bold text-orange-600">₹{totalCost.toLocaleString()}</div>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">
            *Includes flights, accommodation, and estimated meal costs. Actual costs may vary.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Itinerary;
