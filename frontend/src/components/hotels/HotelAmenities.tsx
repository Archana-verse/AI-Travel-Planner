import React from 'react';
import { LucideIcon } from 'lucide-react';

interface Amenity {
  icon: LucideIcon;
  label: string;
}

interface HotelAmenitiesProps {
  amenities: Amenity[];
}

const HotelAmenities = ({ amenities }: HotelAmenitiesProps) => {
  return (
    <div className="mb-6">
      <h3 className="font-medium text-foreground mb-3">Amenities</h3>
      <div className="flex flex-wrap gap-3">
        {amenities.map((amenity, index) => {
          const Icon = amenity.icon;
          return (
            <div key={index} className="flex-center bg-accent px-3 py-2 rounded-lg">
              <Icon className="text-primary" size={16} />
              <span className="text-foreground ml-2">{amenity.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default HotelAmenities;
