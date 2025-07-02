
import React from 'react';
import { Building, Star, Wifi, Car, Utensils, Waves } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import HotelCard from '../components/hotels/HotelCard';

const Hotels = () => {
  const navigate = useNavigate();
  
  const hotels = [
    {
      id: 'oberoi',
      name: 'The Oberoi Grand, Kolkata',
      rating: 4.8,
      reviews: 1250,
      location: 'Esplanade',
      description: 'Luxury heritage hotel in the heart of Kolkata with colonial charm',
      price: 12500,
      image: '🏨',
      recommended: true,
      aiRecommended: true,
      aiReasoning: {
        rating: '4.8/5 from over 1200 verified reviews',
        location: 'Centrally located near top tourist spots',
        amenities: 'Includes WiFi, pool, spa — perfect for family or business',
        value: 'Competitive pricing for a premium 5-star property'
      },
      amenities: [
        { icon: Wifi, label: 'Free WiFi' },
        { icon: Waves, label: 'Pool' },
        { icon: Car, label: 'Spa' },
        { icon: Utensils, label: 'Restaurant' }
      ]
    },
    {
      id: 'itc',
      name: 'ITC Royal Bengal',
      rating: 4.7,
      reviews: 980,
      location: 'Salt Lake',
      description: 'Modern luxury with traditional Bengali hospitality and world-class amenities',
      price: 15800,
      image: '🏨',
      amenities: [
        { icon: Wifi, label: 'Free WiFi' },
        { icon: Waves, label: 'Pool' },
        { icon: Car, label: 'Gym' },
        { icon: Building, label: 'Business Center' }
      ]
    },
    {
      id: 'park',
      name: 'Park Hotel Kolkata',
      rating: 4.5,
      reviews: 750,
      location: 'Park Street',
      description: 'Contemporary luxury in the cultural heart of the city with modern design',
      price: 8200,
      image: '🏨',
      bestValue: true,
      amenities: [
        { icon: Wifi, label: 'Free WiFi' },
        { icon: Waves, label: 'Pool' },
        { icon: Car, label: 'Spa' },
        { icon: Utensils, label: 'Restaurant' }
      ]
    }
  ];

  const handleHotelSelect = (hotelId: string) => {
    console.log('Selecting hotel:', hotelId);
    navigate('/itinerary');
  };

  const handleBookHotel = (hotelId: string) => {
    console.log('Booking hotel:', hotelId);
    navigate('/itinerary');
  };

  return (
    <div className="min-h-screen bg-pattern gradient-warm py-12 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8 animate-fade-in">
          <div className="flex-center mb-6">
            <div className="gradient-saffron p-3 rounded-2xl shadow-lg">
              <Building className="text-white" size={32} />
            </div>
            <h1 className="text-heading ml-4 text-foreground">Perfect Hotels for You</h1>
          </div>
          <p className="text-foreground text-lg">Hand-picked accommodations for your comfort and convenience</p>
        </div>

        {/* Hotels List */}
        <div className="space-y-8">
          {hotels.map((hotel, index) => (
            <HotelCard
              key={hotel.id}
              hotel={hotel}
              index={index}
              onSelect={handleHotelSelect}
              onBook={handleBookHotel}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Hotels;
