import React, { useEffect, useState } from 'react';
import { Building } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import HotelCard from '../components/hotels/HotelCard';
import Loader from '../components/ui/Loader';
import { Wifi, Waves, Car, Utensils, Building as BizIcon } from 'lucide-react';

const Hotels = () => {
  const navigate = useNavigate();
  const [hotels, setHotels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const checkIn = "2025-07-10";
  const checkOut = "2025-07-15";
  const nights = Math.max(
    Math.ceil(
      (new Date(checkOut).getTime() - new Date(checkIn).getTime()) / (1000 * 60 * 60 * 24)
    ),
    1
  );

  useEffect(() => {
    const storedPlan = localStorage.getItem('planResults');
    if (storedPlan) {
      try {
        const parsed = JSON.parse(storedPlan);
        const hotelList = parsed.hotels || [];

        const enhancedHotels = hotelList.map((hotel: any, index: number) => ({
          id: hotel.id || `hotel-${index}`,
          name: hotel.name,
          rating: hotel.rating || 4.5,
          reviews: hotel.reviews || 500,
          location: hotel.location || 'City Center',
          description: hotel.description || '',
          price: parseInt(hotel.price?.toString().replace(/[^\d]/g, '') || '0'),
          image: hotel.image || 'https://via.placeholder.com/300x200?text=Hotel',
          aiRecommended: hotel.aiRecommended || hotel.ai_recommended || false,
          bestValue: hotel.bestValue || hotel.best_value || false,
          aiReasoning: hotel.aiReasoning || hotel.ai_reasoning || {},
          amenities: [
            ...(hotel.amenities || []).map((label: string) => ({
              label,
              icon: mapAmenityToIcon(label),
            })),
          ],
        }));

        enhancedHotels.sort((a, b) => {
          if (a.aiRecommended && !b.aiRecommended) return -1;
          if (!a.aiRecommended && b.aiRecommended) return 1;
          return 0;
        });

        setHotels(enhancedHotels);
      } catch (err) {
        console.error('Error parsing hotel data:', err);
      }
    }

    setLoading(false);
  }, []);

  const handleHotelSelect = (hotelId: string) => {
    const selected = hotels.find(h => h.id === hotelId);
    if (selected) {
      const itinerary = JSON.parse(localStorage.getItem("itinerary") || "{}");
      const totalPrice = selected.price * nights;

      itinerary.hotel = {
        name: selected.name,
        address: selected.location,
        checkIn,
        checkOut,
        image: selected.image,
        pricePerNight: selected.price,
        totalPrice,
        rating: selected.rating,
        reviews: selected.reviews
      };

      localStorage.setItem("itinerary", JSON.stringify(itinerary));
    }

    navigate('/itinerary');
  };

  const handleBookHotel = (hotelId: string) => {
    const selected = hotels.find(h => h.id === hotelId);
    if (selected) {
      const itinerary = JSON.parse(localStorage.getItem("itinerary") || "{}");
      const totalPrice = selected.price * nights;

      itinerary.hotel = {
        name: selected.name,
        address: selected.location,
        checkIn,
        checkOut,
        image: selected.image,
        pricePerNight: selected.price,
        totalPrice,
        rating: selected.rating,
        reviews: selected.reviews
      };

      localStorage.setItem("itinerary", JSON.stringify(itinerary));
    }

    navigate('/itinerary');
  };

  const mapAmenityToIcon = (label: string) => {
    const lower = label.toLowerCase();
    if (lower.includes('wifi')) return Wifi;
    if (lower.includes('pool')) return Waves;
    if (lower.includes('spa') || lower.includes('gym')) return Car;
    if (lower.includes('restaurant')) return Utensils;
    if (lower.includes('business')) return BizIcon;
    return Building;
  };

  const topAIHotels = hotels.filter(h => h.aiRecommended).slice(0, 3);
  const remainingHotels = hotels.filter(h => !topAIHotels.includes(h));
  const visibleHotels = [...topAIHotels, ...remainingHotels];


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
          <p className="text-foreground text-lg">
            Hand-picked accommodations for your comfort and convenience
          </p>
        </div>

        {/* Hotels List */}
        <div className="space-y-8 animate-fade-in">
          {loading ? (
            <Loader />
          ) : (
            visibleHotels.map((hotel, index) => (
              <HotelCard
                key={hotel.id}
                hotel={hotel}
                index={index}
                onSelect={handleHotelSelect}
                onBook={handleBookHotel}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Hotels;
