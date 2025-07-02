
import React from 'react';
import { Star, MapPin, Zap, LucideIcon } from 'lucide-react';
import HotelBadge from './HotelBadge';
import HotelAmenities from './HotelAmenities';
import HotelAIRecommendation from './HotelAIRecommendation';
import HotelActions from './HotelActions';

interface Amenity {
  icon: LucideIcon;
  label: string;
}

interface AIReasoning {
  rating: string;
  location: string;
  amenities: string;
  value: string;
}

interface Hotel {
  id: string;
  name: string;
  rating: number;
  reviews: number;
  location: string;
  description: string;
  price: number;
  image: string;
  recommended?: boolean;
  aiRecommended?: boolean;
  bestValue?: boolean;
  aiReasoning?: AIReasoning;
  amenities: Amenity[];
}

interface HotelCardProps {
  hotel: Hotel;
  index: number;
  onSelect: (hotelId: string) => void;
  onBook: (hotelId: string) => void;
}

const HotelCard = ({ hotel, index, onSelect, onBook }: HotelCardProps) => {
  return (
    <div 
      className={`card-elevated overflow-hidden hover-lift ${
        hotel.aiRecommended ? 'bg-gradient-to-r from-[#fffef2] dark:from-[#2a1f0f] to-white dark:to-card border-l-4 border-primary' : ''
      }`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <HotelBadge recommended={hotel.recommended} bestValue={hotel.bestValue} />
      
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
                <h2 className="text-subheading text-foreground">{hotel.name}</h2>
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
                <span className="text-muted-foreground">{hotel.reviews} reviews</span>
              </div>
              <div className="flex-center mb-4">
                <MapPin className="text-muted-foreground" size={16} />
                <span className="text-muted-foreground ml-1">{hotel.location}</span>
              </div>
              <p className="text-foreground mb-6 leading-relaxed">{hotel.description}</p>

              <HotelAmenities amenities={hotel.amenities} />
              <HotelAIRecommendation aiReasoning={hotel.aiReasoning} />
            </div>

            <HotelActions 
              price={hotel.price} 
              hotelId={hotel.id} 
              onSelect={onSelect} 
              onBook={onBook} 
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HotelCard;
