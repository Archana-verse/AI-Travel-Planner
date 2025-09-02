import React from 'react';
import { Star, MapPin, Zap, LucideIcon } from 'lucide-react';
import HotelAmenities from './HotelAmenities';
import HotelActions from './HotelActions';
import HotelAIRecommendation from './HotelAIRecommendation';

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
  mostPopular?: boolean;
  topRated?: boolean;
  aiReasoning?: AIReasoning;
  amenities: Amenity[];
  priceFallback?: boolean; 
}

interface HotelCardProps {
  hotel: Hotel;
  index: number;
  onSelect: (hotelId: string) => void;
  onBook: (hotelId: string) => void;
}

const HotelCard = ({ hotel, index, onSelect, onBook }: HotelCardProps) => {
  const formattedPrice = `₹${hotel.price.toLocaleString()} / night`;

  return (
    <div
      className={`card-elevated overflow-hidden hover-lift transition-all duration-300 ${
        hotel.aiRecommended
          ? 'bg-gradient-to-r from-[#fff7eb] dark:from-[#2a1f0f] to-white dark:to-card border-l-4 border-primary animate-glow-border'
          : ''
      }`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      {/* Orange top tag (Most Popular / Best Valued / Top Rated) */}
      {(hotel.mostPopular || hotel.bestValue || hotel.topRated) && (
        <div className="bg-gradient-to-r from-orange-500 to-yellow-400 text-white text-sm font-semibold px-4 py-1 pl-6">
          {hotel.mostPopular
            ? '🔥 Most Popular'
            : hotel.bestValue
            ? '💰 Best Valued'
            : hotel.topRated
            ? '🏆 Top Rated'
            : ''}
        </div>
      )}

      {/* AI Recommended Badge */}
      {hotel.aiRecommended && (
        <div className="flex items-center justify-start px-6 pt-6">
          <div className="ml-auto bg-gradient-to-r from-primary to-yellow-400 text-white px-3 py-1 rounded-full text-xs font-medium flex items-center">
            <Zap size={12} className="mr-1" />
            AI Recommended
          </div>
        </div>
      )}

      {/* Content */}
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <h3 className="text-subheading text-foreground mb-1">{hotel.name}</h3>
            <div className="flex items-center text-sm mb-1">
              <Star className="text-yellow-400 fill-yellow-400 mr-1" size={16} />
              <span className="text-foreground font-medium">{hotel.rating}</span>
              <span className="mx-2 text-muted-foreground">•</span>
              <span className="text-muted-foreground">{hotel.reviews} reviews</span>
            </div>
            <div className="flex items-center text-sm text-muted-foreground mb-3">
              <MapPin size={14} className="mr-1" />
              {hotel.location}
            </div>
            <p className="text-sm text-foreground mb-3">{hotel.description}</p>
            <HotelAmenities amenities={hotel.amenities} />
            {hotel.aiRecommended && hotel.aiReasoning && (
              <HotelAIRecommendation aiReasoning={hotel.aiReasoning} />
            )}
          </div>

          {/* Actions */}
          <div className="text-right min-w-[130px]">
            <div className="text-xl font-bold text-foreground mb-1">
              {hotel.priceFallback
                ? `~ ₹${hotel.price.toLocaleString()} / night`
                : formattedPrice}
            </div>
            {hotel.priceFallback && (
              <div className="text-xs text-muted-foreground italic mb-2">Estimated price</div>
            )}
            <div className="text-sm text-muted-foreground mb-4">Includes basic amenities</div>
            <button
              onClick={() => onSelect(hotel.id)}
              className="bg-primary hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-semibold"
            >
              Select Hotel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HotelCard;
