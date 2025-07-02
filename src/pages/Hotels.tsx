
import React from 'react';
import { Building, Star, Wifi, Car, Utensils, Waves, MapPin, CheckCircle, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

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
            <h1 className="text-heading ml-4">Perfect Hotels for You</h1>
          </div>
          <p className="text-body text-lg">Hand-picked accommodations for your comfort and convenience</p>
        </div>

        {/* Hotels List */}
        <div className="space-y-8">
          {hotels.map((hotel, index) => (
            <div 
              key={hotel.id} 
              className={`card-elevated overflow-hidden hover-lift ${
                hotel.aiRecommended ? 'bg-gradient-to-r from-[#fffef2] to-white border-l-4 border-primary' : ''
              }`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Recommended/Best Value Badge */}
              {(hotel.recommended || hotel.bestValue) && (
                <div className="bg-gradient-to-r from-primary to-yellow-400 text-white px-4 py-2 text-sm font-medium flex-center">
                  <Star size={16} className="mr-1" />
                  {hotel.recommended ? 'Recommended' : 'Best Value'}
                </div>
              )}
              
              <div className="flex flex-col lg:flex-row">
                {/* Hotel Image */}
                <div className="w-full lg:w-80 h-64 bg-gradient-to-br from-accent to-primary/10 flex items-center justify-center">
                  <span className="text-8xl">{hotel.image}</span>
                </div>

                {/* Hotel Details */}
                <div className="flex-1 p-8">
                  <div className="flex flex-col lg:flex-row justify-between items-start mb-6">
                    <div className="flex-1">
                      <div className="flex-center mb-3">
                        <h2 className="text-subheading">{hotel.name}</h2>
                        {hotel.aiRecommended && (
                          <div className="ml-3 flex-center bg-gradient-to-r from-primary to-yellow-400 text-white px-3 py-1 rounded-full text-xs font-medium">
                            <Zap size={12} className="mr-1" />
                            AI Recommended
                          </div>
                        )}
                      </div>
                      <div className="flex-center mb-3">
                        <div className="flex-center">
                          <Star className="text-yellow-400 fill-current" size={18} />
                          <span className="font-semibold text-foreground ml-1">{hotel.rating}</span>
                        </div>
                        <span className="text-muted-foreground mx-2">•</span>
                        <span className="text-caption">{hotel.reviews} reviews</span>
                      </div>
                      <div className="flex-center mb-4">
                        <MapPin className="text-muted-foreground" size={16} />
                        <span className="text-caption ml-1">{hotel.location}</span>
                      </div>
                      <p className="text-body mb-6 leading-relaxed">{hotel.description}</p>

                      {/* Amenities */}
                      <div className="mb-6">
                        <h3 className="font-medium text-foreground mb-3">Amenities</h3>
                        <div className="flex flex-wrap gap-3">
                          {hotel.amenities.map((amenity, index) => {
                            const Icon = amenity.icon;
                            return (
                              <div key={index} className="flex-center bg-accent px-3 py-2 rounded-lg">
                                <Icon className="text-primary" size={16} />
                                <span className="text-caption ml-2">{amenity.label}</span>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* AI Recommendation Block */}
                      {hotel.aiRecommended && hotel.aiReasoning && (
                        <div className="bg-white/70 backdrop-blur-sm rounded-xl p-4 border border-primary/20">
                          <div className="flex-center mb-3">
                            <Zap className="text-primary" size={16} />
                            <h4 className="font-medium text-foreground ml-2">Why AI recommends this:</h4>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                            <div><strong>Rating:</strong> {hotel.aiReasoning.rating}</div>
                            <div><strong>Location:</strong> {hotel.aiReasoning.location}</div>
                            <div><strong>Amenities:</strong> {hotel.aiReasoning.amenities}</div>
                            <div><strong>Value:</strong> {hotel.aiReasoning.value}</div>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Price and Actions */}
                    <div className="text-right mt-6 lg:mt-0 lg:ml-8">
                      <div className="text-3xl font-semibold text-primary mb-1">₹{hotel.price.toLocaleString()}</div>
                      <div className="text-caption mb-6">per night</div>
                      
                      <div className="space-y-3">
                        <button
                          onClick={() => handleHotelSelect(hotel.id)}
                          className="btn-primary w-full flex-center"
                        >
                          <CheckCircle size={18} />
                          <span>Select Hotel</span>
                        </button>
                        <button
                          onClick={() => handleBookHotel(hotel.id)}
                          className="btn-secondary w-full"
                        >
                          Book Hotel
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Hotels;
