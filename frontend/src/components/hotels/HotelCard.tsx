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
}

interface HotelCardProps {
  hotel: Hotel;
  index: number;
  onSelect: (hotelId: string) => void;
  onBook: (hotelId: string) => void;
}

const HotelCard = ({ hotel, index, onSelect, onBook }: HotelCardProps) => {
  const formattedPrice = `₹${hotel.price.toLocaleString()} / night`;

  const renderBadges = () => {
    const badges = [];
    if (hotel.mostPopular)
      badges.push(
        <span key="popular" className="text-xs font-medium bg-orange-100 text-orange-600 px-2 py-1 rounded-full">
          🔥 Most Popular
        </span>
      );
    if (hotel.bestValue)
      badges.push(
        <span key="value" className="text-xs font-medium bg-green-100 text-green-600 px-2 py-1 rounded-full">
          💰 Best Valued
        </span>
      );
    if (hotel.topRated)
      badges.push(
        <span key="rated" className="text-xs font-medium bg-purple-100 text-purple-600 px-2 py-1 rounded-full">
          ✨ Top Rated
        </span>
      );
    return badges;
  };

  return (
    <div
      className={`rounded-xl border bg-card dark:border-muted shadow-md hover:shadow-lg transition-all duration-300 mb-5 w-full ${
        hotel.aiRecommended ? 'border-primary/60 bg-muted/20' : ''
      }`}
      style={{ animationDelay: `${index * 0.05}s` }}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex flex-wrap items-center gap-2">
          {renderBadges()}
          {hotel.aiRecommended && (
            <div className="flex items-center text-xs bg-primary text-white px-2 py-1 rounded-full font-medium">
              <Zap size={12} className="mr-1" />
              AI Recommended
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        <div className="flex flex-wrap items-center justify-between mb-2">
          <h2 className="text-lg font-semibold text-foreground">{hotel.name}</h2>
        </div>

        <div className="flex items-center text-sm mb-1">
          <Star className="text-yellow-400 fill-yellow-400 mr-1" size={16} />
          <span className="text-foreground font-medium">{hotel.rating}</span>
          <span className="mx-2 text-muted-foreground">•</span>
          <span className="text-muted-foreground">{hotel.reviews} reviews</span>
        </div>

        <div className="flex items-center text-sm text-muted-foreground mb-2">
          <MapPin size={14} className="mr-1" />
          {hotel.location}
        </div>

        <p className="text-sm text-foreground mb-3">{hotel.description}</p>

        <HotelAmenities amenities={hotel.amenities} />

        {hotel.aiRecommended && hotel.aiReasoning && (
          <HotelAIRecommendation aiReasoning={hotel.aiReasoning} />
        )}

        <HotelActions
          price={formattedPrice}
          hotelId={hotel.id}
          onSelect={onSelect}
          onBook={onBook}
        />
      </div>
    </div>
  );
};

export default HotelCard;
